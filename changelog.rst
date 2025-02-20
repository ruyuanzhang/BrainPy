Release notes (brainpy)
#######################


brainpy 2.x (LTS)
*****************


Version 2.0.2 (2022.02.11)
==========================

There are important updates by `Chaoming Wang <https://github.com/chaoming0625>`_
in BrainPy 2.0.2.

- provide ``pre2post_event_prod`` operator
- support array creation from a list/tuple of JaxArray in ``brainpy.math.asarray`` and ``brainpy.math.array``
- update ``brainpy.ConstantDelay``, add ``.latest`` and ``.oldest`` attributes
- add ``brainpy.IntegratorRunner`` support for efficient simulation of brainpy integrators
- support auto finding of RandomState when JIT SDE integrators
- fix bugs in SDE ``exponential_euler`` method
- move ``parallel`` running APIs into ``brainpy.simulation``
- add ``brainpy.math.syn2post_mean``, ``brainpy.math.syn2post_softmax``,
  ``brainpy.math.pre2post_mean`` and ``brainpy.math.pre2post_softmax`` operators



Version 2.0.1 (2022.01.31)
==========================

Today we release BrainPy 2.0.1. This release is composed of over
70 commits since 2.0.0, made by `Chaoming Wang <https://github.com/chaoming0625>`_,
`Xiaoyu Chen <mailto:c-xy17@tsinghua.org.cn>`_, and
`Tianqiu Zhang <mailto:tianqiuakita@gmail.com>`_ .

BrainPy 2.0.0 updates are focused on improving documentation and operators.
Core changes include:

- Improve ``brainpylib`` operators
- Complete documentation for programming system
- Add more numpy APIs
- Add ``jaxfwd`` in autograd module
- And other changes


Version 2.0.0.1 (2022.01.05)
============================

- Add progress bar in ``brainpy.StructRunner``


Version 2.0.0 (2021.12.31)
==========================

Start a new version of BrainPy.

Highlight
~~~~~~~~~

We are excited to announce the release of BrainPy 2.0.0. This release is composed of over
260 commits since 1.1.7, made by `Chaoming Wang <https://github.com/chaoming0625>`_,
`Xiaoyu Chen <mailto:c-xy17@tsinghua.org.cn>`_, and `Tianqiu Zhang <mailto:tianqiuakita@gmail.com>`_ .

BrainPy 2.0.0 updates are focused on improving performance, usability and consistence of BrainPy.
All the computations are migrated into JAX. Model ``building``, ``simulation``, ``training``
and ``analysis`` are all based on JAX. Highlights of version 2.0.0 include:

- `brainpylib <https://pypi.org/project/brainpylib/>`_ are provided to dedicated operators for
  brain dynamics programming
- Connection APIs in ``brainpy.conn`` module are more efficient.
- Update analysis tools for low-dimensional and high-dimensional systems in ``brainpy.analysis`` module.
- Support more general Exponential Euler methods based on automatic differentiation.
- Improve the usability and consistence of ``brainpy.math`` module.
- Remove JIT compilation based on Numba.
- Separate brain building with brain simulation.


Incompatible changes
~~~~~~~~~~~~~~~~~~~~

- remove ``brainpy.math.use_backend()``
- remove ``brainpy.math.numpy`` module
- no longer support ``.run()`` in ``brainpy.DynamicalSystem`` (see New Features)
- remove ``brainpy.analysis.PhasePlane`` (see New Features)
- remove ``brainpy.analysis.Bifurcation`` (see New Features)
- remove ``brainpy.analysis.FastSlowBifurcation`` (see New Features)


New Features
~~~~~~~~~~~~

- Exponential Euler method based on automatic differentiation
    - ``brainpy.ode.ExpEulerAuto``
- Numerical optimization based low-dimensional analyzers:
    - ``brainpy.analysis.PhasePlane1D``
    - ``brainpy.analysis.PhasePlane2D``
    - ``brainpy.analysis.Bifurcation1D``
    - ``brainpy.analysis.Bifurcation2D``
    - ``brainpy.analysis.FastSlow1D``
    - ``brainpy.analysis.FastSlow2D``
- Numerical optimization based high-dimensional analyzer:
    - ``brainpy.analysis.SlowPointFinder``
- Dedicated operators in ``brainpy.math`` module:
    - ``brainpy.math.pre2post_event_sum``
    - ``brainpy.math.pre2post_sum``
    - ``brainpy.math.pre2post_prod``
    - ``brainpy.math.pre2post_max``
    - ``brainpy.math.pre2post_min``
    - ``brainpy.math.pre2syn``
    - ``brainpy.math.syn2post``
    - ``brainpy.math.syn2post_prod``
    - ``brainpy.math.syn2post_max``
    - ``brainpy.math.syn2post_min``
