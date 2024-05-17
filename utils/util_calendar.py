import caldav
from datetime import datetime
from dateutil.relativedelta import relativedelta
import socket
import netrc
from .config import *
#from .util_logging import logger

# Das ist der Prüfungsamts-Kalender
url_prefix = "http://" + calendar_host
calendar = (url_prefix, username, password, sondertermine_lehre_calendar_url)

def remove_p_tags(text):
    text = text.replace("<p>", "")
    text = text.replace("</p>", "")
    return text

def get_caldav_calendar_events(cal, yearsinthepast=1):
    # Define the calendar
    client = caldav.DAVClient(url = cal[0], username = cal[1], password = cal[2])
    calendar = client.calendar(url = cal[3])

    # This will determine what past and future events are being displayed
    datetime_today  = datetime.combine(datetime.today(), datetime.min.time())
    datetime_start = datetime_today - relativedelta(years=yearsinthepast)

    ### Main for calendar from above
    all=[]
    try:
        events = calendar.date_search(start = datetime_start, end = None)
        for event in events:
            e = event.instance.vevent

            # set start time of event, and determine if it is allDay
            try:
                start_time = e.dtstart.value
            except:
#                logger.INFO("Es kann weder Datum noch Startzeit erkannt werden. Das Event wird übersprungen.")
                continue  # Überspringe Veranstaltungen, die weder Startdatum noch Startzeit haben.
            end = start = e.dtstart.value.strftime("%Y-%m-%d %H:%M:00")
            allDay = ("true" if e.dtstart.value.strftime("%H:%M") == "00:00" else "false")

            # determine end time of event
            try:
                end = e.dtend.value.strftime("%Y-%m-%d %H:%M:00")
            except:
                continue # Wenn kein Ende festgelegt ist und der Termin nicht ganztägig ist, ist die Dauer 0h

            # summary + location + description will give the title of the calendar entry
            try:
                summary= e.summary.value
            except:
                summary = ""
            try:
                location = e.location.value
            except:
                location = ""                    
            try:
                description = e.description.value
            except:
                description = ""

            title = summary + ((", " + location) if location != "" else "") + ((", " + description) if description != "" else "")
            title = remove_p_tags(title.replace("\n", ", "))
            # append all events for display in calendar    
            all.append({
                "start": start,
                "end": end,
                "allDay": allDay,
                "title": title
            })

    except Exception as e:
        # Log the error to a file
        error_message = f"Error accessing the calendar at {cal[3]}: {str(e)}"
        #logger.error(error_message)

    return all
