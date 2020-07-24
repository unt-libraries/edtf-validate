#!/usr/bin/env python
"""
valid_edtf.py is a python commandline tool that takes as input a date/time
string and returns either true or false determined by whether or not the
given input complies with extended date time format level 0, 1, and 2
Information about the extended date time format standard can be found here:
http://www.loc.gov/standards/datetime/pre-submission.html
"""
from __future__ import print_function

import argparse
import calendar
import datetime
import re

from pyparsing import Optional, oneOf, OneOrMore, ZeroOrMore, Empty, StringStart, StringEnd
"""
------------------------------------------------------------------------------
LEVEL 0 GRAMMAR START
------------------------------------------------------------------------------
"""
positiveDigit = oneOf("1 2 3 4 5 6 7 8 9")
digit = positiveDigit | "0"
# year definition
positive_year = (
    positiveDigit + digit + digit + digit
    | digit + positiveDigit + digit + digit
    | digit + digit + positiveDigit + digit
    | digit + digit + digit + positiveDigit
)
non_negative_year = positive_year | "0000"
# date
oneThru12 = oneOf("01 02 03 04 05 06 07 08 09 10 11 12")
oneThru13 = oneThru12 | "13"
oneThru23 = oneThru13 | oneOf("14 15 16 17 18 19 20 21 22 23")
zeroThru23 = "00" | oneThru23
oneThru29 = oneThru23 | oneOf("24 25 26 27 28 29")
oneThru30 = oneThru29 | "30"
oneThru31 = oneThru30 | "31"
oneThru59 = oneThru31 | oneOf("32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 \
    47 48 49 50 51 52 53 54 55 56 57 58 59")
zeroThru59 = "00" | oneThru59
month = oneThru12
monthDay = (
    oneOf("01 03 05 07 08 10 12") + "-" + oneThru31
    | oneOf("04 06 09 11") + "-" + oneThru30
    | "02-" + oneThru29
)
non_negative_yearMonth = non_negative_year + "-" + month
non_negative_yearMonthDay = non_negative_year + "-" + monthDay
hour = zeroThru23
minute = zeroThru59
second = zeroThru59
day = oneThru31
non_negative_date = non_negative_yearMonthDay | non_negative_yearMonth | non_negative_year
baseTime = hour + ":" + minute + ":" + second | "24:00:00"
zoneOffsetHour = oneThru13
zoneOffset = "Z" | (
    oneOf("+ -") + zoneOffsetHour + Optional(":" + minute)
    | "14:00"
    | "00:" + oneThru59
)
time = baseTime + Optional(zoneOffset)
dateAndTime = non_negative_date + "T" + time
L0Interval = non_negative_date + "/" + non_negative_date
"""
------------------------------------------------------------------------------
LEVEL 1 GRAMMAR START
------------------------------------------------------------------------------
"""
# Negative years
negative_year = "-" + positive_year
year = positive_year | negative_year | "0000"
yearMonth = year + "-" + month
yearMonthDay = year + "-" + monthDay
date = yearMonthDay | yearMonth | year
negative_date = negative_year + "-" + monthDay | negative_year + "-" + month | negative_year
negative_time = negative_date + "T" + time
# Auxiliary Assignments for Level 1
UASymbol = oneOf("? ~ %")
seasonNumber = oneOf("21 22 23 24")
season = year + "-" + seasonNumber
dateOrSeason = season | date
# uncertain Or Approximate Date
uncertainOrApproxDate = date + UASymbol
# unspecified
yearWithOneOrTwoUnspecifedDigits = Optional("-") + digit + digit + (digit | 'X') + 'X'
monthUnspecified = year + '-XX'
dayUnspecified = yearMonth + '-XX'
dayAndMonthUnspecified = year + '-XX-XX'
unspecified = (
    dayAndMonthUnspecified
    | dayUnspecified
    | monthUnspecified
    | yearWithOneOrTwoUnspecifedDigits
)
# L1Interval
L1Interval = (
    negative_date + "/" + (date)
    | (dateOrSeason + UASymbol | dateOrSeason | "..") + "/"
    + (dateOrSeason + UASymbol | ".." | season)
    | (dateOrSeason + UASymbol | ".." | season) + "/"
    + (dateOrSeason + UASymbol | dateOrSeason | "..")
    | (Empty() + "/" + (dateOrSeason + UASymbol | dateOrSeason | ".."))
    | (dateOrSeason + UASymbol | dateOrSeason | "..") + "/" + Empty()
)
# Long Year - Simple Form
longYearSimple = (
    "Y" + Optional("-")
    + positiveDigit + digit + digit + digit + OneOrMore(digit)
)
"""
------------------------------------------------------------------------------
LEVEL 2 GRAMMAR START
------------------------------------------------------------------------------
"""
# Internal Uncertain or Approximate
UAYear = (year + UASymbol | UASymbol + year)
UAYearOrYear = UAYear | year
UAMonth = (month + UASymbol | UASymbol + month)
UAMonthOrMonth = UAMonth | month
UADay = (day + UASymbol | UASymbol + day)
UADayOrDay = UADay | day

