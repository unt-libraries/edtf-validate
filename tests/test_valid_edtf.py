import pytest
from itertools import chain
from edtf_validate.valid_edtf import (is_valid_interval, is_valid, isLevel0, isLevel1,
                                      isLevel2, conformsLevel0, conformsLevel1, conformsLevel2)

L0_Intervals = [
    '1964/2008',
    '2004-06/2006-08',
    '2004-02-01/2005-02-08',
    '2004-02-01/2005-02',
    '2004-02-01/2005',
    '2005/2006-02',
    '0000/0000',
    '0000-02/1111',
    '0000-01/0000-01-03',
    '0000-01-13/0000-01-23',
    '1111-01-01/1111',
    '0000-01/0000',
]

L1_Intervals = [
    '-1000/-0999',
    '-2004-02-01/2005',
    '-1980-11-01/1989-11-30',
    '1923-21/1924',
    '2019-12/2020%',
    '1984~/2004-06',
    '1984/2004-06~',
    '1984~/2004~',
    '-1984?/2004%',
    '1984?/2004-06~',
    '1984-06?/2004-08?',
    '1984-06-02?/2004-08-08~',
    '2004-06~/2004-06-11%',
    '1984-06-02?/',
    '2003/2004-06-11%',
    '1952-23~/1953',
    '-2004-06-01/',
    '1985-04-12/',
    '1985-04/',
    '1985/',
    '/1985-04-12',
    '/1985-04',
    '/1985',
    '2003-22/2004-22',
    '2003-22/2003-22',
    '2003-22/2003-23',
    '1985-04-12/..',
    '1985-04/..',
    '1985/..',
    '../1985-04-12',
    '../1985-04',
    '../1985',
    '/..',
    '../',
    '../..',
    '-1985-04-12/..',
    '-1985-04/..',
    '-1985/',
]

L2_Intervals = [
    '2004-06-~01/2004-06-~20',
    '-2004-06-?01/2006-06-~20',
    '-2005-06-%01/2006-06-~20',
    '2019-12/%2020',
    '1984?-06/2004-08?',
    '-1984-?06-02/2004-08-08~',
    '1984-?06-02/2004-06-11%',
    '2019-~12/2020',
    '2003-06-11%/2004-%06',
    '2004-06~/2004-06-%11',
    '1984?/2004~-06',
    '?2004-06~-10/2004-06-%11',
    '2004-06-XX/2004-07-03',
    '2003-06-25/2004-X1-03',
    '20X3-06-25/2004-X1-03',
    'XXXX-12-21/1890-09-2X',
    '1984-11-2X/1999-01-01',
    '1984-11-12/1984-11-XX',
    '198X-11-XX/198X-11-30',
    '2000-12-XX/2012',
    '-2000-12-XX/2012',
    '2000-XX/2012',
    '2000-XX-XX/2012',
    '2000-XX-XX/2012',
    '-2000-XX-10/2012',
    '2000/2000-XX-XX',
    '198X/199X',
    '198X/1999',
    '1987/199X',
    '1919-XX-02/1919-XX-01',
    '1919-0X-02/1919-01-03',
    '1865-X2-02/1865-03-01',
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
    '1919-07-30/1919-07-3X',
    '1908-05-02/1908-05-0X',
    '0501-11-18/0501-11-1X',
    '1112-08-22/1112-08-2X',
    '2015-02-27/2015-02-X8',
    '2016-02-28/2016-02-X9',
    '1984-06-?02/2004-06-11%',
]

Level0 = list(chain([
    '1985-04-12',
    '1985-04',
    '1985',
    '0000',
    '1985-04-12T23:20:30',
    '1985-04-12T23:20:30Z',
    '1985-04-12T23:20:30-04',
    '1985-04-12T23:20:30+04:30',
    '2004-01-01T10:10:10+00:59',
], L0_Intervals))

