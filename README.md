edtf-validate
=========================
[![PyPI](https://img.shields.io/pypi/v/edtf-validate.svg)](https://pypi.python.org/pypi/edtf-validate)
[![Build Status](https://github.com/unt-libraries/edtf-validate/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/unt-libraries/edtf-validate/actions)

Valid EDTF provides validity testing against levels 0-2 of the official [EDTF Specification](https://www.loc.gov/standards/datetime/edtf.html) released February 2019.
You might find it most useful for tasks involving date validation and comparison. Typical usage often looks like this:

```python
>>> from edtf_validate.valid_edtf import is_valid, isLevel2
>>> is_valid('2015-03-05')
True
>>> is_valid('Jan 12, 1990')
False
>>> isLevel2('1998?-12-23')
True
>>> conformsLevel1('-1980-11-01/1989-11-30')
True
```

Or just straight from the command line...

```console
$ edtf-validate 2015
2015	True
```

NOTE
----

Please take special care to note the name difference between command line usage and the other usage cases:

* When importing into python, use an underscore separator, e.g. `import edtf_validate`.
* When using the command line (or when talking about the package name), use a dash separator, e.g. `$ edtf-validate`.

What exactly does edtf-validate do?
===============================================

This program will:

* Determine if a string is valid EDTF according to the specifications provided by the Library of Congress.
* Allow the user to test if a date is a feature of each level of EDTF using `isLevel*` functions.
  i.e. '1964/2008' is a feature introduced in Level 0 rules, and '1964~/2008~' is a feature introduced in Level1.
* Allow the user to test if a date is valid for each level of EDTF using `conformsLevel*` functions.
  i.e. '2014' is a feature introduced in Level 0 and valid for it, but also valid in Level 1 and Level 2 as all EDTF levels validate dates of itself and levels below it.
  Another example, '2001-25' is a feature introduced in Level 2 hence valid for Level 2, but it is not a valid date in Level 0 and Level 1.

If you're confused what exactly the different levels of EDTF validation implicate, you can read about it in exhaustive detail [here](https://www.loc.gov/standards/datetime).


Installation
------------

The easiest way to install is through pip. To use pip to install edtf-validate, along with all the dependencies, use:

```console
$ pip install edtf-validate
```


License
-------

See LICENSE.txt


Acknowledgements
----------------

The edtf-validate was developed at the UNT Libraries and has been worked on by a number of developers over the years including:

[Joey Liechty](https://github.com/yeahdef)

[Lauren Ko](https://github.com/ldko) 

[Mark Phillips](https://github.com/vphill)

[Gio Gottardi](https://github.com/somexpert)

[Madhulika Bayyavarapu](https://github.com/madhulika95b)
If you have questions about the project feel free to contact Mark Phillips at mark.phillips@unt.edu.
