from queue import Queue
from functools import partial

eventloop = None
class EventLoop(Queue):
    def start(self):
        i = 1
        while i < 21:
            function = self.get()
            print ("The", i, "times, function: ", function)
            function()
            i += 1

def do_hello():
    global eventloop
    print ("hello")
    eventloop.put(do_world)

def do_world():
    global eventloop
    print ("world")
    eventloop.put(do_hello)

@coroutine
def save_value(value, callback):
    print ("Saving {} to database".format(value))
    db_response = yield save_result_to_db(result, callback)
    print ("Response from database: {}".format(db_response))

if __name__ == "__main__":
    eventloop = EventLoop()
    eventloop.put(do_hello)
    eventloop.start()
