import yaml,json5,json
from pyhocon import ConfigFactory
from importlib import resources
from .BluesFiler import BluesFiler

class BluesResource:
  '''
  @description : support json json5 yaml hocon files read from package resources
  '''

  @classmethod
  def read(cls,package: str,file: str):
    with resources.open_text(package, file) as f:
      return f.read()

  @classmethod
  def read_yaml(cls,package: str,file: str):
    try:
      return yaml.safe_load(cls.read(package, file))
    except Exception as e:
      print(f"yaml error: {e}")
      return None

  @classmethod
  def read_json5(cls,package: str,file: str):
    try:
      return json5.loads(cls.read(package, file))
    except Exception as e:
      print(f"json5 error: {e}")
      return None

  @classmethod
  def read_hocon(cls,package: str,file: str,as_dict=True):
    try:
      json_config = ConfigFactory.parse_file(cls.read(package, file))
      return BluesFiler.config_to_dict(json_config) if as_dict else json_config
    except Exception as e:
      print(f"hocon error: {e}")
      return None

  @classmethod
  def read_json(cls,package: str,file: str):
    try: 
      return json.loads(cls.read(package, file))
    except Exception as e:
      print(f"json error: {e}")
      return None