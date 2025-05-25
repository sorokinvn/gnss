#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
from time import sleep

import serial
import threading
from tkinter import*
import tkinter as tk

# Класс виджетов надписей
class Wid_label():
    def __init__(self, name, x, y):
        self.name = name
        # координаты размещения виджета
        self.x = x
        self.y = y

    def creat(self):
        lb_name_wid = Label(root, width = 14, text = self.name, font = "Arial 12 bold", relief = RIDGE,
                            borderwidth = 2, anchor = 'w')
        lb_name_wid.place(x = self.x, y = self.y)

        self.lb_value_wid = Label(root, width = 15, font = "Arial 12 bold", relief = RIDGE, borderwidth = 2)
        self.lb_value_wid.place(x = self.x + 150, y = self.y)

    def set(self, value):
        self.value = value
        self.lb_value_wid.config(text = self.value)

    def set_color(self, color):
        self.color = color
        self.lb_value_wid.config(background = self.color)



# Глобальная переменная для передачи данных между функциями
global_data_rmc = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
global_data_gll = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']

# Обертка для функций-потоков
def potok (my_func):
    def wapper(*args, **kwargs):
        my_thread = threading.Thread(target = my_func, args = args, kwargs = kwargs, daemon = True)
        my_thread.start()
    return wapper

# Поток считывания из порта, отправки на обработку и записи в файл
@potok
def read_put():
    global global_data_rmc
    global global_data_gll
    try:
        gnss = serial.Serial('COM7', baudrate=9600)
        print('Подключение GNSS выполнено')
        while True:
            ser_bytes = gnss.readline()
            decoded_bytes = ser_bytes.decode('utf-8')
            data = decoded_bytes.split(',')
            if data[0] == '$GNRMC':
                print(data)
                global_data_rmc = data
                data = str(data)
                gnss_file_rmc = open('gnss_rmc.txt', 'a')
                gnss_file_rmc.write(data + '\n')
                gnss_file_rmc.close()

            if data[0] == '$GNGLL':
                print(data)
                global_data_gll = data
                data = str(data)
                gnss_file_gll = open('gnss_gll.txt', 'a')
                gnss_file_gll.write(data + '\n')
                gnss_file_gll.close()
    except serial.SerialException:
        print('Ошибка подключения GNSS')
        pass

# Функция вычисления Широты
def get_lat(data):
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
    hh = '00'
    mm = '00'
    ss = '00'
    hh = data[:2]
    mm = data[2:4]
    ss = data[4:6]
    return hh + ':' + mm + ':' + ss

# Поток обработки и вывода в форму
@potok
def out_form():
    global global_data_rmc
    data_lat = '0'
    data_long = '0'
    data_time = '0'
    while True:
        if global_data_rmc[2] == 'A':
            data_lat = get_lat(global_data_rmc[3])
            data_long = get_long(global_data_rmc[5])
            data_time = get_time(global_data_rmc[1])
        latitude.set(data_lat)
        longtitude.set(data_long)
        time_clock.set(data_time)
        reliability.set('Достоверно')
        reliability.set_color('green')
        if global_data_rmc[2] == 'V':
            reliability.set('Не достоверно')
            reliability.set_color('red')
        sleep(.5)

# Поток обработки и вывода в форму
@potok
def out_form_gll():
    global global_data_gll
    data_lat = '0'
    data_long = '0'
    data_time = '0'
    while True:
        data_lat = get_lat(global_data_gll[1])
        data_long = get_long(global_data_gll[3])
        data_time = get_time(global_data_gll[5])
        latitude_gll.set(data_lat)
        longtitude_gll.set(data_long)
        time_clock_gll.set(data_time)
        sleep(.5)

# Запускаем поток read_put в фоне
read_put()

root = tk.Tk()
root_w = 1024
root_h = 768
root_size = str(root_w) + 'x' + str(root_h)
root.iconbitmap('image/icon.ico')
root.title('GNSS WRITER')
root.geometry(root_size)
root.resizable(0, 0)

# Поля данных RMC
data_type = Wid_label(name = 'Тип данных: ', x = 10, y = 10)
data_type.creat()
data_type.set('RMC')

time_clock = Wid_label(name = 'Время (UTC): ', x = 10, y = 40)
time_clock.creat()

latitude = Wid_label(name = 'Широта: ', x = 10, y = 70)
latitude.creat()

longtitude = Wid_label(name = 'Долгота: ', x = 10, y = 100)
longtitude.creat()

reliability = Wid_label(name = 'Достоверность: ', x = 10, y = 130)
reliability.creat()

# Поля данных GLL
data_type_gll = Wid_label(name = 'Тип данных: ', x = 400, y = 10)
data_type_gll.creat()
data_type_gll.set('GLL')

time_clock_gll = Wid_label(name = 'Время (UTC): ', x = 400, y = 40)
time_clock_gll.creat()

latitude_gll = Wid_label(name = 'Широта: ', x = 400, y = 70)
latitude_gll.creat()

longtitude_gll = Wid_label(name = 'Долгота: ', x = 400, y = 100)
longtitude_gll.creat()

out_form()
out_form_gll()

root.mainloop()