import builtins

class OneLineError(Exception): ...

class _MISSING: ...



class ProxyObject:
  """Hah try saying that ten times real quick"""
  
  def __init__(self, owner, value):
    self.owner = owner
    self.value = value

  def __getattr__(self, attr):
    self.value = getattr(self.value, attr)
    return self

  def __getitem__(self, *keys):
    self.value = self.value.__getitem__(*keys)
    return self

  def __call__(self, *args, **kwargs):
    self.value = self.value(*args, **kwargs)
    return self
  
  @property
  def RET_OBJ(self):
    """Stop getting items from current object, return to monke"""
    self.owner.last = self.value
    return self.owner



def chainablemethod(func):
  """Convienience decoratror which makes a method return its class"""
  def wrapper(self, *args, **kwargs):
    func(self, *args, **kwargs)
    return self
  return wrapper



class OneLinerise:
  """Where the magic happens"""
  last = _MISSING

  def __init__(self, globals=globals()):
    self._globals = globals

  def __getattr__(self, attr):
    try:
      self.last = getattr(builtins, attr)
    except AttributeError:
      self.last = self._globals[attr]
    return self

  def __getitem__(self, keys):
    self.last = self.last.__getitem__(keys)
    return self

  def __call__(self, *args, **kwargs):
    if self.last is _MISSING:
      raise OneLineError("there is nothing to call!")
    self.last = self.last(*args, **kwargs)
    return self

  @property
  @chainablemethod
  def save_last(self):
    """Saves the value of the last thing returned in '_'"""
    self._globals["_"] = self.last

  @property
  @chainablemethod
  def print_last(self):
    """Prints the last object returned"""
    print(self.last)
  
  @property
  def returned(self):
    """Creates a proxy object which allows you to interact with the last object. To return to the main class run the `RET_OBJ`.
    Yes, it's a bad way to do it, but does it look like I care?"""
    if self.last is _MISSING:
      raise OneLineError("nothing to return!")
    return ProxyObject(self, self.last)

  @chainablemethod
  def save_last_as(self, name):
    """Saves the value of the last thing returned with the name supplied"""
    self._globals[name] = self.last

  @chainablemethod 
  def literal(self, literal):
    """Empty function for you to pass literals like `1` or `None` into"""
    self.last = literal

  @chainablemethod
  def set_var(self, var, name=None):
    """Sets a value of a variable. If no name is given, then '__' will be used"""
    self._globals[name if name is None else "__"] = var