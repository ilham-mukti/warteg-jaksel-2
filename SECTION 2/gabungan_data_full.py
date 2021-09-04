

import pandas as pd


datas_1 = pd.read_csv("A:/belajar python/yok belajar/warteg-jaksel-2/data_full_completed.csv")
datas_2 = pd.read_csv("A:/belajar python/yok belajar/warteg-jaksel-2/SECTION 2/df_places_id.csv")

data_warteg_fixed = pd.concat([datas_1, datas_2], axis=1)
data_warteg_fixed.to_csv("DATA_WARTEG_JAKSEL_FIXED.csv", index=False)
