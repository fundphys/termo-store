
# root@ubuntu: modpoll -m tcp -t3 -r01 -c7  -1 192.168.15.71
# modpoll 3.4 - FieldTalk(tm) Modbus(R) Master Simulator
# Copyright (c) 2002-2013 proconX Pty Ltd
# Visit http://www.modbusdriver.com for Modbus libraries and tools.

# Protocol configuration: MODBUS/TCP
# Slave configuration...: address = 1, start reference = 1, count = 7
# Communication.........: 192.168.15.71, port 502, t/o 1.00 s, poll rate 1000 ms
# Data type.............: 16-bit register, input register table

# -- Polling slave...
# [1]: 724
# [2]: 750
# [3]: 698
# [4]: 32767
# [5]: 701
# [6]: -32768
# [7]: 900

import datetime
import pandas as pd
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

class PET7015:
    def __init__(self, host, port=502):
        self.host = host
        self.port = port
        self.timeout = 1.0

        try:
            self.master =  modbus_tcp.TcpMaster(host=self.host, port=self.port)
            self.master.set_timeout(self.timeout)
        except Exception as e:
            print("Exception in PET7015 class constructor\n{}".format(e))

    def set_timeout(self, timeout):
        try:
            self.master.set_timeout(self.timeout)
            self.timeout = 1.0
        except Exception as e:
            print("Exception in PET7015 class set_timeout method\n{}".format(e))

    def read_values(self, n_values):
        columns_name=["ch_1","ch_2","ch_3","ch_4","ch_5","ch_6","ch_7"]
        timestamps = []
        data = dict()
        for key in columns_name:
            data[key] = []

        for i in range(n_values):
            try:
                raw = [ float(_) for _ in self.master.execute(1, cst.READ_INPUT_REGISTERS, 0, 7)]
                timestamps.append(datetime.datetime.utcnow())
                for i in range(7):
                    data[columns_name[i]].append(raw[i])

            except Exception as e:
                print(e)
                return None

        df = pd.DataFrame(data, index=timestamps)
        df.index.name = "timestamp"
        return df
