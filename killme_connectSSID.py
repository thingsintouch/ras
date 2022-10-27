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