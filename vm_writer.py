class VMWriter:
  def __init__(self):
    pass

  def write_push(self, segment, index: int):
    pass

  def write_pop(self, segment, index: int):
    pass

  def write_arithmetic(self, command):
    pass

  def write_label(self, label: str):
    pass

  def write_goto(self, label: str):
    pass

  def write_if(self, label: str):
    pass

  def write_call(self, name: str, n_args: int):
    pass

  def write_function(self, name: str, n_locals: int):
    pass

  def write_return(self):
    pass

  def close(self):
    pass
  