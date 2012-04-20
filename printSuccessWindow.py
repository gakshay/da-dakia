#! /usr/bin/env python

import sys
import os

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

class PrintSuccessWindow():

  def __init__(self):
    gladefile = "ui/print_success.glade"
    self.xml =  gtk.glade.XML(gladefile, "printSuccessWindow")
    dic = { "destroy" : gtk.main_quit,
            "on_button1_clicked" : gtk.main_quit,
            "on_button1_enter" : gtk.main_quit,
            "on_successWindow_destroy" : gtk.main_quit}

    self.xml.signal_autoconnect(dic)

