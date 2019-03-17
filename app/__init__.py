from flask import Blueprint
from datetime import date

api = Blueprint('api', __name__)


# Helpers for parsing the result of isoformat()
def parse_isoformat_date(dtstr):
    # It is assumed that this function will only be called with a
    # string of length exactly 10, and (though this is not used) ASCII-only
    year = int(dtstr[0:4])
    if dtstr[4] != '-':
        return date.today()
    month = int(dtstr[5:7])

    if dtstr[7] != '-':
        return date.today()
    day = int(dtstr[8:10])

    return date(year, month, day)


from app import others, auth, user, werun, rank, likes
