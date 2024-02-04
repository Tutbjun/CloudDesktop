import time
#import rsa
import hashlib
import sys
from getpass import getpass
import os

def get():
    passwd = getpass("Enter password: ")

    hash_object = hashlib.sha256()
    hash_object.update(passwd.encode())
    encPasswd = hash_object.hexdigest().encode()
    with open("passwrdref.txt", "rb") as f:
        refPasswds = f.readlines()
    refPasswds = [passwd.replace(b"\n", b"") for passwd in refPasswds]

    if encPasswd not in refPasswds:
        print("Wrong password")
        time.sleep(5)
        raise Exception("Wrong password")
    return passwd

import requests
def get_token(passwd):
    
        #api to pikvm to get token
    user = "admin"
    ip = "85.191.70.197:8009"
    header = {'user': user, 'passwd': passwd}
    
    requests.Session().debug = True

    response = requests.post(f"https://{ip}/api/auth/login", data=header, verify=False)
    print(response.text)
    for key, value in response.headers.items():
        print(f"{key}: {value}")
    #in principle also check wether ssh tokens are valid, but can't be bothered right now
    setCookie = response.headers['Set-Cookie'].split(";")[0].split("=")[1]
    print(setCookie)
    if "token.txt" in os.listdir():
        os.remove("token.txt")
    with open("token.txt", "w") as f:
        f.write(setCookie + "\n")
        #put age in here
        f.write(str(time.time()))