Level1 = list(chain([
    'Y170000002',
    'Y-170000002',
    '2001-21',
    '-2004-23',
    '-2010',
    '1984?',
    '2006%',
    '2004-06~',
    '2004-06-11%',
    '-2004~',
    '-2004-06?',
    '-2004-06-11%',
    '201X',
    '19XX',
    '2004-XX',
    '1985-04-XX',
    '1985-XX-XX',
    '-20XX',
    '-2004-XX',
    '-1985-04-XX',
    '-1985-XX-XX',
    '-1985-04-12T23:20:30',
    '-1985-04-12T23:20:30Z',
    '-1985-04-12T23:20:30-04',
    '-1985-04-12T23:20:30+04:30',
    '-2001-02-03',
], L1_Intervals))

Level2 = list(chain([
    'Y-17E7',
    'Y17E8',
    '1950S2',
    'Y171010000S3',
    'Y3388E2S3',
    '-1859S5',
    'Y-171010000S2',
    'Y-3388E2S3',
    '2001-25',
    '2001-26',
    '2001-27',
    '2001-28',
    '2001-29',
    '2001-30',
    '2001-31',
    '2001-32',
    '2001-33',
    '-2001-34',
    '-2001-35',
    '-2001-36',
    '-2001-37',
    '-2001-38',
    '-2001-39',
    '-2001-40',
    '-2001-41',
    '[-1667,1668,1670..1672]',
    '[..1760-12-03]',
    '[1760-12..]',
    '[1760-01,-1760-02,1760-12..]',
    '[-1740-02-12..-1200-01-29]',
    '[-1890-05..-1200-01]',
    '[-1667,1760-12]',
    '[..1984]',
    '{-1667,1668,1670..1672}',
    '{1960,-1961-12}',
    '{-1640-06..-1200-01}',
    '{-1740-02-12..-1200-01-29}',
    '{..1984}',
    '{1760-12..}',
    '%2001',
    '2004-?06-?11',
    '?2004-06-04~',
    '2004-%06',
    '2004?-06-~11',
    '?2004-06%',
    '2004?-%06',
    '2011-23~',
    '?-2004-06-04~',
    '-2004-%06',
    '-2004?-06-~11',
    '?-2004-06%',
    '-2004?-%06',
    '?-2004-06',
    '%-2011-06-13',
    '1560-XX-25',
    '-1X32-X1-X2',
    '156X-12-25',
    '15XX-12-25',
    'XXXX-12-XX',
    '1XXX-XX',
    '1XXX-12',
    '1984-1X',
    '20X0-10-02',
    '1X99-01-XX',
    '-156X-12-25',
    '-15XX-12-25',
    '-XXXX-12-XX',
    '-1XXX-XX',
    '-1XXX-12',
    '-1984-1X',
], L2_Intervals))

invalid_edtf_dates = [
    '1863- 03-29',
    ' 1863-03-29',
    '1863-03 -29',
    '1863-03- 29',
    '1863-03-29 ',
    '18 63-03-29',
    '1863-0 3-29',
    '1960-06-31',
    '20067890%',
    'Y2006',
    '-0000',
    'Y20067890-14-10%',
    '20067890%',
    '+2006%',
    'NONE/',
    '2000/12-12',
    '2012-10-10T1:10:10',
    '2012-10-10T10:1:10',
    '2005-07-25T10:10:10Z/2006-01-01T10:10:10Z',
    '[1 760-01, 1760-02, 1760-12..]',
    '[1667,1668, 1670..1672]',
    '[..176 0-12-03]',
    '{-1667,1668, 1670..1672}',
    '{-1667,1 668-10,1670..1672}',
    '2001-21^southernHemisphere',
    '',
]

