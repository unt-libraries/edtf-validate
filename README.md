=========================
edtf-validate
=========================

Valid EDTF provides validity testing against [EDTF](http://www.loc.gov/standards/datetime/pre-submission.html)
levels 1-3. You might find it most useful for tasks involving date validation and comparison. Typical usage often looks like this:

Import edtf into your own programs...

    #!/usr/bin/env python
    from edtf_validate.valid_edtf import isLevel1
    if isLevel1(edtf_candidate):
        print "The date, %s, is level 1 edtf validated" % edtf_candidate

Or run it in the interpreter...
    
    >>> import edtf_validate
    >>> from edtf_validate.valid_edtf import is_valid
    >>> is_valid('1985')
    True
    >>> is_valid('Two Thousand Fourteen, The Year of Our Lord')
    False

Or just straight from the commandline...

    shabadoo@buntu:~/edtf$ edtf-validate 2015
    2015	True

NOTE
----

Please take special care to note the name difference between command-line usage and the other usage cases:

* When importing into python, use an underscore separator, e.g. `import edtf_validate`.
* When using the command-line (or when talking about the package name), use a dash separator, e.g. `$ edtf-validate`.

What exactly does edtf-validate do?
===============================================

This program will:

* Determine if a string is valid edtf according to the specifications provided by the Library of Congress
* Allow the user to test each level of edtf.
  ie. '2014' is valid according to level 0 rules, but '1984?' is only valid against level 1.

If you're confused what exactly the different levels of EDTF validation implicate, you can read about it in exhaustive detail [here](http://www.loc.gov/standards/datetime/pre-submission.html).


Installation
------------

The easiest way to install is through pip. To use pip to install edtf-validate, along with all the dependencies, use:

    $ pip install edtf-validate


Dependencies
------------

You need these packages for edtf-validate to work. Installing via setup or pip (as shown above) should take care of this for you.

1. pyparsing
2. argparse
3. datetime

License
-------

See LICENSE.txt


Acknowledgements
----------------

The edtf-validate was developed at the UNT Libraries and has been worked on by a number of developers over the years including

[Joey Liechty](https://github.com/yeahdef)

Lauren Ko  

Mark Phillips  

If you have questions about the project feel free to contact Mark Phillips at mark.phillips@unt.edu
