import pytest

from edtf_validate.valid_edtf import (is_valid_interval, is_valid, isLevel0,
                                      isLevel1, isLevel2)


class TestIsValidInterval(object):
    def test_interval_malformed(self):
        # is_valid_interval should fail if not 8601 extended interval
        assert not is_valid_interval('2012/2011')


class TestIsValid(object):
    @pytest.mark.parametrize('date', [
        '2012-10-10T10:10:1',
        '2012-10-10T1:10:10',
        '2012-10-10T10:1:10',
        '2012-10-10t10:10:10',
        '2012-10-10T10:10:10Z10',
        '1960-06-31',
        '[1 760-01, 1760-02, 1760-12..]',
    ])
    def test_invalid_edtf_datetime(self, date):
        # is_valid should fail if match doesn't exist
        assert not is_valid(date)

    def test_valid_edtf_datetime(self):
        assert is_valid('2012-10-10T10:10:10Z')

    @pytest.mark.parametrize('date', [
        '-1000/-0999',
        '-1000/-0090-10',
        '-1000/2000',
        '1000/2000',
        '/2000',
        '/..',
        '../',
        '../1985-04',
        '2001-34',
        '2017-01-14/..',
        '0000/0000',
        '0000-02/1111',
        '0000-01/0000-01-03',
        '0000-01-13/0000-01-23',
        '1111-01-01/1111',
        '0000-01/0000',
        '2000-XX/2012',
        '1952-23~/1953',
        '1923-21/1924',
        '1981/1982-23',
        '1623-11/1900-11',
        '2003-22/2004-22',
        '2003-22/2003-22',
        '2003-22/2003-23',
        '2000-12-XX/2012',
        '2000-XX-10/2012',
        '-2000-XX-10/2012',
        '2000-XX-XX/2012',
        '2000/2000-XX-XX',
        '1712/2012',
        '198X/199X',
        '198X/1999',
        '1987/199X',
        '1984-11-2X/1999-01-01',
        '1984-11-12/1984-11-XX',
        '198X-11-XX/198X-11-30',
        '-1980-11-01/1989-11-30',
        '1919-XX-02/1919-XX-01',
        '1919-0X-02/1919-01-03',
        '1865-X2-02/1865-03-01',
        '-1981-11-10/1980-11-30',
        '1930-X0-10/1930-10-30',
        '1981-1X-10/1981-11-09',
        '1919-12-02/1919-XX-04',
        '1919-11-02/1919-1X-01',
        '1919-09-02/1919-X0-01',
        '1919-08-02/1919-0X-01',
        '1919-10-02/1919-X1-01',
        '1919-04-01/1919-X4-02',
        '1602-10-0X/1602-10-02',
        '2018-05-X0/2018-05-11',
        '-2018-05-X0/2018-05-11',
        '1200-01-X4/1200-01-08',
        '1919-XX-02/1919-XX-01',
        '1919-07-30/1919-07-3X',
        '1908-05-02/1908-05-0X',
        '0501-11-18/0501-11-1X',
        '1112-08-22/1112-08-2X',
        '2015-02-27/2015-02-X8',
        '2016-02-28/2016-02-X9',
    ])
    def test_valid_edtf_interval(self, date):
        assert is_valid(date)

    @pytest.mark.parametrize('date', [
        '2012/2013/1234/55BULBASAUR',
        'NONE/',
        '2012///4444',
        '2012\\2013',
        '2000/12-12',
        '2012-24/2012-21',
        '2012-23/2012-22',
        '0800/-0999',
        '-1000/-2000',
        '1000/-2000',
        'Y-61000/-2000',
        '0001/0000',
        '0000-01-03/0000-01',
        '0000/-0001',
        '0000-02/0000',
    ])
    def test_invalid_edtf_interval(self, date):
        assert not is_valid(date)

    @pytest.mark.parametrize('date', [
        '+20067890%',
        'Y2006',
        '-0000',
        '+Y20067890-14-10%',
        '+20067890%',
        '+2006%',
    ])
    def test_invalid_edtf_date_match(self, date):
        # is_valid should fail if match doesn't exist
        assert not is_valid(date)


