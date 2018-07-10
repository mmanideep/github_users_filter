import datetime
import pytz
from dateutil import tz

from models import SearchApiCallLog


from_zone = tz.gettz('UTC')
to_zone = tz.gettz('Asia/Kolkata')


def log_search_api_call(func, *args, **kwargs):
    def executable(*args, **kwargs):
        current_date = datetime.datetime.utcnow()
        current_date = current_date.replace(tzinfo=from_zone)
        current_tz_date = current_date.astimezone(to_zone).date()
        response = func(*args, **kwargs)
        search_api_log, created = SearchApiCallLog.objects.get_or_create(for_date=current_tz_date)
        search_api_log.count += 1
        search_api_log.save()
        return response
    return executable
