#!/usr/bin/env python
"""
valid_edtf.py is a python commandline tool that takes as input a date/time
string and returns either true or false determined by whether or not the
given input complies with extended date time format level 0, 1, and 2
Information about the extended date time format standard can be found here:
http://www.loc.gov/standards/datetime/pre-submission.html
"""
from pyparsing import Optional, oneOf, OneOrMore, ZeroOrMore, Word, alphas
import argparse
import datetime
"""
------------------------------------------------------------------------------
LEVEL 0 GRAMMAR START
------------------------------------------------------------------------------
"""
positiveDigit = oneOf("1 2 3 4 5 6 7 8 9")
digit = positiveDigit | "0"
# year definition
positive_year = (
    positiveDigit + digit + digit + digit |
    digit + positiveDigit + digit + digit |
    digit + digit + positiveDigit + digit |
    digit + digit + digit + positiveDigit
)
negative_year = "-" + positive_year
year = positive_year | negative_year | "0000"
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
    oneOf("01 03 05 07 08 10 12") + "-" + oneThru31 |
    oneOf("04 06 09 11") + "-" + oneThru30 |
    "02-" + oneThru29
)
yearMonth = year + "-" + month
yearMonthDay = year + "-" + monthDay
hour = zeroThru23
minute = zeroThru59
second = zeroThru59
day = oneThru31
date = yearMonthDay | yearMonth | year
baseTime = hour + ":" + minute + ":" + second | "24:00:00"
zoneOffsetHour = oneThru13
zoneOffset = "Z" | (
    oneOf("+ -") + zoneOffsetHour + Optional(":" + minute) |
    "14:00" |
    "00:" + oneThru59
)
time = baseTime + Optional(zoneOffset)
dateAndTime = date + "T" + time
L0Interval = date + "/" + date
"""
------------------------------------------------------------------------------
LEVEL 1 GRAMMAR START
------------------------------------------------------------------------------
"""
# Auxiliary Assignments for Level 1
UASymbol = oneOf("? ~ ?~")
seasonNumber = oneOf("21 22 23 24")
season = year + "-" + seasonNumber
dateOrSeason = date | season
# uncertain Or Approximate Date
uncertainOrApproxDate = date + UASymbol
# unspecified
yearWithOneOrTwoUnspecifedDigits = digit + digit + (digit | 'u') + 'u'
monthUnspecified = year + '-uu'
dayUnspecified = yearMonth + '-uu'
dayAndMonthUnspecified = year + '-uu-uu'
unspecified = (
    dayAndMonthUnspecified |
    dayUnspecified |
    monthUnspecified |
    yearWithOneOrTwoUnspecifedDigits
)
# L1Interval
L1Start = dateOrSeason + UASymbol | dateOrSeason | "unknown"
L1End = L1Start | "open"
L1Interval = L1Start + "/" + L1End
# Long Year - Simple Form
longYearSimple = (
    "y" + Optional("-") +
    positiveDigit + digit + digit + digit + OneOrMore(digit)
)
"""
------------------------------------------------------------------------------
LEVEL 2 GRAMMAR START
------------------------------------------------------------------------------
"""
# Internal Uncertain or Approximate
# this block of code could stand to be cleaned up a bit.
# there are some cases where we could use Optional() instead of another OR
IUABase = (
    (
        year + UASymbol + "-(" + month + ")" +
        UASymbol + "-(" + day + ")" + UASymbol
    ) |
    year + UASymbol + "-(" + month + ")" + UASymbol + Optional("-" + day) |
    year + "-(" + month + ")" + UASymbol + "-(" + day + ")" + UASymbol |
    year + "-(" + month + ")" + UASymbol + Optional("-" + day) |
    year + UASymbol + "-" + monthDay + UASymbol |
    (
        "(" + year + ")" + Optional(UASymbol) +
        "-" + monthDay + Optional(UASymbol)
    ) |
    year + UASymbol + "-" + monthDay |
    year + UASymbol + "-" + month + "-(" + day + ")" + UASymbol |
    year + UASymbol + "-(" + month + ")" + UASymbol |
    yearMonth + UASymbol + "-(" + day + ")" + UASymbol |
    yearMonth + "-(" + day + ")" + UASymbol |
    year + "-(" + monthDay + ")" + UASymbol |
    yearMonth + UASymbol + "-" + day |
    year + UASymbol + "-" + month |
    season + UASymbol
)
internalUncertainOrApproximate = IUABase | "(" + IUABase + ")" + UASymbol
# Internal Unspecified
positiveDigitOrU = positiveDigit | "u"
digitOrU = positiveDigitOrU | "0"
yearWithU = (
    "u" + digitOrU + digitOrU + digitOrU |
    digitOrU + "u" + digitOrU + digitOrU |
    digitOrU + digitOrU + "u" + digitOrU |
    digitOrU + digitOrU + digitOrU + "u"
)
monthWithU = "u" + digitOrU | "0u" | "1u"
oneThru3 = oneOf("1 2 3")
dayWithU = "u" + digitOrU | oneThru3 + "u"
monthDayWithU = (
    monthWithU + "-" + dayWithU |
    month + "-" + dayWithU |
    monthWithU + "-" + day
)
yearMonthWithU = (
    yearWithU + "-" + monthWithU |
    yearWithU + "-" + month |
    year + "-" + monthWithU
)
yearMonthDayWithU = (
    yearWithU + "-" + monthDayWithU |
    yearWithU + "-" + monthDay |
    year + "-" + monthDayWithU
)
internalUnspecified = yearMonthDayWithU | yearMonthWithU | yearWithU
# Auxiliary Assignments for Level 2
dateWithInternalUncertainty = (
    internalUncertainOrApproximate | internalUnspecified
)
consecutives = (
    yearMonthDay + ".." + yearMonthDay |
    yearMonth + ".." + yearMonth |
    year + ".." + year
)
# Inclusive list and choice list
earlier = ".." + date
later = date + ".."
listElement = (
    dateWithInternalUncertainty |
    uncertainOrApproxDate |
    unspecified |
    consecutives |
    date
)
listContent = (
    earlier + "," + Optional(" ") +
    ZeroOrMore(listElement + "," + Optional(" ")) + later |
    ZeroOrMore(listElement + "," + Optional(" ")) + consecutives |
    ZeroOrMore(listElement + "," + Optional(" ")) + later |
    earlier + ZeroOrMore("," + Optional(" ") + listElement) |
    listElement + OneOrMore("," + Optional(" ") + listElement) |
    consecutives
)
choiceList = "[" + listContent + "]"
inclusiveList = "{" + listContent + "}"
# Masked precision
maskedPrecision = digit + digit + ((digit + "x") | "xx")
# L2Interval
L2Interval = (
    dateWithInternalUncertainty + "/" + dateWithInternalUncertainty |
    dateOrSeason + "/" + dateWithInternalUncertainty |
    dateWithInternalUncertainty + "/" + dateOrSeason
)
# Long Year - Scientific Form
positiveInteger = positiveDigit + ZeroOrMore(digit)
longYearScientific = (
    "y" + Optional("-") + positiveInteger + "e" + positiveInteger +
    Optional("p" + positiveInteger)
)
# SeasonQualified
qualifyingString = Word(alphas)
seasonQualifier = qualifyingString
seasonQualified = season + "^" + seasonQualifier
"""
------------------------------------------------------------------------------
GLOBAL GRAMMAR START
------------------------------------------------------------------------------
"""
# level 0 consists of an interval, date and time or date
level0Expression = L0Interval | dateAndTime | date.leaveWhitespace()
# level 1
level1Expression = (
    L1Interval |
    longYearSimple |
    uncertainOrApproxDate |
    unspecified |
    season
)
# level 2
level2Expression = (
    L2Interval |
    longYearScientific |
    choiceList |
    inclusiveList |
    internalUncertainOrApproximate |
    internalUnspecified |
    maskedPrecision |
    seasonQualified
)
# everything resolves to a 'dateTimeString'
dateTimeString = level2Expression | level1Expression | level0Expression
interval_replacements = {
    '~': '',
    '?': '',
    'uu': '01',
}


