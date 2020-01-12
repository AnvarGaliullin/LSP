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
        print('added objects:',*objects,' to db')
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
        association = db.session.query(AssociationCourseGroup).filter(AssociationCourseGroup.course_id == self.course_id).filter(AssociationCourseGroup.group_id == self.group_id).first()
        if association != None:
            print('association updated')
            if (self.is_active != association.is_active):
                association.is_active = self.is_active
                db.session.commit()
            if (self.extra_data != association.extra_data):
                association.extra_data = self.extra_data
                db.session.commit()
        else:
            print('association created')
            db.session.add(self)
            db.session.commit()


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
    teacher_id = db.Column(db.Integer(), db.ForeignKey('teachers.id'))

    def __init__(self, course_name, course_description, teacher_id = None):
        self.course_name = course_name
        self.course_description = course_description
        self.teacher_id = teacher_id
    
    def add_group(self, group):
        group_x_course = AssociationCourseGroup(self.id, group.id, is_active = 1, extra_data='')
        group_x_course.associate_course_with_group()

    def set_teacher(self, teacher_id):
        self.teacher_id = teacher_id

    def add_course_material(self, material_name, content):
        course_material = CourseMaterial(self.id, material_name, content)
        return course_material


    def add_responsible_person(self, person_id):
        person = db.session.query(CourseResponsiblePerson).filter(CourseResponsiblePerson.person_id == person_id).filter(CourseResponsiblePerson.course_id == self.id).first()
        if person:
            person.set_active_flg(1)
        else:
            person = CourseResponsiblePerson(self.id, person_id)
        return person

    def remove_responsible_person(self, person_id):
        person = db.session.query(CourseResponsiblePerson).filter(CourseResponsiblePerson.person_id == person_id).filter(CourseResponsiblePerson.course_id == self.id).first()
        person.set_active_flg(0)
        return person

    def add_hometask(self, name, content, start_dttm, end_dttm):
        course_hometask = CourseHometask(self.id, name, content, start_dttm, end_dttm)
        return course_hometask

    def __repr__(self):
        return "%s(id=\"%s\",course_name=\"%s\")" % (self.__class__.__name__,self.id,self.course_name)


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.query(User).get(user_id)
    except:
        return None
    
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
        # Говнокод - надо придумать как поправить
        # if 1==2:
        #     db_add_objects(self)
        #     user_info = UserInfo(self.id)
        #     user_social_pages = UserSocialPages(self.id)
        #     db_add_objects(user_info, user_social_pages)
        #     print('Новый юзер и доп инфо о юзере успешно созданы!')
        #Additional info about user, should be created when user created
    
    @staticmethod
    def create_user(name, surname, second_name):
        print('Я статический метод класса Юзер')
        user = User(name, surname, second_name)
        db_add_objects(user)
        print('Сначала создали юзера = ', user)
        user_info = UserInfo(user.id)
        user_social_pages = UserSocialPages(user.id)
        db_add_objects(user_info, user_social_pages)
        print('Я создал: ',user,' ',user_info,' ',user_social_pages)
        return user


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


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable = False, unique = True)
    educational_group_id = db.Column(db.Integer(), db.ForeignKey('EducationalGroup.id'), nullable = False)
    entry_year = db.Column(db.Integer(), nullable = False)
    degree = db.Column(db.String(100), nullable = False)
    tuition_format = db.Column(db.String(100), nullable = False)
    tuition_base = db.Column(db.String(100), nullable = False)

    __table_args__ = (db.CheckConstraint(degree.in_(["бакалавр", "специалист", "магистр"])),
    db.CheckConstraint(tuition_format.in_(["очная", "заочная", "вечерняя"])),
    db.CheckConstraint(tuition_base.in_(["контрактная", "бюджетная"])),
    ) 

    def __init__(self, user_id, educational_group_id, entry_year, degree, tuition_format, tuition_base):
        self.user_id = user_id
        self.educational_group_id = educational_group_id
        self.entry_year = entry_year
        self.degree = degree
        self.tuition_format = tuition_format
        self.tuition_base = tuition_base

    @staticmethod
    def create_student(name, surname, second_name, educational_group_id, entry_year, degree, tuition_format, tuition_base):
        print('Я статический метод класса Студент')
        user = User.create_user(name, surname, second_name)
        print('Создали юзера: ', user)
        student = Student(user_id = user.id, educational_group_id=educational_group_id, entry_year=entry_year, degree=degree, tuition_format=tuition_format, tuition_base=tuition_base)
        print('Студент = ',student)
        print('user_id = ',user.id)
        db_add_objects(student)
        print('Создали студента: ', student)
        return student

    def __repr__(self):
	    return "<Student {}:educational_group_id:{}>".format(self.id, self.educational_group_id)


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable = False, unique = True)

    def __init__(self, user_id):
        self.user_id = user_id

    @staticmethod
    def create_teacher(name, surname, second_name):
        print('Я статический метод класса Учитель')
        user = User.create_user(name, surname, second_name)
        print('Создали юзера: ', user)
        teacher = Teacher(user_id=user.id)
        print('user_id = ',user.id)
        db_add_objects(teacher)
        print('Создали учителя: ', teacher)
        return teacher

    def __repr__(self):
	    return "<Teacher {}: user_id{}>".format(self.id, self.user_id)


