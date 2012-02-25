#! /usr/bin/env python

import sys
import os
from mainWindow import MainWindow
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

class HomeScreen():

  def __init__(self):
    gladefile = "dakia.glade"
    self.xml =  gtk.glade.XML(gladefile, "homeScreen")
    dic = { "destroy" : gtk.main_quit}

    self.xml.signal_autoconnect(dic)
    
    self.homescreen = self.xml.get_widget("homeScreen")
    