internalUncertainOrApproximate = (
    ~(StringStart() + uncertainOrApproxDate + StringEnd()) + (
        UAYear + Optional("-" + UAMonthOrMonth + "-" + UADayOrDay | "-" + UAMonthOrMonth)
        | UAYearOrYear + "-" + UAMonth + Optional("-" + UADayOrDay)
        | UAYearOrYear + "-" + UAMonthOrMonth + "-" + UADay
        | season + UASymbol
    )
)
# Internal Unspecified
positiveDigitOrX = positiveDigit | "X"
digitOrX = positiveDigitOrX | "0"
yearWithX = (
    Optional("-") + "X" + digitOrX + digitOrX + digitOrX
    | Optional("-") + digitOrX + "X" + digitOrX + digitOrX
    | Optional("-") + digitOrX + digitOrX + "X" + digitOrX
    | Optional("-") + digitOrX + digitOrX + digitOrX + "X"
)
monthWithX = "X" + digitOrX | "0X" | "1X"
oneThru3 = oneOf("1 2 3")
dayWithX = "X" + digitOrX | oneThru3 + "X" | "0X"
monthDayWithX = (
    monthWithX + "-" + dayWithX
    | month + "-" + dayWithX
    | monthWithX + "-" + day
)
yearMonthWithX = (
    yearWithX + "-" + monthWithX
    | yearWithX + "-" + month
    | year + "-" + monthWithX
)
yearmonthDayWithX = (
    yearWithX + "-" + monthDayWithX
    | yearWithX + "-" + monthDay
    | year + "-" + monthDayWithX
)
internalUnspecified = (
    ~(StringStart() + unspecified + StringEnd())
    + (yearmonthDayWithX | yearMonthWithX | yearWithX)
)
# Auxiliary Assignments for Level 2
dateWithInternalUncertainty = (
    internalUncertainOrApproximate | internalUnspecified
)
consecutives = (
    yearMonthDay + ".." + yearMonthDay
    | yearMonth + ".." + yearMonth
    | year + ".." + year
)
# Inclusive list and choice list
earlier = ".." + date
later = date + ".."
listElement = (
    dateWithInternalUncertainty.leaveWhitespace()
    | uncertainOrApproxDate.leaveWhitespace()
    | unspecified.leaveWhitespace()
    | consecutives.leaveWhitespace()
    | date.leaveWhitespace()
)
listContent = (
    earlier + "," + ZeroOrMore(listElement + ",") + later
    | ZeroOrMore(listElement + ",") + consecutives
    | ZeroOrMore(listElement + ",") + later
    | earlier + ZeroOrMore("," + listElement)
    | listElement + OneOrMore("," + listElement)
    | consecutives
)
choiceList = "[" + listContent + "]"
inclusiveList = "{" + listContent + "}"
# L2Interval
L2Interval = (
    dateWithInternalUncertainty + "/" + dateWithInternalUncertainty
    | dateOrSeason + "/" + dateWithInternalUncertainty
    | dateWithInternalUncertainty + "/" + dateOrSeason
)
# Long Year - Scientific Form
positiveInteger = positiveDigit + ZeroOrMore(digit)
longYearScientific = (
    "Y" + Optional("-") + positiveInteger + "E" + positiveInteger
)
# Significant digits
significantDigitYear = (
    (year | longYearScientific | longYearSimple)
    + ("S" + positiveInteger)
)
# Season for sub-year grouping
extendedSeasonNumber = oneOf("25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41")
extendedSeason = year + "-" + extendedSeasonNumber
"""
------------------------------------------------------------------------------
GLOBAL GRAMMAR START
------------------------------------------------------------------------------
"""
# level 0 consists of an interval, date and time or date
level0Expression = L0Interval | dateAndTime | non_negative_date.leaveWhitespace()
# level 1
level1Expression = (
    L1Interval
    | longYearSimple
    | uncertainOrApproxDate
    | unspecified
    | season
    | negative_time
    | negative_date
)
# level 2
level2Expression = (
    L2Interval
    | choiceList
    | inclusiveList
    | internalUnspecified
    | internalUncertainOrApproximate
    | extendedSeason
    | significantDigitYear
    | longYearScientific
)
# everything resolves to a 'dateTimeString'
dateTimeString = level2Expression | level1Expression | level0Expression
interval_replacements = {
    '~': '',
    '?': '',
    '%': '',
}


