# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PersonalInfo'
        pass

    def backwards(self, orm):
        # Deleting model 'PersonalInfo'
        pass
    complete_apps = ['costmanager']
