import TransferFiles

# The usage of the two libraries tqdm and pycurl is not working
def main():
  filetransfer = TransferFiles()
  filetransfer.curl_files()

if __name__ == "__main__":
    main()