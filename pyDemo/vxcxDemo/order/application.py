# -*- coding: utf-8 -*-
from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
import os
class Application( Flask ):
    def __init__(self,import_name,template_folder=None,root_path=None):
        super( Application,self ).__init__( import_name ,template_folder=template_folder,static_folder=None)
        self.config.from_pyfile( 'config/base_setting.py' )
        if "ops_config" in os.environ:
            self.config.from_pyfile('config/%s_setting.py' % os.environ['ops_config'])
        db.init_app( self )

db = SQLAlchemy()
app = Application( __name__ ,os.getcwd()+'/web/templates',os.getcwd())
# app包装
manager = Manager( app )
'''
将函数注入到模板中
'''
'''
函数模板
'''
from common.libs.UrlManager import UrlManager
app.add_template_global(UrlManager.buildStaticUrl, 'buildStaticUrl')
app.add_template_global(UrlManager.buildUrl, 'buildUrl')
app.add_template_global(UrlManager.buildImageUrl, 'buildImageUrl')



