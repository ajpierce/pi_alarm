import datetime
import os
import pickle
import random

from app import app
from flask import flash, redirect, get_flashed_messages, request
from light_driver import LightDriver
from mako.lookup import TemplateLookup
from scheduler import Scheduler

PROJECT_DIR = os.path.abspath( os.path.dirname(os.path.realpath(__file__)) )

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


# -- Global Variables
current_day = datetime.date.today() + datetime.timedelta(days=1)

light_driver = LightDriver()
scheduler = Scheduler()

# -- Routes
@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    set_current_day( datetime.date.today() + datetime.timedelta(days=1) )
    return redirect(('/' + get_current_day_name()).lower())

@app.route('/set_alarm', methods=['POST'])
def set_alarm():
    alarm_time = request.form.get('time')
    weekday = get_current_day().weekday()
    hour, minute = alarm_time.split(":")

    scheduler.schedule_alarm(weekday, hour, minute)

    day = get_current_day_name()
    flash("Alarm for %s set!" % day, "message")
    return redirect(('/' + day).lower())

def render_day(day):
    # Set the current day every time we get to this function to ensure that
    # the day persists on form submission.
    set_current_day( get_date_with_day(day) )
    weekday = get_current_day().weekday()

    # Get the time the alarm is currently set to to render it
    alarm_time = scheduler.get_time_for_day(weekday)

    # Get the random messages from the config
    messages = app.config['MESSAGES']

    # Render the page
    return render( 'index.html',
            active_tab=get_current_day().weekday(),
            day=get_current_day_name(),
            time=alarm_time,
            message=random.choice(messages))

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

# -- Light Control Routes
@app.route('/on')
def turn_light_on():
    light_driver.on()
    return redirect(('/' + get_current_day_name()).lower())

@app.route('/off')
def turn_light_off():
    light_driver.off()
    return redirect(('/' + get_current_day_name()).lower())

@app.route('/troll')
def troll_katie():
    from time import sleep
    for i in range(5):
        turn_light_on()
        sleep(0.13)
        turn_light_off()
        sleep(0.13)
    return redirect(('/' + get_current_day_name()).lower())
