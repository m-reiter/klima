#!/usr/bin/env python
# coding: utf-8
""" Kontrolloberfläche für die feuchtegesteuerte Kellerlüftung
"""

# directories
BASEDIR='/opt/klima'
GRAPHDIR=BASEDIR+'/graphics'

# green
green = "#00b000"

from Tkinter import *
import tkMessageBox
import getvalues
import fanctl
import time
import locale

locale.setlocale(locale.LC_ALL,'de_DE')

class LockDialog(Toplevel):

    def __init__(self, parent, controller, onoff="on"):

        Toplevel.__init__(self, parent)
        self.transient(parent)
        self.configure(background="white")
        self.overrideredirect(1)
        self.geometry("300x400+10+40")

        self.onoff = onoff
        self.controller = controller

        self.multiplier = IntVar()
        self.input = StringVar()

        if onoff == "on":
            title = "An"
            action = "einschalten"
            col = green
        else:
            title = "Aus"
            action = "ausschalten"
            col = "red"

        Label(self,text=title, background=col, foreground="white", font="Roboto 12").place(x=0,y=0,width=300,height=20)
        Label(self,text="Lüfter %s für?" % action, background="white", font="Roboto 20").place(x=0,y=20,width=300,height=40)
        self.entry = Entry(self,font="Roboto 24",textvariable=self.input)
        self.entry.place(x=5,y=60,width=172,height=54)
        self.entry.configure(inserton=0,selectforeground="white",selectbackground="black")
        self.entry.bind("<1>",self.noop)
        Button(self,text="1",bg="white",
               activebackground="white",
               font="Roboto 24 bold",command=lambda:self.type("1")).place(x=5,y=119,width=54,height=54)
        Button(self,text="2",bg="white",
               activebackground="white",
               font="Roboto 24 bold",command=lambda:self.type("2")).place(x=64,y=119,width=54,height=54)
        Button(self,text="3",bg="white",
               activebackground="white",
               font="Roboto 24 bold",command=lambda:self.type("3")).place(x=123,y=119,width=54,height=54)
        Button(self,text="4",bg="white",
               activebackground="white",
               font="Roboto 24 bold",command=lambda:self.type("4")).place(x=5,y=178,width=54,height=54)
        Button(self,text="5",bg="white",
               activebackground="white",
               font="Roboto 24 bold",command=lambda:self.type("5")).place(x=64,y=178,width=54,height=54)
        Button(self,text="6",bg="white",
               activebackground="white",
               font="Roboto 24 bold",command=lambda:self.type("6")).place(x=123,y=178,width=54,height=54)
        Button(self,text="7",bg="white",
               activebackground="white",
               font="Roboto 24 bold",command=lambda:self.type("7")).place(x=5,y=237,width=54,height=54)
        Button(self,text="8",bg="white",
               activebackground="white",
               font="Roboto 24 bold",command=lambda:self.type("8")).place(x=64,y=237,width=54,height=54)
        Button(self,text="9",bg="white",
               activebackground="white",
               font="Roboto 24 bold",command=lambda:self.type("9")).place(x=123,y=237,width=54,height=54)
        Button(self,text="0",bg="white",
               activebackground="white",
               font="Roboto 24 bold",command=lambda:self.type("0")).place(x=5,y=296,width=54,height=54)
        Button(self,text="C",bg="red",foreground="white",
               activebackground="red",activeforeground="white",
               font="Roboto 24 bold",command=self.reset).place(x=64,y=296 ,width=113,height=54)
        Radiobutton(self,text="Minuten",bg="blue",fg="white",
                    activebackground="blue",activeforeground="white",
                    selectcolor="lightblue",font="Roboto 18",command=self.checkInf,indicatoron=0,variable=self.multiplier,value=1).place(x=182,y=60,width=113,height=54)
        Radiobutton(self,text="Stunden",bg="blue",fg="white",
                    activebackground="blue",activeforeground="white",
                    selectcolor="lightblue",font="Roboto 18",command=self.checkInf,indicatoron=0,variable=self.multiplier,value=60).place(x=182,y=119,width=113,height=54)
        Radiobutton(self,text="Tage",bg="blue",fg="white",
                    activebackground="blue",activeforeground="white",
                    selectcolor="lightblue",font="Roboto 18",command=self.checkInf,indicatoron=0,variable=self.multiplier,value=1440).place(x=182,y=178,width=113,height=54)
        Radiobutton(self,text="Wochen",bg="blue",fg="white",
                    activebackground="blue",activeforeground="white",
                    selectcolor="lightblue",font="Roboto 18",command=self.checkInf,indicatoron=0,variable=self.multiplier,value=10080).place(x=182,y=237,width=113,height=54)
        Radiobutton(self,text="∞",bg="blue",fg="white",
                    activebackground="blue",activeforeground="white",
                    selectcolor="lightblue",font="Roboto 18",command=self.setInf,indicatoron=0,variable=self.multiplier,value=-1).place(x=182,y=296,width=113,height=54)
        Button(self,text="Abbrechen", bg="red", fg="white",
               activebackground="red", activeforeground="white",
               font="Roboto 16", command=self.destroy).place(x=0,y=364,width=150,height=36)
        Button(self,text="OK", bg=green, fg="white",
               activebackground=green, activeforeground="white",
               font="Roboto 16", command=self.doit).place(x=150,y=364,width=150,height=36)

        self.reset()

        self.grab_set()
        parent.wait_window(self)

    def reset(self):
        self.multiplier.set(60)
        self.input.set("2")
        self.entry.configure(justify="right")
        self.entry.selection_range(0,1)

    def setInf(self):
        self.input.set("dauerhaft")
        self.entry.configure(justify="center")
        self.entry.select_clear()

    def checkInf(self):
        if self.input.get() == "dauerhaft":
            self.multiplier.set(-1)

    def type(self,key):
        if self.input.get() == "dauerhaft":
            return
        if self.entry.select_present():
            if not key == "0":
                self.input.set(key)
                self.entry.select_clear()
        else:
            self.input.set(self.input.get()+key)

    def doit(self):
        if self.onoff == "on":
            state = 1
        else:
            state = 0

        if self.input.get() == "dauerhaft":
            duration = "inf"
        else:
            duration = int(self.input.get()) * int(self.multiplier.get())

        fanctl.lock(state,duration)

        self.controller.updateValues()
            
        self.destroy()

    def noop(self):
        return "break"

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
        self.FanLabel.place(x=1,y=360,height=40,width=139)
        self.LockLabel = Label(master, textvariable=self.LockLine, font="Roboto 18", background="blue", foreground="white")
        self.LockLabel.place(x=141,y=360,height=40,width=178)

        Button(master, text="An", font="Roboto 30 bold",
               fg="white", bg=green,
               activeforeground="white", activebackground=green,
               command=self.lockOn).place(x=5,y=405,width=100,height=70)
        Button(master, text="Auto", font="Roboto 30 bold",
               fg="white", bg="blue",
               activeforeground="white", activebackground="blue",
               command=self.unlock).place(x=110,y=405,width=100,height=70)
        Button(master, text="Aus", font="Roboto 30 bold",
               fg="white", bg="red",
               activeforeground="white", activebackground="red",
               command=self.lockOff).place(x=215,y=405,width=100,height=70)

        self.updateLoop()

    def lockOn(self):
        LockDialog(self.root,self)

    def lockOff(self):
        LockDialog(self.root,self,onoff="off")

    def unlock(self):
        if fanctl.islocked():
            tl = self.tl = Toplevel(self.root,background="white",bd=3)
            tl.overrideredirect(1)
            tl.geometry("300x200+10+140")
            Label(tl,text="Auto", background="blue", foreground="white", font="Roboto 12").place(x=0,y=0,width=300,height=20)
            Label(tl,text="Lüfter entsperren?", width=300, height=3, background="white", font="Roboto 24 bold").place(x=0,y=20,width=300,height=142)
            Button(tl,text="Abbrechen", bg="red", fg="white",
                   activebackground="red", activeforeground="white",
                   font="Roboto 16", command=tl.destroy).place(x=0,y=162,width=150,height=36)
            Button(tl,text="OK", bg=green, fg="white",
                   activebackground=green, activeforeground="white",
                   font="Roboto 16", command=self.dounlock).place(x=150,y=162,width=150,height=36)
            tl.grab_set()
            self.root.wait_window(tl)

    def dounlock(self):
        fanctl.unlock()
        self.updateValues()

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
                self.RHkellerLabel.configure(foreground=green)
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
                self.FanLabel.configure(background=green)
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
                if islocked > ( 6*24*60*60 ):
                    n = ( islocked -1 ) / ( 7*24*60*60 ) + 1
                    unit = "Woche"
                    plural = "n"
                elif islocked > ( 23*60*60 ):
                    n = ( islocked - 1 ) / ( 24*60*60 ) + 1
                    unit = "Tag"
                    plural = "e"
                    self.LockLine.set("%i Tage" % n)
                elif islocked > ( 59*60 ):
                    n = ( islocked - 1 ) / ( 60*60 ) + 1
                    unit = "Stunde"
                    plural = "n"
                    self.LockLine.set("%i Stunden" % n)
                else:
                    n = ( islocked -1 ) / 60 + 1
                    unit = "Minute"
                    plural = "n"
                    self.LockLine.set("% i Minuten" % n)
                if n > 1:
                    unit += plural
                self.LockLine.set("%i %s" % (n,unit))
        else:
            self.LockLabel.configure(background="blue")
            self.LockLine.set("Auto")

        self.TimeLine.set(time.strftime("%a %-d.%-m.%Y %H:%M"))

    def updateLoop(self):
        root.after(60000,self.updateLoop)
        self.updateValues()

root = Tk()

app = Controller(root)

root.mainloop()
