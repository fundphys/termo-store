#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date : 22-07-2016
# fundphys
# review 14-09-2018

from datetime import datetime
from influxdb import InfluxDBClient
import telnetlib
import socket

#Store data from vaisala weather station
#telnet 192.168.10.8', 16303
#777 GET WATER
#777 OK  RH=33 DEW_P=-17.7 PWV=4.3 RAIN=0
#777 GET DATA
#777 OK TEMP=-3.6 WIND=9.0 WIND_DIR=140 RH=32 DEW_P=-17.8 PRESS=796.5 RAIN=0
#777 GET WIND
#777 OK WIND=9.0 WIND_MIN=7.1 WIND_MAX=10.4 WIND_DIR=140
#777 GET TREND
#777 OK TEMP=-1.6 WIND=-1.5 WIND_DIR=12 RH=-3 DEW_P=-1.6 PRESS=-0.3

class WEATHER_SOURCE(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.meteo_data = dict()

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
        self.answer = byte_like_answer.decode("ascii")  #"".join(map(chr, byte_like_answer))

        if 'OK' in self.answer:
            return self.answer
        else:
            return None

    def parse_answer(self, answer):
        for key, value in [(_.split("=")[0], float(_.split("=")[1])) for _ in answer.replace("\n", "").split(" ") if "=" in _ ]:
            if not key in self.meteo_data:
                self.meteo_data[key] = value

    def jsonify_data(self):
        self.json_body = [{
            "measurement": "weather",
            "tags": { "station": "vaisala", },
            "time": str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')),
            "fields": self.meteo_data, 
        }]
                

def main():
    ws = WEATHER_SOURCE('192.168.10.8', 16303)

    data = ws.request("777 get data")
    ws.parse_answer(data)

    data = ws.request("777 get wind")
    ws.parse_answer(data)

    data = ws.request("777 get water")
    ws.parse_answer(data)

    ws.jsonify_data()
    
    try:
        client = InfluxDBClient('192.168.15.57', 8086)
    except Exception as e:
        print("Unable to connect to InfluxDB {}".format(e))
        exit(-5)

    #client.drop_database('weather')
    #client.create_database('weather')
    
    client.switch_database('weather')
    client.write_points(ws.json_body)


if __name__ == '__main__':
        main()