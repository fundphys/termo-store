#from epics import caget, caput, cainfo
import telnetlib
import socket
from datetime import datetime
import pandas as pd
from epics import caput
from sensor_info import jsonify_data
from influxdb import DataFrameClient
from influxdb import InfluxDBClient

class china_controller():
    def __init__(self, ip_address, port):
        self.ip_addres = ip_address
        self.port = port
        self.channels_list = ["#01" + str(_).zfill(2) for _ in range(1, 13)]
        self.columns_name = [ "ch_" + _[-2:] for _ in self.channels_list]
        try:
            self.tn = telnetlib.Telnet(self.ip_addres, self.port)
        except Exception as e:
            print("Unable to connect to termo controller ip = {}, port={}".format(self.ip_addres, self.port))
            print(e)
    

    def read_values(self, n_values):
        timestamps = []
        data = dict()
        for key in self.columns_name:
            data[key] = []
    
        for i in range(n_values):
            try:
                raw = []
                for ch in self.channels_list:
                        self.tn.write(ch.encode('ascii') + b'\r')
                        answer = self.tn.read_until(b"@", 1).decode('ascii').replace("=", "").replace("@", "").replace("\r", "").replace("B", "")
                        raw.append(float(answer))
                timestamps.append(datetime.utcnow())
                
                for i in range(len(self.channels_list)):
                    data[self.columns_name[i]].append(raw[i])

            except Exception as e:
                print(e)
                return None

        df = pd.DataFrame(data, index=timestamps)
        df.index.name = "timestamp"
        return df

def main():
    controller = china_controller( "192.168.15.22", "10001")
    dt = controller.read_values(10)
    index = dt.index.min()
    data = pd.DataFrame([dt.mean()], index=[index])
    #print(data.ch_01)
    try:
        caput('TERMO:TRS1_T1', data.ch_01)       
        caput('TERMO:M2V1_T1', data.ch_02)
        caput('TERMO:TRS2_T1', data.ch_03)
        caput('TERMO:M2_T1', data.ch_04)
        caput('TERMO:TRS3_T1', data.ch_05)
        caput('TERMO:CNT_T1', data.ch_06)
        caput('TERMO:TRS4_T1', data.ch_07)
        caput('TERMO:M2V2_T1', data.ch_08)
        caput('TERMO:M1_T1', data.ch_09)
        caput('TERMO:M1_T2', data.ch_10)
        caput('TERMO:M1_T3', data.ch_11)
        caput('TERMO:BASE_T1', data.ch_12)
    except Exception as e:
        print(e)
    try:
        client = InfluxDBClient('192.168.15.57', 8086)
        json_body = jsonify_data(data, "CHINA", controller.ip_addres)
        #client.drop_database('china_temperatures')
        #client.create_database('china_temperatures')
        client.switch_database('china_temperatures')
        client.write_points(json_body)

    except Exception as e:
        print(e)

    return None

if __name__=="__main__":
    main()
