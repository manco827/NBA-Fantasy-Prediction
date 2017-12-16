# File:        FrontendGUI.py
# Description: This file creates and loads the Fantasy Point projection GUI. The GUI allows the user to predict Fantasy
#              Points for multiple players for games at least 20 days into the future. This file imports the Backend.py 
#              class in order to retrieve the necessary data.

#! /usr/bin/env python

import Backend

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

import GUI_Tool_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    GUI_Tool_support.set_Tk_var()
    top = NBA_Fantasy_Prediction (root)
    GUI_Tool_support.init(root, top)
    root.mainloop()

w = None
def create_NBA_Fantasy_Prediction(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    GUI_Tool_support.set_Tk_var()
    top = NBA_Fantasy_Prediction (w)
    GUI_Tool_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_NBA_Fantasy_Prediction():
    global w
    w.destroy()
    w = None

class NBA_Fantasy_Prediction:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#d9d9d9' # X11 color: 'gray85'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("996x583+281+76")
        top.title("NBA Fantasy Prediction")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")
        self.playerList = []

        # Create the GUI Frame
        self.Frame1 = Frame(top)
        self.Frame1.place(relx=0.03, rely=0.12, relheight=0.83, relwidth=0.93)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(background="#d9d9d9")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")
        self.Frame1.configure(width=925)

        # Create the Scrolled Listbox that allows the user search a list of every active NBA Player
        self.Scrolledlistbox1 = ScrolledListBox(self.Frame1)
        self.Scrolledlistbox1.place(relx=0.01, rely=0.02, relheight=0.91
                , relwidth=0.2)
        self.Scrolledlistbox1.configure(background="white")
        self.Scrolledlistbox1.configure(font="TkFixedFont")
        self.Scrolledlistbox1.configure(foreground="black")
        self.Scrolledlistbox1.configure(highlightbackground="#d9d9d9")
        self.Scrolledlistbox1.configure(highlightcolor="#d9d9d9")
        self.Scrolledlistbox1.configure(selectbackground="#c4c4c4")
        self.Scrolledlistbox1.configure(selectforeground="black")
        self.Scrolledlistbox1.configure(width=10)

        # Creates the "ADD" button which allows the user to select which NBA Players to make predictions for 
        self.btnADD = Button(self.Frame1)
        self.btnADD.place(relx=0.23, rely=0.37, height=42, width=127)
        self.btnADD.configure(activebackground="#d9d9d9")
        self.btnADD.configure(activeforeground="#000000")
        self.btnADD.configure(background="#d9d9d9")
        self.btnADD.configure(foreground="#000000")
        self.btnADD.configure(highlightbackground="#d9d9d9")
        self.btnADD.configure(highlightcolor="black")
        self.btnADD.configure(text='''ADD''')
        self.btnADD.configure(command=self.addEntry)

        # Creates the "DELETE" button which allows the user to remove an NBA Player from the prediction list
        self.btnDELETE = Button(self.Frame1)
        self.btnDELETE.place(relx=0.23, rely=0.47, height=42, width=127)
        self.btnDELETE.configure(activebackground="#d9d9d9")
        self.btnDELETE.configure(activeforeground="#000000")
        self.btnDELETE.configure(background="#d9d9d9")
        self.btnDELETE.configure(foreground="#000000")
        self.btnDELETE.configure(highlightbackground="#d9d9d9")
        self.btnDELETE.configure(highlightcolor="black")
        self.btnDELETE.configure(text='''DELETE''')
        self.btnDELETE.configure(command=self.deleteEntry)

        # Creates the "Calculate FP" button which kicks off the backend script that predicts the Fantasy Points for the 
        # selected NBA Players
        self.btnCALCULATE = Button(self.Frame1)
        self.btnCALCULATE.place(relx=0.63, rely=0.51, height=52, width=127)
        self.btnCALCULATE.configure(activebackground="#d9d9d9")
        self.btnCALCULATE.configure(activeforeground="#000000")
        self.btnCALCULATE.configure(background="#d9d9d9")
        self.btnCALCULATE.configure(foreground="#000000")
        self.btnCALCULATE.configure(highlightbackground="#d9d9d9")
        self.btnCALCULATE.configure(highlightcolor="black")
        self.btnCALCULATE.configure(text='''Calculate FP''')
        self.btnCALCULATE.configure(command=self.calculateFP)

        # Creates the "Update Model" button which updates the data files with the latest season data
        self.btnUPDATE = Button(self.Frame1)
        self.btnUPDATE.place(relx=0.63, rely=0.1, height=52, width=127)
        self.btnUPDATE.configure(activebackground="#d9d9d9")
        self.btnUPDATE.configure(activeforeground="#000000")
        self.btnUPDATE.configure(background="#d9d9d9")
        self.btnUPDATE.configure(foreground="#000000")
        self.btnUPDATE.configure(highlightbackground="#d9d9d9")
        self.btnUPDATE.configure(highlightcolor="black")
        self.btnUPDATE.configure(text='''Update Model''')
        self.btnUPDATE.configure(command=self.updateModel)

        # Create the Scrolled Listbox that specifies which NBA Players to make predictions for 
        self.Scrolledlistbox2 = ScrolledListBox(self.Frame1)
        self.Scrolledlistbox2.place(relx=0.4, rely=0.02, relheight=0.91, relwidth=0.2)
        self.Scrolledlistbox2.configure(background="white")
        self.Scrolledlistbox2.configure(font="TkFixedFont")
        self.Scrolledlistbox2.configure(foreground="black")
        self.Scrolledlistbox2.configure(highlightbackground="#d9d9d9")
        self.Scrolledlistbox2.configure(highlightcolor="#d9d9d9")
        self.Scrolledlistbox2.configure(selectbackground="#c4c4c4")
        self.Scrolledlistbox2.configure(selectforeground="black")
        self.Scrolledlistbox2.configure(width=10)

        Create the Scrolled Listbox that displays the predicted Fantasy Points for the specified players
        self.SL_Prediction = ScrolledListBox(self.Frame1)
        self.SL_Prediction.place(relx=0.78, rely=0.02, relheight=0.91
                , relwidth=0.2)
        self.SL_Prediction.configure(background="white")
        self.SL_Prediction.configure(font="TkFixedFont")
        self.SL_Prediction.configure(foreground="black")
        self.SL_Prediction.configure(highlightbackground="#d9d9d9")
        self.SL_Prediction.configure(highlightcolor="#d9d9d9")
        self.SL_Prediction.configure(selectbackground="#c4c4c4")
        self.SL_Prediction.configure(selectforeground="black")
        self.SL_Prediction.configure(width=10)

        self.Label1 = Label(self.Frame1)
        self.Label1.place(relx=0.63, rely=0.29, height=34, width=131)
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''How many days into''')
        self.Label1.configure(width=131)

        self.Label2 = Label(self.Frame1)
        self.Label2.place(relx=0.62, rely=0.35, height=34, width=141)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''the future to project:''')
        self.Label2.configure(width=141)

        self.titleLabel = ttk.Label(top)
        self.titleLabel.place(relx=0.39, rely=0.05, height=30, width=194)
        self.titleLabel.configure(background="#d9d9d9")
        self.titleLabel.configure(foreground="#000000")
        self.titleLabel.configure(relief=FLAT)
        self.titleLabel.configure(text='''NBA Fantasy Prediction Tool''')

        self.authorLabel = ttk.Label(top)
        self.authorLabel.place(relx=0.88, rely=0.96, height=20, width=113)
        self.authorLabel.configure(background="#d9d9d9")
        self.authorLabel.configure(foreground="#000000")
        self.authorLabel.configure(relief=FLAT)
        self.authorLabel.configure(text='''By Manu Colacot''')

        self.Spinbox1 = Spinbox(top, from_=1.0, to=20.0)
        self.Spinbox1.place(relx=0.64, rely=0.46, relheight=0.05, relwidth=0.08)
        self.Spinbox1.configure(activebackground="#f9f9f9")
        self.Spinbox1.configure(background="white")
        self.Spinbox1.configure(buttonbackground="#d9d9d9")
        self.Spinbox1.configure(foreground="black")
        self.Spinbox1.configure(from_="1.0")
        self.Spinbox1.configure(highlightbackground="black")
        self.Spinbox1.configure(highlightcolor="black")
        self.Spinbox1.configure(insertbackground="black")
        self.Spinbox1.configure(selectbackground="#c4c4c4")
        self.Spinbox1.configure(selectforeground="black")
        self.Spinbox1.configure(textvariable=GUI_Tool_support.spinbox)
        self.Spinbox1.configure(to="20.0")
        self.Spinbox1.configure(width=75)

        # Create Backend object, use it to get player list and populate listbox with those players
        self.backend = Backend.Backend()
        self.playerList = self.backend.getPlayerList()
        for player in self.playerList:
            self.Scrolledlistbox1.insert(END, player)

    def addEntry(self):
        # Add NBA Player's name to Scrolledlistbox2, indicating that Fantasy projections will  be made for him
        self.Scrolledlistbox2.insert(END, self.playerList[self.Scrolledlistbox1.curselection()[0]])
        print()
        
    def deleteEntry(self):
        # Delete NBA Player's name from Scrolledlistbox2, indicating that Fantasy projections will not be made for him
        selection = self.Scrolledlistbox2.curselection()
        self.Scrolledlistbox2.delete(selection[0])

    def updateModel(self):
        # Updates model with current season data
        curSeason = "2017-18"
        self.backend.updateModel(curSeason)

    def calculateFP(self):
        # Obtain selected player list, get intended projection days and obtain list of fantasy points for each player
        playerSelection = self.Scrolledlistbox2.get(0,END)
        fplist = self.backend.getTeamFP(playerSelection,int(self.Spinbox1.get()))

        # Clear list, iterate through each player, display their name and total fantasy points earned
        self.SL_Prediction.delete(0,END)
        i = 0
        for player in playerSelection:
            self.SL_Prediction.insert(END,player+":  "+str(fplist[i]))
            i = i + 1

    @staticmethod
    def popup7(event):
        Popupmenu7 = Menu(root, tearoff=0)
        Popupmenu7.configure(activebackground="#f9f9f9")
        Popupmenu7.configure(activeforeground="black")
        Popupmenu7.configure(background="#d9d9d9")
        Popupmenu7.configure(disabledforeground="#a3a3a3")
        Popupmenu7.configure(foreground="black")
        Popupmenu7.post(event.x_root, event.y_root)

# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        #self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = Pack.__dict__.keys() | Grid.__dict__.keys() \
                  | Place.__dict__.keys()
        else:
            methods = Pack.__dict__.keys() + Grid.__dict__.keys() \
                  + Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        return func(cls, container, **kw)
    return wrapped

class ScrolledListBox(AutoScroll, Listbox):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

if __name__ == '__main__':
    vp_start_gui()