def replace_all(text, dic):
    """Takes a string and dictionary. replaces all occurrences of i with j"""

    for i, j in dic.items():
        text = text.replace(i, j)
    return text


# season start and end dates for use in interval checking
# erring toward inclusivity
seasons = {
    '21': {'from': '01', 'to': '05'},
    '22': {'from': '05', 'to': '08'},
    '23': {'from': '08', 'to': '11'},
    '24': {'from': '10', 'to': '12'},
}


def replace_season(season_date, marker):
    """Replace a season with a month.

    Keyword arguments:
    season_date -- edtf candidate of form year-season
    marker -- 'from' or 'to' representing earliest or latest season month
    """
    y_part, m_part = season_date.split('-')
    m_part = seasons[m_part][marker]
    return '-'.join([y_part, m_part])


X_PATTERN = re.compile(r'(-?)([\dX]{4})(-[\dX]{2})?(-[\dX]{2})?/'
                       r'(-?)([\dX]{4})(-[\dX]{2})?(-[\dX]{2})?')


def replace_X_start_month(month):
    """Find the earliest legitimate month."""
    month = month.lstrip('-')
    if month == 'XX' or month == '0X':
        return '01'
    if month == 'X0':
        return '10'
    return month.replace('X', '0')


def replace_X_end_month(month):
    """Find the latest legitimate month."""
    month = month.lstrip('-')
    if month == 'XX' or month == '1X':
        return '12'
    if month == 'X0':
        return '10'
    if month == '0X':
        return '09'
    if month[1] in ['1', '2']:
        # 'X1' or 'X2'
        return month.replace('X', '1')
    # Otherwise it should match r'X[3-9]'.
    return month.replace('X', '0')


def replace_X_start_day(day):
    """Find the earliest legitimate day."""
    day = day.lstrip('-')
    if day == 'XX' or day == '0X':
        return '01'
    if day == 'X0':
        return '10'
    return day.replace('X', '0')


def replace_X_end_day(day, year, month):
    """Find the latest legitimate day."""
    day = day.lstrip('-')
    year = int(year)
    month = int(month.lstrip('-'))
    if day == 'XX' or day == '3X':
        # Use the last day of the month for a given year/month.
        return str(calendar.monthrange(year, month)[1])
    if day == '0X' or day == '1X':
        return day.replace('X', '9')
    if day == '2X' or day == 'X9':
        if month != '02' or calendar.isleap(year):
            return '29'
        elif day == '2X':
            # It is Feburary and not a leap year.
            return '28'
        else:
            # It is February, not a leap year, day ends in 9.
            return '19'
    # 'X2' 'X3' 'X4' 'X5' 'X6' 'X7' 'X8'
    if 1 < int(day[1]) < 9:
        return day.replace('X', '2')
    # 'X0' 'X1'
    if day == 'X1':
        if calendar.monthrange(year, month)[1] == 31:
            # See if the month has a 31st.
            return '31'
        else:
            return '21'
    if day == 'X0':
        if calendar.monthrange(year, month)[1] >= 30:
            return '30'
    else:
        return '20'


