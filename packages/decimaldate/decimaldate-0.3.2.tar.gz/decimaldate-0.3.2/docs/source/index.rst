######################################################
  ``decimaldate`` Documentation
######################################################

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

.. end-badges

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Contents:

   Overview <self>
   installation
   usage
   decimaldate
   decimaldaterange
   changelog

This documentation was generated |today|.

The source for this ``decimaldate`` project is available on `GitHub <https://github.com/TorbenJakobsen/decimaldate>`_.

================
  Introduction
================

``decimaldate`` is a Python utility package to handle integer dates on the form ``yyyymmdd``.

Many times when you work with dates you encounter dates on the form ``yyyymmdd`` stored as integers.
Compared to other formats like ``ddmmyyyy``, ``mmddyyyy``, and ``mmddyy``
this format is easily comparable (by using ``ìnt``'s comparison operators ``<`` etc.) and thus sortable.

-----------
Convenience
-----------

As the base is an integer, there are no separators (e.g. ``-`` or ``/``) used.

For convenience you can use a Python feature using underscores ``_`` to improve readability
in your source code when writing ``int`` values
like: ``2024_02_28`` which is equivalent to ``20240228`` (or ``2_0_2_4_0_2_2_8``).

Using the underscore ``_`` is a convenient separator for integers with information like:
dates, phone numbers, social security numbers, and zip codes.

The documentation and source code will use ``_`` extensively to improve readability.

>>> 2024_03_12
20240312

This also works for strings when parsed as an integer:

>>> int("2024_03_12")
20240312

>>> from decimaldate import DecimalDate
>>> DecimalDate("2024_02_14")
DecimalDate(20240214)

=======
  Use
=======

--------
Creation
--------

A ``DecimalDate`` accepts:

No argument or ``None`` which both will use today's date
   >>> from decimaldate import DecimalDate
   >>> DecimalDate()
   DecimalDate(20240910)

   >>> from decimaldate import DecimalDate
   >>> DecimalDate(None)
   DecimalDate(20240910)

``int`` on the form ``yyyymmdd``
   >>> from decimaldate import DecimalDate
   >>> DecimalDate(2024_03_12)
   DecimalDate(20240312)

``str`` on the form ``yyyymmdd``
   >>> from decimaldate import DecimalDate
   >>> DecimalDate("2024_03_12")
   DecimalDate(20240312)

``datetime.date``
   >>> from decimaldate import DecimalDate
   >>> from datetime import date
   >>> DecimalDate(date.today())
   DecimalDate(20240910)

``datetime.datetime``
   >>> from decimaldate import DecimalDate
   >>> from datetime import datetime
   >>> DecimalDate(datetime.today())
   DecimalDate(20240910)

===================================
  Class Utilities and Convenience
===================================

See the :doc:`usage <./usage>` page.

======================================
  Instance Utilities and Convenience
======================================

See the :doc:`usage <./usage>` page.

===========
  Example
===========

Loop over all Tuesdays in the month of Valentine's Day 2024.

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
