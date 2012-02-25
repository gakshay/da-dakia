#! /usr/bin/env python

import sys
import os
from mainWindow import MainWindow

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

class Dakia():

  def __init__(self,):
    mainwindow = MainWindow()
    mainwindow.mainwindow.show()

if __name__ == "__main__":
    dakia = Dakia()
    gtk.main()
