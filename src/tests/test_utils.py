from .. import utils

def test_random_string():
  string = utils.random_string(5)
  assert type(string) is str
  assert len(string) == 5
