#!/usr/bin/env python2.6

"""
Daemon that will periodically check the ip address of the server it's running on
and will update 1and1 DNS records when it changes.
"""
#-------------------------------------------------------------------------------

import os
import sys
import getopt
import logging
import yaml

#-------------------------------------------------------------------------------

from datetime import datetime
import urllib3

#-------------------------------------------------------------------------------

__version__   = "1.0.0"
__id__        = "@(#)  ipcheck  [%s]  2011/1/25"

verbose_flg   = False

debug_level   = 0

URL           = "http://www.whatismyip.com/automation/n09230945.asp"
URL1and1      = "https://admin.1and1.com/xml/config/Login"
LOGFILE       = "ipcheck.log"
PIDFILE       = "ipcheck.pid"
CONFIG        = "ipcheck.yaml"
data_dir      = None
tables        = []

log           = None
pid           = None
ipConfig      = None

#===============================================================================

def INFO(msg):
   if log: log.info(' ' + msg)
   if verbose_flg: print "[ipcheck]  %s" % msg

#-------------------------------------------------------------------------------

def ERROR(msg):
   if log: log.error(msg)
   sys.stderr.write('[ipcheck]  %s\n' % msg)

#-------------------------------------------------------------------------------

def WARNING(msg):
   if log: log.warning('*****' + msg + '*****')
   if verbose_flg: print "[ipcheck]  %s" % msg

#===============================================================================

def init():
   global log
   global pid
   global ipConfig

   pid = os.getpid()

   log  = logging.getLogger('ipcheck')
   hdlr = logging.FileHandler(LOGFILE)
   fmtr = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

   hdlr.setFormatter(fmtr)
   log.addHandler(hdlr)
   log.setLevel(logging.INFO)

   INFO("Started processing")

   if (not verbose_flg):
      INFO("PID is %d" % pid)
   try:
      f = open(data_dir + CONFIG)
      ipConfig= yaml.load(f)
      f.close()
   except IOError:
      ERROR("Config File failed to open: " + data_dir + CONFIG)
      return 1

#-------------------------------------------------------------------------------
def ipCheck():
   if ipConfig["ip"] is None:
      #initialize the ipcheck.yaml file
      pass
   http_pool = urllib3.connection_from_url(URL)
   try:
      response = urllib3.urlopen(req)
   except URLError, e:
      if hasattr(e, 'reason'):
         print 'We failed to reach a server.'
         print 'Reason: ', e.reason
      elif hasattr(e, 'code'):
         print 'The server couldn\'t fulfill the request.'
         print 'Error code: ', e.code
   else:
      data = response.read()
      if ipConfig["ip"] != data:
         #write back
         ipConfig["ip"] = data
         try:
            f = open(data_dir + CONFIG, "w")
            yaml.dump(ipConfig, f)
            f.close()
         except IOError:
            ERROR("Config File failed to open: " + data_dir + CONFIG)
            return 1
         ipUpdate(data)
#-------------------------------------------------------------------------------
def ipUpdate(data):
   print "TODO: Update DNS"
   pass
#===============================================================================

def main():
   global verbose_flg
   global debug_level
   global data_dir
   try:
      opts, args = getopt.getopt(sys.argv[1:], "dD:vVw?")
   except getopt.error, msg:
      print __doc__
      return 1

   try:
      terminal_type = os.environ["TERM"]
   except KeyError, e:
      print "[ipcheck]  Set TERM environment variable and rerun!"
      return 1

   wrk_path  = os.getcwd()
   wrk_dir   = os.path.basename(wrk_path)

   data_dir = wrk_path + '/DATA/'
   pid_path = data_dir + PIDFILE

   # os.chdir(data_dir)

   for o, a in opts:
      if o == '-d':
         debug_level   += 1
      elif o == '-D':
         debug_level    = int(a)
      elif o == '-v':
         verbose_flg    = True
      elif o == '-V':
         print "[ipcheck]  Version: %s" % __version__
         return 1
      elif o == '-?':
         print __doc__
         return 1

   print "[ipcheck]  Working directory is %s" % os.getcwd()

   if (debug_level > 0): print "[ipcheck]  Debugging level set to %d" % debug_level

   if args:
      for arg in args:
         print arg

   init()
   ipCheck()
   return 0

#-------------------------------------------------------------------------------

if __name__ == '__main__' or __name__ == sys.argv[0]:
   try:
      sys.exit(main())
   except KeyboardInterrupt, e:
      print "[ipcheck]  Interrupted!"

#-------------------------------------------------------------------------------

"""
Revision History:

     Date     Who   Description
   --------   ---   ------------------------------------------------------------
   20110125   RDK   Initial implementation

Problems to fix:

To Do:

Issues:

"""
