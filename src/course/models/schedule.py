from django.db import models


WEEKDAYS = [
    ("MON", "Mondays"),
    ("TUE", "Tuesdays"),
    ("WED", "Wednesdays"),
    ("THU", "Thursdays"),
    ("FRI", "Fridays"),
    ("SAT", "Saturdays"),
    ("SUN", "Sundays"),
]
TIMESLOTS = [
    ("I", "1st"),
    ("II", "2nd"),
    ("III", "3rd"),
    ("IV", "4th"),
    ("V", "5th"),
    ("VI", "6th"),
    ("VII", "7th"),
]


class Schedule(models.Model):
    TYPES = [
        ('W', "weekly"),
        ('O', 'one time')
    ]

    _type = models.CharField(max_length=1, choices=TYPES)

    def is_weekly(self):
        """
        Returns whether this course operates on a weekly schedule
        """
        return self._type == 'W'

    def is_one_time(self):
        """
        Returns whether this course happens only a distinct number of times.
        """
        return self._type == 'O'

    @property
    def slots(self):
        if self.is_weekly():
            return WeeklySlot.objects.filter(schedule=self)
        else:
            return DateSlot.objects.filter(schedule=self)

    def __str__(self):
        #return "{type} - {slots}".format(type=self.get__type_display(), slots="; ".join(map(str,self.slots)))
        course = self.course
        return "{} - {} - {}".format(self._type, course.id, course.subject.name)


class WeeklySlot(models.Model):
    weekday = models.CharField(max_length=3, choices=WEEKDAYS)
    timeslot = models.CharField(max_length=3, choices=TIMESLOTS)
    location = models.CharField(max_length=100, blank=True)
    schedule = models.ForeignKey(Schedule)

    def __str__(self):
        return "{weekday}, {timeslot}".format(
            weekday=self.get_weekday_display(),
            timeslot=self.get_timeslot_display()
        )

    def as_summary(self):
        return '{} {} at {}'.format(self.weekday, self.timeslot, self.place)


class DateSlot(models.Model):
    date = models.DateTimeField()
    location = models.CharField(max_length=100, blank=True)
    schedule = models.ForeignKey(Schedule)

    def __str__(self):
        return str(self.date)

    def as_summary(self):
        return '{} at {}'.format(self.date, self.place)
