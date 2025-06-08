#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
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


# Функция обработки и вывода в форму
def out_form():
    data_lat = '0'
    data_long = '0'
    data_time = '0'

    while True:
        data_rmc = unit_nmea.data_rmc
        con_port = unit_nmea.con_port
        if data_rmc[0] == '$GNRMC':
            data_lat = get_lat(data_rmc[3])
            data_long = get_long(data_rmc[5])
            data_time = get_time(data_rmc[1])
            data_type.set(data_rmc[0])
            latitude.set(data_lat + '  ' + data_rmc[4])
            longtitude.set(data_long + '  ' + data_rmc[6])
            time_clock.set(data_time)
        if data_rmc[2] == 'A':
            reliability.set('OK')
            reliability.set_color('green')
        if data_rmc[2] == 'V':
            reliability.set('No')
            reliability.set_color('red')
        sleep(.1)
        if unit_nmea.con_port == True:
            connect.set('Подключено')
            connect.set_color('green')
        if unit_nmea.con_port == False:
            unit_nmea.data_rmc = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
            reliability.set('')
            reliability.set_color(root.cget('bg'))
            connect.set('Отключено')
            connect.set_color('red')
            data_type.set('')
            latitude.set('')
            longtitude.set('')
            time_clock.set('')

#Процедура кнопки Подключить
def select_port():
    unit_nmea.num_port = cb_com_value.get()
    dt = datetime.now()
    unit_nmea.time_now = str(dt.year) + '_' +  str(dt.month) + '_' + str(dt.day) + '_' + str(dt.hour) + '_' + str(dt.minute) + '_' + str(dt.second)
    thread_01 = Thread(target = read_put, daemon = True)
    thread_02 = Thread(target = out_form, daemon = True)
    thread_01.start()
    thread_02.start()

#Процедура кнопки Отключить
def un_select_port():
    unit_nmea.thread_01_stop = False

#Гоавный цикл окна программы
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
