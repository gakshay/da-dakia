#! /usr/bin/env python

import sys
import os
import re
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

from successWindow import SuccessWindow
import urllib
from xml.dom.minidom import parseString

DOCUMENT_RECEIVE_URL = "edakia.in/transactions/receive.xml"
PROTOCOL = "http://"

class SecretCode:

  def __init__(self, mobile):
    gladefile = "ui/secret_code.glade"
    self.mobile = mobile
    self.wTree =  gtk.glade.XML(gladefile, "secret_window")
    dic = { "destroy" : gtk.main_quit,
            "on_secret_enter_button_clicked" : self.secret_code_entered,
            "on_secret_cancel_button_clicked" : gtk.main_quit,
            "on_field_secret_code_key_press_event" : self.secret_code_key_press_event,
            "on_secret_window_destroy" : gtk.main_quit}

    self.wTree.signal_autoconnect(dic)
    
  def secret_code_entered(self, widget, data = None):
    self.secret_code = self.wTree.get_widget("field_secret_code").get_text()
    print self.secret_code
    status, message = self.validate_secret_code()
    if status:
      self.secret_code_entered_success(message)
    else:
      self.secret_code_entered_failure(message)
      
  def validate_secret_code(self):
    p = re.compile('(^[a-zA-Z0-9]{6}$)')
    if p.match(self.secret_code)!= None :
      return True, "Given Secret Code is Valid"
    else:
      return False, "Given Secret Code is  not Valid"
      
  def secret_code_key_press_event(self, widget, event):
    keyname = gtk.gdk.keyval_name(event.keyval)
    #print "Key %s (%d) was pressed" % (keyname, event.keyval)
    if keyname == "Return":
      print "Return is pressed"
      self.secret_code_entered(widget)
      
  def secret_code_entered_success(self, message):
    print message
    status, result = self.document_request()
    if status:
      self.fetch_document(result)
    else:
      self.secret_code_entered_failure("result")
    #self.wTree.get_widget("secret_window").hide()
    #ReceiveSuccessWindow()
    
    
  def secret_code_entered_failure(self, message):
    print message
    self.wTree.get_widget("secret_error_hbox").show()
  
  def document_request(self):
    parameters = urllib.urlencode({"transaction[receiver_mobile]": self.mobile, "transaction[document_secret]" : self.secret_code})
    f = urllib.urlopen(PROTOCOL + DOCUMENT_RECEIVE_URL+"?"+parameters)
    data = f.read()
    print data
    f.close()

    #parse the xml you downloaded
    dom = parseString(data)
    #retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
    try:
      xmlTag = dom.getElementsByTagName('document_url')[0].toxml()
      print xmlTag
      url=xmlTag.replace('<document_url>','').replace('</document_url>','')
      print url
      return True, url
    except:
      xmlTag = dom.getElementsByTagName('error')[0].toxml()
      print xmlTag
      error_msg=xmlTag.replace('<error>','').replace('</error>','')
      print error_msg
      return False, error_msg
      
  def fetch_document(self, url):
    pass
    
