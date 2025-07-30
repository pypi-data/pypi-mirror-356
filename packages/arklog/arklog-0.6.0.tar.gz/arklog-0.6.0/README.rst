======
arklog
======

.. image:: https://img.shields.io/pypi/v/arklog.svg
        :target: https://pypi.python.org/pypi/arklog

A python logging module with colors.

Examples
--------

.. code-block:: python3

    from arklog import ColorLogger

    logger = ColorLogger(__name__, 1)
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    logger.success("success message")
    logger.extra("extra message")
    logger.exception("exception message")


Changelog
=========

0.6.0 (2025-06-20)
------------------
* Create custom logger class instead of monkey patching.

0.5.3 (2024-12-02)
------------------
* Fix readme path for correct deployment.

0.5.2 (2024-12-02)
------------------
* Add convenience method ``set_logging``.

0.5.1 (2023-03-03)
------------------
* Fix missing import.
* Update requirements.

0.5.0 (2022-09-07)
------------------
* Add two logging methods.

0.4.1 (2020-06-22)
------------------
* Check if dev file exists.

0.4.1 (2020-06-15)
------------------
* Revert mistake removing color from console.

0.4.0 (2020-06-13)
------------------
* Add exception method.

0.3.0 (2020-06-13)
------------------
* Fix requirements generation.

0.2.0 (2020-06-03)
------------------
* Add extra method.
* Add success method.

0.1.0 (2020-06-03)
------------------
* Allow direct access to functions.

0.0.1 (2020-06-03)
------------------
* First release on PyPI.
