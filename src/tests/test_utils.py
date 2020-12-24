from .. import utils

def test_random_string():
  string = utils.random_string(5)
  assert type(string) is str
  assert len(string) == 5

def test_load_config():
  config = utils.load_config("test")
  assert config['loaded'] == True