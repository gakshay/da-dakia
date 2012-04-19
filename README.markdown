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
3. If hindi is not supported by your system
     add ui/fonts/raghu.ttf to your fonts directory e.g `cp ui/fonts/raghu.ttf ~/.fonts/`
4. To set locale as hi_IN set `LOCALE=hi_IN; LC_ALL=hi_IN export; $LOCALE $LC_ALL`

RUN
===
1. cd $EDAKIA_PATH
2. python dakia.py

ToDO
====
1. SMS integration at server side (http://www.edakia.in) 


How to Start ATOM
=================
1. Short the corresponding PINS marked red on the ATOM Board
2. Make sure to insert our EDAKIA bootable SlitAZ pen drive
3. At boot prompt 
   **press enter**
    or
    **slitaz vga=791** if using a monitor and having problems in display
4. Once booted follow the steps on how to run an application