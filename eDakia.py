#! /usr/bin/env python

import sys
import re
from pprint import pprint 
import urllib2
import pycurl
import cStringIO
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

USER_LOGIN_URL = "edakia.in/api/users.json"

class Edakia (object):

  def __init__(self,):
    self.gladefile = "edakia.glade"
    self.wTree =  gtk.glade.XML(self.gladefile)
    self.mobile = ""
    self.password = ""
    dic = { "on_pydakia_destroy" : gtk.main_quit,
            "on_enter_clicked" : self.mobile_entered,
            "on_oncancel_clicked" : gtk.main_quit,
            "on_pypassword_destroy" : gtk.main_quit,
            "on_login_clicked" : self.password_entered,
            "on_password_cancel_clicked" : gtk.main_quit,
            "destroy" : gtk.main_quit
          }

    self.wTree.signal_autoconnect(dic)

  def mobile_entered(self, widget, data= None):
    self.mobile = self.wTree.get_widget("field_sender_mobile").get_text()
    print self.mobile
    status, message = self.validate_mobile_number()
    if status:
      self.wTree.get_widget("error").hide()
      print message
      self.wTree.get_widget("pydakia").hide()
      self.display_password_window()
    else:
      self.wTree.get_widget("error").show()
      print message
  
  def validate_mobile_number(self):
    p = re.compile('(^((0)?|(\+?91)?)[789][0-9]{9}$)')
    if p.match(self.mobile)!= None :
      return True, "Given Mobile Number is Valid"
    else:
      return False, "Given Mobile Number is  not Valid"
  
  def display_password_window(self):
    self.wTree =  gtk.glade.XML(self.gladefile, "pypassword")
    self.wTree.get_widget("pypassword").show();
  
  def password_entered(self, widget, data=None):
    self.password = self.wTree.get_widget("field_sender_password").get_text()
    print self.password
    status, message = self.validate_password()
    if status:
      self.wTree.get_widget("password_error").hide()
      print message
      self.display_loading_window()
      self.authenticate_user()
    else:
      self.wTree.get_widget("password_error").show()
      print message
  
  def validate_password(self):
    p = re.compile('(^[0-9]{4,12}$)')
    if p.match(self.password)!= None :
      return True, "Given Password is Valid"
    else:
      return False, "Given Password is  not Valid"
  
  def display_loading_window(self):
    self.wTree.get_widget("pypassword").hide();
    self.wTree =  gtk.glade.XML(self.gladefile, "processWindow")
    self.wTree.get_widget("processWindow").show();
  
  def authenticate_user(self):
    self.wTree.get_widget("processWindow").show()
    buf = cStringIO.StringIO()
    p = pycurl.Curl()
    p.setopt(p.WRITEFUNCTION, buf.write)
    p.setopt(pycurl.URL, "http://"+ self.mobile + ":" + self.password +"@" + USER_LOGIN_URL)
    p.perform()
    result = eval(buf.getvalue())
    buf.close()
    p.close()
    if result.has_key('user'):
      print "Successful login"
      return True
    elif result.has_key('error'):
      print "Login Failed"
      #self.hide_process_window(result['error'])
    else:
      print "reading error"  


  
if __name__ == "__main__":
    dakia = Edakia()
    gtk.main()
