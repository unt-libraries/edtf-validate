edtf-validate
=========================
[![PyPI](https://img.shields.io/pypi/v/edtf-validate.svg)](https://pypi.python.org/pypi/edtf-validate)
[![Build Status](https://travis-ci.org/unt-libraries/edtf-validate.svg?branch=master)](https://travis-ci.org/unt-libraries/edtf-validate)

Valid EDTF provides validity testing against levels 0-2 of the [draft EDTF specification](https://www.loc.gov/standards/datetime/pre-submission.html).
Please note that the draft specification is quite different from the [current specification](https://www.loc.gov/standards/datetime/edtf.html),
which uses different syntax than what is validated here.
You might find it most useful for tasks involving date validation and comparison. Typical usage often looks like this:

```python
>>> from edtf_validate.valid_edtf import is_valid, isLevel2
>>> is_valid('2015-03-05')
True
>>> is_valid('Jan 12, 1990')
False
>>> isLevel2('1998?-12-23')
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

* Determine if a string is valid edtf according to the specifications provided by the Library of Congress.
* Allow the user to test each level of edtf.  
  ie. '2014' is valid according to level 0 rules, but '1984?' is only valid against level 1.

If you're confused what exactly the different levels of EDTF validation implicate, you can read about it in exhaustive detail [here](http://www.loc.gov/standards/datetime/pre-submission.html).


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

If you have questions about the project feel free to contact Mark Phillips at mark.phillips@unt.edu.