def replace_X(matchobj):
    """Break the interval into parts, and replace 'X's.

    pieces - [pos/neg, start_year, start_month, start_day,
              pos/neg, end_year, end_month, end_day]
    """
    pieces = list(matchobj.groups(''))
    # Replace "X"s in start and end years.
    if 'X' in pieces[1]:
        pieces[1] = pieces[1].replace('X', '0')
    if 'X' in pieces[5]:
        pieces[5] = pieces[5].replace('X', '9')
    # Replace "X"s in start month.
    if 'X' in pieces[2]:
        pieces[2] = '-' + replace_X_start_month(pieces[2])
    # Replace "X"s in end month.
    if 'X' in pieces[6]:
        pieces[6] = '-' + replace_X_end_month(pieces[6])
    # Replace "X"s in start day.
    if 'X' in pieces[3]:
        pieces[3] = '-' + replace_X_start_day(pieces[3])
    # Replace "X"s in end day.
    if 'X' in pieces[7]:
        pieces[7] = '-' + replace_X_end_day(pieces[7], year=pieces[5],
                                            month=pieces[6])
    return ''.join((''.join(pieces[:4]), '/', ''.join(pieces[4:])))


def zero_year_special_case(from_date, to_date, start, end):
    """strptime does not resolve a 0000 year, we must handle this."""

    if start == 'pos' and end == 'pos':
        # always interval from earlier to later
        if from_date.startswith('0000') and not to_date.startswith('0000'):
            return True
        # always interval from later to earlier
        if not from_date.startswith('0000') and to_date.startswith('0000'):
            return False
        # an interval from 0000-MM-DD/0000-MM-DD ??? PARSE !!!
        if from_date.startswith('0000') and to_date.startswith('0000'):
            # fill from date assuming first subsequent date object if missing
            # missing m+d, assume jan 1
            if len(from_date) == 4:
                fm, fd = 1, 1
            # missing d, assume the 1st
            elif len(from_date) == 7:
                fm, fd = int(from_date[5:7]), 1
            # not missing any date objects
            elif len(from_date) == 10:
                fm, fd = int(from_date[5:7]), int(from_date[8:10])
            # fill to date assuming first subsequent date object if missing
            # missing m+d, assume jan 1
            if len(to_date) == 4:
                tm, td = 1, 1
            # missing d, assume the 1st
            elif len(to_date) == 7:
                tm, td = int(to_date[5:7]), 1
            # not missing any date objects
            elif len(to_date) == 10:
                tm, td = int(to_date[5:7]), int(to_date[8:10])
            # equality check
            if from_date == to_date:
                return True
            # compare the dates
            if fm <= tm:
                if fd <= td:
                    return True
                else:
                    return False
            else:
                return False
    # these cases are always one way or the other
    # "-0000" is an invalid edtf
    elif start == 'neg' and end == 'neg':
        return False
    # False unless start is not "0000"
    elif start == 'neg' and end == 'pos':
        if from_date.startswith("0000"):
            return False
        else:
            return True


