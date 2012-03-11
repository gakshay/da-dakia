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

class ProcessWindow:

  def __init__(self):
    gladefile = "ui/edakia.glade"
    self.xml =  gtk.glade.XML(gladefile, "processWindow")
    dic = { "destroy" : gtk.main_quit,
            "on_processWindow_destroy" : gtk.main_quit}

    self.xml.signal_autoconnect(dic)
    
  def show(self):
    print "process window show called"
    self.xml.get_widget("processWindow").show_all()
    
  def hide(self):
    self.xml.get_widget("processWindow").hide_all()
