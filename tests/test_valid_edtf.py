from edtf_validate.valid_edtf import (is_valid_interval, is_valid, isLevel0,
                                      isLevel1, isLevel2)


class TestIsValidInterval(object):
    def test_interval_malformed(self):
        # is_valid_interval should fail if not 8601 extended interval
        assert not is_valid_interval('2012/2011')


class TestIsValid(object):
    def test_invalid_edtf_datetime(self):
        # is_valid should fail if match doesn't exist
        assert not is_valid('2012-10-10T10:10:1')
        assert not is_valid('2012-10-10T1:10:10')
        assert not is_valid('2012-10-10T10:1:10')
        assert not is_valid('2012-10-10t10:10:10')
        assert not is_valid('2012-10-10T10:10:10Z10')

    def test_valid_edtf_datetime(self):
        assert is_valid('2012-10-10T10:10:10Z')

    def test_valid_edtf_interval(self):
        assert is_valid('-1000/-0999')
        assert is_valid('-1000/-0090-10')
        assert is_valid('-1000/2000')
        assert is_valid('1000/2000')
        assert is_valid('unknown/2000')
        assert is_valid('unknown/open')
        assert is_valid('2017-01-14/open')
        assert is_valid('0000/0000')
        assert is_valid('0000-02/1111')
        assert is_valid('0000-01/0000-01-03')
        assert is_valid('0000-01-13/0000-01-23')
        assert is_valid('1111-01-01/1111')
        assert is_valid('0000-01/0000')
        assert is_valid('2000-uu/2012')
        assert is_valid('2000-12-uu/2012')
        assert is_valid('2000-uu-10/2012')
        assert is_valid('2000-uu-uu/2012')
        assert is_valid('2000/2000-uu-uu')
        assert is_valid('198u/199u')
        assert is_valid('198u/1999')
        assert is_valid('1987/199u')
        assert is_valid('1984-11-2u/1999-01-01')
        assert is_valid('1984-11-12/1984-11-uu')
        assert is_valid('198u-11-uu/198u-11-30')
        assert is_valid('-1980-11-01/1989-11-30')
        assert is_valid('1919-uu-02/1919-uu-01')
        assert is_valid('1919-0u-02/1919-01-03')
        assert is_valid('1865-u2-02/1865-03-01')
        assert is_valid('-1981-11-10/1980-11-30')
        assert is_valid('1930-u0-10/1930-10-30')
        assert is_valid('1981-1u-10/1981-11-09')
        assert is_valid('1919-12-02/1919-uu-04')
        assert is_valid('1919-11-02/1919-1u-01')
        assert is_valid('1919-09-02/1919-u0-01')
        assert is_valid('1919-08-02/1919-0u-01')
        assert is_valid('1919-10-02/1919-u1-01')
        assert is_valid('1919-04-01/1919-u4-02')
        assert is_valid('1602-10-0u/1602-10-02')
        assert is_valid('2018-05-u0/2018-05-11')
        assert is_valid('1200-01-u4/1200-01-08')
        assert is_valid('1919-uu-02/1919-uu-01')
        assert is_valid('1919-07-30/1919-07-3u')
        assert is_valid('1908-05-02/1908-05-0u')
        assert is_valid('0501-11-18/0501-11-1u')
        assert is_valid('1112-08-22/1112-08-2u')
        assert is_valid('2015-02-27/2015-02-u8')
        assert is_valid('2016-02-28/2016-02-u9')

    def test_invalid_edtf_interval(self):
        assert not is_valid('2012/2013/1234/55BULBASAUR')
        assert not is_valid('NONE/unknown')
        assert not is_valid('2012///4444')
        assert not is_valid('2012\\2013')
        assert not is_valid('2000/12-12')
        assert not is_valid('0800/-0999')
        assert not is_valid('-1000/-2000')
        assert not is_valid('1000/-2000')
        assert not is_valid('y-61000/-2000')
        assert not is_valid('0001/0000')
        assert not is_valid('0000-01-03/0000-01')
        assert not is_valid('0000/-0001')
        assert not is_valid('0000-02/0000')

    def test_invalid_edtf_date_match(self):
        # is_valid should fail if match doesn't exist
        assert not is_valid('+20067890?~')
        assert not is_valid('y2006')
        assert not is_valid('-0000')
        assert not is_valid('+y20067890-14-10?~')
        assert not is_valid('+20067890?~')
        assert not is_valid('+2006?~')

    def test_invalid_other(self):
        # Not quite sure what to label these tests.
        # Duplicates of level 2 tests.
        assert not is_valid('1960-06-31')
        assert not is_valid('[1 760-01, 1760-02, 1760-12..]')