def is_valid_interval(edtf_candidate):
    """Test to see if the edtf candidate is a valid interval"""

    # resolve interval into from / to datetime objects
    from_date = None
    to_date = None
    # initialize interval flags for special cases, assume positive
    end, start = 'pos', 'pos'
    if edtf_candidate.count('/') == 1:
        # replace all 'problem' cases (unspecified, 0000 date, %, -, y)
        # break the interval into two date strings
        edtf_candidate = replace_all(edtf_candidate, interval_replacements)
        edtf_candidate = re.sub(X_PATTERN, replace_X, edtf_candidate)
        parts = edtf_candidate.split('/')
        # set flag for negative start date
        if parts[0].startswith("-"):
            start = 'neg'
            parts[0] = parts[0][1:]
        # set flag for negative end date
        if parts[1].startswith("-"):
            end = 'neg'
            parts[1] = parts[1][1:]
        # if starts positive and ends negative, that's always False
        if start == 'pos' and end == 'neg':
            return False
        # handle special case of 0000 year
        if parts[0].startswith("0000") or parts[1].startswith("0000"):
            return zero_year_special_case(parts[0], parts[1], start, end)
        # 2 '-' characters means we are matching year-month-day
        if parts[0].count("-") == 2:
            from_date = datetime.datetime.strptime(parts[0], "%Y-%m-%d")
        if parts[1].count("-") == 2:
            to_date = datetime.datetime.strptime(parts[1], "%Y-%m-%d")
        # handle special case of same year season/season range due to
        # the overlap of the months we are designating for the seasons
        if parts[0].count("-") == 1 and parts[1].count("-") == 1:
            from_year, from_month = parts[0].split("-")
            to_year, to_month = parts[1].split("-")
            if from_year == to_year and from_month in seasons and to_month in seasons:
                return from_month <= to_month
        # 1 '-' character means we are match year-month
        if parts[0].count("-") == 1:
            try:
                from_date = datetime.datetime.strptime(parts[0], "%Y-%m")
            except ValueError:
                # month is a season; use earliest possible month
                replaced_season = replace_season(parts[0], 'from')
                from_date = datetime.datetime.strptime(replaced_season, "%Y-%m")
        if parts[1].count("-") == 1:
            try:
                to_date = datetime.datetime.strptime(parts[1], "%Y-%m")
            except ValueError:
                # month is a season; use latest possible month
                replaced_season = replace_season(parts[1], 'to')
                to_date = datetime.datetime.strptime(replaced_season, "%Y-%m")
        # zero '-' characters means we are matching a year
        if parts[0].count("-") == 0:
            # if from_date is unknown, we can assume the lowest possible date
            if parts[0] in [Empty(), '..']:
                from_date = datetime.datetime.strptime("0001", "%Y")
            else:
                from_date = datetime.datetime.strptime(parts[0], "%Y")
        if parts[1].count("-") == 0:
            # when the to_date is open and the from_date is valid, it's valid
            if not parts[1] in [Empty(), '..']:
                to_date = datetime.datetime.strptime(parts[1], "%Y")
        # if it starts negative and ends positive, that's always True
        if start == 'neg' and end == 'pos':
            return True
        # if start and end are negative, the from_date must be >= to_date
        elif start == 'neg' and end == 'neg':
            if from_date >= to_date and from_date and to_date:
                return True
        # if the to_date is unknown or open, it could be any date, therefore
        elif (
            parts[1] == Empty()
            or parts[1] == '..'
            or parts[0] == Empty()
            or parts[0] == '..'
        ):
            return True
        # if start and end are positive, the from_date must be <= to_date
        elif start == 'pos' and end == 'pos':
            if from_date <= to_date and from_date and to_date:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def isLevel0(edtf_candidate):
    """Checks to see if the date is level 0 valid"""

    if " " not in edtf_candidate:
        result = edtf_candidate == level0Expression
    else:
        result = False
    return result


def isLevel1(edtf_candidate):
    """Checks to see if the date is level 1 valid"""

    if " " not in edtf_candidate:
        result = edtf_candidate == level1Expression
    else:
        result = False
    return result


def isLevel2(edtf_candidate):
    """Checks to see if the date is level 2 valid"""

    if "[" in edtf_candidate or "{" in edtf_candidate:
        result = edtf_candidate == level2Expression
    elif " " in edtf_candidate:
        result = False
    else:
        result = edtf_candidate == level2Expression
    return result


def is_valid(edtf_candidate):
    """isValid takes a candidate date and returns if it is valid or not"""
    if (
        isLevel0(edtf_candidate)
        or isLevel1(edtf_candidate)
        or isLevel2(edtf_candidate)
    ):
        if '/' in edtf_candidate:
            return is_valid_interval(edtf_candidate)
        else:
            return True
    else:
        return False


def main():
    # setup the argument parser to accept the edtf candidate identifier
    parser = argparse.ArgumentParser(description='edtf compliance.')
    parser.add_argument('edtf', type=str, help='edtf candidate')
    args = parser.parse_args()
    print(args.edtf + '\t' + str(is_valid(args.edtf)))


if __name__ == '__main__':
    main()
