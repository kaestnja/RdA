#!/usr/bin/env python
import tkinter as tk
import os

def temp_label(label):

    def Temp():
        t = os.popen("vcgencmd measure_temp").readline()
        c=(t.replace("temp=","").replace("'C\n",""))
        f=round(9.0/5.0*int(float(c))+32,1)
        label.config(text="\nTemp= "+str(f)+" F\n\n"+"Temp= "+str(c)+" C\n")
        label.after(2000, Temp)
    Temp()

box = tk.Tk()
box.title("Temperatures")
box.geometry('+1800+1030')
box.configure(bg="light green")
label = tk.Label(box, fg="black", bg="light green", padx=12, pady=12, height=3, relief= "flat")
label.pack()
temp_label(label)
stop = tk.Button(box, text='Stop', width=5, fg="white", bg="red", relief= "raised", command=box.destroy)
stop.pack()
box.mainloop()
