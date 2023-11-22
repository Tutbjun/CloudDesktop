import yaml
import sys
import subprocess
import os
import pexpect
import time

flags = sys.argv[1:]
print(flags)

with open(os.path.join("interactions/interfaces",'launcherConfig.yaml')) as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    #print config
    for key, value in config.items():
        print(key, value)
#launcherName = config["settings"]["sshLauncher"]
#print(launcherName)
cmd = []
#exePath = str(os.path.join(config["config"][launcherName]["path"]))
#print(exePath)
#cmd.append(exePath)
#args = config["config"][launcherName]["args"]
#print(args)
#cmd.append(args)
url = f"ssh {flags[2]}@{flags[0]}"
if flags[1] == "none":
    pass
else:
    url += f" -p {flags[1]}"
if len(flags) > 3:
    #everything after the first 3 flags in quatation marks is the command to be executed
    #so find the quatation marked part
    flag = " ".join(flags[3:])
    print(flag)
    try:
        phrase, password = flag.split(' password')[0], flag.split(' password ')[1]
        url += f' "{phrase}"'
    except:
        password = flag.split('password ')[1]
    #flag = flag.split(' ')[0]
    print(password)

print(url)
cmd.append(url) 
#print(args)
#rewrite but with pexpect
"""pop = subprocess.Popen(" ".join(cmd), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print("Writing password")
pop.wait()
pop.stdin.write(f"{password}\n")
pop.stdin.flush()
pop.wait()
print(pop.returncode, pop.communicate())"""
print(cmd)
child = pexpect.spawn(" ".join(cmd))
child.expect(f"{flags[2]}@85.191.70.197's password:")
#time.sleep(3)
child.sendline(password)
#wait for the command to finish
child.expect(pexpect.EOF)