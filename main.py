#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import threading
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import  messagebox
from tkinter import*

def potok (my_func):
    def wapper(*args, **kwargs):
        my_thread = threading.Thread(target = my_func, args = args, kwargs = kwargs, daemon = True)
        my_thread.start()
    return wapper

@potok
def read_put():
    try:
        gps = serial.Serial('COM7', baudrate=9600)
        print('Подключение GNSS выполнено')
        while True:
            ser_bytes = gps.readline()
            decoded_bytes = ser_bytes.decode('utf-8')
            data = decoded_bytes.split(',')
            if data[0] == '$GNRMC':
                if data[2] == 'V':
                    print('Данные GNSS не достоверны')
                else:
                    print(data)
                lat = str(data[3])
                lat_d = lat[:2]
                if lat_d[0] == '0':
                    lat_d = lat_d[1:2]
                lat_m = lat[2:10]
                if lat_m[0] == '0':
                    lat_m = lat_m[1:8]
                lat_m = str(float(lat_m)/60)[1:8]
                lat = lat_d + lat_m
                print('Latitude: ', lat)

                long = str(data[5])
                long_d = long[:3]
                if long_d[0] == '0':
                    long_d = long_d[1:3]
                if long_d[0] == '0' and long_d[1] == '0':
                    long_d = long_d[2:3]
                long_m = long[3:11]
                if long_m[0] == '0':
                    long_m = long_m[1:8]
                long_m = str(float(long_m) / 60)[1:8]
                long = long_d + long_m
                print('Longtitude: ', long)

                data = str(data)
                gnss_file = open('gnss.txt', 'a')
                gnss_file.write(data + '\n')
                gnss_file.close()
    except serial.SerialException:
        print('Ошибка подключения GNSS')
        pass

root = tk.Tk()
root.iconbitmap('image/icon.ico')
root.title('GNSS WRITER')
root.geometry('1024x768')
root.resizable(0, 0)
read_put()
root.mainloop()