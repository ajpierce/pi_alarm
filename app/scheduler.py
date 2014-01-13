import datetime
import pickle
from app import app
from apscheduler.scheduler import Scheduler as ApScheduler
from light_driver import LightDriver


class Scheduler(object):
    """
    A class containing methods for scheduling the alarm.
    Operates both the scheduler and persisting the data
    """
    def __init__(self):
        self.scheduler = ApScheduler()
        self.scheduler.start()
        self.light_driver = LightDriver()

    def start(self):
        self.reschedule()
        return self.scheduler.start()

    def get_jobs(self):
        return self.scheduler.get_jobs()

    def unschedule_jobs(self):
        for job in self.scheduler.get_jobs():
            self.scheduler.unschedule_job(job)

    def unscheldue_job(self, job):
        return self.schedule.unschedule_job(job)

    def schedule_alarm(self, weekday, hour, minute):
        """
        Weekday: Integer from 0 to 6
            + 0 is sunday
            + 1 is monday
            + ...
            + 6 is saturday
        
        Hour: Integer from 0 to 23
            + 0 is midnight
            + 13 is 1:00 PM

        Minute: Integer from 0 to 59
        """

        # -- First, unschedule the alarm for that day
        for job in self.scheduler.get_jobs():
            # Field at index 4 is the day of the week integer
            if job.trigger.fields[4] == weekday:
                self.scheduler.unschedule_job(job)

        # -- Second, persist the new time to the hard drive
        alarm_time = datetime.datetime(2014, 1, 1, int(hour), int(minute))
        duration = app.config['ALARM_DURATION']
        on = alarm_time.strftime("%H:%M")
        off = (alarm_time + datetime.timedelta(minutes=int(duration))).strftime("%H:%M")
        off_hour, off_minute = off.split(":")

        alarm_data = pickle.load( open( app.config['ALARM_DATA'], "rb" ) )
        alarm_data[weekday] = { 'on': on, 'off': off, 'enabled': True }
        pickle.dump(alarm_data, open( app.config['ALARM_DATA'], "wb" ) )

        # -- Finally, schedule the new time
        self.scheduler.add_cron_job(self.light_driver.on,
                day_of_week = weekday,
                hour = int(hour),
                minute = int(minute) )

        self.scheduler.add_cron_job(self.light_driver.off,
                day_of_week = weekday,
                hour = int(off_hour),
                minute = int(off_minute) )

        return True

    def reschedule(self):
        """
        Gets the alarm information from the config file and adds jobs to the
        scheduler
        """
        alarm_data = pickle.load( open( app.config['ALARM_DATA'], "rb" ) )
        for weekday, datum in enumerate(alarm_data):
            hour, minute = datum['on'].split(":")
            self.schedule_alarm(weekday, hour, minute)

        return True
