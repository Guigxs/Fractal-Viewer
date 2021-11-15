from bottle import run, get, post, request, response
import json
from compute import compute
import requests

LOAD_BALANCER_URL = "http://127.0.0.1:8181/register"
IP = "127.0.0.1"
PORT = 8182

@get('/')
def index():
    complex_r = float(request.params.get("complex_r"))
    complex_i = float(request.params.get("complex_i"))
    iter = int(request.params.get("iter"))

    result = compute(complex_r, complex_i, iter)
    response.content_type = 'application/json'
    
    return json.dumps({"response":result})


def registerWorker():
    print("Registering new worker...")
    resp = requests.post(LOAD_BALANCER_URL, json= {"ip":IP, "port":PORT})
    print(resp.status_code)

if __name__ == '__main__':
    registerWorker()
    run(host='0.0.0.0', port=PORT)
