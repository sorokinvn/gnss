#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import sleep
from tkinter import *
from tkinter import ttk
import tkinter as tk
from thread import Thread
from unit_ui import Wid_label
from unit_nmea import read_put
from unit_nmea import get_lat
from unit_nmea import get_long
from unit_nmea import get_time
from unit_nmea import get_port_list
import unit_nmea

global thread_01, thread_02

# Функция обработки и вывода в форму
def out_form():
    data_lat = '0'
    data_long = '0'
    data_time = '0'
    while True:
        data_rmc = unit_nmea.data_rmc
        data_gll = unit_nmea.data_gll
        con_port = unit_nmea.con_port
        if data_gll[0] == '$GNGLL':
            data_lat = get_lat(data_gll[1])
            data_long = get_long(data_gll[3])
            data_time = get_time(data_gll[5])
            latitude.set(data_lat + '  ' + data_gll[2])
            longtitude.set(data_long + '  ' + data_gll[4])
            time_clock.set(data_time)
        if data_rmc[2] == 'A':
            reliability.set('OK')
            reliability.set_color('green')
        if data_rmc[2] == 'V':
            reliability.set('No')
            reliability.set_color('red')
        sleep(.3)
        if con_port == True:
            connect.set('Подключено')
            connect.set_color('green')
        if con_port == False:
            connect.set('Отключено')
            connect.set_color('red')

def select_port():
    global thread_01, thread_02
    unit_nmea.num_port = cb_com_value.get()
    thread_01 = Thread(read_put)
    thread_02 = Thread(out_form)
    thread_01.start()
    thread_02.start()

def un_select_port():
    global thread_01, thread_02
    unit_nmea.thread_01_stop = False
    thread_01.kill()
    thread_02.kill()
    thread_01.join()
    thread_02.join()

root = tk.Tk()
root_w = 1024
root_h = 768
root_size = str(root_w) + 'x' + str(root_h)
root.iconbitmap('image/icon.ico')
root.title('GNSS IL-114')
root.geometry(root_size)
root.resizable(0, 0)

# Поля данных GNSS
data_type = Wid_label(name = 'Тип данных: ', x = 10, y = 10, root = root)
data_type.creat()
data_type.set('GNGLL')

time_clock = Wid_label(name = 'Время (UTC): ', x = 10, y = 40, root = root)
time_clock.creat()

latitude = Wid_label(name = 'Широта: ', x = 10, y = 70, root = root)
latitude.creat()

longtitude = Wid_label(name = 'Долгота: ', x = 10, y = 100, root = root)
longtitude.creat()

reliability = Wid_label(name = 'Достоверность: ', x = 10, y = 130, root = root)
reliability.creat()

connect = Wid_label(name = 'Подключение: ', x = 10, y = 160, root = root)
connect.creat()

cb_com_value = StringVar()
cb_com = ttk.Combobox(root, values = get_port_list(), width = 10, state = 'readonly', textvariable = cb_com_value)
cb_com.place(x = 350, y = 10)
cb_com.current(0)

bt_connect = tk.Button(root, text = 'Подключить', width = 10, command = select_port)
bt_connect.place(x = 350, y = 40)

bt_dis_connect = tk.Button(root, text = 'Отключить', width = 10, command = un_select_port)
bt_dis_connect.place(x = 350, y = 70)

root.mainloop()
