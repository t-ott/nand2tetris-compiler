class SymbolTable:
  def __init__(self):
    pass

  def start_subroutine(self):
    pass

  def define(self, name: str, type: str, kind):
    pass

  def var_count(self, kind: str) -> int:
    pass

  def kind_of(self, name: str):
    pass

  def type_of(self, name: str) -> str:
    pass

  def index_of(self, name: str) -> int:
    pass
