import TransferFiles

def main():
  filetransfer = TransferFiles.TransferFiles()
  filetransfer.get_files_tobe_transferred()
  filetransfer.send_files("127.0.0.1", 1234)
  
if __name__ == "__main__":
    main()