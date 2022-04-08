
from __future__ import annotations

import builtins

from typing import Any, Callable

class OneLineError(Exception): ...

class _MISSING: ...

def chainablemethod(func: Callable) -> Callable:
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

  def __init__(self, func: Callable):
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
  owner : `OneLinerise`
  value : `Any`

  Attributed Callables
  --------------------
  RET_OBJ :
    Stop getting items from current object, return to monke
  """
  
  def __init__(self, owner: OneLinerise, value):
    self.owner = owner
    self.value = value

  def __getattr__(self, attr) -> _ProxyObject:
    self.value = getattr(self.value, attr)
    return self

  def __getitem__(self, *keys) -> _ProxyObject:
    self.value = self.value.__getitem__(*keys)
    return self

  def __call__(self, *args, **kwargs) -> _ProxyObject:
    self.value = self.value(*args, **kwargs)
    return self
  
  @AttributedCallable
  def RET_OBJ(self) -> OneLinerise:
    """Stop getting items from current object, return to monke"""
    self.owner.last = self.value
    return self.owner



class OneLinerise:
  """
  Where the magic happens
  
  Parameters
  ----------
  globals : `dict`
    The dictionary in which the variables will be stored.
    Pass in `globals()` in order for it to store the variables
    directly in your python file to be run
  """

  last = _MISSING

  def __init__(self, globals=globals()):
    self._globals = globals

  @chainablemethod
  def __getattr__(self, attr) -> OneLinerise:
    try:
      self.last = getattr(builtins, attr)
    except AttributeError:
      self.last = self._globals[attr]

  @chainablemethod
  def __getitem__(self, keys) -> OneLinerise:
    self.last = self.last.__getitem__(keys)

  @chainablemethod
  def __call__(self, *args, **kwargs) -> OneLinerise:
    if self.last is _MISSING:
      raise OneLineError("there is nothing to call!")
    self.last = self.last(*args, **kwargs)

  @AttributedCallable
  @chainablemethod
  def save_last(self) -> OneLinerise:
    """Saves the value of the last thing returned in '_'
    
    Raises
    ------
    OneLineError
      If there is no objects created yet
    """
    if self.last is _MISSING:
      raise OneLineError("nothing to save!")
    self._globals["_"] = self.last

  @AttributedCallable
  @chainablemethod
  def print_last(self) -> OneLinerise:
    """Prints the last object returned
    
    Raises
    ------
    OneLineError
      If there is no objects created yet
    """
    if self.last is _MISSING:
      raise OneLineError("no objects to print!")
    print(self.last)
  
  @AttributedCallable
  def returned(self) -> _ProxyObject:
    """
    Creates a proxy object which allows you to interact with the last object. To return to the main class run the `RET_OBJ`.
    Yes, it's a bad way to do it, but does it look like I care?

    Raises
    ------
    OneLineError
      If there is no objects created yet
    """
    if self.last is _MISSING:
      raise OneLineError("nothing to return!")
    return _ProxyObject(self, self.last)

  @chainablemethod
  def save_last_as(self, name) -> OneLinerise:
    """Saves the value of the last thing returned with the name supplied
    
    Parameters
    ----------
    name : `str`
      Name to save the value as

    Raises
    ------
    OneLineError
      If there is no objects created yet
    """
    if self.last is _MISSING:
      raise OneLineError("nothing to save!")
    self._globals[name] = self.last

  @chainablemethod 
  def literal(self, literal: Any) -> OneLinerise:
    """Empty function for you to pass literals like `1` or `None` into
    
    Parameters
    ----------
    literal : `Any`
      The literal to be passed in
    """
    self.last = literal

  @chainablemethod
  def set_var(self, var, name="__") -> OneLinerise:
    """Sets a value of a variable. If no name is given, then '__' will be used
    
    Parameters
    ----------
    var : `Any`
      The value to be set
    name : `Optional[str]`
      Name of the variable, defaults to '__'
    """
    self._globals[name] = var