#!/bin/bash

git clone https://github.com/DominicBreuker/pspy.git
cd pspy
go build
go mod init Gopkg.lock
go mod tidy
go mod vendor
go build
cp Gopkg.lock ../pspy.go
rm -r ../pspy