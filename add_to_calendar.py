from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from pprint import pprint
from datetime import *

from keys import CALENDAR_KEY

GMT_OFF = '+05:00'
TIMEZONE = 'Asia/Karachi'
# https://eduardopereira.pt/2012/06/google-calendar-api-v3-set-color-color-chart/
colors = ['3', '11', '7', '6', '10', '10']

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET = 'client_id.json'

store = file.Storage('storage.json')
credz = store.get()
if not credz or credz.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
    credz = tools.run_flow(flow, store)

service = build('calendar', 'v3', http=credz.authorize(Http()))

with open('courses.txt', 'r') as f:
    for i, line in enumerate(f):
        course_name, section, component, timing, location, instructors, dates = line.strip().split(',')

        begin_date, end_date = dates.split(' - ')
        begin_date = '-'.join([begin_date.split('/')[-1]] + begin_date.split('/')[:-1])
        end_date = ''.join([end_date.split('/')[-1]] + end_date.split('/')[:-1])

        days = timing.split(' ')[0].upper()
        days = ','.join([days[d:d+2] for d in range(0, len(days), 2)])

        start_time = timing.split(' ')[1]
        start_time = str(datetime.strptime(start_time, '%I:%M%p')).split(' ')[1][:-3]
        end_time = timing.split(' ')[3]
        end_time = str(datetime.strptime(end_time, '%I:%M%p')).split(' ')[1][:-3]

        event = {
        'summary': course_name, 
        'description': '{} - {}'.format(component, section), 
        'location': location, 
        'colorId': colors[i],
        'recurrence': [
            'RRULE:FREQ=WEEKLY;BYDAY={};UNTIL={}'.format(days, end_date)
            ],
        'start': {
            'dateTime': '{}T{}:00+05:00'.format(begin_date, start_time), 
            'timeZone': TIMEZONE
            }, 
        'end': {
            'dateTime': '{}T{}:00+05:00'.format(begin_date, end_time),
            'timeZone': TIMEZONE
            }, 
        }

        # pprint(event)

        event = service.events().insert(calendarId=CALENDAR_KEY, body=event).execute()
        print('Event created for "{}"'.format(course_name))
