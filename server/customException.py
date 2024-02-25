class PreProcessorExceptions(Exception):
  def __init__(self, *args: object, additionalMsg: str = '') -> None:
      super().__init__(*args)
      self.addtionalMsg= additionalMsg
