from common.common import runShellCommand_and_returnOutput as rs

answer = (rs("ip neigh show | grep \"$(ip route show | grep default | awk '{print $3}')\" | awk '{print $5}'")) 
answer = answer.replace("\n", "")
print(f"MAC address of the router {answer}")
