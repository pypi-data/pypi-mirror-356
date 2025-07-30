# Arcane bigquery-storage README

A package to call the BigQuery Storage Write API. To have more info check https://cloud.google.com/bigquery/docs/write-api
This API uses the protocol buffers for serialization and deserialization. You can find the protobuf definitions in the `proto` folder.
More information on protobuf https://protobuf.dev/getting-started/pythontutorial/

## Using the compiler

### Install the compiler
To compile a protocol buffer, you will to have the compiler install.
Check this page to see the latest version https://protobuf.dev/downloads/.
It is important to check the version of the compiler and the version of the protobuf definitions. They must be compatible.
Check https://protobuf.dev/support/version-support/#python for the compatibility matrix.
At the time of writing, the protoc version is 21.12 and the protobuf version is 3.20.3.

Download the binary for the Mac OS. The name is something like `protoc-21.12-osx-universal_binary.zip`
Unzip the file and copy the `protoc` binary to `/usr/local/bin` : `mv ~/Downloads/protoc-21.12-osx-universal_binary/bin/protoc /usr/local/bin/`
Finally copy the include folder `sudo cp -r ~/Documents/projet/protoc-21.12-osx-universal_binary/include/* /usr/local/include/`
Verify that the compiler is installed by running `protoc --version`

### Running the compiler
In the arcane/bigquery-storage/proto/ folder, you will find the protobuf definitions.
To compile a file, run the following command `protoc --python_out=. --pyi_out=. <file>.proto`
It generates a python file with the same name as the proto file. You can now commit it and create a new version of this package.

## Release history
To see changes, please see CHANGELOG.md
