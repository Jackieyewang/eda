#coding:utf-8
import bisect
import struct
from tkinter import *
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import oop
import option
import ver
import cirdraw
import input
import prepare
import caculater



##################################################################################################
# main
##################################################################################################

def main():
        input.get_input()
        NumnodeS = cirdraw.draw()
        prepare.cube_ready(NumnodeS)
        caculater.caclulater(NumnodeS)


#################################################################################################
#GUI
#################################################################################################
class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name


    def set_init_window(self):
        self.init_window_name.title("王业伟的hspice")
        self.init_window_name.geometry('1068x681+10+10')
        self.init_data_label = Label(self.init_window_name, text="netlist")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window_name, text="输出结果")
        self.result_data_label.grid(row=0, column=12)
        self.init_data_Text = Text(self.init_window_name, width=67, height=35)
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_window_name, width=70, height=35)
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.str_trans_to_md5_button = Button(self.init_window_name, text="输出", bg="lightblue", width=10,command=self.do)
        self.str_trans_to_md5_button.grid(row=1, column=11)

    def do(self):
        ver.init()
        src = self.init_data_Text.get(1.0,END).strip().replace("\n","").encode()
        with open('text3.txt','w') as f:
            f.write(self.init_data_Text.get(1.0,END))
        f.close()
        print(ver.list)

        main()
        self.result_data_Text.delete(1.0,END)
        self.result_data_Text.insert(1.0,ver.res)

def gui_start():
    init_window = Tk()
    ZMJ_PORTAL = MY_GUI(init_window)
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()


#gui_start()

main()
