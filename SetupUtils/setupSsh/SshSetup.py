import os

def installSsh(security,PFRules,returns=[]):
    print("Installing SSH")
    data = {"keyLocation" : "", "securityType" : security, "localIP" : "", "localPort" : ""}
    #if PF is true in PFRules, do PF and append returnsdata to data
    #if openssh-server is not installed, install
    os.system("yum install -y openssh-server")
    #then put all the known data into data
    print("SSH installed")
    #return parts of data defined by returns