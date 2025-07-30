.. _readthedocs: https://decimaldate.readthedocs.io/en/latest/ 
.. _PyPI: https://pypi.org/

A Python class to handle decimal dates on the form ``yyyymmdd``.

.. start-badges

.. list-table::
    :stub-columns: 1

    * - general
      - |license|
    * - docs
      - |docs|
    * - code
      - | |code-style| |commits-since| |github-test-multiple| 
        | |scrutinizer-code-quality| |scrutinizer-coverage| |scrutinizer-build| 
        | |ossf| 
    * - package
      - |wheel| |supported-versions| |supported-implementations|
    * - downloads
      - |downloads-total| |downloads-monthly| |downloads-weekly|

.. |docs| image:: https://readthedocs.org/projects/decimaldate/badge/?version=latest
   :alt: Documentation Status
   :target: https://decimaldate.readthedocs.io/en/latest/?badge=latest

.. |code-style| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :alt: Using black formatter
   :target: https://github.com/psf/black

.. |commits-since| image:: https://img.shields.io/github/commits-since/TorbenJakobsen/decimaldate/v0.3.1.svg
   :alt: Commits since latest release
   :target: https://github.com/TorbenJakobsen/decimaldate/compare/v0.3.1...main

.. |license| image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
   :alt: BSD 3 Clause
   :target: https://opensource.org/licenses/BSD-3-Clause

.. |wheel| image:: https://img.shields.io/pypi/wheel/decimaldate.svg
   :alt: PyPI Wheel
   :target: https://pypi.org/project/decimaldate

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/decimaldate.svg
   :alt: Supported versions
   :target: https://pypi.org/project/decimaldate

.. |downloads-total| image:: https://static.pepy.tech/badge/decimaldate
   :alt: Total downloads counter
   :target: https://pepy.tech/project/decimaldate

.. |downloads-monthly| image:: https://static.pepy.tech/badge/decimaldate/month
   :alt: Weekly downloads counter
   :target: https://pepy.tech/project/decimaldate

.. |downloads-weekly| image:: https://static.pepy.tech/badge/decimaldate/week
   :alt: Weekly downloads counter
   :target: https://pepy.tech/project/decimaldate

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/decimaldate.svg
   :alt: Supported implementations
   :target: https://pypi.org/project/decimaldate

.. |scrutinizer-code-quality| image:: https://scrutinizer-ci.com/g/TorbenJakobsen/decimaldate/badges/quality-score.png?b=main
   :alt: Scrutinizer code quality
   :target: https://scrutinizer-ci.com/g/TorbenJakobsen/decimaldate/?branch=main

.. |scrutinizer-coverage| image:: https://scrutinizer-ci.com/g/TorbenJakobsen/decimaldate/badges/coverage.png?b=main
   :alt: Scrutinizer coverage
   :target: https://scrutinizer-ci.com/g/TorbenJakobsen/decimaldate/?branch=main

.. |scrutinizer-build| image:: https://scrutinizer-ci.com/g/TorbenJakobsen/decimaldate/badges/build.png?b=main
   :alt: Scrutinizer build
   :target: https://scrutinizer-ci.com/g/TorbenJakobsen/decimaldate/?branch=main

.. |github-test-multiple| image:: https://github.com/TorbenJakobsen/decimaldate/actions/workflows/action.yaml/badge.svg
   :alt: Test multiple Python versions
   :target: https://github.com/TorbenJakobsen/decimaldate/actions/workflows/action.yaml

.. |ossf| image:: https://api.scorecard.dev/projects/github.com/TorbenJakobsen/decimaldate/badge
   :alt: OpenSSF
   :target: https://scorecard.dev/viewer/?uri=github.com/TorbenJakobsen/decimaldate

.. end-badges

=========
  About
=========

Python decimal date utility to handle integer dates on the form ``yyyymmdd``.

=================
  Main Features
=================

Simplifies handling of decimal dates, here being integers on the form :code:`yyyymmdd`.

See documentation hosted on readthedocs_.

As an example loop over all Tuesdays in the month of Valentine's Day 2024.

>>> from decimaldate import DecimalDateRange
>>> 
>>> TUESDAY = 1
>>> 
>>> for dd in [
>>>     dd
>>>     for dd in DecimalDateRange.range_month_of_decimal_date(20240214)
>>>     if dd.weekday() == TUESDAY
>>> ]:
>>>     print(repr(dd))
DecimalDate(20240206)
DecimalDate(20240213)
DecimalDate(20240220)
DecimalDate(20240227)

===================
  Where to get it
===================

The source code is hosted at `GitHub <https://github.com/TorbenJakobsen/decimaldate>`_.

An installer for the latest released version is available at PyPI_.

.. code:: bash

    python3 -m pip install decimaldate

================
  Dependencies
================

Python >=3.11

There are no other dependencies for deployment.

=================
  Documentation
=================

Documentation is hosted on readthedocs_.
