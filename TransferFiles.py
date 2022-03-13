import socket
import os
import threading
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

 
    def send_one_file(self,filename, input_ip, input_port):

        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096
        host = input_ip 
        port = input_port
        filesize = os.path.getsize(filename)
        s = socket.socket()
        print(f"[+] Connecting to {host}:{port}")
        s.connect((host, port))
        print("[+] Connected.")
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())

        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
                print("Sending in Progress")
        s.close()

    
    def receive_one_file(self,filename,input_ip,input_port):
      
        SERVER_HOST = input_ip
        SERVER_PORT = input_port
        BUFFER_SIZE = 4096
        SEPARATOR = "<SEPARATOR>"
        s = socket.socket()
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(5)
        print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
        client_socket, address = s.accept()
        print(f"[+] {address} is connected.")
        with open(filename, "wb") as f:
            while True:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
        client_socket.close()
        s.close()

  
    def send_files(self,client_ip,client_port):
          for i in range(len(self.filesnames)):
              file_thread = threading.Thread(target=self.send_one_file(i,client_ip,client_port),
                                             args=(self.filesnames[i]))
              file_thread.start()

  
    def receive_files(self,server_ip,server_port):
        for i in range(len(self.filesnames)):
            file_thread = threading.Thread(target=self.receive_one_file(i,server_ip,server_port),
                                           args=(self.filesnames[i]))
            file_thread.start()