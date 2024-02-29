class PreProcessorExceptions(Exception):
  def __init__(self, *args: object, additionalMsg: str = '') -> None:
      super().__init__(*args)
      self.addtionalMsg= additionalMsg

class TextParserExceptions(Exception):
  def __init__(self, *args: object, additionalMsg: str = '') -> None:
      super().__init__(*args)
      self.addtionalMsg= additionalMsg

