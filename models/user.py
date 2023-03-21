#from flask_security import UserMixin, RoleMixin
#from flask_security import (
#    MongoEngineUserDatastore,
#    hash_password,
#    verify_password,
#)
#from . import _db, collectionid
#from flask_security.forms import LoginForm
#from wtforms import StringField
#from wtforms.validators import InputRequired
#import sys
#from datetime import datetime
#
#USER_DATASTORE = None
#
#"""
#    setup
#"""
#class ExtendedLoginForm(LoginForm):
#    email = StringField('Username', [InputRequired()])
#        
#def setup():
#    # 不同種權限身份
#    class Role(_db.DB.Document, RoleMixin):
#        name = _db.DB.StringField(max_length=80, unique=True)
#        description = _db.DB.StringField(max_length=255)
#
#    # 使用者資訊
#    class User(_db.DB.Document, UserMixin):
#        name = _db.DB.StringField(max_length=255)
#        password = _db.DB.StringField(max_length=255)
#        phone = _db.DB.StringField(max_length=255)
#        user_id = _db.DB.StringField(max_length=255)
#        email = _db.DB.StringField(max_length=255)
#        role = _db.DB.StringField(max_length=255)
#        major = _db.DB.ListField()
#        course_list = _db.DB.ListField()
#        personal_plan = _db.DB.ListField()
#        active = _db.DB.BooleanField(default=True)
#        confirmed_at = _db.DB.DateTimeField()
#        
#        roles = _db.DB.ListField(_db.DB.ReferenceField(Role), default=[])
#        # meta = {'strict': False}
#
#    # Setup Flask-Security
#    global USER_DATASTORE
#    USER_DATASTORE = MongoEngineUserDatastore(_db.DB, User, Role)
#
#
#
#
#"""
#    others
#"""
#
#
#def create_user(input_name,input_password,input_phone,input_user_id,input_email,input_role,input_major,input_course_list,input_personal_plan):
#    student_role = USER_DATASTORE.find_or_create_role("student")
#    teacher_role = USER_DATASTORE.find_or_create_role("teacher")
#    if input_role == "teacher":
#        my_role = teacher_role
#    else:
#        my_role = student_role
#    if USER_DATASTORE.get_user("Liao") is None:
#        
#        USER_DATASTORE.create_user(
#            name = input_name,
#            password=hash_password(input_password),
#            phone = input_phone,
#            user_id = input_user_id,
#            email = input_email,
#            role = input_role,
#            major = input_major,
#            course_list = input_course_list,
#            personal_plan = input_personal_plan,
#            
#            roles=[my_role]
#        )
#
#def create_manager():
#    CSManager_role = USER_DATASTORE.find_or_create_role("CSManager")
#    USER_DATASTORE.create_user(
#        name = '管理員',
#        password=hash_password('beautifulgirl'),
#        phone = '0912345678',
#        user_id = 'handsomeboy',            
#        email = 'admin@gmail.com',
#        role = 'CSManager',
#        major = None,
#        course_list = None,
#        personal_plan = None,
#        
#        roles=[CSManager_role]
#    )
#
#def validate_user(user_id: str, password: str):
#    cur_user = USER_DATASTORE.find_user(user_id=user_id)
#    if cur_user is None:
#        return
#    if verify_password(password, cur_user.password):
#        return cur_user
#    return None
#
#
##Lin
#sys.path.insert(0, './models')
#
##學生成員名單
#def get_student_list():
#    return [{'name':i['name'], 'user_id':i['user_id'], 'course_list':i['course_list'], 'email':i['email'], 'phone':i['phone']} for i in _db.USER_COLLECTION.find({'role':'student'})]
#
#
##老師成員名單
#def get_teacher_list():
#    return [{'name':i['name'], 'user_id':i['user_id'], 'course_list':i['course_list'], 'email':i['email'], 'phone':i['phone'], 'major':i['major']} for i in _db.USER_COLLECTION.find({'role':'teacher'})]
#
##使用者個人資料(name)
#def get_user_info_by_name(name):
#    return [{'name':i['name'], 'user_id':i['user_id'], 'course_list':i['course_list'], 'email':i['email'], 'phone':i['phone'], 'role':i['role']} for i in _db.USER_COLLECTION.find({'name':name})]
#    
#
#
##使用者個人資料(id)
#def get_user_info(user_id):
#    return _db.USER_COLLECTION.find_one({'user_id':user_id})
#
#
##新增成員
#def insert_user(password, name, course_list, phone, email, major, personal_plan, role):
#    now=datetime.now()
#    #用民國年份當id開頭
#    register_year= now.year - 1911
#    #取得目前user id值
#    user_now=collectionid.get_collection_id()['user_now']
#    if role == 'teacher':
#        user_id= str(register_year) + str("-") + "T-"+ str(user_now+1).zfill(3)
#    else:
#        user_id= str(register_year) + str("-") + "S-"+ str(user_now+1).zfill(3)
#    create_user(name,password,phone,user_id,email,role,major,course_list,personal_plan)
#    collectionid.update_collection_id(2, user_now)
#    return user_id
#    
##刪除成員（教師）
#def delete_user(userid):
#    _db.USER_COLLECTION.delete_one(userid)
#    
#    
##編輯成員
#def update_user(userid, userdict):
#    _db.USER_COLLECTION.update_one(userid, {'$set':userdict})
#
## 依據 user_id 找單一物件
#def get_by_userid(user_id):
#    item = _db.USER_COLLECTION.find_one({'user_id' : user_id})
#    return item
#
#def update_personal_plan(user_id,data):
#    _db.USER_COLLECTION.update_one({'user_id':user_id},{'$push':{'personal_plan':data}})
#    
#
#def delete_personal_plan(user_id,data):
#    _db.USER_COLLECTION.update_one({'user_id':user_id},{'$pull':{'personal_plan':data}})