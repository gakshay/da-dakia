#! /usr/bin/env python

import sys
import re
import os
from password import Password

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

class Mobile (object):
  def __init__(self):
    self.gladefile = "ui/edakia.glade"
    self.wTree =  gtk.glade.XML(self.gladefile,"pydakia")
    self.mobile = ""
    self.password = ""
    dic = { "on_pydakia_destroy" : gtk.main_quit,
            "on_enter_clicked" : self.mobile_entered,
            "on_oncancel_clicked" : gtk.main_quit,
            "destroy" : gtk.main_quit
          }

    self.wTree.signal_autoconnect(dic)
    self.wTree.get_widget("pydakia").show()

  def mobile_entered(self, widget, data= None):
    self.mobile = self.wTree.get_widget("field_sender_mobile").get_text()
    print self.mobile
    status, message = self.validate_mobile_number()
    if status:
      self.wTree.get_widget("pydakiaError").hide()
      print message
      self.wTree.get_widget("pydakia").hide()
      Password(self.mobile)
    else:
      self.wTree.get_widget("pydakiaError").show()
      print message
  
  def validate_mobile_number(self):
    p = re.compile('(^((0)?|(\+?91)?)[789][0-9]{9}$)')
    if p.match(self.mobile)!= None :
      return True, "Given Mobile Number is Valid"
    else:
      return False, "Given Mobile Number is  not Valid"
      
