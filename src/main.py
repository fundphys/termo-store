from Pet7015 import PET7015
import pandas as pd

from influxdb import DataFrameClient
from influxdb import InfluxDBClient
from sensor_info import jsonify_data


controller_type = "PET7015"
controller_ip = "192.168.15.71"
try:
    dome_temperatures = PET7015(controller_ip)
    client = InfluxDBClient('192.168.15.57', 8086)
    while True:
        dt = dome_temperatures.read_values(100)
        index = dt.index.min() +  (dt.index.max() - dt.index.min()) / 2
        data = pd.DataFrame([dt.mean()], index=[index])

        json_body = jsonify_data(data, controller_type, controller_ip)

        #client.drop_database('temperatures')
        #client.create_database('temperatures')
        client.switch_database('temperatures')
        client.write_points(json_body)
        
        print(dt.index.max() - dt.index.min())

except Exception as e:
    print("err")
    print(e)

#print(json_body)

#result = client.query("""select temperture, channel from "temperatures"."autogen"."temperatures";""")
#result = client.query("""select temperature from "temperatures"."autogen"."temperatures" where "medium" = 'air' ;""")
#print("Result: {}".format(result.raw))
# print(client.get_list_database())

