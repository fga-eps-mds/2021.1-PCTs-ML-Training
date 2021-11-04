
## Dados
**Localização**
`./Data/training_data/df_v2.parquet.gzip`

**Distribuição**
|classe|treino|teste|global|
|---:|---:|---:|---:|
|Território|118(42%)|30(43%)|148|
|identidade|94(34%)|24(34%)|118|
|Quilombolas|66(24%)|16(23%)|82|
|3|278|70|348|

## Desempenho
|class|precision|recall|f1-score|support|
|---:|---:|---:|---:|---:|
|Quilombolas|1.00|0.81|0.90|16|
|Território|0.91|0.97|0.94|30|
|identidade|0.96|1.00|0.98|24|
|||||
|accuracy|||0.94|
|macro avg|0.96|0.93|0.94|70|
|weighted avg|0.95|0.94|0.94|70|

![alt](./imgs/confusion_matrix.png)