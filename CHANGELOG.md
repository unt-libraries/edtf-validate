Change Log
==========


1.1.1
=====

* Fixed error on `is_valid` when checking an [interval with a season](https://github.com/unt-libraries/edtf-validate/issues/20).
* In README.md, updated draft EDTF specification link to fix the 404.

1.1.0
=====

* Fixed [an issue](https://github.com/unt-libraries/edtf-validate/issues/15/) where some negative dates weren't validating under level 1 or level 2.
* Modified tests to use pytest, and more specifically, [parametrization](https://github.com/unt-libraries/edtf-validate/issues/3). Makes it easier to identify what specific
  input is the cause of any failed test.
* Added continuous integration.
* Improved support for [dates with "u"](https://github.com/unt-libraries/edtf-validate/issues/5).
* Fixed an issue where [level 0 dates validated as level 1 dates](https://github.com/unt-libraries/edtf-validate/issues/6).
* Support Python versions through 3.7.

1.0.0
-----

* Initial release on both Github and PyPI.
