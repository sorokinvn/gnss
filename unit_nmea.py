#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import serial

# Глобальная переменная для передачи данных между функциями
data_rmc = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
data_gll = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
con_port = True

# Функция считывания из порта, отправки на обработку и записи в файл
def read_put():
    global data_rmc, data_gll
    try:
        gnss = serial.Serial('COM7', 9600)
        while True:
            con_port = True
            ser_bytes = gnss.readline()
            decoded_bytes = ser_bytes.decode('utf-8')
            data = decoded_bytes.split(',')
            if data[0] == '$GNRMC' and data[1] != '':
                data_rmc = data
                data = str(data)
                gnss_file_rmc = open('gnss_rmc.txt', 'a')
                gnss_file_rmc.write(data + '\n')
                gnss_file_rmc.close()

            if data[0] == '$GNGLL' and data[5] != '':
                data_gll = data
                data = str(data)
                gnss_file_gll = open('gnss_gll.txt', 'a')
                gnss_file_gll.write(data + '\n')
                gnss_file_gll.close()
    except serial.SerialException:
        con_port = False
        read_put()

# Функция вычисления Широты
def get_lat(data):
    if data == '':
        return str(0)
    else:
        lat = str(data)
        lat_d = lat[:2]
        if lat_d[0] == '0':
            lat_d = lat_d[1:2]
        lat_m = lat[2:10]
        if lat_m[0] == '0':
            lat_m = lat_m[1:8]
        lat_m = str(float(lat_m)/60)[1:8]
        return lat_d + lat_m

# Функция вычисления Долготы
def get_long(data):
    if data == '':
        return str(0)
    else:
        long_d = data[:3]
        if long_d[0] == '0':
            long_d = long_d[1:3]
        if long_d[0] == '0' and long_d[1] == '0':
            long_d = long_d[2:3]
        long_m = data[3:11]
        if long_m[0] == '0':
            long_m = long_m[1:8]
        long_m = str(float(long_m) / 60)[1:8]
        return long_d + long_m

# Функция вычисления Времени UTC
def get_time(data):
    if data == '':
        return str(0)
    else:
        hh = '00'
        mm = '00'
        ss = '00'
        hh = data[:2]
        mm = data[2:4]
        ss = data[4:6]
        return hh + ':' + mm + ':' + ss

if __name__ == "__main__":
    pass