from TwStreamListener import *

print("Start process")
myStreamListener = TwStreamListener()
myStreamListener.connect()
myStreamListener.run()
print("Stop process")