invalid_edtf_intervals = [
    '2012/2013/1234/55BULBASAUR',
    '2012///4444',
    '2012\\2013',
    '2012-24/2012-21',
    '2012-23/2012-22',
    '0800/-0999',
    '-1000/-2000',
    '1000/-2000',
    '0001/0000',
    '0000-01-03/0000-01',
    '0000/-0001',
    '0000-02/0000',
    'Y-61000/-2000',
    '2004-06-11%/2004-%06',
    '2004-06-11%/2004-06~',
    '2005-07-25T10:10:10Z/2006-01-01T10:10:10Z',
    '2005-07-25T10:10:10Z/2006-01',
    '2005-07-25/2006-01-01T10:10:10Z',
]

invalid_edtf_datetimes = [
    '1985-04-12T23:20:30z',
    '1985-04-12t23:20:30',
    '2012-10-10T10:10:1',
    '2012-10-10T10:50:10Z15',
    '2012-10-10T10:40:10Z00:62',
    '2004-01-01T10:10:40Z25:00',
    '2004-01-01T10:10:40Z00:60',
    '2004-01-01T10:10:10-05:60',
    '2004-01-01T10:10:10+02:00:30',
    '2004-01-01T10:10:1000:59',
    '-1985-04-12T23:20:30+24',
    '-1985-04-12T23:20:30Z12:00',
]

L0_L1 = list(chain(Level0, Level1))
L0_L2 = list(chain(Level0, Level2))
L1_L2 = list(chain(Level1, Level2))
L0_L1_L2 = list(chain(Level0, Level1, Level2))


class TestIsValidInterval(object):
    @pytest.mark.parametrize('date', invalid_edtf_intervals)
    def test_interval_malformed(self, date):
        # is_valid_interval should fail if not 8601 extended interval
        assert not is_valid_interval(date)

    @pytest.mark.parametrize('date', chain(L0_Intervals, L1_Intervals, L2_Intervals))
    def test_valid_intervals(self, date):
        assert is_valid_interval(date)


class TestIsValid(object):
    @pytest.mark.parametrize('date', L0_L1_L2)
    def test_valid_edtf_all(self, date):
        assert is_valid(date)

    @pytest.mark.parametrize('date', chain(invalid_edtf_dates, invalid_edtf_datetimes,
                             invalid_edtf_intervals))
    def test_invalid_edtf_all(self, date):
        assert not is_valid(date)


class TestLevel0(object):
    @pytest.mark.parametrize('date', Level0)
    def test_valid_level_0(self, date):
        assert isLevel0(date)

    @pytest.mark.parametrize('date', L1_L2)
    def test_invalid_level_0(self, date):
        assert not isLevel0(date)


class TestLevel1(object):
    @pytest.mark.parametrize('date', Level1)
    def test_valid_level_1(self, date):
        assert isLevel1(date)

    @pytest.mark.parametrize('date', L0_L2)
    def test_invalid_level_1(self, date):
        assert not isLevel1(date)


class TestLevel2(object):
    @pytest.mark.parametrize('date', Level2)
    def test_valid_level_2(self, date):
        assert isLevel2(date)

    @pytest.mark.parametrize('date', L0_L1)
    def test_invalid_level_2(self, date):
        assert not isLevel2(date)


class TestConformsLevel0(object):
    @pytest.mark.parametrize('date', Level0)
    def test_valid_conformsLevel0(self, date):
        assert conformsLevel0(date)

    @pytest.mark.parametrize('date', L1_L2)
    def test_invalid_conformsLevel0(self, date):
        assert not conformsLevel0(date)


class TestConformsLevel1(object):
    @pytest.mark.parametrize('date', L0_L1)
    def test_valid_conformsLevel1(self, date):
        assert conformsLevel1(date)

    @pytest.mark.parametrize('date', Level2)
    def test_invalid_conformsLevel1(self, date):
        assert not conformsLevel1(date)


class TestConformsLevel2(object):
    @pytest.mark.parametrize('date', L0_L1_L2)
    def test_valid_conformsLevel2(self, date):
        assert conformsLevel2(date)

    @pytest.mark.parametrize('date', invalid_edtf_dates)
    def test_invalid_conformsLevel2(self, date):
        assert not conformsLevel2(date)
