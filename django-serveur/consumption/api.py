from tastypie.resources import ModelResource, Resource
from tastypie import fields
from tastypie.exceptions import Unauthorized
from .models import Record, User
import json
from django.http import HttpResponse
from tastypie.serializers import Serializer


class RecordResource2(Resource):
    """ API for creation of a record """
    rfid_uid_0 = fields.IntegerField()
    rfid_uid_1 = fields.IntegerField()
    rfid_uid_2 = fields.IntegerField()
    rfid_uid_3 = fields.IntegerField()
    quantity = fields.FloatField()

    class Meta:
        resource_name = 'record_rfid'
        object_class = Record

    def obj_create(self, bundle, **kwargs):
        """ Creation of a new record with rfid & (pulse | quantity) """
        new_record = Record()

        if(type(bundle.data) == str):
            data = json.loads(bundle.data)
        else:
            data = bundle.data

        if 'pulse' in data:
            new_record.pulse = data['pulse']
            new_record.quantity = new_record.pulse * 2.25
        else:
            new_record.quantity = data['quantity']

        users = User.objects.filter(
            rfid_uid_0=data['rfid_uid_0'],
            rfid_uid_1=data['rfid_uid_1'],
            rfid_uid_2=data['rfid_uid_2'],
            rfid_uid_3=data['rfid_uid_3'])

        if users.count() == 0:
            new_user = User()
            new_user.set_rfid(
                data['rfid_uid_0'], data['rfid_uid_1'],
                data['rfid_uid_2'], data['rfid_uid_3'])
            new_user.facebook_id = 'new rifd %i %i %i %i ' % (
                data['rfid_uid_0'], data['rfid_uid_1'], data['rfid_uid_2'],
                data['rfid_uid_3'])
            new_user.save(force_insert=True)
            new_record.user = new_user
        else:
            new_record.user = users[0]
        new_record.save(force_insert=True)


class RecordResource(ModelResource):
    """ API access to the records"""
    class Meta:
        queryset = Record.objects.all()
        resource_name = 'record'


class urlencodeSerializer(Serializer):
    """ serializer for catching urlencode """
    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'urlencode']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'plist': 'application/x-plist',
        'urlencode': 'application/x-www-form-urlencoded',
        }

    def from_urlencode(self, data, options=None):
        """ handles basic formencoded url posts """
        qs = dict((k, v if len(v) > 1 else v[0])
            for k, v in urlparse.parse_qs(data).iteritems())
        return qs

    def to_urlencode(self, content):
        pass


class UserResource(Resource):
    """ API for user creation """
    first_name = fields.CharField()
    last_name = fields.CharField()
    facebook_id = fields.CharField()

    class Meta:
        resource_name = 'user'
        object_class = User
        serializer = urlencodeSerializer()

    def obj_create(self, bundle, **kwargs):
        bundle.obj = User()

        if User.objects.filter(facebook_id=bundle.data['facebook_id']).count() == 1:
            # do nothing
            pass
            # rep = {'status': 'ok', 'action': 'in db', 'data': {}}
            # return HttpResponse(rep, content_type='application/json', status=200)
        else:
            new_user = User()
            new_user.first_name = bundle.data['first_name']
            new_user.last_name = bundle.data['last_name']
            new_user.facebook_id = bundle.data['facebook_id']
            new_user.save(force_insert=True)
            # rep = {'status': 'ok', 'action': 'stored', 'data': {}}
            # return HttpResponse(rep, content_type='application/json', status=200)
