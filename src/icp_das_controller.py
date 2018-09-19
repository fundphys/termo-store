from Pet7015 import PET7015
import pandas as pd

from influxdb import DataFrameClient
from influxdb import InfluxDBClient
from sensor_info import jsonify_data


controller_type = "PET7015"
controller_ip = "192.168.15.71"
try:
    controller = PET7015(controller_ip)
    client = InfluxDBClient('192.168.15.57', 8086)
    dt = controller.read_values(100)
    index = dt.index.min()
    data = pd.DataFrame([dt.mean()], index=[index])

    json_body = jsonify_data(data, controller_type, controller_ip)

    #client.drop_database('temperatures')
    #client.create_database('temperatures')
    client.switch_database('temperatures')
    client.write_points(json_body)

except Exception as e:
    print(e)