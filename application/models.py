# from sqlalchemy import db.Column, String, db.Integer, create_engine, ForeignKey, DateTime, or_
# from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.exc import SQLAlchemyError
# from datetime import datetime, date, time
# from flask_login import UserMixin
# from werkzeug.security import generate_password_hash,  check_password_hash
# import random
# import string



from application import db, login_manager
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import string
import random
from sqlalchemy import MetaData, create_engine
from sqlalchemy.exc import SQLAlchemyError
from flask import flash

#..
def db_add_objects(*objects):
    try:
        db.session.add_all(objects)
        db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        flash( ("Возникла ошибка:\n" + error), 'error')
        print("Возникла ошибка:\n" + error)
#     print('Возникла ошибка:\n', error)




class AssociationCourseGroup(db.Model):
    __tablename__ = 'Course_X_Group'
    course_id = db.Column(db.Integer, db.ForeignKey('EducationalСourse.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('EducationalGroup.id'), primary_key=True)
    extra_data = db.Column(db.String(50))
    is_active = db.Column(db.Integer, nullable=False, default = 0)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)
    child = db.relationship("EducationalGroup", back_populates="parents")
    parent = db.relationship("EducationalCourse", back_populates="children")

    def __init__(self, course_id:int, group_id:int, is_active = 1, extra_data = ''):
        self.course_id = course_id
        self.group_id = group_id
        self.is_active = is_active
        self.extra_data = extra_data
    """
    Many-to-Many association between courses and groups
    Firstly, check: Is association exist? 
    -> Exists:  Update optional parametrs
    -> Doesn't exist:  Create new association with all available parametrs
    """
    def associate_course_with_group(self):
        association = session.query(AssociationCourseGroup).filter(AssociationCourseGroup.course_id == self.course_id).filter(AssociationCourseGroup.group_id == self.group_id).first()
        if association != None:
            print('association updated')
            if (self.is_active != association.is_active):
                association.is_active = self.is_active
                session.commit()
            if (self.extra_data != association.extra_data):
                association.extra_data = self.extra_data
                session.commit()
        else:
            print('association created')
            session.add(self)
            session.commit()


class EducationalGroup(db.Model):
    __tablename__ = 'EducationalGroup'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(250), nullable=False, unique = True)
    faculty_name = db.Column(db.String(250), nullable=False)
    course_number = db.Column(db.Integer(), nullable=False)
    parents = db.relationship("AssociationCourseGroup", back_populates="child")

    def __init__(self, group_name, faculty_name, course_number):
        self.group_name = group_name
        self.faculty_name = faculty_name
        self.course_number = course_number
       
    def __repr__(self):
	    return "%s(id=\"%s\",group_name=\"%s\")" % (self.__class__.__name__,self.id,self.group_name)


class EducationalCourse(db.Model):
    __tablename__ = 'EducationalСourse'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(250), nullable=False, unique = True)
    course_description = db.Column(db.String(250), nullable=False)
    children = db.relationship("AssociationCourseGroup", back_populates="parent")
    teacher_id = db.Column(db.Integer(), db.ForeignKey('teachers.user_id'))

    def __init__(self, course_name, course_description):
        self.course_name = course_name
        self.course_description = course_description
    
    def add_group(self, group):
        group_x_course = AssociationCourseGroup(self.id, group.id, is_active = 1, extra_data='')
        group_x_course.associate_course_with_group()

    def set_teacher(self, teacher_id):
        self.teacher_id = teacher_id

    def __repr__(self):
        return "%s(id=\"%s\",course_name=\"%s\")" % (self.__class__.__name__,self.id,self.course_name)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)
    
# , UserMixin
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    surname = db.Column(db.String(100), nullable = False)
    second_name = db.Column(db.String(100), nullable = False)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100),  unique=True)
    password_hash = db.Column(db.String(100))
    registration_password_hash = db.Column(db.String(100))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)

    def __init__(self, name, surname, second_name):
        self.name = name
        self.surname = surname
        self.second_name = second_name

    def __repr__(self):
	    return "<{}:{}>".format(self.id, self.name + ' ' + self.surname)
    
    def set_username(self, username):
	    self.username = username

    def set_email(self, email):
	    self.email = email

    def set_password(self, password):
	    self.password_hash = generate_password_hash(password)

    def check_password(self, password):
	    return check_password_hash(self.password_hash, password)
    
    def set_registration_password(self, password_length = 10):
        lettersAndDigits = string.ascii_letters + string.digits
        registration_password = ''
        for i in range(password_length):
            registration_password = registration_password + random.choice(lettersAndDigits)
        self.registration_password_hash = generate_password_hash(registration_password)
        return registration_password


class Student(User):
    __tablename__ = 'students'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)
    educational_group_id = db.Column(db.Integer(), db.ForeignKey('EducationalGroup.id'), nullable = False)
    entry_year = db.Column(db.Integer(), nullable = False)
    degree = db.Column(db.String(100), nullable = False)
    tuition_format = db.Column(db.String(100), nullable = False)
    tuition_base = db.Column(db.String(100), nullable = False)

    __table_args__ = (db.CheckConstraint(degree.in_(["бакалавр", "специалист", "магистр"])),
    db.CheckConstraint(tuition_format.in_(["очная", "заочная", "вечерняя"])),
    db.CheckConstraint(tuition_base.in_(["контрактная", "бюджетная"])),
    ) 

    def __init__(self, name, surname, second_name, educational_group_id, entry_year, degree, tuition_format, tuition_base):
        super().__init__(name, surname, second_name)
        self.educational_group_id = educational_group_id
        self.entry_year = entry_year
        self.degree = degree
        self.tuition_format = tuition_format
        self.tuition_base = tuition_base

    def __repr__(self):
	    return "<Student {}:{}>".format(self.id, self.name + ' ' + self.surname)


