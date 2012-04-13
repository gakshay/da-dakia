#! /usr/bin/env python

import sys
import os
import time
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

INBOXPATH = "./files/send/inbox"

class ScanPage:
  def __init__(self, mobile, password, receiver):
    self.mobile = mobile
    self.password = password
    self.receiver = receiver
    self.gladefile = "ui/scan_window.glade"
    self.wTree =  gtk.glade.XML(self.gladefile)
    dic = { "on_scanWindow_destroy" : gtk.main_quit,
            "on_send_enter_clicked" : self.scan_page,
          }
    self.wTree.signal_autoconnect(dic)

  def scan_page(self, widget, data=None):
    print "creating files"
    folder_name = "%(timestamp)s_%(mobile)s" % { 'timestamp' : int(time.time()), 'mobile' : self.mobile } 
    file_name =  "%(path)s/%(folder_name)s/%(folder_name)s.txt" % { 'path' : INBOXPATH,  'folder_name' : folder_name }
    os.system("mkdir -p %(path)s/%(folder_name)s" % {'path' : INBOXPATH, 'folder_name' : folder_name})
    fin = open(file_name, "w")
    print >>fin, self.mobile 
    print >>fin, self.password
    print >>fin, self.receiver
    file.close

    print "Scanning done"    
    scan_result = os.system("scanimage --format=tiff > %(path)s/%(image)s.tiff" % {'path' : INBOXPATH, 'image' : folder_name})

    self.wTree.get_widget("scanWindow").hide()
    SuccessWindow()

