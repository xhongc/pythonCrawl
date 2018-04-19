from ws4py.client.threadedclient import WebSocketClient

class DummyClient(WebSocketClient):
    def opened(self):
        self.send("www.baidu.com")

    def closed(self, code, reason=None):
        print ("Closed down", code, reason)

    def received_message(self, m):
        print (m)

if __name__ == '__main__':
    try:
        ws = DummyClient('ws://10.222.138.163:1889/websocket', protocols=['chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
