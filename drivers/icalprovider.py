from datetime import datetime
from icalevents import icalevents

import icalendar
import pytz
import urllib3

urllib3.disable_warnings()

class ICalProvider():
    def __init__(self):
        self.tz = pytz.timezone('Europe/Madrid')

    def get_calendar(self, url, date_start, date_end):
        #print("%s %s" % (date_start, date_end))
        returned_events = []
        try:
            events_found = icalevents.events(url=url, start=date_start, end=date_end)
            if events_found:
                for event in events_found:
                    single_event = {}
                    single_event['event_start'] = event.start.astimezone(self.tz)
                    single_event['event_end'] = event.end.astimezone(self.tz)
                    single_event['event_title'] = event.summary
                    returned_events.append(single_event)
        except Exception:
            pass

        return returned_events
