# -*- coding: utf-8 -*-

import _thread as thread
import threading

import numpy as np
from jax import lax
from jax.experimental import host_callback
from tqdm.auto import tqdm

__all__ = [
  'size2num',
  'timeout',
  'init_progress_bar',
]


def size2num(size):
  if isinstance(size, int):
    return size
  elif isinstance(size, (tuple, list)):
    a = 1
    for b in size:
      a *= b
    return a
  else:
    raise ValueError


def timeout(s):
  """Add a timeout parameter to a function and return it.

  Parameters
  ----------
  s : float
      Time limit in seconds.

  Returns
  -------
  func : callable
      Functional results. Or, raise an error of KeyboardInterrupt.
  """

  def outer(fn):
    def inner(*args, **kwargs):
      timer = threading.Timer(s, thread.interrupt_main)
      timer.start()
      try:
        result = fn(*args, **kwargs)
      finally:
        timer.cancel()
      return result

    return inner

  return outer


def init_progress_bar(duration, dt, report=0.01, message=None):
  """Setup a progress bar."""
  if message is None:
    message = f"Running a duration of {duration}"

  num_samples = int(duration / dt)
  print_rate = int(duration * report / dt)
  remainder = num_samples % print_rate

  tqdm_bars = {}

  def _define_tqdm(arg, transform):
    tqdm_bars[0] = tqdm(np.arange(0, duration, dt))
    tqdm_bars[0].set_description(message, refresh=False)

  def _update_tqdm(num_processed, transform):
    tqdm_bars[0].update(num_processed * dt)

  def _update_progress_bar(num_iter):
    _ = lax.cond(
      num_iter == 0,
      lambda _: host_callback.id_tap(_define_tqdm, None, result=num_iter),
      lambda _: num_iter,
      operand=None,
    )

    _ = lax.cond(
      # update tqdm every multiple of `print_rate` except at the end
      (num_iter % print_rate == 0) & (num_iter != num_samples - remainder),
      lambda _: host_callback.id_tap(_update_tqdm, print_rate, result=num_iter),
      lambda _: num_iter,
      operand=None,
    )

    _ = lax.cond(
      # update tqdm by `remainder`
      num_iter == num_samples - remainder,
      lambda _: host_callback.id_tap(_update_tqdm, remainder, result=num_iter),
      lambda _: num_iter,
      operand=None,
    )

  def _close_tqdm(arg, transform):
    tqdm_bars[0].close()

  def close_tqdm(iter_num):
    return lax.cond(
      iter_num == num_samples - 1,
      lambda _: host_callback.id_tap(_close_tqdm, None, result=None),
      lambda _: None,
      operand=None,
    )

  def _progress_bar(iter_num):
    _update_progress_bar(iter_num)
    close_tqdm(iter_num)

  return _progress_bar
