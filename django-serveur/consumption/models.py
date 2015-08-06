from django.db import models
from datetime import datetime


class User(models.Model):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    facebook_id = models.CharField(max_length=100, unique=True)
    rfid_uid_0 = models.IntegerField(default=0)
    rfid_uid_1 = models.IntegerField(default=0)
    rfid_uid_2 = models.IntegerField(default=0)
    rfid_uid_3 = models.IntegerField(default=0)

    def __str__(self):
        if(self.first_name and self.last_name):
            return self.first_name + ', ' + self.last_name
        else:
            return self.facebook_id

    def set_rfid(self, r0, r1, r2, r3):
        self.rfid_uid_0 = r0
        self.rfid_uid_1 = r1
        self.rfid_uid_2 = r2
        self.rfid_uid_3 = r3


class Valve(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Record(models.Model):
    user = models.ForeignKey(User)
    quantity = models.FloatField()
    pulse = models.IntegerField(null=True)
    valve = models.ForeignKey(Valve, null=True)
    time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        if self.user:
            return str(self.user) + '[' + str(self.quantity) + ']'
        else:
            return 'no user' + '[' + str(self.quantity) + ']'