class Teacher(User):
    __tablename__ = 'teachers'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)

    def __init__(self, name, surname, second_name):
        super().__init__(name, surname, second_name)

    def __repr__(self):
	    return "<Teacher {}:{}>".format(self.id, self.name + ' ' + self.surname)





""" ADD TABLE """
db_base_type = 'postgres'
db_base_name = 'LMS'
db_base_password = '1234567890Aa'
db_path = db_base_type+'://'+db_base_type+':'+db_base_password+'@localhost/'+db_base_name
engine = create_engine(db_base_type+'://'+db_base_type+':'+db_base_password+'@localhost/'+db_base_name)
meta = MetaData()
meta.create_all(engine)
db.create_all()
print('end')

""" TEST AREA """
test_registration_user = db.session.query(User).filter(User.id == 23).first()
print('test_registration_user = ', test_registration_user)
print(test_registration_user.set_registration_password(password_length = 4))
db_add_objects(test_registration_user)



# test_user_3 = Student(educational_group_id = 1, entry_year=2018, degree = "бакалавр", tuition_format = "очная", tuition_base = "бюджетная")
# db_add_objects(test_user_3)
# print('dict = ', test_user_3.__dict__)

# test_user_4 =  User(name='Тестов',surname='Тест',second_name='4')
test_user_2 =  Student(name='Юзер',surname='Тестовый',second_name='5'
,educational_group_id = 1, entry_year=2018, degree = "бакалавр", tuition_format = "очная", tuition_base = "бюджетная")

test_user_2 =  Teacher(name='Препод',surname='Тестовый',second_name='6')
print(test_user_2)
# db_add_objects(test_user_2)

# IMsO
# test_user_2 =  User(name='Тестов',surname='Тест',second_name='2')
# print('test_registration_user = ', test_registration_user)
# print("reg_pass = ",test_user_2.set_registration_password(password_length = 4))
# sUNQ
# db.session.add(test_user_2)
# db.session.commit()

""" TEST AREA END"""


# db.metadata.create_all(engine)

# Session = sessionmaker(bind=engine)
# session = Session()



# test_registration_user = session.query(User).filter(User.id == 21).first()
# print('test_registration_user = ', test_registration_user)
# #  =  User(name='Тестовый регистрации',surname='1',second_name='2')
# print("reg_pass = ",test_registration_user.set_registration_password(password_length = 4))
# session.add(test_registration_user)

# try:
#     session.commit()
# except SQLAlchemyError as e:
#     error = str(e.__dict__['orig'])
#     print('Возникла ошибка:\n', error)


# # course = session.query(EducationalCourse).filter(EducationalCourse.course_name == 'test_course_1').first()
# # print(course)
# # set_registration_password(self, password_length)
# # Anvar = session.query(User).all()
# # print('Anvar')

# # spike = User(name='spike',surname='Тестовый',second_name='Тестович',username = 'spike')
# # tyke = User(name='tyke',surname='Тестовый',second_name='Тестович',username = 'tyke')
# # u1 = session.query(User).filter(User.name == 'Тест').first()
# # print(u1)
# # User.__table__.drop(engine)
# # User.__table__.drop()
#     # anvar = User(name='Анвар',surname='Галиуллин',second_name='Ринатович')
#     # print(anvar)
#     # session.add(anvar)
#     # print(session.new)
#     # session.commit()


# # u1 = User(username='spike', email='spike@example.com')
# # u1 = db.session.query(User).filter(User.username == 'spike').first()

# # Не удаляем этот кусок. Это пример генерации пароля регистрации для пользователя
#     # user1 = session.query(User).filter(User.name == 'Анвар').first()
#     # print('Для пользователя "',user1.surname,' ',user1.name,' ',user1.second_name,'" сгенерирован пароль: ',user1.set_registration_password())
#     # session.add(user1)
#     # session.commit()

# user1 = session.query(User).filter(User.name == 'Анвар').first()
# user1.set_username('admin')
# user1.set_email('anvargal@mail.ru')
# user1.set_password('admin')
# session.add(user1)
# session.commit()


# # geros = User(name='geros',surname='1',second_name='2')
# # print('Для пользователя "',geros.surname,' ',geros.name,' ',geros.second_name,'" сгенерирован пароль: ',geros.set_registration_password())
# # session.add(geros)
# # session.commit()




# course = session.query(EducationalCourse).filter(EducationalCourse.course_name == 'test_course_1').first()
# group = session.query(EducationalGroup).filter(EducationalGroup.group_name == 'my_test_group_2').first()
# print(course)

# course.add_group(group)
# # AssociationCourseGroup(course.id, group.id, is_active = 1, extra_data='my attempts').associate_course_with_group()
# # course_x_group

# try:
#     session.commit()
# except SQLAlchemyError as e:
#     error = str(e.__dict__['orig'])
#     print('Возникла ошибка:\n', error)

# db_result = session.query(EducationalGroup).all()
# print('\nТаблица EducationalGroup')
# for row in db_result:
#     print (row.id, row.group_name, row.faculty_name, row.course_number)

# db_result = session.query(EducationalCourse).all()
# print('\nТаблица EducationalCourse')
# for row in db_result:
#     print (row.id, row.course_name, row.course_description)


