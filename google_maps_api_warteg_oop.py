import time
import json
import requests
import pandas as pd
from urllib.parse import urlencode
import csv
import os.path
import numpy as np

class GooglePlaces:
	def __init__(self, path, list_kelurahan, kecamatan, kota, api_key, type=1):
		self.list_kelurahan = list_kelurahan
		self.kecamatan = kecamatan
		self.kota = kota
		self.api_key = api_key
		self.count = 1
		self.path = path
		self.type = type

	def start(self):
		if(self.type==1):
			self.radius = 2000
			self.datas = self.extract_lat_lng()
			for self.nama_kelurahan, self.latitude, self.longitude in zip(self.datas.nama_kelurahan, self.datas.latitude, self.datas.longitude):
				print(self.nama_kelurahan)
				self.params_for_request()
		else:
			self.radius = 500
			for self.kelurahan in self.list_kelurahan:
				datas = pd.read_csv(self.path+'type_1_warteg_kelurahan_'+self.kelurahan+'.csv')
				datas_sorted = datas.sort_values('distance', ascending=False)
				self.datas = datas_sorted.head(4)
				for self.latitude, self.longitude in zip(self.datas.latitude, self.datas.longitude):
					print(self.kelurahan, self.latitude)
					self.params_for_request()

	def extract_lat_lng(self):
		lat_kelurahan, lng_kelurahan = [], []
		for kelurahan in self.list_kelurahan:
			address = f"{kelurahan},{self.kecamatan},{self.kota}"
			params = {'address': address, 'key': self.api_key}
			result = self.request_data(params)
			lat = result['results'][0]['geometry']['location']['lat']
			lng = result['results'][0]['geometry']['location']['lng']
			lat_kelurahan.append(lat)
			lng_kelurahan.append(lng)

		df_kelurahan = pd.DataFrame({"nama_kelurahan": self.list_kelurahan, "latitude": lat_kelurahan, "longitude": lng_kelurahan})
		df_kelurahan.to_csv(self.path+f"lat_long_kecamatan_{kecamatan}.csv", index=False)
		return df_kelurahan

	def params_for_request(self):
		type_place = 'restaurant'
		params = {
			"location": f"{self.latitude},{self.longitude}",
			"radius": self.radius,
			"keyword": 'warteg',
			"type": 'type_place',
			"key": self.api_key,
			"rankby": "prominence"
		}
		self.parse_places(params)

	def parse_places(self, params, page=0):
		print(f"Pages: {page}")
		my_dict = {'nama_tempat': [], 'rating_tempat': [], 'user_ratings_total': [], 'latitude': [], 'longitude': [], 'alamat_tempat': [], 'place_id': [], 'distance': []}
		result = self.request_data(params, type_search="nearbysearch", sleep=5)
		for data in result['results']:
			name = data['name'].lower().replace("'", "").replace('"', '')
			rating_tempat = 0
			user_ratings_total = 0
			place_id = data['place_id']
			if("rating" in data.keys()):
				rating_tempat = data['rating']
			if("user_ratings_total" in data.keys()):
				user_ratings_total = data['user_ratings_total']
			alamat_tempat = data['vicinity'].lower()
			if 'jakarta barat' in alamat_tempat or 'jakarta timur' in alamat_tempat or 'jakarta pusat' in alamat_tempat or 'jakarta utara' in alamat_tempat or 'depok' in alamat_tempat or 'tangerang' in alamat_tempat or 'bekasi' in alamat_tempat:
				continue
			types = [type for type in data['types']]
			location = [data['geometry']['location'][loc] for loc in data['geometry']['location']]
			lat = location[0]
			lng = location[1]
			if(type!=1):
				distance = 0
			else:
				distance = np.abs(self.longitude - lng) + np.abs(self.latitude - lat)
			print(f"{self.count}. {name} {lat}, {lng} -> {rating_tempat}")
			self.count+=1
			my_dict['nama_tempat'].append(name)
			my_dict['rating_tempat'].append(rating_tempat)
			my_dict['user_ratings_total'].append(user_ratings_total)
			my_dict['latitude'].append(lat)
			my_dict['longitude'].append(lng)
			my_dict['alamat_tempat'].append(alamat_tempat)
			my_dict['place_id'].append(place_id)
			my_dict['distance'].append(distance)
		if('next_page_token' not in result.keys()):
			self.save_to(my_dict)
			print("##################### Selesai")
		else:
			self.save_to(my_dict)
			page+=1
			next_page_token = result['next_page_token']
			params = {
				'pagetoken': next_page_token,
				'key': self.api_key
				}
			self.parse_places(params, page)

	def request_data(self, params, type_search='geocode', sleep=0):
		if type_search == 'nearbysearch':
			type_search = 'place/nearbysearch'
		params_encoded = urlencode(params)
		url = f"https://maps.googleapis.com/maps/api/{type_search}/json?{params_encoded}"
		result = requests.get(url, time.sleep(sleep)).json()
		return result

	def save_to(self, dict_row):
		if(self.type==2):
			path_output = self.path+ "2/type_"+ str(self.type) + "_warteg_kelurahan_" +self.kelurahan+".csv"
		else:
			path_output = self.path+ "type_"+ str(self.type) + "_warteg_kelurahan_" +self.nama_kelurahan+".csv"
		is_new = not os.path.isfile(path_output)
		rows = zip(*dict_row.values())
		modes = 'a'
		if is_new:
			os.makedirs(os.path.dirname(path_output), exist_ok=True)
			modes = 'w'
		with open(path_output, mode=modes, newline='', encoding='utf-8') as csv_file:
			writer = csv.writer(csv_file)
			if is_new:
				writer.writerow(dict_row.keys())
			for row in rows:
				writer.writerow(row)

api_key = 'xxx' # Api Key
list_kelurahan= ['Tebet Barat', 'Tebet Timur', 'Kebon Baru', 'Bukit Duri', 'Manggarai', 'Manggarai Selatan', 'Menteng Dalam']
kecamatan = 'Tebet'
type = 1

kota = "Jakarta Selatan"
path = f"A:/belajar python/yok belajar/warteg-jaksel-2/{kecamatan}/"

# Type 1 -> cari warteg terdekat
# Type 2-> cari warteg terdekat dengan 4 distance terjauh dari type 1
model = GooglePlaces(path, list_kelurahan, kecamatan, kota, api_key, type)
model.start()
