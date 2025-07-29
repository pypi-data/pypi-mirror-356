Analyze with IMAS-Python
========================

For this part of the training we will learn to open an IMAS database entry, and
plot some basic data in it using `matplotlib <https://matplotlib.org/>`_.


.. _`Open an IMAS database entry`:

Open an IMAS database entry
---------------------------

IMAS explicitly separates the data on disk from the data in memory. To get
started we load an existing IMAS data file from disk. The on-disk file
is represented by an :class:`imas.DBEntry <imas.db_entry.DBEntry>`, which we have to
:meth:`~imas.db_entry.DBEntry.open()` to get a reference to the data file we
will manipulate. The connection to the data file is kept intact until we
:meth:`~imas.db_entry.DBEntry.close()` the file. Note that the on-disk file
will not be changed until an explicit :meth:`~imas.db_entry.DBEntry.put()` or
:meth:`~imas.db_entry.DBEntry.put_slice()` is called.
We load data in memory with the :meth:`~imas.db_entry.DBEntry.get()` and
:meth:`~imas.db_entry.DBEntry.get_slice()` methods, after which we
can use the data.

.. hint::
    Use the ASCII data supplied with IMAS-Python for all exercises. It contains two
    IDSs (``equilibrium`` and ``core_profiles``) filled  with data from three
    time slices of ITER reference data. Two convenience methods are available in the
    :mod:`imas.training` module to open the DBEntry for this training data.

    1. :meth:`imas.training.get_training_db_entry()` returns an opened
       ``imas.DBEntry`` object. Use this method if you want to use the IMAS-Python
       interface.
    2. :meth:`imas.training.get_training_imas_db_entry()` returns an opened
       ``imas.DBEntry`` object. Use this method if you want to use the Python Access
       Layer interface.

Exercise 1
''''''''''

.. md-tab-set::

    .. md-tab-item:: Exercise

        Open the training database entry: ``entry = imas.training.get_training_db_entry()``

        1. Load the ``equilibrium`` IDS into memory using the
           :meth:`entry.get <imas.db_entry.DBEntry.get()>` method
        2. Read and print the ``time`` array of the ``equilibrium`` IDS
        3. Load the ``core_profiles`` IDS into memory
        4. Explore the ``core_profiles.profiles_1d`` property and try to match
           :math:`t\approx 433\,\mathrm{s}` to one of the slices.

           .. note::

                ``core_profiles.profiles_1d`` is time dependent with coordinate
                ``core_profiles.time`` [#tm]_. This means that
                ``core_profiles.profiles_1d[i]`` corresponds to the time
                ``core_profiles.time[i]``.

                .. [#tm] Time dependent coordinates may point to different quantities
                    depending on the time mode of the IDS
                    (``core_profiles.ids_properties.homogeneous_time``). In this case
                    the IDS uses homogeneous time, so all time coordinates use
                    ``core_profiles.time``. See also the `Data Dictionary documentation 
                    <https://imas-data-dictionary.readthedocs.io/en/latest/coordinates.html>`_.

        5. Read and print the 1D electron temperature profile (:math:`T_e`,
           ``core_profiles.profiles_1d[i].electrons.temperature``) from the
           ``core_profiles`` IDS at time slice :math:`t\approx 433\,\mathrm{s}`

    .. md-tab-item:: IMAS-Python

        .. literalinclude:: imas_snippets/read_whole_equilibrium.py

.. caution::
   When dealing with unknown data, you shouldn't blindly ``get()`` all data:
   large data files might quickly fill up the available memory of your machine.

   The recommendations for larger data files are:

   - Only load the time slice(s) that you are interested in.
   - Alternatively, IMAS-Python allows to load data on-demand, see
     :ref:`Lazy loading` for more details.


Exercise 2
''''''''''

.. md-tab-set::

    .. md-tab-item:: Exercise

        Write a function that finds the closest time slice index to
        :math:`t=433\,\mathrm{s}` inside the ``equilibrium`` IDS. Use the
        ``equilibrium.time`` property

        .. hint::
            :collapsible:

            Create an array of the differences between the ``equilibrium.time``
            array and your search term (:math:`t=433\,\mathrm{s}`).

            Now the index of the closest time slice can be found with
            :external:func:`numpy.argmin`.


    .. md-tab-item:: IMAS-Python

        .. literalinclude:: imas_snippets/read_equilibrium_time_array.py

.. attention::

    IMAS-Python objects mostly behave the same way as numpy arrays. However, in some cases
    functions explicitly expect a pure numpy array and supplying an IMAS-Python object raises
    an exception. When this is the case, the ``.value`` attribute can be used to obtain
    the underlying data.