class UserInfo(db.Model):
    __tablename__ = 'User_Info'
    id = db.Column(db.Integer, nullable = False, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable = False, unique = True )
    phone = db.Column(db.String(100))
    home_region = db.Column(db.String(100))
    detailed_description = db.Column(db.String(255))

    def __init__(self, user_id):
        self.user_id = user_id
    
    def set_phone(self, phone):
	    self.phone = phone

    def set_home_region(self, home_region):
	    self.home_region = home_region

    def set_detailed_description(self, detailed_description):
	    self.detailed_description = detailed_description

    def __repr__(self):
	    return "<User Info {}:{}>".format(self.id, self.user_id)

class UserSocialPages(db.Model):
    __tablename__ = 'User_Social_Pages'
    id = db.Column(db.Integer, nullable = False, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable = False, unique = True )
    vk = db.Column(db.String(100))
    facebook = db.Column(db.String(100))
    linked_in = db.Column(db.String(100))
    instagram = db.Column(db.String(100))

    def __init__(self, user_id):
        self.user_id = user_id
    
    def set_vk_page(self, vk):
	    self.vk = vk

    def set_facebook_page(self, facebook):
	    self.facebook = facebook

    def set_linked_in_page(self, linked_in):
	    self.linked_in = linked_in

    def set_instagram_page(self, instagram):
	    self.instagram = instagram

    def __repr__(self):
	    return "<UserSocialPages Info {}:{}>".format(self.id, self.user_id)


class CourseMaterial(db.Model):
    __tablename__ = 'Course_Material'
    id = db.Column(db.Integer, nullable = False, primary_key=True)
    course_id = db.Column(db.Integer(), db.ForeignKey('EducationalСourse.id'), nullable = False )
    name = db.Column(db.String(100), nullable = False)
    content = db.Column(db.String(10000), nullable = False)
    deleted = db.Column(db.Integer() )
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)

    def __init__(self, course_id, name, content):
        self.course_id = course_id
        self.name = name
        self.content = content
        self.deleted = 0
    
    def set_content(self, content):
	    self.content = content

    def delete(self):
        self.deleted = 1

    def __repr__(self):
	    return "<CourseMaterial Info {}:{}>".format(self.id, self.name)

class CourseResponsiblePerson(db.Model):
    __tablename__ = 'Course_Responsible_Person'
    id = db.Column(db.Integer, nullable = False, primary_key=True)
    course_id = db.Column(db.Integer(), db.ForeignKey('EducationalСourse.id'), nullable = False )
    person_id = db.Column(db.Integer(), db.ForeignKey('students.id'), nullable = False )
    is_active = db.Column(db.Integer )
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('course_id', 'person_id', name='_course_person_uniq_const'),)

    def __init__(self, course_id, person_id):
        self.course_id = course_id
        self.person_id = person_id
        self.is_active = 1
    
    def set_active_flg(self, is_active):
	    self.is_active = is_active

    # def add(self, person_id):
    #     person = db.session.query(CourseResponsiblePerson).filter(CourseResponsiblePerson.id == person_id).filter(EducationalСourse.id == self.id).first()
    #     person.set_active_flg(0)
    #     return person

    def __repr__(self):
	    return "<CourseResponsiblePerson Info {}:{}:{}>".format(self.id, self.course_id, self.person_id)


