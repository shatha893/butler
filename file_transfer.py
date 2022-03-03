# Simplify getting reverse shells as follows  

# 1. I have to handle the file transfer between the two machines
# How do I do that?   
    # 
# 2. I have to make sure that I can transfer files with a simple sh shell before I upgrade it.
# The user has to be in a writable directory when running the script on the victim machine
# 3. I want to transfer the following files  
    # Linpeas, linenum and lse
    # suid3num or sth like that ( I forgot the name ).
    # pspy
    # I have this idea to add these files in the repository of the code so that the user doesn't have to download them separately
    # So that *I* don't have to download them separately or worry if they're in the same directory I'm in...etc
# 4. I want to run the files and write their output each in a separate file
# 5. I also want to create a directory to put these files and their output inside of it.
# For pspy I can run it maybe for like 5 minutes to check for the cron jobs and if I can save its output in a file too.
# But maybe 5 minutes is a very long time for a script to run. So I'll see what to do about it. Maybe just copy the pspy binary and then let the user run it
# 6. Now I have to upgrade the reverse shell (I'll research that more).  


# Shit on Crackers
# I should write a bunch of modules (functions) 

# File transfer
# I will be downloading the script after I got a rev shell
# Ask user to go to /tmp or maybe I can download shit in /tmp without the user being there.
# I want to download linpeas, run it and save the output in a file

# https://www.thepythoncode.com/article/send-receive-files-using-sockets-python  
# Shit on Crackers
# I should write a bunch of modules (functions) 

# File transfer
# I will be downloading the script after I got a rev shell
# Ask user to go to /tmp or maybe I can download shit in /tmp without the user being there.
# I want to download linpeas, run it and save the output in a file

# https://www.thepythoncode.com/article/send-receive-files-using-sockets-python  
import socket
import os
# import tqdm

def transfer_file(filename):

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