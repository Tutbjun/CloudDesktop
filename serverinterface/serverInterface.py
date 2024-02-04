#launch a small interface window to control the server
import tkinter
import tkinter.ttk as ttk
import os
import subprocess
import time

import yaml

import passwdcheck
passwd = ""
token = ""
def readTokenFile():
    with open("token.txt") as f:
        file = f.readlines()
        token = file[0].replace("\n", "")
        age = float(file[1])
        if time.time() - age > 43200:#12hours
            passwd = passwdcheck.get()
            passwdcheck.get_token(passwd)
    return token
if "token.txt" in os.listdir():
    token = readTokenFile()
else:
    passwd = passwdcheck.get()
    #get token
    passwdcheck.get_token(passwd)
    token = readTokenFile()
    passwd = ""

verbose = False

#sanitycheck password





with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    #print config
    for key, value in config.items():
        if verbose: print(key, value)

class ServerInterface(tkinter.Tk):
    def __init__(self, config):
        tkinter.Tk.__init__(self)
        self.title("Server Interface")
        self.geometry("800x600")
        self.configFile = config
        self.createWidgets()
    
    def launch(self, launcher, args):
        #launch a program with the given arguments
        pop = subprocess.Popen(["python3", os.path.join("interactions/interfaces",launcher), *args])
        pop.wait()
        if not "web" in launcher:
            exit()
        #exit()

    def showMenu(self, frame, data, layer=0, buttonNmbr=1, buttonCnt=1):
        #clear the current buttons
        def clearButtons(frame, depth):
            if depth+1 < len(self.menuFrameLayers):
                clearButtons(self.menuFrameLayers[layer+1], depth+1)
            for button in frame.winfo_children():
                button.pack_forget()
            if depth > layer:
                self.menuFrameLayers[depth].pack_forget()
                self.menuFrameLayers.pop(depth)
        clearButtons(frame, layer)
        #create buttons for the available options
        newFrame = ttk.Frame(self.parentFrame)
        self.menuFrameLayers.append(newFrame)
        self.menuFrameLayers[layer+1].pack(side="left", fill="y")
        def selectBracket():
            length = buttonCnt
            h = buttonNmbr
            imgName = f"bracket{h}x{length}.png"
            if imgName not in os.listdir():
                imgName = "bracket.png"
            return imgName
        if layer > 0:
            #insert a curly bracket image to the left of the new button, and scale it to the height of the button
            bracket = tkinter.PhotoImage(file=selectBracket())
            bracketLabel = ttk.Label(frame, image=bracket)
            bracketLabel.image = bracket
            bracketLabel.pack(side="left")
        frame.interfaceButtons = []
        if layer == 0:
            self.subButtonAttributes = []
        j = 0
        for key, value in data.items():
            valueIsDict = isinstance(value, dict)
            #check if the entry of value is a dictionary
            subValueIsDict = False
            if valueIsDict:
                for subKey, subValue in value.items():
                    if isinstance(subValue, dict):
                        subValueIsDict = True
                        break
            if valueIsDict and subValueIsDict:
                self.subButtonAttributes.append((self.menuFrameLayers[layer+1], value, layer+1,j+1, len(data)))
                i = len(self.subButtonAttributes)-1
                button = ttk.Button(frame, text=key, command=lambda index=i: self.showMenu(*self.subButtonAttributes[index]))
                button.pack(side="top", fill="both", expand=True)
                frame.interfaceButtons.append(button)
            else:
                #password passon
                value['args'].append(f"password {passwd}")
                value['args'].append(f"token {token}")
                self.subButtonAttributes.append((value["launcher"], value["args"]))
                i = len(self.subButtonAttributes)-1
                button = ttk.Button(frame, text=key, command=lambda index=i: self.launch(*self.subButtonAttributes[index]))
                button.pack(side="top", fill="both", expand=True)
                frame.interfaceButtons.append(button)
            j += 1
        #pack the sub-menu frame to the right side of the current frame
        """for i in range(layer+1, len(self.menuFrameLayers)):
            self.menuFrameLayers[i].pack(side="right", fill="y")"""
        #self.menuFrameLayers[layer] = frame
    
    def createWidgets(self):
        #create a parent frame for the main menu and the sub-menu, and a scrollbar
        self.parentFrame = ttk.Frame(self)
        #self.scrollbar = ttk.Scrollbar(self, orient="horizontal")
        #self.scrollbar.pack(side="bottom", fill="x")
        self.parentFrame.pack(side="left", fill="y")
        self.menuFrameLayers = []
        """#create a frame for the main menu and pack it to the left side of the parent frame
        self.menuFrame = ttk.Frame(self.parentFrame)
        self.menuFrame.pack(side="left", fill="y")
        #create a frame for the sub-menu and pack it to the right side of the parent frame
        self.subMenuFrame = ttk.Frame(self.parentFrame)
        self.subMenuFrame.pack(side="right", fill="y")"""
        #create a frame for the main menu and pack it to the left side of the parent frame
        self.menuFrameLayers.append(ttk.Frame(self.parentFrame))
        self.menuFrameLayers[0].pack(side="left", fill="y")
        #show the main menu
        self.showMenu(self.menuFrameLayers[0], self.configFile, 0)
    
if __name__ == "__main__":
    serverInterface = ServerInterface(config)
    serverInterface.mainloop()