class TestLevel0(object):
    @pytest.mark.parametrize('date', [
        '2001-02-03',
        '-2001-02-03',
        '2008-12',
        '2008',
        '-0999',
        '-9999',
        '0000',
        '2001-02-03T09:30:01',
        '2004-01-01T10:10:10Z',
        '2012-10-10T10:10:10Z',
        '-2012-10-10T10:10:10Z',
        '2004-01-01T10:10:10+05:00',
        '1964/2008',
        '2004-06/2006-08',
        '2004-02-01/2005-02-08',
        '2004-02-01/2005-02',
        '2004-02-01/2005',
        '-2004-02-01/2005',
        '2005/2006-02',
    ])
    def test_valid_level_0(self, date):
        assert isLevel0(date)

    @pytest.mark.parametrize('date', [
        '1863- 03-29',
        ' 1863-03-29',
        '1863-03 -29',
        '1863-03- 29',
        '1863-03-29 ',
        '18 63-03-29',
        '1863-0 3-29',
    ])
    def test_invalid_level_0(self, date):
        assert not isLevel0(date)


class TestLevel1(object):
    @pytest.mark.parametrize('date', [
        '1984?',
        '-1984?',
        '2004-06?',
        '2004-06-11?',
        '1984~',
        '1984%',
        '199X',
        '19XX',
        '-19XX',
        '1999-XX',
        '1999-01-XX',
        '1999-XX-XX',
        '-1999-XX-XX',
        '/2006',
        '2004-06-01/',
        '-2004-06-01/',
        '2004-01-01/..',
        '1984~/2004-06',
        '1984/2004-06~',
        '1984~/2004~',
        '1984?/2004%',
        '1984-06?/2004-08?',
        '1984-06-02?/2004-08-08~',
        '1984-06-02?/',
        'Y170000002',
        'Y-170000002',
        '2001-21',
        '2003-22',
        '-2003-22',
        '2000-23',
        '2010-24',
        '2013/2014',
    ])
    def test_valid_level_1(self, date):
        assert isLevel1(date)

    def test_invalid_level_1(self):
        assert not isLevel1('~2013/2014')


class TestLevel2(object):
    @pytest.mark.parametrize('date', [
        '2004?-06-11',
        '-2004?-06-11',
        '2004-06~-11',
        '2004-(06)?-11',
        '2004-06-(11)~',
        '-2004-06-(11)~',
        '2004-(06)%',
        '2004-(06-11)?',
        '2004?-06-(11)~',
        '(2004-(06)~)?',
        '2004?-(06)%',
        '(2004)?-06-04~',
        '(2011)-06-04~',
        '2011-(06-04)~',
        '2011-23~',
        '-2011-23~',
        '156X-12-25',
        '15XX-12-25',
        '15XX-12-XX',
        '-15XX-12-XX',
        '1560-XX-25',
        '[1667,1668, 1670..1672]',
        '[..1760-12-03]',
        '[1760-12..]',
        '[1760-01, 1760-02, 1760-12..]',
        '[-1760-01, 1760-02, 1760-12..]',
        '[1667, 1760-12]',
        '{1667,1668, 1670..1672}',
        '{1960, 1961-12}',
        '2004-06-(01)~/2004-06-(20)~',
        '2004-06-XX/2004-07-03',
        'Y17E7',
        'Y-17E7',
        'Y17101E4S3',
        '1950S2',
        'Y171010000S3',
        '2001-21^southernHemisphere',
    ])
    def test_valid_level_2(self, date):
        assert isLevel2(date)

    @pytest.mark.parametrize('date', [
        '1960-06-31',
        '[1 760-01, 1760-02, 1760-12..]',
        '196x',
        '19xx',
        '-19xx',
    ])
    def test_invalid_level_2(self, date):
        assert not isLevel2(date)