def replace_all(text, dic):
    """Takes a string and dictionary. replaces all occurrences of i with j"""

    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text


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
        # replace all 'problem' cases (unspecified, 0000 date, ?~, -, y)
        # break the interval into two date strings
        parts = replace_all(edtf_candidate, interval_replacements).split('/')
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
        # 1 '-' character means we are match year-month
        if parts[0].count("-") == 1:
            from_date = datetime.datetime.strptime(parts[0], "%Y-%m")
        if parts[1].count("-") == 1:
            to_date = datetime.datetime.strptime(parts[1], "%Y-%m")
        # zero '-' characters means we are matching a year
        if parts[0].count("-") == 0:
            # if from_date is unknown, we can assume the lowest possible date
            if parts[0] == 'unknown':
                from_date = datetime.datetime.strptime("0001", "%Y")
            else:
                from_date = datetime.datetime.strptime(parts[0], "%Y")
        if parts[1].count("-") == 0:
            # when the to_date is open and the from_date is valid, it's valid
            if parts[1] == 'open' or parts[1] == 'unknown':
                to_date = 'open'
            else:
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
            parts[1] == 'unknown' or
            parts[1] == 'open' or
            parts[0] == 'unknown'
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
        isLevel0(edtf_candidate) or
        isLevel1(edtf_candidate) or
        isLevel2(edtf_candidate)
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
    print args.edtf + '\t' + str(is_valid(args.edtf))


if __name__ == '__main__':
    main()
