import pandas as pd
import urllib.parse

list_kelurahan = ['Tebet Barat', 'Tebet Timur', 'Kebon Baru', 'Bukit Duri', 'Manggarai', 'Manggarai Selatan', 'Menteng Dalam']
kecamatan = 'Tebet'

list_data_gabugan = []
for kelurahan in list_kelurahan:
	main_path = f'A:/belajar python/yok belajar/warteg-jaksel-2/{kecamatan}/'
	url_kelurahan_1 = main_path+f'type_1_warteg_kelurahan_{kelurahan}.csv'
	url_kelurahan_2 = main_path+f'2/type_2_warteg_kelurahan_{kelurahan}.csv'
	data_1 = pd.read_csv(url_kelurahan_1)
	data_2 = pd.read_csv(url_kelurahan_2)
	print(f"Kelurahan: {kelurahan}")
	print(f"Data 1 shape: {data_1.shape}")
	print(f"Data 2 shape: {data_2.shape}")
	data_warteg_fixed = pd.concat([data_1, data_2], ignore_index=True)
	list_data_gabugan.append(data_warteg_fixed)


datas = pd.concat(list_data_gabugan, ignore_index=True)
print(f"Data gabungan shape: {datas.shape}")
datas.drop_duplicates(subset=['latitude', 'longitude', 'place_id'], keep='last', inplace=True)
print(f"Data fixed duplicates shape: {datas.shape}")
datas.to_csv(f"{main_path}datas_completed_{kecamatan}.csv", index=False)
