import time
import json
import requests
import pandas as pd
from urllib.parse import urlencode
import csv
import os.path
import numpy as np


class PlacesID:
	def __init__(self, path_file_input, api_key):
		self.path_file_input = path_file_input
		self.api_key = api_key

	def get_place_id(self):
		data_input = pd.read_csv(self.path_file_input)
		my_dict = []
		for x in range(0, len(data_input)):
			place_id = data_input['place_id'][x]
			print(place_id)
			data_raw = self.get_data_address(place_id)
			results = data_raw['result']['address_components']
			for result in results:
				for type in result['types']:
					if(type=='administrative_area_level_4'):
						nama_kelurahan = result['long_name']
					if(type=='administrative_area_level_3'):
						nama_kecamatan = result['long_name'].replace('Kecamatan ', '')
					if(type=='administrative_area_level_2'):
						nama_kota = result['long_name']

						print(nama_kelurahan, nama_kecamatan, nama_kota)
						my_dict.append({'nama_kelurahan': nama_kelurahan, 'nama_kecamatan': nama_kecamatan, 'nama_kota': nama_kota})
		df_places_id = self.save_to_dataframe('df_places_id.csv', my_dict)

	def get_data_address(self, place_id, sleep=5):
		url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=address_component&key={self.api_key}'
		result = requests.get(url, time.sleep(1)).json()
		return result

	def save_to_dataframe(self, name_file, my_dict):
		df = pd.DataFrame(my_dict, columns=my_dict[0].keys())
		df.to_csv(name_file, index=False)
		return df


api_key = 'xxx'
path_file_input = 'A:/belajar python/yok belajar/warteg-jaksel-2/data_full_completed.csv'

tes = PlacesID(path_file_input, api_key)
tes.get_place_id()