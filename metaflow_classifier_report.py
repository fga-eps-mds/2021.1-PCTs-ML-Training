from metaflow import (
        FlowSpec,
        step,
        IncludeFile,
        Parameter, 
        current)
from xgboost import XGBClassifier
from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import os
import pickle


def classification_report_to_md(report):
    report_table =\
'''|class|precision|recall|f1-score|support|
|---:|---:|---:|---:|---:|
'''
    classes = list(report.keys())[:-3]
    for _class in classes:
        precision = report[_class]['precision']
        recall = report[_class]['recall']
        f1 = report[_class]['f1-score']
        support = report[_class]['support']
        line = f'|{_class}|{precision:.2f}|{recall:.2f}|{f1:.2f}|{support}|\n'
        report_table += line

    report_table += '|||||\n'
    acc = report['accuracy']
    report_table += f'|accuracy|||{acc:.2f}|\n'

    for approach in ['macro avg', 'weighted avg']:
        precision = report[approach]['precision']
        recall = report[approach]['recall']
        f1 = report[approach]['f1-score']
        support = report[approach]['support']
        line = f'|{approach}|{precision:.2f}|{recall:.2f}|{f1:.2f}|{support}|\n'
        report_table += line
    return report_table


def dataset_dist_to_md(dists, totals):
    table =\
'''|classe|treino|teste|global|
|---:|---:|---:|---:|
'''
    classes = list(dists['global'].keys())
    splits = list(dists.keys())[-2:]
    
    for _class in classes:
        line = f'|{_class}|'
        for split in splits:
            amount = dists[split][_class]
            percent = 100*amount/totals[split]
            line+=f'{amount}({percent:.0f}%)|'
        amount = dists['global'][_class]
        line+=f'{amount}|\n'
        table+= line
    len_classes = len(classes)
    line=f'|{len_classes}|'
    for split in splits:
        total_split = totals[split]
        line+=f'{total_split}|'
    total_split = totals['global']
    line+=f'{total_split}|\n'
    table += line
    return table

def plot_confusion_matrix(labels, pred_labels, classes, path):
    fig = plt.figure(figsize = (25, 25));
    ax = fig.add_subplot(1, 1, 1);
    cm = confusion_matrix(labels, pred_labels);
    cm = ConfusionMatrixDisplay(cm, display_labels = classes);
    cm.plot(values_format = 'd', cmap = 'Blues', ax = ax)
    plt.xticks(rotation = 90)
    plt.savefig(path)

def export_README(name, path, dists, totals, report, labels, pred_labels):
    README = f'\n## Dados\n'
    README += f'**Localização**\n`{path}`\n\n'
    README += f'**Distribuição**\n'
    README += dataset_dist_to_md(dists, totals)
    README += f'\n## Desempenho\n'
    README += classification_report_to_md(report)
    README += f'\n'
    classes = list(report.keys())[:-3]
    path = './imgs/confusion_matrix.png'
    if not os.path.exists('./imgs'):
        os.makedirs('./imgs')

    plot_confusion_matrix(labels, pred_labels,classes, path)
    README += f'![alt]({path})'
    return README
    

class ClassificadorPCTS(FlowSpec):
    test_size = Parameter('test_size',
                      help='Test size split',
                      default=0.2)
    path = Parameter('path',
                  help='Dataset path',
                  default='./Data/training_data/df_v4.parquet.gzip')
    model_version = Parameter('model_version',
                  help='Model version',
                  default='4')
    max_df = Parameter('max_df',
                  help='When building the vocabulary ignore terms that have a document frequency strictly higher than the given threshold',
                  default=1.0) #0.5
    min_df = Parameter('min_df',
                  help='When building the vocabulary ignore terms that have a document frequency strictly lower than the given threshold.',
                  default=1) #20
    
    @step
    def start(self):
        
        import pandas as pd
        
        self.dataframe = pd.read_parquet(self.path)
        self.dataframe = self.dataframe[~self.dataframe.y.isna()]

        aux_df = dict(self.dataframe.y.value_counts())
        classes = [key for key, value in aux_df.items() if value > 10]
        self.dataframe = self.dataframe[self.dataframe.y.isin(classes)]
        self.next(self.transform_data)

    @step
    def transform_data(self):
        from sklearn.feature_extraction.text import TfidfVectorizer

        self.vectorizer = TfidfVectorizer()
        self.X = self.vectorizer.fit_transform(self.dataframe["texto"])
        self.next(self.split_dataset)

    @step
    def split_dataset(self):
        from sklearn.model_selection import train_test_split
        
        self.Y = self.dataframe['y']

        self.Xtrain, self.Xtest, self.Ytrain, self.Ytest = train_test_split(
                self.X,
                self.Y,
                test_size=self.test_size,
                random_state=42,
                stratify = self.Y)

        self.next(self.xboost_train, self.nb_train)

    @step
    def xboost_train(self):
        import multiprocessing

        cpus = multiprocessing.cpu_count()
        self.model = XGBClassifier(n_jobs=cpus-4).fit(self.Xtrain, self.Ytrain)
        self.next(self.evaluate)
        
    @step
    def nb_train(self):

        self.model = MultinomialNB().fit(self.Xtrain, self.Ytrain)
        
        self.next(self.evaluate)      
    
    @step 
    def evaluate(self, inputs):
        from sklearn.metrics import classification_report
        
        # metaflow misses confidence into data created before parallel execution
        #that's why it's appropriate to merge artifacts of our interest
        self.merge_artifacts(inputs, exclude=['model'])
        
        self.all_pred = {}
        bestF1 = -1
        for i in inputs:
            Yhat = i.model.predict(self.Xtest)
            self.all_pred[type(i.model).__name__] = Yhat
            report = classification_report(self.Ytest, Yhat, output_dict=True)
            if float(report['macro avg']['f1-score']) > bestF1:
                self.model = i.model
                self.classifier = type(i.model).__name__
                self.report = report
                self.pred = Yhat
                bestF1 = float(report['macro avg']['f1-score'])
                print("best model so far: %s with f1-score %.2f" % (type(i.model).__name__, bestF1))
        self.next(self.end)

    @step
    def end(self):
        global_dist = self.dataframe['y'].value_counts().rename_axis('classe').to_frame('global').to_dict()
        train_dist = self.Ytrain.value_counts().rename_axis('classe').to_frame('train').to_dict()
        test_dist = self.Ytest.value_counts().rename_axis('classe').to_frame('test').to_dict()
        
        global_dist.update(train_dist)
        global_dist.update(test_dist)
        
        totals = {'global':len(self.dataframe), 'train': len(self.Ytrain), 'test': len(self.Ytest) }
        
        README = export_README(type(self).__name__, self.path, global_dist, totals, self.report, self.Ytest, self.pred)
        with open(f'ModelReport_V{self.model_version}.md', 'w') as f:
            f.write(README)

        pickle.dump(self.model, open(f"Data/model_versioning/model_v{self.model_version}.p", "wb"))
        pickle.dump(self.vectorizer, open(f"Data/model_versioning/vectorizer_v{self.model_version}.p", "wb"))


if __name__ == "__main__":
    ClassificadorPCTS()
