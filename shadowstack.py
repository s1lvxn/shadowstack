import socket
import pyfiglet
import threading
from datetime import datetime
import os
import ipaddress
import time

doagain = 1
while doagain == 1:
    startbanner = pyfiglet.figlet_format("Shadow Stack", font="slant")
    os.system('cls' if os.name == 'nt' else 'clear')
    print(startbanner)

    mode = input("Select mode: \n [1] Portscan:\n [2] Banner grabbing\n [3] Search for Hosts in Subnet\n")
#Port Scan:
    if mode == "1":
            rhost = input("Type IP Address:\n")
            os.system('cls' if os.name == 'nt' else 'clear')
            print(startbanner)
            print("----------------------------------------------------------") 
            print(f"Scanning Target {rhost}")
            print(f"SCanning startet at: {datetime.now()} ")
            print("----------------------------------------------------------") 
            def scan(rhost, port):            
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(0.1)
                    
                result = sock.connect_ex((rhost, port))
                if result ==0:
                    print (f"Port {port} is open")

                sock.close()

            threads = []
            for port in range(1,1024):
                thread = threading.Thread(target=scan, args=(rhost, port))
                thread.start()
                
            print("----------------------------------------------------------\n" \
            f"Scan Finished at: {datetime.now()} \n---------------------------------------------------------- ")
            again = input("\nDo you want to scan again? (y/n): ").lower()
            if again != "y":
                doagain = 0
 #Banner grabbin  
    elif mode == "2":
            rhost = input("Type IP Address:\n")
            os.system('cls' if os.name == 'nt' else 'clear')
            print(startbanner)
            print("----------------------------------------------------------") 
            print(f"Scanning Target {rhost}")
            print(f"Banner grabbing startet at: {datetime.now()} ")
            print("----------------------------------------------------------") 
            def bannergrab(rhost, port):
                try:
                    
                    s = socket.socket()
                    s.settimeout(5)  
                    s.connect((rhost, int(port)))
                    if port == 80:
                                s.sendall(b"GET / HTTP/1.1\r\nHost: %s\r\n\r\n" % rhost.encode())
                    elif port == 25:
                                s.sendall(b"EHLO example.com\r\n")
                    elif port == 443:
                                print(f"Port {port} (HTTPS) needs SSL. Skipping.")
                                s.close()
                                return

                    banner = s.recv(1024).decode().strip()
                    print(f"Banner for {rhost}:{port} -> {banner}")
                except socket.error as e:
                    pass
                
                finally:
                    s.close()

            threads = []
            for port in range(1,1024):
                thread = threading.Thread(target=bannergrab, args=(rhost, port))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()    

               
            again = input("\nDo you want to scan again? (y/n): ").lower()
            if again != "y":
                doagain = 0
#Scan subnet
    elif mode == "3":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(startbanner)
            subnet = input("Type Subnet (CIDR) \n")
            addresses = [str(ip) for ip in ipaddress.IPv4Network(subnet)]
            ports = [22, 25, 80, 443, 3389, 445, 53]
            
            def netscan(host):
                hostisup = False
                for port in ports:
                    try:
                        s = socket.socket()
                        s.settimeout(5)
                        s.connect((host, port))
                        hostisup = True  
                        break 
                    except:
                        pass
                    finally:
                        s.close()
                if hostisup:
                    print(f"{host} is UP!")

            threads = []
            for host in addresses:
                thread = threading.Thread(target=netscan, args=(host,))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            time.sleep(1.5)
            print("----------------------------------------------------------\n" \
            f"Scan Finished at: {datetime.now()} \n---------------------------------------------------------- ")


            again = input("\nDo you want to scan again? (y/n): ").lower()
            if again != "y":
                doagain = 0