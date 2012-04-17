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

class SuccessWindow():

  def __init__(self):
    gladefile = "ui/final_success.glade"
    self.xml =  gtk.glade.XML(gladefile, "successWindow")
    dic = { "destroy" : gtk.main_quit,
            "on_successWindow_destroy" : gtk.main_quit}

    self.xml.signal_autoconnect(dic)

