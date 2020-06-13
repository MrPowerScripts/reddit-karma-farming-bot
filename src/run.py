import init
import web
from multiprocessing import Process

if __name__ == "__main__":

  # p1 = Process(target=web.webapp)
  p2 = Process(target=init.init)
  # p1.start()
  p2.start()
  # p1.join()
  p2.join()