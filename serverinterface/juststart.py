import passwdcheck
import os
import time
def do():
    passWordAge = None#43200#12hours

    passwd = ""
    token = ""
    def readTokenFile():
        with open("token.txt") as f:
            file = f.readlines()
            token = file[0].replace("\n", "")
            age = float(file[1])
            if passWordAge != None:
                if time.time() - age > passWordAge:#12hours
                    passwd = passwdcheck.get()
                    passwdcheck.get_token(passwd)
        return token
    if 'token.txt' in os.listdir():
        token = readTokenFile()
    else:
        raise Exception("No token file found")

    #change os folder to __file__ folder
    #run start_server.py with the token
    os.system(f"python3 {os.path.join(os.path.dirname(__file__), 'interactions', 'interfaces', 'start_server.py')} 0_on password {passwd} token {token}")

if '0' not in str(response := os.system("curl -k https://85.191.70.197:8006 --connect-timeout 1")):
    print(response)

    do()
else:
    if '0' not in str(response := os.system("curl -k https://85.191.70.197:8006 --connect-timeout 1")):
        print(response)
        do()
    else:
        print(response)
        print("Server is already running")
