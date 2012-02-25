#! /usr/bin/env python

import sys
import re
import urllib2
import pycurl
import cStringIO
import os
from scanPage import ScanPage

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

USER_LOGIN_URL = "edakia.in/api/users.json"
PROTOCOL = "http://"

class Password (object):

  def __init__(self, mobile):
    self.gladefile = "ui/edakia.glade"
    self.wTree =  gtk.glade.XML(self.gladefile,"pypassword")
    self.mobile = mobile
    self.password = ""
    dic = { "on_pypassword_destroy" : gtk.main_quit,
            "on_login_clicked" : self.password_entered,
            "on_password_cancel_clicked" : gtk.main_quit,
            "destroy" : gtk.main_quit
          }

    self.wTree.signal_autoconnect(dic)
    self.wTree.get_widget("pypassword").show()

  def password_entered(self, widget, data=None):
    self.password = self.wTree.get_widget("field_sender_password").get_text()
    print self.password
    status, message = self.validate_password()
    if status:
      self.display_process_window()
      self.wTree.get_widget("pypasswordError").hide()
      login_response, login_message = self.authenticate_user()
      if login_response:
        self.wTree.get_widget("pypassword").hide()
        #self.wTree.get_widget("processWindow").hide()
        ScanPage(self.mobile, self.password)
      else:
        self.hide_process_window(login_message)
     
    else:
      self.wTree.get_widget("field_sender_password").set_text("")
      self.wTree.get_widget("pypasswordError").show()
  
  def validate_password(self):
    p = re.compile('(^[0-9]{4,12}$)')
    if p.match(self.password)!= None :
      return True, "Given Password is Valid"
    else:
      return False, "Given Password is  not Valid"
  
  def display_process_window(self):
    self.wTree.get_widget("pypasswordError").hide()
    self.wTree.get_widget("password_status").hide()
    #self.wTree.get_widget("processWindow").show()
    #self.wTree.get_widget("pypassword").hide()
  
  def hide_process_window(self, message):
    self.wTree.get_widget("pypasswordError").show()
    status = self.wTree.get_widget("password_status")
    status.set_text(message)
    self.wTree.get_widget("password_status").show()
    #self.wTree.get_widget("processWindow").hide()
    self.wTree.get_widget("pypassword").show()
    self.wTree.get_widget("field_sender_password").set_text("")
   
  def authenticate_user(self):
    #self.wTree.get_widget("processWindow").show()
    buf = cStringIO.StringIO()
    p = pycurl.Curl()
    p.setopt(p.WRITEFUNCTION, buf.write)
    p.setopt(pycurl.URL, PROTOCOL + self.mobile + ":" + self.password +"@" + USER_LOGIN_URL)
    p.perform()
    result = eval(buf.getvalue())
    buf.close()
    p.close()
    if result.has_key('user'):
      print "Successful login"
      return True, "Login Successful"
    elif result.has_key('error'):
      print "Login Failed"
      return False, result['error']
    else:
      print "reading error" 
      return False, "Network not reachable"