- Conversion APIs in ``brainpy.math`` module:
    - ``brainpy.math.as_device_array()``
    - ``brainpy.math.as_variable()``
    - ``brainpy.math.as_jaxarray()``
- New autograd APIs in ``brainpy.math`` module:
    - ``brainpy.math.vector_grad()``
- Simulation runners:
    - ``brainpy.ReportRunner``
    - ``brainpy.StructRunner``
    - ``brainpy.NumpyRunner``
- Commonly used models in ``brainpy.models`` module
    - ``brainpy.models.LIF``
    - ``brainpy.models.Izhikevich``
    - ``brainpy.models.AdExIF``
    - ``brainpy.models.SpikeTimeInput``
    - ``brainpy.models.PoissonInput``
    - ``brainpy.models.DeltaSynapse``
    - ``brainpy.models.ExpCUBA``
    - ``brainpy.models.ExpCOBA``
    - ``brainpy.models.AMPA``
    - ``brainpy.models.GABAa``
- Naming cache clean: ``brainpy.clear_name_cache``
- add safe in-place operations of ``update()`` method and ``.value``  assignment for JaxArray


Documentation
~~~~~~~~~~~~~

- Complete tutorials for quickstart
- Complete tutorials for dynamics building
- Complete tutorials for dynamics simulation
- Complete tutorials for dynamics training
- Complete tutorials for dynamics analysis
- Complete tutorials for API documentation


brainpy 1.x
*****************

1.1.x (LTS)
===========

Version 1.1.7 (2021.12.13)
--------------------------

- fix bugs on ``numpy_array()`` conversion in `brainpy.math.utils` module


Version 1.1.5 (2021.11.17)
--------------------------

**API changes:**

- fix bugs on ndarray import in `brainpy.base.function.py`
- convenient 'get_param' interface `brainpy.simulation.layers`
- add more weight initialization methods

**Doc changes:**

- add more examples in README


Version 1.1.4
-------------

**API changes:**

- add ``.struct_run()`` in DynamicalSystem
- add ``numpy_array()`` conversion in `brainpy.math.utils` module
- add ``Adagrad``, ``Adadelta``, ``RMSProp`` optimizers
- remove `setting` methods in `brainpy.math.jax` module
- remove import jax in `brainpy.__init__.py` and enable jax setting, including

  - ``enable_x64()``
  - ``set_platform()``
  - ``set_host_device_count()``
- enable ``b=None`` as no bias in `brainpy.simulation.layers`
- set `int_` and `float_` as default 32 bits
- remove ``dtype`` setting in Initializer constructor

**Doc changes:**

- add ``optimizer`` in "Math Foundation"
- add ``dynamics training`` docs
- improve others


Version 1.1.3
-------------

- fix bugs of JAX parallel API imports
- fix bugs of `post_slice` structure construction
- update docs


Version 1.1.2
-------------

- add ``pre2syn`` and ``syn2post`` operators
- add `verbose` and `check` option to ``Base.load_states()``
- fix bugs on JIT DynamicalSystem (numpy backend)


Version 1.1.1
-------------

- fix bugs on symbolic analysis: model trajectory
- change `absolute` access in the variable saving and loading to the `relative` access
- add UnexpectedTracerError hints in JAX transformation functions


Version 1.1.0 (2021.11.08)
--------------------------

This package releases a new version of BrainPy.

Highlights of core changes:

``math`` module
~~~~~~~~~~~~~~~

- support numpy backend
- support JAX backend
- support ``jit``, ``vmap`` and ``pmap`` on class objects on JAX backend
- support ``grad``, ``jacobian``, ``hessian`` on class objects on JAX backend
- support ``make_loop``, ``make_while``, and ``make_cond`` on JAX backend
- support ``jit`` (based on numba) on class objects on numpy backend
- unified numpy-like ndarray operation APIs
- numpy-like random sampling APIs
- FFT functions
- gradient descent optimizers
- activation functions
- loss function
- backend settings


``base`` module
~~~~~~~~~~~~~~~

- ``Base`` for whole Version ecosystem
- ``Function`` to wrap functions
- ``Collector`` and ``TensorCollector`` to collect variables, integrators, nodes and others


``integrators`` module
~~~~~~~~~~~~~~~~~~~~~~

- class integrators for ODE numerical methods
- class integrators for SDE numerical methods

``simulation`` module
~~~~~~~~~~~~~~~~~~~~~

- support modular and composable programming
- support multi-scale modeling
- support large-scale modeling
- support simulation on GPUs
- fix bugs on ``firing_rate()``
- remove ``_i`` in ``update()`` function, replace ``_i`` with ``_dt``,
  meaning the dynamic system has the canonic equation form
  of :math:`dx/dt = f(x, t, dt)`