class CourseHometask(db.Model):
    __tablename__ = 'course_hometask'
    id = db.Column(db.Integer, nullable = False, primary_key=True)
    course_id = db.Column(db.Integer(), db.ForeignKey('EducationalСourse.id'), nullable = False )
    name = db.Column(db.String(100), nullable = False)
    content = db.Column(db.String(10000), nullable = False)
    start_dttm = db.Column(db.DateTime(), nullable = False)
    end_dttm = db.Column(db.DateTime(), nullable = False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)
    deleted = db.Column(db.Integer() )

    def __init__(self, course_id, name, content, start_dttm, end_dttm):
        self.course_id = course_id
        self.name = name
        self.content = content
        self.start_dttm = start_dttm
        self.end_dttm = end_dttm
        self.deleted = 0
    
    def set_content(self, content):
	    self.content = content

    def delete(self):
        self.deleted = 1
    
    def __repr__(self):
	    return "<CourseHometask Info {}:{}:{}>".format(self.id, self.course_id, self.name)


class StudentHometask(db.Model):
    __tablename__ = 'student_hometask'
    id = db.Column(db.Integer, nullable = False, primary_key=True)
    course_hometask_id = db.Column(db.Integer(), db.ForeignKey('course_hometask.id'), nullable = False )
    student_id = db.Column(db.Integer(), db.ForeignKey('students.id'), nullable = False )
    content = db.Column(db.String(100000), nullable = False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('course_hometask_id', 'student_id', name='_course_hometask_student_uniq_const'),)

    def __init__(self, course_hometask_id, student_id, content):
        self.course_hometask_id = course_hometask_id
        self.student_id = student_id
        self.content = content
    
    def set_content(self, content):
	    self.content = content

    def __repr__(self):
	    return "<StudentHometask Info {}:{}:{}>".format(self.id, self.student_id, self.course_hometask_id)


""" ADD TABLE """
db_base_type = 'postgres'
db_base_name = 'LMS'
db_base_password = '1234567890Aa'
db_path = db_base_type+'://'+db_base_type+':'+db_base_password+'@localhost/'+db_base_name
engine = create_engine(db_base_type+'://'+db_base_type+':'+db_base_password+'@localhost/'+db_base_name)
meta = MetaData()
# meta.create_all(engine)
# db.create_all()
# db.session.commit()
print('end')

# User_Info.__table__.drop(engine)
# https://vk.com/id319329506

""" TEST AREA """
ivan = db.session.query(User).filter(User.id == 106).first()
print('reg_password = ', ivan.set_registration_password(password_length = 4))

# hometask = CourseHometask(course_id=12, name='Hometask 1', content = 'content', start_dttm='10-01-2019 00:00:00', end_dttm='10-01-2020 00:00:00')
# print('created hometask = ',hometask)


# new_group = db.session.query(EducationalGroup).filter(EducationalGroup.id == 22).first()
# print('new_group = ',new_group)

# course = db.session.query(EducationalCourse).filter(EducationalCourse.id == 12).first()
# course.add_group(new_group)
# print('course = ',course)




# new_student = Student.create_student(name='Паша2', surname='Тестовый', second_name='Тестович', educational_group_id=22, entry_year=2016, degree='бакалавр', tuition_format='очная', tuition_base='бюджетная')
# db_add_objects(course)
# association = AssociationCourseGroup(course_id=12, group_id=1, is_active = 1, extra_data = '')
# db_add_objects(association)

# new_student = Student.create_student(name='Ваня', surname='Тестовый', second_name='Тестович', educational_group_id=1, entry_year=2016, degree='бакалавр', tuition_format='очная', tuition_base='бюджетная')

# db_add_objects(new_student)

