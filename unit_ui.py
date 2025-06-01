#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tkinter import*

# Класс виджетов надписей
class Wid_label():
    def __init__(self, name, x, y, root):
        self.name = name
        self.root = root
        # координаты размещения виджета
        self.x = x
        self.y = y

    def creat(self):
        lb_name_wid = Label(self.root, width = 14, text = self.name, font = "Arial 12 bold", relief = RIDGE,
                            borderwidth = 2, anchor = 'w')
        lb_name_wid.place(x = self.x, y = self.y)

        self.lb_value_wid = Label(self.root, width = 15, font = "Arial 12 bold", relief = RIDGE, borderwidth = 2)
        self.lb_value_wid.place(x = self.x + 150, y = self.y)

    def set(self, value):
        self.value = value
        self.lb_value_wid.config(text = self.value)

    def set_color(self, color):
        self.color = color
        self.lb_value_wid.config(background = self.color)

if __name__ == "__main__":
    pass