import requests

url = "http://localhost:8000/mcp/"

headers = {
    "Accept": "application/json,text/event-stream"
}

body = {

    "jsonrpc":"2.0",

    "method":"tools/list",

    "id":1,

    "params":{}
}

response = requests.post(
    url,
    headers=headers,
    json=body
)


#  how we access the tool from the client side
# {
#   "jsonrpc": "2.0",
#   "id": 3,
#   "method": "tools/call",
#   "params": {
#     "name": "weather_current",  tool's name
#     "arguments": {
#       "location": "San Francisco",
#       "units": "imperial"
#     }
#   }
# }