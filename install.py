import yaml
from WOLSetup.setupWOL import installWOL

with open('installSettings.yaml') as f:
    config = yaml.safe_load(f)

def UIInstall():
    print("UI Install starting...")
    raise NotImplementedError("UI Install not implemented yet")

def CLIInstall():
    def installClient():
        print("Client Install starting...")
        raise NotImplementedError("Client Install not implemented yet")
    def installServer():
        print("Server Install starting...")
        raise NotImplementedError("Server Install not implemented yet")
    
    print()
    print("CLI Install starting...")
    setupOptions = config["SetupType"]
    setupOptionsList = []
    for option in setupOptions.items():
        setupOptionsList.append(option[1])
    setupType = ""
    if len(setupOptionsList) == 1:
        setupType = setupOptionsList[0]
    elif len(setupOptionsList) == 0:
        print("No setup options found in config file")
        return
    while setupType == "":
        print("choose one of the following setup types:")
        for i,option in enumerate(setupOptionsList):
            print(f"{i+1}. {option} type setup")
        chosen = input()
        try:
            chosen = int(chosen)
        except ValueError:
            print("Invalid input")
            continue
        if chosen-1 not in range(len(setupOptionsList)):
            print("Invalid input")
            continue
        setupType = setupOptionsList[chosen-1]
    print(f"Setup type chosen: {setupType}")
    print()
    if setupType == "WOLServer":
        installWOL()
    elif setupType == "Client":
        installClient()
    elif setupType == "Server":
        installServer()
    
    print("CLI Install finished")

if __name__ == '__main__':
    CLIInstall()