class TestLevel0(object):
    def test_valid_level_0(self):
        assert isLevel0('2001-02-03')
        assert isLevel0('2008-12')
        assert isLevel0('2008')
        assert isLevel0('-0999')
        assert isLevel0('-9999')
        assert isLevel0('0000')
        assert isLevel0('2001-02-03T09:30:01')
        assert isLevel0('2004-01-01T10:10:10Z')
        assert isLevel0('2012-10-10T10:10:10Z')
        assert isLevel0('2004-01-01T10:10:10+05:00')
        assert isLevel0('1964/2008')
        assert isLevel0('2004-06/2006-08')
        assert isLevel0('2004-02-01/2005-02-08')
        assert isLevel0('2004-02-01/2005-02')
        assert isLevel0('2004-02-01/2005')
        assert isLevel0('2005/2006-02')

    def test_invalid_level_0(self):
        assert not isLevel0('1863- 03-29')
        assert not isLevel0(' 1863-03-29')
        assert not isLevel0('1863-03 -29')
        assert not isLevel0('1863-03- 29')
        assert not isLevel0('1863-03-29 ')
        assert not isLevel0('18 63-03-29')
        assert not isLevel0('1863-0 3-29')


class TestLevel1(object):
    def test_valid_level_1(self):
        assert isLevel1('1984?')
        assert isLevel1('2004-06?')
        assert isLevel1('2004-06-11?')
        assert isLevel1('1984~')
        assert isLevel1('1984?~')
        assert isLevel1('199u')
        assert isLevel1('19uu')
        assert isLevel1('1999-uu')
        assert isLevel1('1999-01-uu')
        assert isLevel1('1999-uu-uu')
        assert isLevel1('unknown/2006')
        assert isLevel1('2004-06-01/unknown')
        assert isLevel1('2004-01-01/open')
        assert isLevel1('1984~/2004-06')
        assert isLevel1('1984/2004-06~')
        assert isLevel1('1984~/2004~')
        assert isLevel1('1984?/2004?~')
        assert isLevel1('1984-06?/2004-08?')
        assert isLevel1('1984-06-02?/2004-08-08~')
        assert isLevel1('1984-06-02?/unknown')
        assert isLevel1('y170000002')
        assert isLevel1('y-170000002')
        assert isLevel1('2001-21')
        assert isLevel1('2003-22')
        assert isLevel1('2000-23')
        assert isLevel1('2010-24')

    def test_invalid_level_1(self):
        assert not isLevel1('2013/2014')


class TestLevel2(object):
    def test_valid_level_2(self):
        assert isLevel2('2004?-06-11')
        assert isLevel2('2004-06~-11')
        assert isLevel2('2004-(06)?-11')
        assert isLevel2('2004-06-(11)~')
        assert isLevel2('2004-(06)?~')
        assert isLevel2('2004-(06-11)?')
        assert isLevel2('2004?-06-(11)~')
        assert isLevel2('(2004-(06)~)?')
        assert isLevel2('2004?-(06)?~')
        assert isLevel2('(2004)?-06-04~')
        assert isLevel2('(2011)-06-04~')
        assert isLevel2('2011-(06-04)~')
        assert isLevel2('2011-23~')
        assert isLevel2('156u-12-25')
        assert isLevel2('15uu-12-25')
        assert isLevel2('15uu-12-uu')
        assert isLevel2('1560-uu-25')
        assert isLevel2('[1667,1668, 1670..1672]')
        assert isLevel2('[..1760-12-03]')
        assert isLevel2('[1760-12..]')
        assert isLevel2('[1760-01, 1760-02, 1760-12..]')
        assert isLevel2('[1667, 1760-12]')
        assert isLevel2('{1667,1668, 1670..1672}')
        assert isLevel2('{1960, 1961-12}')
        assert isLevel2('196x')
        assert isLevel2('19xx')
        assert isLevel2('2004-06-(01)~/2004-06-(20)~')
        assert isLevel2('2004-06-uu/2004-07-03')
        assert isLevel2('y17e7')
        assert isLevel2('y-17e7')
        assert isLevel2('y17101e4p3')
        assert isLevel2('2001-21^southernHemisphere')

    def test_invalid_level_2(self):
        assert not isLevel2('1960-06-31')
        assert not isLevel2('[1 760-01, 1760-02, 1760-12..]')
