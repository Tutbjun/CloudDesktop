from SetupUtils.setupSsh.SshSetup import installSsh
from SetupUtils.setupPortforwarding.PFSetup import setupPF
import yaml

with open('installSettings.yaml') as f:
    config = yaml.safe_load(f)

def installWOL():
    print("WOL Install starting...")
    print("Using settings from config file...")
    installSsh(security="keyed",PFRules=config['WOLServer']['PortForwardingRules'],returns=["puplicIP,keyPath"])
    print("SSH installed")
    setupPF(config["Port"], config["IP"])
    print("Portforwarding setup finished")

    #setup portforwarding
    #setup ssh