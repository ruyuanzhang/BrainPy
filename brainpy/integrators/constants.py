# -*- coding: utf-8 -*-

from brainpy.base import naming

__all__ = [
  'DT',
  'F',

  'SUPPORTED_VAR_TYPE',
  'SCALAR_VAR',
  'POP_VAR',
  'SYSTEM_VAR',

  'SUPPORTED_WIENER_TYPE',
  'SCALAR_WIENER',
  'VECTOR_WIENER',

  'SUPPORTED_INTG_TYPE',
  'ITO_SDE',
  'STRA_SDE',

  'DE_INT',
  'ODE_INT',
  'SDE_INT',
  'DDE_INT',
  'FDE_INT',
  'PDE_INT',

  'unique_name',
]


DT = 'dt'
F = 'f'
G = 'g'




# Ito SDE_INT
# ---
# The SDE_INT integral proposed by Ito in 1940s.
ITO_SDE = 'Ito'

# Stratonovich SDE_INT
# ---
# The SDE_INT integral proposed by Stratonovich in 1960s.
STRA_SDE = 'Stratonovich'

SUPPORTED_INTG_TYPE = [
  ITO_SDE,
  STRA_SDE
]

# ------------------------------------------------------

# Scalar Wiener process
# ----
#
SCALAR_WIENER = 'scalar'

# Vector Wiener process
# ----
#
VECTOR_WIENER = 'vector'

SUPPORTED_WIENER_TYPE = [
  SCALAR_WIENER,
  VECTOR_WIENER
]

# ------------------------------------------------------

# Denotes each variable is a scalar variable
# -------
# For example:
#
# def derivative(a, b, t):
#     ...
#     return da, db
#
# The "a" and "b" are scalars: a=1, b=2
#
SCALAR_VAR = 'scalar'

# Denotes each variable is a homogeneous population
# -------
# For example:
#
# def derivative(a, b, t):
#     ...
#     return da, db
#
# The "a" and "b" are vectors or matrix:
#    a = np.array([1,2]),  b = np.array([3,4])
# or,
#    a = np.array([[1,2], [2,1]]),  b=np.array([[3,4], [4,3]])
#
POP_VAR = 'population'

# Denotes each variable is a system
# ------
# For example, the above defined differential equations can be defined as:
#
# def derivative(x, t):
#     a, b = x
#     ...
#     dx = np.array([da, db])
#     return dx
SYSTEM_VAR = 'system'

SUPPORTED_VAR_TYPE = [
  SCALAR_VAR,
  POP_VAR,
  SYSTEM_VAR,
]

# ------------------------------------------------------

# Differential equation type
# --------------------------

DE_INT = 'brainpy_itg_of'
ODE_INT = 'brainpy_itg_of_ode'
SDE_INT = 'brainpy_itg_of_sde'
DDE_INT = 'brainpy_itg_of_dde'
FDE_INT = 'brainpy_itg_of_fde'
PDE_INT = 'brainpy_itg_of_pde'


def unique_name(type):
  if type == 'ode':
    return naming.get_unique_name(ODE_INT)
  elif type == 'sde':
    return naming.get_unique_name(SDE_INT)
  elif type == 'dde':
    return naming.get_unique_name(DDE_INT)
  elif type == 'fde':
    return naming.get_unique_name(FDE_INT)
  elif type == 'pde':
    return naming.get_unique_name(PDE_INT)
  else:
    raise ValueError(f'Unknown differential equation type: {type}')
