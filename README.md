=========================
Extended Date Time Format
=========================

Valid EDTF provides validity testing against EDTF levels 1-3. You might find it most useful for tasks involving date validation and comparison. Typical usage often looks like this:

#!/usr/bin/env python

from valid_edtf import isLevel1

if isLevel1(edtf_candidate):
    print "The date, %s, is level 1 edtf validated" % edtf_candidate

EDTF specification can be viewed `here <http://www.loc.gov/standards/datetime/pre-submission.html>`_.

What exactly does Extended Date Time Format do?
===============================================

This program will:

* Determine if a string is valid edtf according to the specifications provided by the Library of Congress

* Allow the user to test each level of edtf.
  ie. '2014' is valid according to level 0 rules, but '1984?' is only valid against level 1.

Dependencies
-------------

You need these packages for edtf to work, installing via setup should take care of this for you.

1. pyparsing

2. argparse

3. datetime
