import csv
import datetime
import os

from app import app
from apscheduler.scheduler import Scheduler
from flask import flash, redirect, get_flashed_messages, session, \
                    url_for, request, g
from mako.lookup import TemplateLookup

PROJECT_DIR = os.path.abspath( os.path.dirname(os.path.realpath(__file__)) )

print "looking for templates in %s" % PROJECT_DIR + '/templates'
template_lookup = TemplateLookup(
    directories=[PROJECT_DIR + '/templates'], 
    module_directory='/tmp/mako_modules')

def render(templatename, **kwargs):
    mytemplate = template_lookup.get_template(templatename)
    navbar = get_navbar_template()
    active_tab = kwargs.get('active_tab', None)

    if active_tab is 0 or active_tab:
        navbar[active_tab]['active'] = True

    kwargs['navbar'] = navbar
    return mytemplate.render(
        get_flashed_messages = get_flashed_messages, **kwargs)


# -- CSV Management Functions
def get_alarm_data(day=None):
    """
    Extracts alarm data from the alarm.csv file in the static/data directory.
    Returns a list of dictionaries whose keys are the column headers.

    If optional "day" agrument is passed, function will return data for only
    the specified day
    """
    app_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    alarm_csv_path = os.path.join(app_path, 'static/data/alarm.csv')

    with open(alarm_csv_path) as csv_file:
        rows = [row for row in csv.DictReader(csv_file, delimiter=',')]

    if day:
        for row in rows:
            if row['day'].lower() == day.lower():
                return row

    return rows

def persist_alarm_data(ad=None):
    """
    Writes the alarm data out to the alarm.csv file in the static/data
    directory. If the optioanl alarm_data is passed, that is what's written.
    If omitted, the global instance of the alarm is persisted
    """
    if not ad:
        ad = get_alarm_data()

    app_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    alarm_csv_path = os.path.join(app_path, 'static/data/alarm.csv')

    with open(alarm_csv_path, 'wb') as csv_file:
        alarm_writer = csv.writer(csv_file, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        alarm_writer.writerow(ad[0].keys())
        alarm_writer.writerows([ current_day.values() for current_day in ad ])


# -- Global Variables
current_day = datetime.date.today() + datetime.timedelta(days=1)
alarm_data = get_alarm_data()
light_on = False
sched = Scheduler()
sched.start()

# -- Routes
@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    global sched
    if not sched.get_jobs():
        reschedule()

    set_current_day( datetime.date.today() + datetime.timedelta(days=1) )
    return redirect(('/' + get_current_day_name()).lower())

@app.route('/set_alarm', methods=['POST'])
def set_alarm():
    global alarm_data

    alarm_time = request.form.get('time')
    day = get_current_day_name()
    set_alarm_data(day, alarm_time)
    reschedule()

    flash("Alarm for %s set!" % day, "message")
    return redirect(('/' + day).lower())

def render_day(day):
    global alarm_data

    # Set the current day every time we get to this function to ensure that 
    # the day persists on form submission.
    set_current_day( get_date_with_day(day) )

    # Get the time the alarm is currently set to to render it
    alarm_time = get_alarm_data( day )['on']

    # Render the page
    return render( 'index.html', 
            active_tab=get_current_day().weekday(),
            day=get_current_day_name(),
            time=alarm_time )

@app.route('/monday')
def monday():
    return render_day("Monday")

@app.route('/tuesday')
def tuesday():
    return render_day("Tuesday")

@app.route('/wednesday')
def wednesday():
    return render_day("Wednesday")

@app.route('/thursday')
def thursday():
    return render_day("Thursday")

@app.route('/friday')
def friday():
    return render_day("Friday")

@app.route('/saturday')
def saturday():
    return render_day("Saturday")

@app.route('/sunday')
def sunday():
    return render_day("Sunday")


# -- Error Pages
@app.errorhandler(404)
def page_not_found(e):
    return render('404.html')

@app.errorhandler(500)
def page_error(e):
    return render('500.html')

# -- Helper Functions
def get_current_day():
    global current_day
    return current_day

def set_current_day(cd):
    global current_day
    current_day = cd

def get_current_day_name():
    global current_day
    return current_day.strftime("%A")

def get_date_with_day(target_day):
    """Given a string representing a day of the week, returns a datetime
    object representing the next occurrence of that day. If the current day is
    the same day as passed, it returns the current date.
    
    WARNING: If you don't pass this function a day of the week, it will
    loop indefinitely! """
    day = datetime.date.today() 
    while day.strftime("%A").lower() != target_day.lower():
        day = day + datetime.timedelta(days=1)

    return day

def set_alarm_data(day, time):
    """
    For a given day (string; ex: Tuesday), takes the specified time and
    persist it to the "on" field in the global alarm_data variable. 

    Sets the "off" field to be 15 minutes after the alarm turns on, because
    this is just a light and we want to conserve electricity!
    """
    global alarm_data
    hour, minute = time.split(':')
    alarm_time = datetime.datetime(2014, 1, 1, int(hour), int(minute))
    for row in alarm_data:
        if row['day'].lower() == day.lower():
            row['on'] = alarm_time.strftime("%H:%M")
            row['off'] = ( alarm_time + datetime.timedelta(minutes=15) \
                    ).strftime("%H:%M")

    persist_alarm_data(alarm_data)

def get_navbar_template():
    return [{
        'title': 'Monday',
        'url' : '/monday',
        'active' : False
    },{
        'title': 'Tuesday',
        'url' : '/tuesday',
        'active' : False
    },{
        'title': 'Wednesday',
        'url' : '/wednesday',
        'active' : False
    },{
        'title': 'Thursday',
        'url' : '/thursday',
        'active' : False
    },{
        'title': 'Friday',
        'url' : '/friday',
        'active' : False
    },{
        'title': 'Saturday',
        'url' : '/saturday',
        'active' : False
    },{
        'title': 'Sunday',
        'url' : '/sunday',
        'active' : False
    }]

# -- Scheduler and Light Functions
def reschedule():
    global sched

    # -- First, remove all current jobs
    jobs = sched.get_jobs()
    for job in jobs:
        sched.unschedule_job(job)

    # -- Then, reschedule all jobs!
    alarm_data = get_alarm_data()
    for datum in alarm_data:
        weekday = get_date_with_day(datum['day']).weekday()
        hour, minute = datum['on'].split(":")

        # -- Schedule "on" time
        sched.add_cron_job(turn_light_on,
                day_of_week= weekday,
                hour= int(hour),
                minute= int(minute) )

        # -- Schedule "off" time
        hour, minute = datum['off'].split(":")
        sched.add_cron_job(turn_light_off,
                day_of_week= weekday,
                hour= int(hour),
                minute= int(minute) )


@app.route('/on')
def turn_light_on():
    try:
        import RPi.GPIO as GPIO
        pin = 10

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, True)

    except Exception as exc:
        print "ERROR: %s" % exc
        print "Turning light on!"

    return redirect(('/' + get_current_day_name()).lower())


@app.route('/off')
def turn_light_off():
    try:
        import RPi.GPIO as GPIO
        pin = 10

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)

    except Exception as exc:
        print "ERROR: %s" % exc
        print "Turning light off!"

    return redirect(('/' + get_current_day_name()).lower())
