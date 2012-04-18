eDakia Client Side Application
==============================

Components
==========
1. Cross-platform Desktop application 
2. Scripts that run on client eDakia Machine

Requirements
============
1. Python, Gtk, pygtk (2.24), pycurl, pypil, urllib for native cross-platform Desktop application
2. cron, cups, hplip, sane, curl and their corresponding dependencies 
3. It is assumned that all the mentioned libraries mentioned in 2 are working fine

Install
=======
0. Change the project edakia path on top in this file `./scripts/client/crontab`
1. Add these two lines to your bashrc/.profile/.bash_profile
   `export EDAKIA_PATH=/home/tux/project/dakia`
   `sh $EDAKIA_PATH/scripts/client/local.sh`
    EDAKIA_PATH is the path where you downloaded this project and should change according to your path
    local.sh sets the default cron, make printer/scanner permissible

RUN
===
1. cd $EDAKIA_PATH
2. python dakia.py

ToDO
====
1. SMS integration at server side (http://www.edakia.in) 
