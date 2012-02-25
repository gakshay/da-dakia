#! /usr/bin/env python

import sys
import os
from successWindow import SuccessWindow
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

class ScanPage (object):
  def __init__(self, mobile, password):
    self.mobile = mobile
    self.password = password
    self.gladefile = "ui/scan_window.glade"
    self.wTree =  gtk.glade.XML(self.gladefile)
    dic = { "on_scanWindow_destroy" : gtk.main_quit,
            "on_send_enter_clicked" : self.scan_page,
          }
    self.wTree.signal_autoconnect(dic)

  def scan_page(self, widget, data=None):
    #scan_result = os.system("scanimage --format=tiff > images/image.tiff")
    print "Scanning done"
    self.wTree.get_widget("scanWindow").hide()
    SuccessWindow()

