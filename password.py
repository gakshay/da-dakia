#! /usr/bin/env python

import sys
import re
import urllib2
import pycurl
import cStringIO
import os
from scanPage import ScanPage
from processWindow import ProcessWindow
import threading
import time
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
#import gobject
#gobject.threads_init()

from receiverMobile import ReceiverMobile

class Password:

  def __init__(self, mobile):
    self.gladefile = "ui/edakia.glade"
    self.wTree =  gtk.glade.XML(self.gladefile,"pypassword")
    self.mobile = mobile
    self.password = ""
    dic = { "on_pypassword_destroy" : gtk.main_quit,
            "on_login_clicked" : self.password_entered,
            "on_field_sender_password_key_press_event" : self.pypassword_password_key_press_event,
            "on_password_cancel_clicked" : gtk.main_quit,
            "destroy" : gtk.main_quit
          }

    self.wTree.signal_autoconnect(dic)
    self.wTree.get_widget("pypassword").show()
    self.loading = ProcessWindow()

  def password_entered(self, widget, data=None):
    self.password = self.wTree.get_widget("field_sender_password").get_text()
    print self.password
    status, message = self.validate_password()
    if status:
      #ps = Processing(self)
      #ps.start()
      self.display_process_window()
      login_response, login_message = self.authenticate_user()
      #ps.quit = True
      if login_response:
        self.wTree.get_widget("pypassword").hide()
        self.loading.hide()
        ReceiverMobile(self.mobile, self.password)
      else:
        self.hide_process_window(login_message)
     
    else:
      self.password = ""
      self.wTree.get_widget("field_sender_password").set_text("")
      self.wTree.get_widget("pypasswordError").show()
  
  def validate_password(self):
    p = re.compile('(^[0-9]{4,12}$)')
    if p.match(self.password)!= None :
      return True, "Given Password is Valid"
    else:
      return False, "Given Password is not Valid"
  
  def display_process_window(self):
    self.wTree.get_widget("pypasswordError").hide()
    self.wTree.get_widget("pypassword").hide()
    self.loading.show()
      
  def hide_process_window(self, message):
    self.wTree.get_widget("field_sender_password").set_text("")
    status = self.wTree.get_widget("password_status")
    status.set_text(message)
    self.wTree.get_widget("pypasswordError").show()
    self.loading.hide()
    self.wTree.get_widget("pypassword").show()

  def authenticate_user(self):
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

  def pypassword_password_key_press_event(self, widget, event):
    keyname = gtk.gdk.keyval_name(event.keyval)
    #print "Key %s (%d) was pressed" % (keyname, event.keyval)
    if keyname == "Return":
      print "Return is pressed"
      self.password_entered(widget)  
      
      
class Processing(threading.Thread):
	"""This class sets the fraction of the progressbar"""
	
	def __init__(self, obj):
		super(Processing, self).__init__()
		self.ppd = obj
		self.quit = False
		print self.ppd
	
	def run(self):
		"""Run method, this is the code that runs while thread is alive."""
		#While the stopthread event isn't setted, the thread keeps going on
		while not self.quit :
			gobject.idle_add(self.show_loading_window)
			time.sleep(0.1)
			
	def show_loading_window(self):
		self.ppd.display_process_window()
		return False
