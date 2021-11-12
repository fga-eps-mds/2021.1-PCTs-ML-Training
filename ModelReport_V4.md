
## Dados
**Localização**
`./Data/training_data/df_v4.parquet.gzip`

**Distribuição**
|classe|treino|teste|global|
|---:|---:|---:|---:|
|conflito|177(20%)|45(20%)|222|
|comunidade|128(14%)|32(14%)|160|
|Estado|128(14%)|32(14%)|160|
|Território|118(13%)|30(14%)|148|
|identidade |82(9%)|21(9%)|103|
|estado|82(9%)|21(9%)|103|
|Quilombolas|66(7%)|16(7%)|82|
|Território;Quilombolas|56(6%)|14(6%)|70|
|Conflito|15(2%)|4(2%)|19|
|identidade e território |13(1%)|3(1%)|16|
|identidade|10(1%)|2(1%)|12|
|identidade e território|10(1%)|2(1%)|12|
|12|885|222|1107|

## Desempenho
|class|precision|recall|f1-score|support|
|---:|---:|---:|---:|---:|
|Conflito|1.00|0.75|0.86|4|
|Estado|0.83|0.91|0.87|32|
|Quilombolas|0.62|0.50|0.55|16|
|Território|0.71|0.83|0.77|30|
|Território;Quilombolas|0.55|0.43|0.48|14|
|comunidade|0.75|0.75|0.75|32|
|conflito|0.86|0.98|0.92|45|
|estado|0.95|0.95|0.95|21|
|identidade|0.00|0.00|0.00|2|
|identidade |0.84|0.76|0.80|21|
|identidade e território|0.00|0.00|0.00|2|
|identidade e território |1.00|0.67|0.80|3|
|||||
|accuracy|||0.80|
|macro avg|0.68|0.63|0.65|222|
|weighted avg|0.78|0.80|0.78|222|

![alt](./imgs/confusion_matrix.png)