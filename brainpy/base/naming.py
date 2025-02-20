# -*- coding: utf-8 -*-

from brainpy import errors

import logging

logger = logging.getLogger('brainpy.base.naming')


__all__ = [
  'check_name_uniqueness',
  'get_unique_name',
  'clear_name_cache',
]

_name2id = dict()
_typed_names = {}


def check_name_uniqueness(name, obj):
  """Check the uniqueness of the name for the object type."""
  if not name.isidentifier():
    raise errors.BrainPyError(f'"{name}" isn\'t a valid identifier '
                              f'according to Python language definition. '
                              f'Please choose another name.')
  if name in _name2id:
    if _name2id[name] != id(obj):
      raise errors.UniqueNameError(f'In BrainPy, each object should have a unique name. '
                                   f'However, we detect that {obj} has a used name "{name}".')
  else:
    _name2id[name] = id(obj)


def get_unique_name(type_):
  """Get the unique name for the given object type."""
  if type_ not in _typed_names:
    _typed_names[type_] = 0
  name = f'{type_}{_typed_names[type_]}'
  _typed_names[type_] += 1
  return name


def clear_name_cache():
  """Clear the cached names."""
  _name2id.clear()
  _typed_names.clear()
  logger.warning(f'All named models and their ids are cleared.')
