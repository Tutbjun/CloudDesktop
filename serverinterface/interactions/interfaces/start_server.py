import requests
#import pyotp
import os
import requests
from requests.auth import HTTPBasicAuth
from getpass import getpass
import sys
import time
import socket
#from requests.auth


#TODO: use token instead of password
#TODO: ping computer to see if on/off

args = sys.argv[1:]
print(args)
state = args[0]#example: 1_on
onoff = state.split("_")[1]
port = state.split("_")[0]
doruntel = args[1]#example: 1
passwd = " ".join(args).split(" password ")[1]

#first ssh into the server and run the following command to get the secret
#passwd = getpass("Enter password: ")
if onoff == "on":
    os.system(f'python3 interactions/interfaces/ssh.py 85.191.70.197 8011 root "python /home/kvmd-webterm/telnetCom/telnetChangeSetting.py {state}" password {passwd}')
    if doruntel == "1":
        os.system(f'python3 interactions/interfaces/ssh.py 85.191.70.197 8011 root "/home/kvmd-webterm/telnetCom/runner.sh" password {passwd}')


user = "admin"

secret = ""  # Can be found in /etc/kvmd/totp.secret
ip = "85.191.70.197:8009"

header = {'user': user, 'passwd': passwd}
requests.Session().debug = True
response = requests.post(f"https://{ip}/api/auth/login", data=header, verify=False)
print(response.text)
for key, value in response.headers.items():
    print(f"{key}: {value}")

token = response.headers['Set-Cookie'].split(";")[0].split("=")[1]
header = {
    "Authorization": f"access_token {token}",
}

response = requests.get(f"https://{ip}/api/auth/check", verify=False, auth=HTTPBasicAuth(user, passwd))
print(response.text)
for key, value in response.headers.items():
    print(f"{key}: {value}")

"""response = requests.get(f"https://{ip}/api/auth/check", headers=header, verify=False)
print(response.text)
for key, value in response.headers.items():
    print(f"{key}: {value}")"""


response = requests.get(f"https://{ip}/api/atx", verify=False, auth=HTTPBasicAuth(user, passwd))
print(response.text)
for key, value in response.headers.items():
    print(f"{key}: {value}")


#POST https://<pikvm-ip>/api/atx/power?action=on
if onoff == "off":
    response = requests.post(f"https://{ip}/api/atx/power?action={onoff}", verify=False, auth=HTTPBasicAuth(user, passwd))
else:
    response = requests.post(f"https://{ip}/api/atx/click?button=power", verify=False, auth=HTTPBasicAuth(user, passwd))
print(response.text)
for key, value in response.headers.items():
    print(f"{key}: {value}")
time.sleep(1)

#wait for power to be off

switch = False
while not switch:
    response = os.system("curl -k https://85.191.70.197:8006 --connect-timeout 1")
    print(response)
    if response == 0:
        on = True
    else:
        on = False
    if onoff == "on" and on:
        switch = True
    elif onoff == "off" and not on:
        switch = True
    time.sleep(1)

switch = False
while not switch:
    if onoff == "on":
        break
    response = requests.get(f"https://{ip}/api/atx", verify=False, auth=HTTPBasicAuth(user, passwd))
    print(response.text)
    response = requests.get(f"https://{ip}/api/hid", verify=False, auth=HTTPBasicAuth(user, passwd))
    print(response.text)
    for key, value in response.headers.items():
        print(f"{key}: {value}")
    #look for first "online" tag and check if it is true
    for line in response.text.split("\n"):
        if "online" in line:
            print(line)
            if "false" in line and onoff == "off":
                switch = True
            else:
                switch = False
            break

    print(f"waiting for power to be {onoff}...")
    time.sleep(1)


    
if onoff == "off":
    time.sleep(12)

if onoff == "off":
    os.system(f'python3 interactions/interfaces/ssh.py 85.191.70.197 8011 root "python /home/kvmd-webterm/telnetCom/telnetChangeSetting.py {state}" password {passwd}')
    if doruntel == "1":
        os.system(f'python3 interactions/interfaces/ssh.py 85.191.70.197 8011 root "/home/kvmd-webterm/telnetCom/runner.sh" password {passwd}')

time.sleep(3)
print("done")
exit()