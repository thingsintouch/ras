import subprocess

ssidName = "__nebuchadnezzar__"
ssidPassword = "mi"
print(f'ssidName : {ssidName}; ssidPassword : {ssidPassword};')
#answer = (rs('nmcli dev wifi con "'+ssidName+'" password '+ssidPassword))
name =ssidName
print(f"name {name}")
subprocess.Popen(["nmcli","dev","wifi", 'con', name, 'password', ssidPassword])

# import subprocess
# import time

# print("1"*100)
# time.sleep(90)
# ssidName = "FRITZ!Box 6490 Cable"0
# ssidPassword = "522968262011056618"
# print("2"*100)
# print(f'ssidName : {ssidName}; ssidPassword : {ssidPassword};')
# #answer = (rs('nmcli dev wifi con "'+ssidName+'" password '+ssidPassword))
# name =ssidName
# print(f"name {name}")
# subprocess.Popen(["nmcli","dev","wifi", 'con', name, 'password', ssidPassword])
# print("3"*100)
# time.sleep(90)
# print("4"*100)
