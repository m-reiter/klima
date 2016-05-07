#!/usr/bin/env python
# coding: utf-8
""" Kontrolloberfläche für die feuchtegesteuerte Kellerlüftung
"""

# directories
BASEDIR='/opt/klima'
GRAPHDIR=BASEDIR+'/graphics'

from Tkinter import *
import getvalues

class Controller:

    def __init__(self, master):

        self.KellerLine1 = StringVar()
        self.KellerLine2 = StringVar()
        self.AussenLine1 = StringVar()
        self.AussenLine2 = StringVar()
        self.FanLine = StringVar()
        
        self.root = master

        master.geometry('320x480')
        master.resizable(width=False, height=False)
        master.configure(background='white')

        if root.winfo_screenwidth() == 320 and root.winfo_screenheight() == 480:
            master.attributes("-fullscreen",True)

        Label(master, text="Keller", font="Roboto 18", background="white", anchor="w").pack()
        Label(master, textvariable=self.KellerLine1, font="Roboto 28 bold", background="white").pack()
        Label(master, textvariable=self.KellerLine2, font="Roboto 28 bold", background="white").pack()
        self.RHLabel = Label(master)
        self.RHLabel.pack()
        self.AHLabel = Label(master)
        self.AHLabel.pack()
        Label(master, text="Aussen", font="Roboto 18", background="white", anchor="w").pack()
        Label(master, textvariable=self.AussenLine1, font="Roboto 28 bold", background="white").pack()
        Label(master, textvariable=self.AussenLine2, font="Roboto 28 bold", background="white").pack()
        self.FanLabel = Label(master, textvariable=self.FanLine, font="Roboto 18", background="white", width=320)
        self.FanLabel.pack()

        self.updateValues()


    def updateValues(self):

        currentState = getvalues.getValues()

        if currentState['Tkeller'] == "U":
            Tkeller = "--"
        else:
            Tkeller = "%5.1f°C" % float(currentState['Tkeller'])
        if currentState['RHkeller'] == "U":
            RHkeller = "--"
        else:
            RHkeller = "%2.0f%%" % float(currentState['RHkeller'])
        if currentState['DPkeller'] == "U":
            DPkeller = "--"
        else:
            DPkeller = "%5.1f°C" % float(currentState['DPkeller'])
        if currentState['AHkeller'] == "U":
            AHkeller = "--"
        else:
            AHkeller = "%3.1fg/m³" % float(currentState['AHkeller'])

        if currentState['Taussen'] == "U":
            Taussen = "--"
        else:
            Taussen = "%5.1f°C" % float(currentState['Taussen'])
        if currentState['RHaussen'] == "U":
            RHaussen = "--"
        else:
            RHaussen = "%2.0f%%" % float(currentState['RHaussen'])
        if currentState['DPaussen'] == "U":
            DPaussen = "--"
        else:
            DPaussen = "%5.1f°C" % float(currentState['DPaussen'])
        if currentState['AHaussen'] == "U":
            AHaussen = "--"
        else:
            AHaussen = "%3.1fg/m³" % float(currentState['AHaussen'])

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

        self.KellerLine1.set(Tkeller+" "+RHkeller)
        self.KellerLine2.set(DPkeller+" "+AHkeller)

        self.AussenLine1.set(Taussen+" "+RHaussen)
        self.AussenLine2.set(DPaussen+" "+AHaussen)

        self.FanLine.set("Lüfter: "+Fan)

        root.after(60000,self.updateValues)

root = Tk()

app = Controller(root)

root.mainloop()
