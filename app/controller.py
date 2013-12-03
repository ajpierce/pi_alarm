import datetime

from app import app
from flask import flash, redirect, get_flashed_messages, session, \
                    url_for, request, g
from mako.lookup import TemplateLookup

template_lookup = TemplateLookup(
    directories=['app/templates'], module_directory='/tmp/mako_modules')


def render(templatename, **kwargs):
    mytemplate = template_lookup.get_template(templatename)
    navbar = get_navbar_template()
    active_tab = kwargs.get('active_tab', None)

    if active_tab is 0 or active_tab:
        navbar[active_tab]['active'] = True

    kwargs['navbar'] = navbar
    return mytemplate.render(
        get_flashed_messages = get_flashed_messages, **kwargs)


# -- Routes
@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    day_name = tomorrow.strftime("%A")
    return redirect(('/' + day_name).lower())

@app.route('/monday')
def monday():
    return render('index.html', active_tab=0, day="Monday")

@app.route('/tuesday')
def tuesday():
    return render('index.html', active_tab=1, day="Tuesday")

@app.route('/wednesday')
def wednesday():
    return render('index.html', active_tab=2, day="Wednesday")

@app.route('/thursday')
def thursday():
    return render('index.html', active_tab=3, day="Thursday")

@app.route('/friday')
def friday():
    return render('index.html', active_tab=4, day="Friday")

@app.route('/saturday')
def saturday():
    return render('index.html', active_tab=5, day="Saturday")

@app.route('/sunday')
def sunday():
    return render('index.html', active_tab=6, day="Sunday")


# -- Error Pages
@app.errorhandler(404)
def page_not_found(e):
    return render('404.html')

@app.errorhandler(500)
def page_error(e):
    return render('500.html')

# -- Helper Functions
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
