from importlib.machinery import SourceFileLoader


def main():
  TransferFiles = SourceFileLoader("TransferFiles", "/home/runner/butler/TransferFiles.py").load_module()
  filestransfer = TransferFiles.TransferFiles()
  filestransfer.receive_files("127.0.0.1",1234)


if __name__ == "__main__":
    main()