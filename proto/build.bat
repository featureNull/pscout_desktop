@echo off

echo build matcher.proto
python -m grpc_tools.protoc -I. --python_out=../ --grpc_python_out=../ matching.proto

echo build database.proto
python -m grpc_tools.protoc -I. --python_out=../ --grpc_python_out=../ metadata.proto