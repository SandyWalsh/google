import datetime
import gdata.calendar.service
import sys

username = None
password = None

try:
    from local_settings import *
except ImportError:
    print "Must define username and password in local_settings.py"
    sys.exit(1)

print "Attempting login of", username

client = gdata.calendar.service.CalendarService()
client.email = username
client.password = password
client.source = 'FamilyCalendar-1.0'
client.ProgrammaticLogin()

def PrintAllEventsOnCalendar(_client, family):
    start_date = datetime.datetime.utcnow().date()
    end_date = start_date + datetime.timedelta(days=7)

    query = gdata.calendar.service.CalendarEventQuery('default', 'all', 'full')
    query.start_min = str(start_date)
    query.start_max = str(end_date)
    query.__dict__['feed'] = family
    feed = _client.CalendarQuery(query)

    print 'Events on Family Calendar: %s' % (feed.title.text,)
    final = []
    for i, an_event in enumerate(feed.entry):
        #print '\t%s. %s' % (i, an_event.title.text,)
        for j, a_when in enumerate(an_event.when):
            #print "\t\t%s. %s" % (j, a_when.start_time)
            final.append((a_when.start_time, i, an_event.title.text))

    final = sorted(final)
    for when, index, title in final:
        print "%s. %s @ %s" % (index, title, when)


family = None
feed = client.GetAllCalendarsFeed()
print feed.title.text
for i, a_calendar in enumerate(feed.entry):
    print '\t%s. %s' % (i, a_calendar.title.text,)
    if a_calendar.title.text == 'Family':
        family = a_calendar.link[0].href

PrintAllEventsOnCalendar(client, family)
