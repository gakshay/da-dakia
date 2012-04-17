#! /usr/bin/env python

import sys
import re
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

from scanPage import ScanPage
from processWindow import ProcessWindow

class ReceiverMobile:
  def __init__(self, mobile, password):
    self.gladefile = "ui/send_receiver_mobile.glade"
    self.wTree =  gtk.glade.XML(self.gladefile,"receiverMobileWindow")
    self.mobile = mobile
    self.password = password
    self.receiver = ""
    dic = { "on_receiverMobileWindow_destroy" : gtk.main_quit,
            "on_enter_clicked" : self.mobile_entered,
            "on_field_receiver_mobile_key_press_event" : self.pydakia_receiver_mobile_key_press_event,
            "on_oncancel_clicked" : gtk.main_quit,
            "destroy" : gtk.main_quit
          }

    self.wTree.signal_autoconnect(dic)
    self.wTree.get_widget("receiverMobileWindow").show()

  def mobile_entered(self, widget, data= None):
    self.receiver = self.wTree.get_widget("field_receiver_mobile").get_text()
    print self.receiver
    status, message = self.validate_mobile_number()
    if status:
      self.mobile_entered_success(message)
    else:
      self.mobile_entered_failure(message)
  
  def validate_mobile_number(self):
    p = re.compile('(^((0)?|(\+?91)?)[789][0-9]{9}$)')
    if p.match(self.receiver)!= None :
      return True, "Given Mobile Number is Valid"
    else:
      self.receiver = ""
      return False, "Given Mobile Number is  not Valid"
  
  def mobile_entered_success(self, message="Mobile entered is correct"):
    self.wTree.get_widget("pydakiaError").hide()
    print message
    self.wTree.get_widget("receiverMobileWindow").hide()
    ScanPage(self.mobile, self.password, self.receiver)
      
  def mobile_entered_failure(self, message = "Mobile entered is incorrect"):
    self.wTree.get_widget("pydakiaError").show()
    print message
      
  def pydakia_receiver_mobile_key_press_event(self, widget, event):
    keyname = gtk.gdk.keyval_name(event.keyval)
    #print "Key %s (%d) was pressed" % (keyname, event.keyval)
    if keyname == "Return":
      print "Return is pressed"
      self.mobile_entered(widget)  
