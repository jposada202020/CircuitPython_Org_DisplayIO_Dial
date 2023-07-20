Introduction
============


.. image:: https://readthedocs.org/projects/circuitpython-displayio_dial/badge/?version=latest
    :target: https://circuitpython-simple-dial.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/jposada202020/CircuitPython_simple_dial/workflows/Build%20CI/badge.svg
    :target: https://github.com/jposada202020/CircuitPython_simple_dial/actions/
    :alt: Build Status

.. image:: https://img.shields.io/pypi/v/circuitpython-simnple-dial.svg
    :alt: latest version on PyPI
    :target: https://pypi.python.org/pypi/circuitpython-simnple-dial

.. image:: https://static.pepy.tech/personalized-badge/circuitpython-simnple-dial?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Pypi%20Downloads
    :alt: Total PyPI downloads
    :target: https://pepy.tech/project/circuitpython-simnple-dial


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

A dial gauge widget for displaying graphical information. Derived from Dial made by Kevin Matocha. Main Differences:
    * Dial is a complete circle
    * Needle is a line. This line could be full or half
    * Needle size could be shortened using the pad option
    * Can have more than one needle.
    * Minor ticks can have their own labels



.. image:: https://github.com/jposada202020/CircuitPython_simple_dial/blob/main/docs/dial.png

.. image:: https://github.com/jposada202020/CircuitPython_simple_dial/blob/main/docs/watch.jpg

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install simple_dial

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

See scripts in the examples directory of this repository.
