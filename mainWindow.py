#! /usr/bin/env python

import sys
import os
from eDakia import Edakia
from mobile import Mobile
try:
  import pygtk
  pygtk.require("2.24")
except:
  pass

try:
  import gtk
  import gtk.glade
except:
  sys.exit(1)

class MainWindow():

  def __init__(self):
    gladefile = "ui/dakia.glade"
    self.xml =  gtk.glade.XML(gladefile, "mainWindow")
    dic = { "destroy" : gtk.main_quit,
            "on_mainWindow_key_press_event" : self.main_window_key_press,
            "on_mainWindow_destroy" : gtk.main_quit}

    self.xml.signal_autoconnect(dic)
    self.mainwindow = self.xml.get_widget("mainWindow")
    
  def main_window_key_press(self, widget, event):
    keyname = gtk.gdk.keyval_name(event.keyval)
    #print "Key %s (%d) was pressed" % (keyname, event.keyval)
    if keyname == "1":
      print "1 is pressed"
      self.mainwindow.hide()
      Mobile()
    elif keyname == "2":
      print "2 is pressed"
    

