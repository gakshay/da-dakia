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

class ReceiveSuccessWindow:

  def __init__(self):
    gladefile = "ui/final_success.glade"
    self.xml =  gtk.glade.XML(gladefile, "receiveSuccessWindow")
    dic = { "destroy" : gtk.main_quit,
            "on_printButton_clicked" : self.print_button_clicked
            "on_receiveSuccessWindow_destroy" : gtk.main_quit}

    self.xml.signal_autoconnect(dic)
    
  def print_button_clicked(self):
    print "print button clicked"
    # print command to take print out from connected printer
