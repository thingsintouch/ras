import dbus
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=1).pprint

PATH_SERVICE = '/com/thingsintouch/service'
GATESETUP_SERVICE =  '000100'
CONNECT_TO_SSID_CHARACTERISTIC = '100006'
GATT_CHRC_IFACE = 'org.bluez.GattCharacteristic1'
GATT_SERVICE_IFACE = 'org.bluez.GattService1'

bus = dbus.SystemBus()

# dbus_object = bus.get_object('org.freedesktop.DBus',
#                             '/org/freedesktop/DBus')

# dbus_iface = dbus.Interface(dbus_object, 'org.freedesktop.DBus')

# services = dbus_iface.ListNames()
# services.sort()
# for service in services:
#     print("-"*100)
#     pp(service)
remote_object = bus.get_object( "org.bluez",
                                PATH_SERVICE+GATESETUP_SERVICE)

iface = dbus.Interface(remote_object, GATT_CHRC_IFACE)

pp(remote_object)
pp(iface)

ssidName = 'FRITZ!Box 6490 Cable'
ssidPassword = '522968262011056618'
value = ssidName+"\n"+ssidPassword

iface.WriteValue(value, "")
