from bottle import HTTPResponse, run, get, post, request, response
import json
import requests
import threading

import tornado.ioloop
import tornado.web

WORKER_LIST = []

class MainHandler(tornado.web.RequestHandler):
    def test(self, un):
        print("Starting new thread...")
        a = 0
        while True:
            a+=1
            if a%6000000==0:
                print(a)
                
            if a == 60000000:
                print("finish")
                return self.write("finish")

    def get(self):
        self.test("un")
        # self.write("hey")
        


class RegisterHandler(tornado.web.RequestHandler):
    def post(self):
        ip, port = json.loads(self.request.body).values()
        WORKER_LIST.append((ip, port))
        self.write("Registered")

def make_app():
    return tornado.web.Application([
        (r"/register", RegisterHandler),
        (r"/.*", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8181)
    tornado.ioloop.IOLoop.current().start()



# def test(request, response):
#     print("Starting new thread...")
#     a = 0
#     while True:
#         a+=1
#         if a%6000000==0:
#             print(a)
            
#         if a == 120000000:
#             # print("finish")
#             return HTTPResponse(status=200, body={"success":True})
    

# @get('/')
# def index():
#     print("Recieving new pixel...")
#     complex_r = float(request.params.get("complex_r"))
#     complex_i = float(request.params.get("complex_i"))
#     iter = int(request.params.get("iter"))

#     x = threading.Thread(target=test, args=(request, response))
#     x.start()


    

# @post('/register')
# def index():
#     print('New worker request')
#     ip = request.json.get("ip")
#     port = request.json.get("port")

#     WORKER_LIST.append((ip, port))
#     print(WORKER_LIST)

#     return HTTPResponse(status=201, body={"success":True})


