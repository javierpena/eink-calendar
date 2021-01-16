from datetime import datetime

import caldav
import icalendar
import pytz
import urllib3

urllib3.disable_warnings()

class CalDavProvider():
    def __init__(self, username, password):
        self.tz = pytz.timezone('Europe/Madrid')
        self.username = username
        self.password = password

    def get_calendar(self, url, date_start, date_end):
        # print("%s %s" % (date_start, date_end))
        client = caldav.DAVClient(url=url, username=self.username, password=self.password, ssl_verify_cert=False)
        calendar = caldav.Calendar(client=client, url=url)
        returned_events = []

        events_found = calendar.date_search(
            start=date_start, end=date_end,
            compfilter='VEVENT', expand=True)
        if events_found:
            for event in events_found:
                cal = icalendar.Calendar.from_ical(event.data)
                single_event = {}
                for event in cal.walk('vevent'):
                    date_start = event.get('dtstart')
                    duration = event.get('duration')
                    summary = event.get('summary')
                single_event['event_start'] = date_start.dt.astimezone(self.tz)
                single_event['event_end'] = (date_start.dt + duration.dt).astimezone(self.tz)
                single_event['event_title'] = summary
                returned_events.append(single_event)

        return returned_events
