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
from printSuccessWindow import PrintSuccessWindow

class ReceiveSuccessWindow:

  def __init__(self, filename):
    gladefile = "ui/receive_success.glade"
    self.filename = filename
    print self.filename
    self.xml =  gtk.glade.XML(gladefile, "receiveSuccessWindow")
    dic = { "destroy" : gtk.main_quit,
            "on_printButton_clicked" : self.print_button_clicked,
            "on_receiveSuccessWindow_destroy" : gtk.main_quit}

    self.xml.signal_autoconnect(dic)
    
  def print_button_clicked(self, widget, data = None):
    print "print button clicked"
    os.system("convert %(filename)s test.pdf" % {'filename': self.filename})
    os.system("lp %(filename)s" % {'filename' : "test.pdf"})
    # print command to take print out from connected printer
    PrintSuccessWindow()
