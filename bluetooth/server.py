import sys
import os
from random import seed
from random import randint

from bluetooth.specificClassesBLE import GateSetupApplication, GateSetupAdvertisement, HelloWorld

# import dbus, uuid

# def connect_to_new_wifi_network(ssidName,ssidPassword):
#     print(">"*100)
#     print(">"*100)
#     print(">"*100)
#     print(f'ssidName : {ssidName}; ssidPassword : {ssidPassword};')
#     s_con = dbus.Dictionary(
#     {"type": "802-11-wireless", "uuid": str(uuid.uuid4()), "id": "RAS"}
#     )

#     s_wifi = dbus.Dictionary(
#     {"ssid": dbus.ByteArray(ssidName.encode("utf-8")), "mode": "infrastructure"}
#     )

#     s_wsec = dbus.Dictionary(
#         {"key-mgmt": "wpa-psk", "auth-alg": "open", "psk": ssidPassword}
#     )

#     s_ip4 = dbus.Dictionary({"method": "auto"})
#     s_ip6 = dbus.Dictionary({"method": "ignore"})

#     con = dbus.Dictionary(
#     {
#         "connection": s_con,
#         "802-11-wireless": s_wifi,
#         "802-11-wireless-security": s_wsec,
#         "ipv4": s_ip4,
#         "ipv6": s_ip6,
#     }
#     )
#     print("Creating connection:", s_con["id"], "-", s_con["uuid"])

#     bus = dbus.SystemBus()
#     proxy = bus.get_object(
#         "org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager/Settings"
#     )
#     settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings")

#     settings.AddConnection(con)


# def connect_to_new_wifi_network(ssidName,ssidPassword):
#     print(">"*100)
#     print(">"*100)
#     print(">"*100)
#     print(f'ssidName : {ssidName}; ssidPassword : {ssidPassword};')
#     connectToSSIDProcess = Process(target=connect_To_SSID.main, args=(ssidName, ssidPassword, ))
#     connectToSSIDProcess.start()
#     print("<"*100)
#     print("<"*100)
#     print("<"*100)

def server():
    #changeDeviceHostname()
    application     = GateSetupApplication()
    application.registerApplication()
    advertisement   = GateSetupAdvertisement()
    advertisement.makeDeviceDiscoverable()
    advertisement.registerAdvertisement()
    helloworld = Helloworld()
    #connect_to_new_wifi_network('FRITZ!Box 6490 Cable','522968262011056618')
    advertisement.infiniteLoop()

def main():
    server()

if __name__ == '__main__':
    main()

# progname = "com.example.HelloWorld"
# objpath  = "/HelloWorld"
# intfname = "com.example.HelloWorldInterface"
# methname = 'SayHello'

# bus = dbus.SystemBus()

# obj = bus.get_object(progname, objpath)
# interface = dbus.Interface(obj, intfname)     # Get the interface to obj
# method = interface.get_dbus_method(methname)  # The method on that interface

# method("Luis")                                      # And finally calling the method

