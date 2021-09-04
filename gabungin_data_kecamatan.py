import pandas as pd
import urllib.parse

list_kecamatan = ['Cilandak', 'Jagakarsa', 'Kebayoran Baru', 'Kebayoran Lama', 'Mampang Prapatan', 'Pancoran', 'Pasar Minggu', 'Pesanggrahan', 'Setiabudi', 'Tebet']

list_data_kecamatan = []
for kecamatan in list_kecamatan:
	main_path = f'A:/belajar python/yok belajar/warteg-jaksel-2/{kecamatan}/'
	url_kecamatan = main_path+f'datas_completed_{kecamatan}.csv'
	data_mentah = pd.read_csv(url_kecamatan)
	list_data_kecamatan.append(data_mentah)

datas = pd.concat(list_data_kecamatan, ignore_index=True)
datas.to_csv('data_full_completed.csv', index=False)
print(datas.shape)
