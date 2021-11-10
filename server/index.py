from bottle import run, get, post, request, response
import json
from compute import compute

@get('/')
def index():
    complex_r = float(request.params.get("complex_r"))
    complex_i = float(request.params.get("complex_i"))
    iter = int(request.params.get("iter"))

    result = compute(complex_r, complex_i, iter)
    response.content_type = 'application/json'
    
    return json.dumps({"response":result})
    # f'<b>Hello Guillaume, your complex is : {complex_r} + {complex_i}j with {iter} iterations </b>!<p> Result : {result} </p>'

run(host='0.0.0.0', port=8181)
