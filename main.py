#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

# Настройки порта
port_num = 'COM7'
baud_rate = 9600

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
    global port_num
    global baud_rate
    try:
        gnss = serial.Serial(port_num, baudrate=baud_rate)
        connect.set_color('green')
        while True:
            ser_bytes = gnss.readline()
            decoded_bytes = ser_bytes.decode('utf-8')
            data = decoded_bytes.split(',')
            if data[0] == '$GNRMC' and data[1] != '':
                print(data)
                global_data_rmc = data
                data = str(data)
                gnss_file_rmc = open('gnss_rmc.txt', 'a')
                gnss_file_rmc.write(data + '\n')
                gnss_file_rmc.close()

            if data[0] == '$GNGLL' and data[5] != '':
                print(data)
                global_data_gll = data
                data = str(data)
                gnss_file_gll = open('gnss_gll.txt', 'a')
                gnss_file_gll.write(data + '\n')
                gnss_file_gll.close()
    except serial.SerialException:
        connect.set_color('red')
        time_clock.set('Нет данных')
        latitude.set('Нет данных')
        longtitude.set('Нет данных')
        reliability.set('Нет данных')
        reliability.set_color(root.cget('bg'))
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

# Поток обработки и вывода в форму
@potok
def out_form():
    global global_data_rmc
    global global_data_gll
    data_lat = '0'
    data_long = '0'
    data_time = '0'
    while True:
        if global_data_rmc[2] == 'V':
            reliability.set('Не достоверно')
            reliability.set_color('red')
        if global_data_rmc[2] == 'A':
            reliability.set('Достоверно')
            reliability.set_color('green')
        if global_data_gll[0] == '$GNGLL':
            data_lat = get_lat(global_data_gll[1])
            data_long = get_long(global_data_gll[3])
            data_time = get_time(global_data_gll[5])
            latitude.set(data_lat)
            longtitude.set(data_long)
            time_clock.set(data_time)
        sleep(.5)

# Запускаем поток read_put в фоне


root = tk.Tk()
root_w = 1024
root_h = 768
root_size = str(root_w) + 'x' + str(root_h)
root.iconbitmap('image/icon.ico')
root.title('GNSS IL-114')
root.geometry(root_size)
root.resizable(0, 0)

# Поля данных GNSS
data_type = Wid_label(name = 'Тип данных: ', x = 10, y = 10)
data_type.creat()
data_type.set('GNGLL')

time_clock = Wid_label(name = 'Время (UTC): ', x = 10, y = 40)
time_clock.creat()

latitude = Wid_label(name = 'Широта: ', x = 10, y = 70)
latitude.creat()

longtitude = Wid_label(name = 'Долгота: ', x = 10, y = 100)
longtitude.creat()

reliability = Wid_label(name = 'Достоверность: ', x = 10, y = 130)
reliability.creat()

connect = Wid_label(name = 'Подключение: ', x = 10, y = 160)
connect.creat()
connect.set(port_num + ', ' + str(baud_rate))

read_put()

out_form()

root.mainloop()