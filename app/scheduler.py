import datetime, os
from app import app
from crontab import CronTab


class Scheduler(object):
    """
    A class containing methods for scheduling the alarm.
    Operates both the scheduler and persisting the data
    """
    def __init__(self):
        self.cron = CronTab()

    def get_time_for_day(self, weekday):
        """
        Finds the time the alarm will switch 'on' for the given weekday.

        Weekday: Integer from 0 to 6
            + 0 is sunday
            + 1 is monday
            + ...
            + 6 is saturday
        """
        jobs = self.cron.find_comment("ON for %s" % weekday)
        if not jobs:
            return ""

        for job in jobs:
            # -- We only care about the first job
            return "%s:%s" % (str(job.hour).zfill(2),
                    str(job.minute).zfill(2))

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
        self.cron.remove_all(comment="ON for %s" % weekday)
        self.cron.remove_all(comment="OFF for %s" % weekday)

        # -- Second, create new jobs
        current_dir = os.path.abspath(\
                os.path.dirname(os.path.realpath(__file__)) )
        on_job = self.cron.new(command=current_dir+'/on.py',
                comment = "ON for %s" % weekday)
        off_job = self.cron.new(command=current_dir+'/off.py',
                comment = "OFF for %s" % weekday)

        # -- Third, calculate the alarm times
        alarm_time = datetime.datetime(2014, 1, 1, int(hour), int(minute))
        duration = app.config['ALARM_DURATION']
        on_time = alarm_time.strftime("%H:%M")
        off_time = (alarm_time + \
                datetime.timedelta(minutes=int(duration))).strftime("%H:%M")

        on_hour, on_minute = on_time.split(':')
        off_hour, off_minute = off_time.split(':')

        # -- Finally, add the new job to the crontab
        on_job.minute.on(on_minute)
        on_job.hour.on(on_hour)
        on_job.dow.on(weekday)

        off_job.minute.on(off_minute)
        off_job.hour.on(off_hour)
        off_job.dow.on(weekday)

        self.cron.write()

        return True
