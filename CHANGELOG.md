Change Log
==========

x.x.x
-----
* Drop testing for now unsupported Python 2.7, 3.4, 3.5.
* Add testing for Python 3.8, 3.9.

2.0.0
=====

* Updated from draft specification to official Extended Date/Time Format (EDTF) Specification released February 2019 ([issue #22](https://github.com/unt-libraries/edtf-validate/issues/22)).
* Added `conformsLevel*` functionality ([issue #24](https://github.com/unt-libraries/edtf-validate/issues/24)).
* Added '+/-' to fix a bug in `zoneOffset` to allow datetime ahead or behind UTC ([issue #28](https://github.com/unt-libraries/edtf-validate/issues/28)).
* Fixed `ValueError` in `is_valid_interval` when invalid datetime patterns are given ([issue #27](https://github.com/unt-libraries/edtf-validate/issues/27)).

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
