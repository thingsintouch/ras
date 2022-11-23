from multiprocessing import Process
from common import connect_To_SSID

ssidName = "'FRITZ!Box 6490 Cable'"
ssidPassword = '522968262011056618'
print("#"*100)
print("#"*100)
print("#"*100)
print(f'ssidName : {ssidName}; ssidPassword : {ssidPassword};')
connectToSSIDProcess = Process(target=connect_To_SSID.main, args=(ssidName, ssidPassword, ))
connectToSSIDProcess.start()
print("#"*100)
print("#"*100)
print("#"*100)

# NetworkManager[319]: <info>  [1667127059.8917] device (wlan0): state change: unavailable -> disconnected (reason 'supplicant-available', sys-iface-state: 'managed')