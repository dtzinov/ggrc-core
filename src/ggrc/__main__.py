if __name__ == "__main__" and (__package__ is None or __package__ == ""):
  import os, sys
  parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  sys.path.insert(0, parent_dir)
  import ggrc
  __package__ = "ggrc"
  del sys, os

from . import app

app.run()
