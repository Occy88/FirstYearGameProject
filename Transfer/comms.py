#    mmm   mmmm  mmm     mmmm   mmmm   mmmm 
#  m"   " #"   "   #    #    # "   "# m"  "m
#  #      "#mmm    #    "mmmm"   mmm" #  m #
#  #          "#   #    #   "#     "# #    #
#   "mmm" "mmm#" mm#mm  "#mmm" "mmm#"  #mm# 
# Networking class
                                          

import queue, threading, time, pycurl, json, io
from Classes.Objects import com as server
from flask import Flask, request, Response

class FlaskAppWrapper(object):
    app = None

    def __init__(self, name, inqueue):
        self.app = Flask(name)
        print("Passing inqueue to Flask")
        self.iq = inqueue

    def run(self):
        print("Flask starting...")
        self.app.run("", 5027)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=["POST"])

    def action():
        #get the dictionary of the message
        jsonData = request.get_json(force=True)
        #seperate into the queue
        for value in jsonData:
            server.recieved.put(value)
        #set the body to empty
        body = json.dumps([])

        while(not server.send.empty()):
            data = json.loads(body)
            data.append(server.send.get())
            body = json.dumps(data)
        return Response(body, status=200, headers={})

class server:

    def __init__(self):
        print("Starting server...")
        #init queues
        self.recieved = queue.Queue()
        self.send = queue.Queue()

        self.a = FlaskAppWrapper('wrap', self.recieved)
        self.a.add_endpoint(endpoint='/', endpoint_name='root', handler=FlaskAppWrapper.action)

        #start flask in a thread we can control
        self.t = threading.Thread(target=self.a.run)
        self.t.start()

class client:
    def __init__(self, peer, port):
        print("Starting client...")
        self.peer = peer 
        self.port = port

        #init queues
        self.recieved = queue.Queue()
        self.send = queue.Queue()

        #start the curl stuff in a thread we can control
        self.t = threading.Thread(target=self.makeRequest)
        self.t.start()

    def makeRequest(self):
        while(1 == 1):
            #only start a curl if we actually have something to send
            if(not self.send.empty()):
                c = pycurl.Curl()
                storage = io.BytesIO()

                c.setopt(c.URL, self.peer)
                c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
                c.setopt(pycurl.POST, 1)
                c.setopt(pycurl.PORT, self.port)
                c.setopt(c.WRITEFUNCTION, storage.write)

                #set the body to empty
                body = json.dumps([])

                while(not self.send.empty()):
                    data = json.loads(body)
                    data.append(self.send.get())
                    body = json.dumps(data)

                c.setopt(pycurl.POSTFIELDS, body)

                c.perform()
                print(c.getinfo(pycurl.RESPONSE_CODE))
                c.close()

                #get the json
                content = json.loads(storage.getvalue().decode('UTF-8'))
                print(content)
                for value in content:
                    self.recieved.put(value)