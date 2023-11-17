@app
arc-python-example

@http
get /

@aws
runtime python3.11
region us-east-1
architecture arm64
memory 256
timeout 30
