#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date : 22-07-2016
# fundphys
# review 14-09-2018

from datetime import datetime
import telnetlib
import socket
import re

#Store data from vaisala weather station
#telnet 192.168.10.8', 16303
#777 GET WATER
#777 OK  RH=33 DEW_P=-17.7 PWV=4.3 RAIN=0
#
#777 GET DATA
#777 OK TEMP=-3.6 WIND=9.0 WIND_DIR=140 RH=32 DEW_P=-17.8 PRESS=796.5 RAIN=0
#
#777 GET WIND
#777 OK WIND=9.0 WIND_MIN=7.1 WIND_MAX=10.4 WIND_DIR=140
#
#777 GET TREND
#777 OK TEMP=-1.6 WIND=-1.5 WIND_DIR=12 RH=-3 DEW_P=-1.6 PRESS=-0.3
#

def main():
    ws = WEATHER_SOURCE('192.168.10.8', 16303)
    data = ws.request("777 get data")
    ws.parse_answer(data)

    data = ws.request("777 get wind")
    ws.parse_answer(data)

    data = ws.request("777 get water")
    ws.parse_answer(data)

    timestamp = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    print(timestamp)

class WEATHER_SOURCE(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        try:
            self.tn = telnetlib.Telnet(ip, port)
        except socket.error as e:
            print("Error on init socket {}".format(e))
            exit(-1)


    def request(self, request_string):
        if not isinstance(request_string, str):
            print("request(str): Argument must be string!")
            exit(-4)

        try:
            self.tn.write(request_string.encode('ascii') + b"\n")
        except socket.error as e:
            print("Error on write to telnet socket: {}".format(e))
            exit(-2)

        try:
            byte_like_answer = self.tn.read_until(b"\n", 1)
        except socket.timeout as e:
            print("Socket timeout: {}".format(e))
            exit(-3)
        self.answer = byte_like_answer.decode("ascii") #"".join(map(chr, byte_like_answer))

        if 'OK' in self.answer:
            return self.answer
        else:
            return None


    def parse_answer(self, answer):
        data = dict()
        for item in [_ for _ in answer.replace("\n", "").split(" ") if "=" in _ ]:
            key = item.split("=")[0]
            value = float(item.split("=")[1])
            data[key] = value
        print(data)






    # def get_data(self):
        
    #     request_string = "777 get data\n"
        
        

    #     try:
    #         s = self.tn.read_until('\n', 1)
    #     except socket.timeout:
    #         pass
    #     if 'OK' in s:

    #         self.temp = float(re.findall(r'TEMP=([-+]?\d.\d)', s)[0])
    #         self.rh = int(re.findall('RH=([\d]+)', s)[0])
    #         self.dew_point = float(re.findall(r'DEW_P=([-+]?\d*\.\d+)', s)[0])
    #         self.press = float(re.findall('PRESS=([\d.\d]+)', s)[0])
    #         self.rain = int(re.findall('RAIN=([\d]+)', s)[0])
    #     else:
    #         pass

    #     string = '777 get wind\n'
    #     # 777 OK WIND=4.6 WIND_MIN=3.2 WIND_MAX=5.3 WIND_DIR=27
    #     self.tn.write(string)
    #     try:
    #         s = self.tn.read_until('\n', 1)
    #     except socket.timeout:
    #         pass
    #     if 'OK' in s:
    #         self.wind = float(re.findall('WIND=([\d.\d]+)', s)[0])
    #         self.wind_dir = int(re.findall('WIND_DIR=([\d]+)', s)[0])
    #     else:
	#         pass

    #     #777 OK  RH=33 DEW_P=-17.7 PWV=4.3 RAIN=0
    #     # string = '777 get water\n'
    #     self.tn.write(string)
        
    #     try:
    #         s = self.tn.read_until('\n', 1)
    #     except socket.timeout:
    #         pass
    #     if 'OK' in s:
    #         self.pwv = float(re.findall('PWV=([\d.\d]+)', s)[0])
    #     else:
    #         pass

    #     timestamp = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    #     return [timestamp, self.temp, self.rh, self.dew_point, self.press, self.rain, self.wind, self.wind_dir, self.pwv]


if __name__ == '__main__':
        main()