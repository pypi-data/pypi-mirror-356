import serial
import DoerGPIO.portscan as portscan

DEBUG = True
# STATIC REDIRECTORS ===================================================

# Find out if there is a pre-cached port name.
# If not, try and find a port by using the portscanner
#
#name = portscan.getName()
#if name != None:
#  if DEBUG:
#    print("Using port:" + name)
#  PORT = name
#else:
#  name = portscan.find()
#  if name == None:
#    raise ValueError("No port selected, giving in")
#  PORT = name
#  print("Your anyio board has been detected")
#  print("Now running your program...")

doerGPIOPort = ""
import serial.tools.list_ports
serialPorts = serial.tools.list_ports.comports()

for port in serialPorts:
    if( "1a86:7523" in port[2].lower() or "1a86:7523" in port[2].lower()):
        if(DEBUG):
            print ("Doer GPIO board Found on port: "+port[0])
        doerGPIOPort = port[0]
        break
if(doerGPIOPort == ""):
	print ("\nError: Doer GPIO board is not detected.\nFor more support please visit our website at https://doer.ee\nPress enter to close.")
	input()
	exit()

#print ("Debug cable fully detected fine.\n Press enter to launch the terminal.")


BAUD = 230400


s = serial.Serial(doerGPIOPort)
s.baudrate = BAUD
s.parity   = serial.PARITY_NONE
s.databits = serial.EIGHTBITS
s.stopbits = serial.STOPBITS_ONE
#s.write_timeout = 
timeout = None

s.close()
s.port = doerGPIOPort
s.open()

# Send version command and read response with timeout
s.timeout = 2  # Set timeout to 2 seconds
while True:
    try:
        s.write(b'VVZ')
        response = s.readline().decode('utf-8').strip()
        if response:
            # Check if response matches DoerGPIO_HWX.Y_SWZ.W format
            if response.startswith('DoerGPIO_HW'):
                try:
                    # Split into hardware and software parts
                    hw_part, sw_part = response.split('_SW')
                    hw_version = hw_part[11:]  # Remove 'DoerGPIO_HW' prefix
                    sw_version = sw_part
                    
                    # Verify both versions are in X.Y format
                    hw_major, hw_minor = hw_version.split('.')
                    sw_major, sw_minor = sw_version.split('.')
                    
                    if (hw_major.isdigit() and hw_minor.isdigit() and 
                        sw_major.isdigit() and sw_minor.isdigit()):
                        print(f"Hardware Version: {hw_version}")
                        print(f"Software Version: {sw_version}")
                        break
                    else:
                        print("Wrong Board Version, contact customer support at cs@doer.ee")
                        s.close()
                        exit()
                except ValueError:
                    print("Wrong Board Version, contact customer support at cs@doer.ee")
                    s.close()
                    exit()
            else:
                print("Wrong Board Version, contact customer support at cs@doer.ee")
                s.close()
                exit()
        else:
            print("Connection failed. Retrying...")
        retry = input("Press Enter to retry or 'q' to quit: ")
        if retry.lower() == 'q':
            print("Exiting...")
            s.close()
            exit()
    except serial.SerialTimeoutException:
        print("Connection failed. Retrying...")
        retry = input("Press Enter to retry or 'q' to quit: ")
        if retry.lower() == 'q':
            print("Exiting...")
            s.close()
            exit()
