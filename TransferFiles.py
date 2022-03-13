import socket
import os
import time
import subprocess


class TransferFiles:
    filesnames = []

    def __init__(self):
        self.filesnames = ["linpeas.sh", "pspy.go"]

    
    def get_files_tobe_transferred(self):
        os.system(
            "curl -o linpeas.sh -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh"
        )
        print(subprocess.call("./pspy_install.sh"))

 
    def send_one_file(self,filename,client_ip,client_port):
        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096
        s = socket.socket()
      
        print(f"[+] Connecting to {client_ip}:{client_port}")
        s.connect((client_ip, client_port))
        print("[+] Connected.")

        filesize = os.path.getsize(filename)
        time.sleep(20)
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
                print("Sending in Progress")
        s.close()

    
    def receive_one_file(self,filename,server_ip,server_port):
        s = socket.socket()
        s.bind((server_ip, server_port))
        s.listen(5)
        print(f"[*] Listening as {server_ip}:{server_port}")
        client_socket, address = s.accept()
        print(f"[+] {address} is connected.")
        BUFFER_SIZE = 4096
        SEPARATOR = "<SEPARATOR>"
      
        recieved = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = recieved.split(SEPARATOR)
        filename = os.path.basename(filename)
        print(filesize,"  --- filesizeeee !!!")
        filesize = int(filesize)
      
        with open(filename, "wb") as f:
            while True:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
        client_socket.close()
        s.close()
      
  
    def send_files(self,client_ip, client_port):
        self.send_one_file("linpeas.sh",client_ip,client_port)
        time.sleep(20)
        self.send_one_file("pspy.go",client_ip,client_port)
        

  
    def receive_files(self,server_ip,server_port):
        self.receive_one_file("linpeas.sh",server_ip,server_port)
        time.sleep(20)
        self.receive_one_file("pspy.go",server_ip,server_port)
        