# teacher = db.session.query(Teacher).filter(Teacher.user_id == 100).first()
# user_teacher = db.session.query(User).filter(User.id == 100).first()
# print('set reg pass = ', user_teacher.set_registration_password())
# db_add_objects(user_teacher)
# course1 = db.session.query(EducationalCourse).filter(EducationalCourse.id == 11).first()
# course2 = db.session.query(EducationalCourse).filter(EducationalCourse.id == 12).first()
# print('teacher.id = ',teacher.id)
# course1.set_teacher(teacher.id)
# course2.set_teacher(teacher.id)
# db_add_objects(course1,course2)

# course = EducationalCourse("test_course_1", "usual edu course")
# course2 = EducationalCourse("Тестовый курс по физике", "Какое-то описание тестового курса по физике")
# course3 = EducationalCourse("Тестовый курс по математике", "Какое-то описание тестового курса по математике")
# course4 = EducationalCourse("Тестовый курс по информатике", "Какое-то описание тестового курса по информатике")
# db_add_objects(course,course2,course3,course4)
# association1 = AssociationCourseGroup(9, 15)
# association2 = AssociationCourseGroup(10, 1)
# association3 = AssociationCourseGroup(10, 15)
# association4 = AssociationCourseGroup(11, 1)
# association5 = AssociationCourseGroup(11, 15)
# db_add_objects(association1,association2,association3,association4,association5)
# new_user = User.create_user('удали1', 'удали1', 'удали3')
# new_student = Student.create_student('удали1', 'удали1', 'удали3', educational_group_id = 1, entry_year=2018, degree = "бакалавр", tuition_format = "очная", tuition_base = "бюджетная")
# new_teacher = Teacher.create_teacher('удали1', 'удали11', 'удали3')
# student = Student(user_id = 100, educational_group_id = 1, entry_year=2018, degree = "бакалавр", tuition_format = "очная", tuition_base = "бюджетная")
# print('Студент = ',new_student)
# print('new_teacher = ',new_teacher)
# db_add_objects(new_teacher)
   
    # new_course = db.session.query(EducationalCourse).filter(EducationalCourse.id == 6).first()
    # new_material = new_course.add_course_material('Материал №1 другого курса', 'Пишем 1-jt описание материала...')

    # print('new_material = ',new_material)

# db_add_objects(new_material,new_material2,new_material3,new_material4)

# new_resp_person_1 = CourseResponsiblePerson(7, 39)
# new_resp_person_2 = CourseResponsiblePerson(7, 42)
# new_resp_person_3 = CourseResponsiblePerson(7, 43)

# new_student = Student(name='Студенчес', surname='Студенческий', second_name='Студенчев', educational_group_id = 1, entry_year=2018, degree = "бакалавр", tuition_format = "очная", tuition_base = "бюджетная")
    # new_student=db.session.query(Student).filter(Student.user_id == 59).first()
    # course = db.session.query(EducationalCourse).filter(EducationalCourse.id == 7).first()
    # print('new_student.user_id = ',new_student.user_id)
    # association = course.add_responsible_person(new_student.user_id)
# association = course.remove_responsible_person(new_student.user_id)

    # print('association = ', association)
    # test_student = Student(name ='Вася', surname='Пупкин', second_name='Тестович', educational_group_id = 15, entry_year=2017, degree = "магистр", tuition_format = "очная", tuition_base = "бюджетная")
# db_add_objects(test_student)

# new_user = User.create_user('name', 'surname', 'second name')
# user = new_user[0]
# user_info = new_user[1]
# user_social_pages = new_user[2]

# print('new user = ',new_user)
# print('user = ',user)
# print('user_info = ',user_info)
# print('user_social_pages = ',user_social_pages)


# db_add_objects(user,user_info,user_social_pages)
    # @staticmethod
    # def create_user(name, surname, second_name):
    #     print('Я статический метод')
    #     user = User(name, surname, second_name)
    #     user_info = UserInfo(user.id)
    #     user_social_pages = UserSocialPages(user.id)
    #     return user, user_info, user_social_pages
