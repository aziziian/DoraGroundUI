import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import tkinter as tk




window = Tk()
window.title("Dora Ground Commands")

window.geometry('600x300')

window.tk.call('tk', 'scaling',2.0)


lbl = Label(window, text = "Choose Command")
lbl.grid(column =8, row=0)


btnSchd = Button(window, text = "Schedule Command", command=btnSchd_clicked)
btnSchd.grid(column=4, row=2)

btnI2C = Button(window, text = "I2C Command", command=btnI2C_clicked)
btnI2C.grid(column =9, row=2 )

btnBash = Button(window, text = "Run Bash", command=btnBash_clicked)
btnBash.grid(column = 4, row = 3)

btnADCS = Button(window, text = "ADCS Set Config", command=btnADCS_clicked)
btnADCS.grid(column = 9, row = 3)

btnFileTran = Button(window, text = "File Burst Transfer Request", command=btnFileTran_clicked)
btnFileTran.grid(column = 4, row = 4)

btnFileUp = Button(window, text = "File Upload Packet", command=btnFileUp_clicked)
btnFileUp.grid(column = 9, row = 4)

btnFile = Button(window, text = "Files From Directory", command=btnFile_clicked)
btnFile.grid(column = 4, row =5)

btnFileSize = Button(window, text = "Get File Size", command=btnFileSize_clicked)
btnFileSize.grid(column = 9, row = 5)


window.mainloop()