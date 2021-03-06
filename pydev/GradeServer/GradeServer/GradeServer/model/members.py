# -*- coding: utf-8 -*-
"""
    photolog.model.photo
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    photolog 어플리케이션을 사용할 사용자 정보에 대한 model 모듈.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


from sqlalchemy import Column
from sqlalchemy.dialects.mysql import DATETIME, VARCHAR, TEXT, SET

from GradeServer.model import Base

from GradeServer.resource.setResources import SETResources

class Members (Base) :
    
    __tablename__ ='Members'
    
    memberId =Column (VARCHAR (20), primary_key =True, nullable =False)
    password =Column (VARCHAR (1024), nullable =False)
    memberName =Column (VARCHAR (1024), nullable =False)
    contactNumber =Column (VARCHAR  (20), nullable =True)
    emailAddress =Column (VARCHAR  (1024), nullable =True)
    authority =Column (SET (SETResources.const.SERVER_ADMINISTRATOR,
                            SETResources.const.COURSE_ADMINISTRATOR,
                            SETResources.const.USER),
                       default = SETResources.const.USER,
                       nullable =False)
    signedInDate =Column (DATETIME, nullable =False)
    lastAccessDate =Column (DATETIME, nullable =True)
    comment =Column (TEXT, nullable =True)   