.. note::
    IMAS-Python has two main ways of accessing IDSs. In the exercises above, we used
    the "attribute-like" access. This is the main way of navigating the IDS tree.
    However, IMAS-Python also provides a "dict-like" interface to access data, which
    might be more convenient in some cases. For example:

    .. literalinclude:: imas_snippets/iterate_core_profiles.py


Retreiving part of an IDS
-------------------------

If the data structure is too large, several problems may pop up:

- Loading the data from disk will take a long(er) time
- The IDS data may not fit in the available memory

To overcome this, we can load only part of the IDS data from disk.


Retrieve a single time slice
''''''''''''''''''''''''''''

When we are interested in quantities at a single time slice (or a low number of time
slices), we can decide to only load the data at specified times. This can be
accomplished with the aforementioned :meth:`~imas.db_entry.DBEntry.get_slice()`
method.


Exercise 3
^^^^^^^^^^

.. md-tab-set::

    .. md-tab-item:: Exercise

        Use the :meth:`~imas.db_entry.DBEntry.get_slice()` method to obtain the electron density
        :math:`n_e` at :math:`t\approx 433\,\mathrm{s}`.
        
        .. hint::
            :collapsible:

            :meth:`~imas.db_entry.DBEntry.get_slice()` requires an ``interpolation_method`` as one
            of its arguments, here you can use ``imas.ids_defs.CLOSEST_INTERP``.


    .. md-tab-item:: IMAS-Python

        .. literalinclude:: imas_snippets/read_core_profiles_ne_timeslice.py


.. attention::
    When working with multiple IDSs such as ``equilibrium`` and ``core_profiles`` the
    time arrays are not necessarily aligned. Always check this when working with random data!


Now we can plot the :math:`n_e` profile obtained above:


Exercise 4
^^^^^^^^^^

.. md-tab-set::

    .. md-tab-item:: Exercise

        Using ``matplotlib``, create a plot of :math:`n_e` on the y-axis and
        :math:`\rho_{tor, norm}` on the x-axis at :math:`t=433\mathrm{s}`

    .. md-tab-item:: IMAS-Python

        .. literalinclude:: imas_snippets/plot_core_profiles_ne_timeslice.py

    .. md-tab-item:: Plot
        
        .. figure:: core_profiles_ne_timeslice.png
            :scale: 100%
            :alt: matplotlib plot of electron temperature vs normalized toroidal flux coordinate

            A plot of :math:`n_e` vs :math:`\rho_{tor, norm}`.


Lazy loading
''''''''''''

When you are interested in the time evolution of a quantity, using ``get_slice`` may be
impractical. It gets around the limitation of the data not fitting in memory, but will
still need to read all of the data from disk (just not at once).

IMAS-Python has a `lazy loading` mode, where it will only read the requested data from disk
when you try to access it. You can enable it by supplying ``lazy=True`` to a call to 
:meth:`~imas.db_entry.DBEntry.get()` or :meth:`~imas.db_entry.DBEntry.get_slice()`.


Exercise 5
^^^^^^^^^^

.. md-tab-set::

    .. md-tab-item:: Exercise

        Using ``matplotlib``, create a plot of :math:`T_e[0]` on the y-axis and
        :math:`t` on the x-axis.

        .. note::

            Lazy loading is not very useful for the small training data. When you are on
            the ITER cluster, you can load the following data entry with much more data,
            to better notice the difference that lazy loading can make::

                import imas
                from imas.ids_defs import MDSPLUS_BACKEND
                
                database, pulse, run, user = "ITER", 134173, 106, "public"
                data_entry = imas.DBEntry(MDSPLUS_BACKEND, database, pulse, run, user)
                data_entry.open()

    .. md-tab-item:: IMAS-Python

        .. literalinclude:: imas_snippets/plot_core_profiles_te.py

    .. md-tab-item:: Plot

        .. figure:: core_profiles_te.png
            :scale: 100%
            :alt: matplotlib plot of electron temperature vs time

            A plot of :math:`T_e` vs :math:`t`.

.. seealso:: :ref:`Lazy loading`


Explore the DBEntry and occurrences
'''''''''''''''''''''''''''''''''''

You may not know a priori which types of IDSs are available within an IMAS database entry.
It can also happen that several IDSs objects of the same type are stored within
this entry, in that case each IDS is stored as a separate `occurrence`
(occurrences are identified with an integer value, 0 being the default).

In IMAS-Python, the function :meth:`~imas.db_entry.DBEntry.list_all_occurrences()` will
help you finding which occurrences are available in a given database entry and for a given
IDS type.

The following snippet shows how to list the available IDSs in a given database entry:

.. literalinclude:: imas_snippets/explore_data_entry.py
