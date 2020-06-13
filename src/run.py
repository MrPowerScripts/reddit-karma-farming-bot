import init
import web
from multiprocessing import Process

if __name__ == "__main__":

  p1 = Process(target=web.webapp)
  p1.start()
  init.init()