- reimplement the ``input_step`` and ``monitor_step`` in a more intuitive way
- support to set `dt`  in the single object level (i.e., single instance of DynamicSystem)
- common used DNN layers
- weight initializations
- refine synaptic connections


1.0.x
=====

Version 1.0.3 (2021.08.18)
--------------------------

Fix bugs on

- firing rate measurement
- stability analysis


Version 1.0.2
-------------

This release continues to improve the user-friendliness.

Highlights of core changes:

* Remove support for Numba-CUDA backend
* Super initialization `super(XXX, self).__init__()` can be done at anywhere
  (not required to add at the bottom of the `__init__()` function).
* Add the output message of the step function running error.
* More powerful support for Monitoring
* More powerful support for running order scheduling
* Remove `unsqueeze()` and `squeeze()` operations in ``brainpy.ops``
* Add `reshape()` operation in ``brainpy.ops``
* Improve docs for numerical solvers
* Improve tests for numerical solvers
* Add keywords checking in ODE numerical solvers
* Add more unified operations in brainpy.ops
* Support "@every" in steps and monitor functions
* Fix ODE solver bugs for class bounded function
* Add build phase in Monitor


Version 1.0.1
-------------

- Fix bugs


Version 1.0.0
-------------

- **NEW VERSION OF BRAINPY**
- Change the coding style into the object-oriented programming
- Systematically improve the documentation


brainpy 0.x
***********

Version 0.3.5
=============

- Add 'timeout' in sympy solver in neuron dynamics analysis
- Reconstruct and generalize phase plane analysis
- Generalize the repeat mode of ``Network`` to different running duration between two runs
- Update benchmarks
- Update detailed documentation


Version 0.3.1
=============

- Add a more flexible way for NeuState/SynState initialization
- Fix bugs of "is_multi_return"
- Add "hand_overs", "requires" and "satisfies".
- Update documentation
- Auto-transform `range` to `numba.prange`
- Support `_obj_i`, `_pre_i`, `_post_i` for more flexible operation in scalar-based models



Version 0.3.0
=============

Computation API
~~~~~~~~~~~~~~~

- Rename "brainpy.numpy" to "brainpy.backend"
- Delete "pytorch", "tensorflow" backends
- Add "numba" requirement
- Add GPU support

Profile setting
~~~~~~~~~~~~~~~

- Delete "backend" profile setting, add "jit"

Core systems
~~~~~~~~~~~~

- Delete "autopepe8" requirement
- Delete the format code prefix
- Change keywords "_t_, _dt_, _i_" to "_t, _dt, _i"
- Change the "ST" declaration out of "requires"
- Add "repeat" mode run in Network
- Change "vector-based" to "mode" in NeuType and SynType definition

Package installation
~~~~~~~~~~~~~~~~~~~~

- Remove "pypi" installation, installation now only rely on "conda"



Version 0.2.4
=============

API changes
~~~~~~~~~~~

- Fix bugs


Version 0.2.3
=============

API changes
~~~~~~~~~~~

- Add "animate_1D" in ``visualization`` module
- Add "PoissonInput", "SpikeTimeInput" and "FreqInput" in ``inputs`` module
- Update phase_portrait_analyzer.py


Models and examples
~~~~~~~~~~~~~~~~~~~

- Add CANN examples


Version 0.2.2
=============

API changes
~~~~~~~~~~~

- Redesign visualization
- Redesign connectivity
- Update docs


Version 0.2.1
=============

API changes
~~~~~~~~~~~

- Fix bugs in `numba import`
- Fix bugs in `numpy` mode with `scalar` model


Version 0.2.0
=============

API changes
~~~~~~~~~~~

- For computation: ``numpy``, ``numba``
- For model definition: ``NeuType``, ``SynConn``
- For model running: ``Network``, ``NeuGroup``, ``SynConn``, ``Runner``
- For numerical integration: ``integrate``, ``Integrator``, ``DiffEquation``
- For connectivity: ``One2One``, ``All2All``, ``GridFour``, ``grid_four``,
  ``GridEight``, ``grid_eight``, ``GridN``, ``FixedPostNum``, ``FixedPreNum``,
  ``FixedProb``, ``GaussianProb``, ``GaussianWeight``, ``DOG``
- For visualization: ``plot_value``, ``plot_potential``, ``plot_raster``,
  ``animation_potential``
- For measurement: ``cross_correlation``, ``voltage_fluctuation``,
  ``raster_plot``, ``firing_rate``
- For inputs: ``constant_current``, ``spike_current``, ``ramp_current``.


Models and examples
~~~~~~~~~~~~~~~~~~~

- Neuron models: ``HH model``, ``LIF model``, ``Izhikevich model``
- Synapse models: ``AMPA``, ``GABA``, ``NMDA``, ``STP``, ``GapJunction``
- Network models: ``gamma oscillation``

