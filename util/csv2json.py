import pandas as pd
import yaml
# 因为和风API 只接受locationID, 所以需要把城市名换成locationID
mappings = []
def locationID_mapping_city_name():
     df = pd.read_csv("../China-City-List-latest.csv")
     all_data = df.values[1:]

     for i in all_data:
          mappings.append({
               "location_id": i[0],
               "city_name": i[1],
               "city_name_ZH": i[2],
               'Adm1_Name_ZH': i[7],
               'Adm2_Name_ZH': i[9]
          })

     with open("../city_name_locationID.yml", 'w', encoding='utf8') as yaml_file:
          yaml.dump(mappings, yaml_file, allow_unicode=True)
     print("ok")

def mapping_locationID_city_name(mappings,city_name):
     for i in mappings:
          if i['city_name_ZH'] == city_name:
               return i['location_id']


import json
def yml_to_json():

     with open("../city_name_locationID.json", 'w', encoding='utf8') as json_file:
          json.dump(mappings, json_file, indent=4)
     print("ok")

locationID_mapping_city_name()
yml_to_json()
# a = mapping_locationID_city_name("深圳")
# print(a)