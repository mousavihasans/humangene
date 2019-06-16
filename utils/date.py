import re
import time
from datetime import datetime

import jdatetime
from django.conf import settings
from django.utils.timezone import is_naive
from pytz import timezone
from rest_framework import serializers
from tzlocal import get_localzone

# from varzeshgah.utils.persian import replace_persian_digits


class DateConverter(object):
    DAY_STR_TO_INT = {
        u'يکم': 1,
        u'یکم': 1,
        u'دوم': 2,
        u'سوم': 3,
        u'چهارم': 4,
        u'پنجم': 5,
        u'ششم': 6,
        u'هفتم': 7,
        u'هشتم': 8,
        u'نهم': 9,
        u'دهم': 10,
        u'یازدهم': 11,
        u'دوازدهم': 12,
        u'سیزدهم': 13,
        u'چهاردهم': 14,
        u'پانزدهم': 15,
        u'شانزدهم': 16,
        u'هفدهم': 17,
        u'هجدهم': 18,
        u'هیجدهم': 18,
        u'نوزدهم': 19,
        u'بیستم': 20,
        u'بیست و یکم': 21,
        u'بیست و دوم': 22,
        u'بیست و سوم': 23,
        u'بیست و چهارم': 24,
        u'بیست و پنجم': 25,
        u'بیست و ششم': 26,
        u'بیست و هفتم': 27,
        u'بیست و هشتم': 28,
        u'بیست و نهم': 29,
        u'سی ام': 30,
        u'سی و یکم': 31,
    }
    DAYS_STR = '|'.join(DAY_STR_TO_INT.keys())

    MONTH_STR_TO_INT = {
        u'فروردین': 1,
        u'فروردين': 1,
        u'اردیبهشت': 2,
        u'ارديبهشت': 2,
        u'خرداد': 3,
        u'تیر': 4,
        u'تير': 4,
        u'مرداد': 5,
        u'شهریور': 6,
        u'شهريور': 6,
        u'مهر': 7,
        u'آبان': 8,
        u'آذر': 9,
        u'دی': 10,
        u'بهمن': 11,
        u'اسفند': 12,
    }
    MONTHS_STR = '|'.join(MONTH_STR_TO_INT.keys())

    DAY_PARTS = {
        u'صبح': 'AM',
        u'عصر': 'PM',
    }
    PARTS_STR = '|'.join(DAY_PARTS.keys())

    @staticmethod
    def convert_to_date_array(date_str):
        """
        Given a fuzzy string containing a date (and maybe time) in Persian and Jalali calendar, returns
        """
        date = {
            'year': 0,
            'month': 0,
            'day': 0,
            'hour': 0,
            'minute': 0,
        }

        regexps = [
            #  ۰۷ مرداد ۱۳۹۴ - ۱۰:۵۸
            r'^.*?(?P<day>\d{1,2})\s(?P<month>' + DateConverter.MONTHS_STR + r')\s(?P<year>\d{4})\s(.*?)\s(?P<hour>\d{1,2}):(?P<minute>\d{1,2})',
            #شنبه،   ۰۷ مرداد ۱۳۹۴ - ۱۰:۵۸
            r'^.*\s.*?(?P<day>\d{1,2})\s(?P<month>' + DateConverter.MONTHS_STR + r')\s(?P<year>\d{4})\s(.*?)\s(?P<hour>\d{2}):(?P<minute>\d{2})',
            r'^.*?\s(?P<day>' + DateConverter.DAYS_STR + r')\s(?P<month>' + DateConverter.MONTHS_STR + r')\s(?P<year>\d{4})\s-\s(?P<hour>\d{2}):(?P<minute>\d{2})\s(?P<day_part>' + DateConverter.PARTS_STR + ')',
            r'^.*?:\s\n(.*?)(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})',
            r'^.*?(?P<day>\d{2})/(?P<month>\d{2})/(?P<year>\d{4})\s-\s(?P<hour>\d{1,2}):(?P<minute>\d{1,2})',
            r'^.*?(?P<year>\d{2,4})/(?P<month>\d{2})/(?P<day>\d{2})\s-\s(?P<hour>\d{1,2}):(?P<minute>\d{1,2})',
            r'^.*?(?P<year>\d{2,4})/(?P<month>\d{2})/(?P<day>\d{2})\s(::\s)?(?P<hour>\d{1,2}):(?P<minute>\d{1,2})(:\d{1,2})?',
            #13:45 - 1394/8/30
            r'^.*?(?P<hour>\d{1,2}):(?P<minute>\d{1,2})\s-\s(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})',

        ]

        # date_str = replace_persian_digits(date_str.strip())

        for regexp in regexps:
            result = re.match(regexp, date_str)

            if result is not None:
                result = result.groupdict()
                day_part = DateConverter.DAY_PARTS.get(result.pop('day_part', None))
                date.update(result)

                if len(date['year']) == 2:
                    date['year'] = '13' + date['year']

                # Replace string representation of day and month to integer if they are not integers already.
                date['day'] = DateConverter.DAY_STR_TO_INT.get(date['day'], date['day'])
                date['month'] = DateConverter.MONTH_STR_TO_INT.get(date['month'], date['month'])

                for element in date:
                    date[element] = int(date[element])

                if day_part == 'PM' and date['hour'] != 12:
                    date['hour'] += 12
                if day_part == 'AM' and date['hour'] == 12:
                    date['hour'] = 0
                return date

        raise Exception(u'Can not parse persian date str: `{}`'.format(date_str))

    @staticmethod
    def convert_to_gregorian(year=None, month=None, day=None, hour=None, minute=None):
        date = None
        time_pattern = "%H:%M"
        if hour and minute:
            time = "%s:%s" % (hour, minute)
        else:
            time = "05:00"

        if year and month and day:
            date = jdatetime.date(year, month, day).togregorian()
            date = "%s-%s-%s" % (date.year, date.month, date.day)

        if date is None:
            return None

        if time is not None:
            date_time = datetime.strptime(date + ' ' + time, '%Y-%m-%d ' + time_pattern)
        else:
            date_time = datetime.strptime(date, '%Y-%m-%d')

        if settings.USE_TZ:
            local_timezone = timezone(settings.TIME_ZONE)
            return local_timezone.localize(date_time)

        return date_time


def to_ms_timestamp(date_time):
    if not is_naive(date_time):
        date_time = date_time.astimezone(get_localzone())
    return int(time.mktime(date_time.timetuple()) * 1000)


class TimestampField(serializers.IntegerField):
    """
    Represents a datetime as a millisecond integer timestamp to client.
    """
    def __init__(self, **kwargs):
        # From year 1970 to 2100
        super(TimestampField, self).__init__(min_value=0, max_value=4105123200000, **kwargs)

    def to_representation(self, value):
        return to_ms_timestamp(value)

    def to_internal_value(self, data):
        int_value = super(TimestampField, self).to_internal_value(data)
        return datetime.fromtimestamp(int_value / 1000)
