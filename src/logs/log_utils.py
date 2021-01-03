import logging
import json
from logging.handlers import RotatingFileHandler

def log_json(tojson: object) -> str:
  return json.dumps(tojson, indent=2, sort_keys=True)

class NewLineFileHandler(RotatingFileHandler):
  """Handler that controls the writing of the newline character"""

  special_code = '[!n]'

  def emit(self, record) -> None:

    if self.special_code in record.msg:
      record.msg = record.msg.replace( self.special_code, '' )
      self.terminator = ''
    else:
      self.terminator = '\n'

    return super().emit(record)

class NewLineStreamHandler(logging.StreamHandler):
  """Handler that controls the writing of the newline character"""

  special_code = '[!n]'

  def emit(self, record) -> None:

    if self.special_code in record.msg:
      record.msg = record.msg.replace( self.special_code, '' )
      self.terminator = ''
    else:
      self.terminator = '\n'

    return super().emit(record)