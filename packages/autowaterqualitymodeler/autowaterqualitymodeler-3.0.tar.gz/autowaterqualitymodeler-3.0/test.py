import pandas as pd
from autowaterqualitymodeler.run import main

if 0:
    spectrum_data=pd.read_csv("data/ref_data.csv", index_col=0, header=0)
    metric_data=pd.read_csv("data/measure_data.csv", index_col=0)
    origin_merged_data=pd.read_csv("data/merged_data.csv", index_col=0)
    result = main(spectrum_data, origin_merged_data, metric_data, [0, 12, 32, 43, 46, 63])
else:
    spectrum_data=pd.read_csv("data/ref_data.csv", index_col=0, header=0).iloc[:6]
    metric_data=pd.read_csv("data/measure_data.csv", index_col=0)
    origin_merged_data=pd.read_csv("data/merged_data.csv", index_col=0).iloc[:6]

    result = main(spectrum_data, origin_merged_data, metric_data)

print(result)

print('done')