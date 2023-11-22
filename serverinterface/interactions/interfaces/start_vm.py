import requests
#import pyotp
import os
import requests
from requests.auth import HTTPBasicAuth
from getpass import getpass
import sys
import time
import socket
import subprocess
#from requests.auth


#TODO: use token instead of password
#TODO: ping computer to see if on/off

args = sys.argv[1:]
print(args)
startstop = args[0]
VMID = args[1]
passwd = " ".join(args).split(" password ")[1]


#first ssh into the server and run the following command to get the secret
#passwd = getpass("Enter password: ")
#os.system(f'wsl python3 interactions/interfaces/ssh.py 85.191.70.197 8007 root "qm {startstop} {VMID}" password {passwd}')
#response = subprocess.run(f'python3 interactions/interfaces/ssh.py 85.191.70.197 8007 root "qm {startstop} {VMID}" password {passwd}')
os.system(f'python3 interactions/interfaces/ssh.py 85.191.70.197 8007 root "qm {startstop} {VMID}" password {passwd}')
#print(response)
#print(response.stdout)

time.sleep(5)