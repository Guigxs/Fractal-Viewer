from bottle import run, get, post, request

@get('/')
def index():
    complex_r = request.params.get("complex_r")
    complex_i = request.params.get("complex_i")
    iter = request.params.get("iter")
    return f'<b>Hello Guillaume, your complex is : {complex_r} + {complex_i}j with {iter} iterations </b>!'

run(host='0.0.0.0', port=8181)
