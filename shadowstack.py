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

    mode = input("Select mode: \n [1] Portscan:\n [2] Scan specific port\n")

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
         rhost