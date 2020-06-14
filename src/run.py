import init
from web import webapp
from multiprocessing import Process

if __name__ == "__main__":

  p1 = Process(target=webapp.run)
  p1.start()
  init.init()