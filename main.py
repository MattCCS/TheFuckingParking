"""
Tool for deciding where to fucking park!

For Nat <3
"""

import datetime
import pytz  # apparently very standard?

from nocache import nocache

from flask import Flask

app = Flask(__name__)


TIMEZONE = "US/Eastern"

DICT_DAYSTRING_TO_DAY = dict(zip('MTWRFSU', range(7)))  # datetime.weekday()
DICT_DAYSTRING_TO_HUMAN_DAY = {
    'M': 'Monday',
    'T': 'Tuesday',
    'W': 'Wednesday',
    'R': 'Thursday',
    'F': 'Friday',
    'S': 'Saturday',
    'U': 'Sunday',
}

META_SIDE_A = {
    'name': "side A",
    'filename': 'images/side_a.JPG',
    'banned': (
        ('T', 7, False), ('W', 6, True),
        ('R', 7, False), ('F', 6, True),
        ('S', 7, False), ('M', 6, True),
    )
}

META_SIDE_B = {
    'name': "side B",
    'filename': 'images/side_b.JPG',
    'banned': (
        ('M', 7, False), ('T', 6, True),
        ('W', 7, False), ('R', 6, True),
        ('F', 7, False), ('S', 6, True),
    )
}


def which_side():
    now = datetime.datetime.now(tz=pytz.timezone(TIMEZONE))

    # side A
    result_A = report(META_SIDE_A, now)

    # side B
    result_B = report(META_SIDE_B, now)

    return (result_A, result_B)


def report(side_meta, now):
    this_marker = (now.weekday(), now.hour, None)

    sorted_side = sorted(side_meta['banned'], key=lambda marker: difference(this_marker, marker))

    marker_from = sorted_side[0]
    marker_until = sorted_side[-1]

    ok = marker_from[2]

    return (side_meta['name'], ok, marker_until)


def difference(marker_a, marker_b):
    (day_a, hour_a, _) = marker_a
    (day_b, hour_b, _) = marker_b

    day_a = DICT_DAYSTRING_TO_DAY.get(day_a, day_a)
    day_b = DICT_DAYSTRING_TO_DAY.get(day_b, day_b)

    return ((day_a - day_b) % 7, (hour_a - hour_b) % 24)


########################################

def human_report(result):
    (side_name, ok, marker_until) = result

    human_until_day = DICT_DAYSTRING_TO_HUMAN_DAY[marker_until[0]]
    human_until_hour = "{}pm".format(marker_until[1])

    if ok:
        return "<font color=\"green\">Park on {} until {} at {}.</font>".format(side_name, human_until_day, human_until_hour)
    else:
        return "You <strong>CANNOT</strong> park on {} until {} at {}!!".format(side_name, human_until_day, human_until_hour)


def human_report_complete():
    (result_A, result_B) = which_side()

    if result_A[1]:
        good = result_A
        bad = result_B
    else:
        good = result_B
        bad = result_A

    good = human_report(good)
    bad = human_report(bad)

    return "<h1>{}</h1><br>({})".format(good, bad)


@nocache
@app.route('/')
def page_which_side():
    return human_report_complete()
