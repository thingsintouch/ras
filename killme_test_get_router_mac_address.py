import psutil
import socket

def get_router_info(ip_address):
    # Get network interfaces
    interfaces = psutil.net_if_addrs()
    
    # Initialize variables for MAC address and connection type
    mac_address = None
    connection_type = None

    # Iterate through network interfaces
    for interface, addrs in interfaces.items():
        #print(f"interface - {interface}; addrs - {addrs}")
        for addr in addrs:
            if addr.address == ip_address:  # MAC address
                mac_address = addr.address
                if interface.startswith('w'):
                    connection_type = 'Wi-Fi'
                elif interface.startswith('eth'):
                    connection_type = 'Ethernet'
                else:
                    connection_type = str(interface)
    
    return mac_address, connection_type

def get_ip_address():
    try:
        # Create a socket to determine the IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.1)  # Short timeout
        s.connect(("8.8.8.8", 80))  # Connect to a public DNS server
        ip_address = s.getsockname()[0]
        s.close()
        return str(ip_address)
    except Exception as e:
        print(f"Exception while retreiving IP address - {e}")
        return False

if __name__ == "__main__":



    ip_address = get_ip_address()
    
    if ip_address:
        mac, connection = get_router_info(ip_address)
        
        if mac:
            print(f"Router MAC Address: {mac}")
            if connection:
                print(f"Connection Type: {connection}")
            else:
                print("Connection Type: Unknown")
        else:
            print("Router MAC Address not found.")