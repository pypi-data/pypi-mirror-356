# ports_unix.py  06/18/2025  Pasco Tang
#
# Get a list of ports on a unix system
# Note that the precise /dev/* filter depends on the platform

# SYSTEM AND VERSION VARIANCE ==========================================

#this is for linux
DEV_TTY    = "/dev/tty*"

#TODO for mac, it's /dev/cua*???
  
  
# BODY =================================================================

import glob

def scan():
  """ scan devices that might be com ports """
  devices = glob.glob(DEV_TTY)
  #print("found " + str(len(devices)) + " devices")
  return devices


# TEST HARNESS =========================================================
 
if __name__ == "__main__":
  d = scan()
  print(str(d)) 
    
# END
