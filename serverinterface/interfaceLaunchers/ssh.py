import yaml
import sys
import subprocess
import os

flags = sys.argv[1:]

with open(os.path.join("interfaceLaunchers",'launcherConfig.yaml')) as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    #print config
    for key, value in config.items():
        print(key, value)
launcherName = config["settings"]["sshLauncher"]
print(launcherName)
cmd = []
exePath = str(os.path.join(config["config"][launcherName]["path"]))
print(exePath)
cmd.append(exePath)
args = config["config"][launcherName]["args"]
print(args)
cmd.append(args)
url = f"ssh {flags[2]}@{flags[0]}"
if flags[1] == "none":
    pass
else:
    url += f" -p {flags[1]}"
print(url)
cmd.append(url) 
print(args)
subprocess.Popen(" ".join(cmd), shell=True)