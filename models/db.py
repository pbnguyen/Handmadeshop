# -*- coding: utf-8 -*-
from gluon.tools import *

db = DAL('sqlite://storage.sqlite')

mail = Mail()
auth = Auth(db)
crud = Crud(db)
service = Service(globals())
plugins = PluginManager()

auth.define_tables()

response.generic_patterns = ['*']
