import socket
import pyfiglet
import threading
from datetime import datetime
import os

doagain = 1
while doagain == 1:
    startbanner = pyfiglet.figlet_format("Shadow Stack", font="slant")
    os.system('cls' if os.name == 'nt' else 'clear')
    print(startbanner)

    mode = input("Select mode: \n [1] Portscan:\n [2] Banner grabbing\n")

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
    
    elif mode == "2":
            rhost = input("Type IP Address:\n")
            #port = input("Type the Port to scan:\n")
            os.system('cls' if os.name == 'nt' else 'clear')
            print(startbanner)
            print("----------------------------------------------------------") 
            print(f"Scanning Target {rhost}")
            print(f"Banner grabbing startet at: {datetime.now()} ")
            print("----------------------------------------------------------") 
            def bannergrab(rhost, port):
                try:
                    # Initialize a socket and connect to the given IP and port
                    s = socket.socket()
                    s.settimeout(5)  # Set a 5-second timeout
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