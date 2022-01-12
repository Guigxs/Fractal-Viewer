from bottle import run, get, request, response
import json
from compute import compute

PORT = 8181

@get('/')
def index():
    complex_r = float(request.params.get("complex_r"))
    complex_i = float(request.params.get("complex_i"))
    iter = int(request.params.get("iter"))

    result = compute(complex_r, complex_i, iter)
    response.content_type = 'application/json'
    
    return json.dumps({"response":result})

if __name__ == '__main__':
    run(host='0.0.0.0', port=PORT)
