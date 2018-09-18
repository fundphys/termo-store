#from epics import caget, caput, cainfo
import telnetlib
import socket
from datetime import datetime
import pandas as pd


class china_controller():
    def __init__(self, ip_address, port):
        self.ip_addres = ip_address
        self.port = port
        self.channels_list = ["#01" + str(_).zfill(2) for _ in range(1, 13)]
        self.columns_name = [ _[-2:] for _ in self.channels_list]

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
                    answer = self.tn.read_until(b"@", 1).decode('ascii').replace("=", "").replace("@", "")
                    raw.append(float(answer))
                timestamps.append(datetime.utcnow())
                
                for i in range(len(self.columns_name)):
                    data[self.columns_name[i]].append(raw[i])

            except Exception as e:
                print(e)
                return None

            df = pd.DataFrame(data, index=timestamps)
            df.index.name = "timestamp"
            return df

def main():
    controller = china_controller( "192.168.15.22", "10001")
    dt = controller.read_values(2)
    print(dt)
    return None


if __name__=="__main__":
    main()