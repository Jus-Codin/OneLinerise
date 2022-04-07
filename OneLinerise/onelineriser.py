import builtins

from __future__ import annotations

class OneLineError(Exception): ...

class _MISSING: ...

def chainablemethod(func):
  """Convienience decoratror which makes a method return its class"""
  def wrapper(self, *args, **kwargs):
    func(self, *args, **kwargs)
    return self
  return wrapper



class AttributedCallable:
  """
  Due to the confusion of using a property decorator for the chaining of functions, 
  it is better to make a new class to tell the difference

  This class decorator functions similar to `@property`, except that it is view only and cannot be set
  """

  def __init__(self, func):
    self.func = func

  def __get__(self, instance, owner=None):
    if instance is None:
      return self
    return self.func(instance)



class _ProxyObject:
  """
  Hah try saying that ten times real quick
  This is not meant to be created by the user, its only used internally

  Parameters
  ----------
  owner: :class:`OneLinerise`
  value: `Any`


  """
  
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
  
  @AttributedCallable
  def RET_OBJ(self):
    """Stop getting items from current object, return to monke"""

    self.owner.last = self.value
    return self.owner



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

  @AttributedCallable
  @chainablemethod
  def save_last(self):
    """Saves the value of the last thing returned in '_'"""
    self._globals["_"] = self.last

  @AttributedCallable
  @chainablemethod
  def print_last(self):
    """Prints the last object returned"""
    print(self.last)
  
  @AttributedCallable
  def returned(self):
    """
    Creates a proxy object which allows you to interact with the last object. To return to the main class run the `RET_OBJ`.
    Yes, it's a bad way to do it, but does it look like I care?
    """

    if self.last is _MISSING:
      raise OneLineError("nothing to return!")
    return _ProxyObject(self, self.last)

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