# db_add_objects(association)
# teacher = db.session.query(Teacher).filter(Teacher.user_id == 55).first()
# print('teacher = ', teacher)
# print('Пароль регистрации = ', teacher.set_registration_password(password_length = 4))
# db_add_objects(teacher)
# teacher = Teacher('Препод_1', 'Тестовый', 'Тестович')
# teacher2 = Teacher('Препод_2', 'Тестовый', 'Тестович')
# print('two teachers added')

# new_course = EducationalCourse('Тестовый курс по информатике', 'Какое-то описание тестового курса по информатике')
# db_add_objects(new_course)

# teacher = db.session.query(Teacher).filter(Teacher.user_id == 55).first()
# new_course = db.session.query(EducationalCourse).filter(EducationalCourse.id == 7).first()
# new_course2 = db.session.query(EducationalCourse).filter(EducationalCourse.id == 8).first()
# new_course.set_teacher(teacher.id)
# new_course2.set_teacher(teacher.id)
# db_add_objects(new_course,new_course2)

# print('new_course = ',new_course,'  has added')

# new_course = db.session.query(EducationalCourse).filter(EducationalCourse.id == 7).first()
# group = db.session.query(EducationalGroup).filter(EducationalGroup.id == 1).first()
# group_2 = db.session.query(EducationalGroup).filter(EducationalGroup.id == 15).first()
# new_course.add_group(group)
# new_course.add_group(group_2)
# print('added 2 groups')




# test_registration_user = db.session.query(User).filter(User.id == 23).first()
# print('test_registration_user = ', test_registration_user)
# print(test_registration_user.set_registration_password(password_length = 4))
# db_add_objects(test_registration_user)

# user_info = User_Info(1)
# db_add_objects(user_info)

# test_user_3 = Student(educational_group_id = 1, entry_year=2018, degree = "бакалавр", tuition_format = "очная", tuition_base = "бюджетная")
# db_add_objects(test_user_3)
# print('dict = ', test_user_3.__dict__)

# test_user_4 =  User(name='Тестов',surname='Тест',second_name='4')




# test_user_2 =  Student(name='Студент5',surname='Тестовый',second_name='5'
# ,educational_group_id = 1, entry_year=2018, degree = "бакалавр", tuition_format = "очная", tuition_base = "бюджетная")
# db_add_objects(test_user_2)
# user_id = test_user_2.id
# print('user id = ', user_id)
# user_info = UserInfo(user_id)
# user_social_pages = UserSocialPages(user_id)
# # user_info = db.session.query(UserInfo).filter(UserInfo.user_id == user_id).first()
# # user_social_pages = db.session.query(UserSocialPages).filter(UserSocialPages.user_id == user_id).first()
# print('Пароль для регистрации: ', test_user_2.set_registration_password(password_length = 4))
# print('Создание нового студента:' , test_user_2)
# db_add_objects(user_info, user_social_pages)


# test_user_2.set_email('a@mail.ru')
# print(test_user_2.email)
# User
# test_user_2.set_vk_page = 'assd'




# db_add_objects(test_user_2)
# test_user_2 =  Teacher(name='Препод',surname='Тестовый',second_name='6')

# db_add_objects(test_user_2)
# Поменять название классов без ____
# UserInfo=db.session.query(UserInfo).filter(UserInfo.user_id == 1).first()
# # UserInfo = UserInfo(1)
# # UserInfo.set_phone("+7-985-25-25-25")
# UserInfo.set_home_region("")
# # UserInfo.set_deltailed_description("Подробное описание -ла-ла-ла")
# db_add_objects(UserInfo)

# # User_Social_Pages=db.session.query(User_Social_Pages).filter(User_Social_Pages.user_id == 1).first()
# # User_Social_Pages = User_Social_Pages(1)
# UserSocialPages = UserSocialPages(1)
# UserSocialPages.set_vk_page("https://vk.com/id319329506")
# db_add_objects(UserSocialPages)

# db.metadata.create_all(engine)

# IMsO
# test_user_2 =  User(name='Тестов',surname='Тест',second_name='2')
# print('test_registration_user = ', test_registration_user)
# print("reg_pass = ",test_user_2.set_registration_password(password_length = 4))
# sUNQ
# db.session.add(test_user_2)
# db.session.commit()

""" TEST AREA END"""



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
# # User_Info.__table__.drop(engine)
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


