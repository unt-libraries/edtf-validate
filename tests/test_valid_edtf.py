import pytest
from itertools import chain
from edtf_validate.valid_edtf import (is_valid_interval, is_valid, isLevel0, isLevel1,
                                      isLevel2, conformsLevel0, conformsLevel1, conformsLevel2)

Level0 = [
    '1985-04-12',
    '1985-04',
    '1985',
    '0000',
    '1985-04-12T23:20:30',
    '1985-04-12T23:20:30Z',
    '1985-04-12T23:20:30-04',
    '1985-04-12T23:20:30+04:30',
    '1964/2008',
    '2004-06/2006-08',
    '2004-02-01/2005-02-08',
    '2004-02-01/2005-02',
    '2004-02-01/2005',
    '2005/2006-02',
]

Level1 = [
    'Y170000002',
    'Y-170000002',
    '2001-21',
    '-2004-23',
    '-2010',
    '1984?',
    '2004-06~',
    '2004-06-11%',
    '-2004~',
    '-2004-06?',
    '-2004-06-11%',
    '201X',
    '2004-XX',
    '1985-04-XX',
    '1985-XX-XX',
    '-20XX',
    '-2004-XX',
    '-1985-04-XX',
    '-1985-XX-XX',
    '1985-04-12/',
    '1985-04/',
    '1985/',
    '/1985-04-12',
    '/1985-04',
    '/1985',
    '1985-04-12/..',
    '1985-04/..',
    '1985/..',
    '../1985-04-12',
    '../1985-04',
    '../1985',
    '-1985-04-12/',
    '-1985-04/..',
    '-1985/',
    '-1985-04-12T23:20:30',
    '-1985-04-12T23:20:30Z',
    '-1985-04-12T23:20:30-04',
    '-1985-04-12T23:20:30+04:30',
    '-1964/2008',
    '-2004-06/2006-08',
    '-2004-02-01/2005-02-08',
    '-2004-02-01/2005-02',
    '-2004-02-01/2005',
    '-2005/2006-02',
]

Level2 = [
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
    '[-1667,1760-12]',
    '[..1984]',
    '{-1667,1668,1670..1672}',
    '{1960,-1961-12}',
    '{..1984}',
    '2004-06~-11',
    '2004?-06-11',
    '?2004-06-~11',
    '2004-06-%11',
    '2004-%06-11',
    '-2004-06?-11',
    '-2004~-06-11',
    '?-2004-06-%11',
    '-2004-06-~11',
    '-2004-?06-11',
    '156X-12-25',
    '15XX-12-25',
    'XXXX-12-XX',
    '1XXX-XX',
    '1XXX-12',
    '1984-1X',
    '-156X-12-25',
    '-15XX-12-25',
    '-XXXX-12-XX',
    '-1XXX-XX',
    '-1XXX-12',
    '-1984-1X',
    '2004-06-~01/2004-06-~20',
    '2004-06-~01/2004-06-~20',
    '-2004-06-?01/2006-06-~20',
    '-2005-06-%01/2006-06-~20',
]

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
]

invalid_edtf_interval = [
    '2012/2013/1234/55BULBASAUR',
    '2012///4444',
    '2012\\2013',
    '2012-24/2012-21',
    '2012-23/2012-22',
    '0800/-0999',
    '-1000/-2000',
    '1000/-2000',
    '2012/2010',
    '2000/-2010',
    'Y-61000/-2000',
    '0001/0000',
    '0000-01-03/0000-01',
    '0000/-0001',
    '0000-02/0000',
]

invalid_edtf_datetime = [
    '1985-04-12T23:20:30z',
    '1985-04-12t23:20:30',
    '2012-10-10T10:10:1',
    '2012-10-10T1:10:10',
    '2012-10-10T10:1:10',
    '2012-10-10T10:10:10Z10',
]

L0_L1 = list(chain(Level0, Level1))
L0_L2 = list(chain(Level0, Level2))
L1_L2 = list(chain(Level1, Level2))
L0_L1_L2 = list(chain(Level0, Level1, Level2))


class TestIsValidInterval(object):
    @pytest.mark.parametrize('date', invalid_edtf_interval)
    def test_interval_malformed(self, date):
        # is_valid_interval should fail if not 8601 extended interval
        assert not is_valid_interval(date)


class TestIsValid(object):
    @pytest.mark.parametrize('date', invalid_edtf_datetime)
    def test_invalid_edtf_datetime(self, date):
        # is_valid should fail if match doesn't exist
        assert not is_valid(date)

    def test_valid_edtf_datetime(self):
        assert is_valid('2012-10-10T10:10:10Z')

    @pytest.mark.parametrize('date', L0_L1_L2)
    def test_valid_edtf_interval(self, date):
        assert is_valid(date)

    @pytest.mark.parametrize('date', invalid_edtf_interval)
    def test_invalid_edtf_interval(self, date):
        assert not is_valid(date)

    @pytest.mark.parametrize('date', invalid_edtf_dates)
    def test_invalid_edtf_date_match(self, date):
        # is_valid should fail if match doesn't exist
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
