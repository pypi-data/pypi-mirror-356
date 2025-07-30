# Dweetme-python-client
This is a python client library for dweetme

## Installation 
pip3 install dweetme-client

## Example
import dweetme-client
dweet = dweetme_client.DweetClient("http://dweet.me:3333")
dweet.get_latest_dweet("demoESP32")
