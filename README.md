[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2021.1-PCTs-ML-Training&metric=alert_status)](https://sonarcloud.io/dashboard?id=fga-eps-mds_2021.1-PCTs-ML-Training)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2021.1-PCTs-ML-Training&metric=coverage)](https://sonarcloud.io/dashboard?id=fga-eps-mds_2021.1-PCTs-ML-Training)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2021.1-PCTs-ML-Training&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=fga-eps-mds_2021.1-PCTs-ML-Training)

# 2021.1-PCTs-ML-Training

Repositório com modelos de Machine Learning do projeto  "Povos e Comunidades Tradicionais"

## Contribuição

1. Clone io repositório
2. Crie uma branch (`git checkout -b feat/x-branch-name`)
3. Commit suas alterações (`git commit -am "Add feat"`)
4. Push para a branch (`git push origin feat/x-branch-name`)

### Extras

- [Guia completo de contribuição completo](https://github.com/fga-eps-mds/2021.1-PCTs-Docs/blob/main/CONTRIBUTING.md)


## Utilização do repo

### Preparando o ambiente
1. Crie um virtual environment python com o comando:
```bash
    python3 -m venv <virtual_env_name>
```
2. Ative o ambiente virtual com o comando:
```bash
    source <virtual_env_name>/bin/activate
```
3. Instale as dependeências:
```bash
    pip install -r requirements.txt
```
4. Adicionando a envrinoment criado ao `ipykernel`:
```bash
    python3 -m ipykernel install --name <virtual_env_name>
```

## Iniciando o jupyterlab
Com o virtual environment ativado, utilize o comando:
```bash
    jupyter lab
```