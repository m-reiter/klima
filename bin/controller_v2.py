#!/usr/bin/env python
# coding: utf-8
""" Kontrolloberfläche für die feuchtegesteuerte Kellerlüftung
"""

# directories
BASEDIR='/opt/klima'
GRAPHDIR=BASEDIR+'/graphics'

from Tkinter import *
import tkMessageBox
import getvalues
import fanctl
import time
import locale

locale.setlocale(locale.LC_ALL,'de_DE')

class LockDialog(Toplevel):

    def __init__(self, parent, onoff="on"):

        Toplevel.__init__(self, parent)
        self.transient(parent)
        self.configure(background="white")
        self.overrideredirect(1)
        self.geometry("300x200+10+140")

        self.onoff = onoff

        if onoff == "on":
            title = "An"
            msg = "Lüfter einschalten?"
            col = "green"
        else:
            title = "Aus"
            msg = "Lüfter ausschalten?"
            col = "red"

        Label(self,text=title, width=300, background=col, foreground="white", font="Roboto 12").pack()
        Label(self,text=msg, width=300, height=3, background="white", font="Roboto 24 bold").pack()
        Button(self,text="Abbrechen", width=9, background="red", foreground="white", font="Roboto 18", command=self.destroy).pack(side=LEFT)
        Button(self,text="OK", width=9, background="green", foreground="white", font="Roboto 18", command=self.doit).pack(side=BOTTOM)
        self.grab_set()
        parent.wait_window(self)

    def doit(self):
        if self.onoff == "on":
            fanctl.lock(1,"inf")
        else:
            fanctl.lock(0,"inf")

        self.LockLabel.configure(background="red")
        self.LockLine.set("gesperrt")
            
        self.destroy()

class Controller:

    def __init__(self, master):

        self.Tkeller = StringVar()
        self.RHkeller = StringVar()
        self.DPkeller = StringVar()
        self.AHkeller = StringVar()
        self.Taussen = StringVar()
        self.RHaussen = StringVar()
        self.DPaussen = StringVar()
        self.AHaussen = StringVar()
        self.FanLine = StringVar()
        self.LockLine = StringVar()
        self.TimeLine = StringVar()
        
        self.root = master

        master.geometry('320x480')
        master.resizable(width=False, height=False)
        master.configure(background='white')

        if root.winfo_screenwidth() == 320 and root.winfo_screenheight() == 480:
            master.attributes("-fullscreen",True)

        Label(master, text="Keller", font="Roboto 16", background="white", anchor=W).place(x=0,y=0,height=20)
        Label(master, textvariable=self.TimeLine, font="Roboto 10", background="white", anchor=E).place(x=320,y=-1,anchor=NE,height=16)
        Label(master, textvariable=self.Tkeller, font="Roboto 25 bold", background="white",anchor=E).place(x=140,y=20,anchor=NE,height=40)
        Label(master, text="RF", font="Roboto 12 bold", background="white").place(x=148,y=22)
        self.RHkellerLabel = Label(master, textvariable=self.RHkeller, font="Roboto 25 bold", background="white")
        self.RHkellerLabel.place(x=170,y=20,width=150,height=40)
        Label(master, text="TP", font="Roboto 12 bold", background="white").place(x=0,y=60)
        Label(master, textvariable=self.DPkeller, font="Roboto 25 bold", background="white").place(x=140,y=55,anchor=NE,height=45)
        Label(master, text="AF", font="Roboto 12 bold", background="white").place(x=148,y=60)
        Label(master, textvariable=self.AHkeller, font="Roboto 25 bold", background="white").place(x=170,y=55,width=150,height=45)
        self.RHLabel = Label(master)
        self.RHLabel.place(x=0,y=100,height=80)
        self.AHLabel = Label(master,pady=0)
        self.AHLabel.place(x=0,y=180,height=80)
        Label(master, text="Aussen", font="Roboto 16", background="white", anchor=W).place(x=0,y=260,height=20)
        Label(master, textvariable=self.Taussen, font="Roboto 25 bold", background="white").place(x=140,y=280,anchor=NE,height=40)
        Label(master, text="RF", font="Roboto 12 bold", background="white").place(x=148,y=282)
        Label(master, textvariable=self.RHaussen, font="Roboto 25 bold", background="white").place(x=170,y=280,width=150,height=40)
        Label(master, text="TP", font="Roboto 12 bold", background="white").place(x=0,y=320)
        Label(master, textvariable=self.DPaussen, font="Roboto 25 bold", background="white").place(x=140,y=315,anchor=NE,height=45)
        Label(master, text="AF", font="Roboto 12 bold", background="white").place(x=148,y=320)
        Label(master, textvariable=self.AHaussen, font="Roboto 25 bold", background="white").place(x=170,y=315,width=150,height=45)
        self.FanLabel = Label(master, textvariable=self.FanLine, font="Roboto 18", background="white")
        self.FanLabel.place(x=0,y=360,height=40,width=140)
        self.LockLabel = Label(master, textvariable=self.LockLine, font="Roboto 18", background="blue", foreground="white")
        self.LockLabel.place(x=140,y=360,height=40,width=180)

        Button(master, text="An", font="Roboto 30 bold", foreground="white", background="green", command=self.lockOn).place(x=5,y=405,width=100,height=70)
        Button(master, text="Auto", font="Roboto 30 bold", foreground="white", background="blue", activebackground="blue", command=self.unlock).place(x=110,y=405,width=100,height=70)
        Button(master, text="Aus", font="Roboto 30 bold", foreground="white", background="red", command=self.lockOff).place(x=215,y=405,width=100,height=70)

        self.updateLoop()

    def lockOn(self):
        LockDialog(self.root)

    def lockOff(self):
        LockDialog(self.root,onoff="off")

    def unlock(self):
        if fanctl.islocked():
            tl = self.tl = Toplevel(self.root,background="white",bd=3)
            tl.overrideredirect(1)
            tl.geometry("300x200+10+140")
            Label(tl,text="Auto", width=300, background="blue", foreground="white", font="Roboto 12").pack()
            Label(tl,text="Lüfter entsperren?", width=300, height=3, background="white", font="Roboto 24 bold").pack()
            Button(tl,text="Abbrechen", width=9, background="red", foreground="white", font="Roboto 18", command=tl.destroy).pack(side=LEFT)
            Button(tl,text="OK", width=9, background="green", foreground="white", font="Roboto 18", command=self.dounlock).pack(side=BOTTOM)
            tl.grab_set()
            self.root.wait_window(tl)

    def dounlock(self):
        fanctl.unlock()
        self.LockLabel.configure(background="blue")
        self.LockLine.set("Auto")

        self.tl.destroy()

    def updateValues(self):

        currentState = getvalues.getValues()

        if currentState['Tkeller'] == "U":
            self.Tkeller.set("--    ")
        else:
            self.Tkeller.set("%5.1f°C" % float(currentState['Tkeller']))
        if currentState['RHkeller'] == "U":
            self.RHkeller.set("--")
            self.RHkellerLabel.configure(foreground="black")
        else:
            RHkeller = float(currentState['RHkeller'])
            self.RHkeller.set("%2.0f%%" % RHkeller)
            if RHkeller > 60.0:
                self.RHkellerLabel.configure(foreground="red")
            else:
                self.RHkellerLabel.configure(foreground="black")
        if currentState['DPkeller'] == "U":
            self.DPkeller.set("--    ")
        else:
            self.DPkeller.set("%5.1f°C" % float(currentState['DPkeller']))
        if currentState['AHkeller'] == "U":
            self.AHkeller.set("--")
        else:
            self.AHkeller.set("%3.1fg/m³" % float(currentState['AHkeller']))

        if currentState['Taussen'] == "U":
            self.Taussen.set("--    ")
        else:
            self.Taussen.set("%5.1f°C" % float(currentState['Taussen']))
        if currentState['RHaussen'] == "U":
            self.RHaussen.set("--")
        else:
            self.RHaussen.set("%2.0f%%" % float(currentState['RHaussen']))
        if currentState['DPaussen'] == "U":
            self.DPaussen.set("--    ")
        else:
            self.DPaussen.set("%5.1f°C" % float(currentState['DPaussen']))
        if currentState['AHaussen'] == "U":
            self.AHaussen.set("--")
        else:
            self.AHaussen.set("%4.1fg/m³" % float(currentState['AHaussen']))

        if currentState['Fan'] == "U":
            Fan = "--"
            self.FanLabel.configure(background="black")
            self.FanLabel.configure(foreground="white")
        else:
            if float(currentState['Fan']) > .99:
                Fan = "AN"
                self.FanLabel.configure(background="green")
                self.FanLabel.configure(foreground="white")
            else:
                Fan = "AUS"
                self.FanLabel.configure(background="red")
                self.FanLabel.configure(foreground="white")

        RHimage = PhotoImage(file=GRAPHDIR+'/rhsmall.png')
        AHimage = PhotoImage(file=GRAPHDIR+'/ahsmall.png')

        self.RHLabel.configure(image=RHimage)
        self.AHLabel.configure(image=AHimage)

        self.RHLabel.image = RHimage
        self.AHLabel.image = AHimage

        self.FanLine.set("Lüfter: "+Fan)

        islocked = fanctl.islocked()

        if islocked:
            self.LockLabel.configure(background="red")
            if islocked == "inf":
                self.LockLine.set("gesperrt")
            else:
                if islocked > 604800:
                    n = islocked / 604800
                    self.LockLine.set("%i Wochen" % n)
                elif islocked > 86400:
                    n = islocked / 86400
                    self.LockLine.set("%i Tage" % n)
                elif islocked > 3600:
                    n = islocked / 3600
                    self.LockLine.set("%i Stunden" % n)
                else:
                    n = islocked / 60
                    self.LockLine.set("% i Minuten" % n)
        else:
            self.LockLabel.configure(background="blue")
            self.LockLine.set("Auto")

        self.TimeLine.set(time.strftime("%a %-d.%-m.%Y %H:%M"))

    def updateLoop(self):
        self.updateValues()
        root.after(60000,self.updateLoop)

root = Tk()

app = Controller(root)

root.mainloop()
