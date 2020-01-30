from application import db, login_manager
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import string
import random
from sqlalchemy import MetaData, create_engine
from sqlalchemy.exc import SQLAlchemyError
from flask import flash

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

def db_delete_objects(*objects):
    try:
        db.session.delete(objects)
        db.session.commit()
        # print('added objects:',*objects,' to db')
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        flash( ("Возникла ошибка:\n" + error), 'error')
        print("Возникла ошибка:\n" + error)




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
            if (self.is_active != association.is_active):
                association.is_active = self.is_active
                db.session.commit()
            if (self.extra_data != association.extra_data):
                association.extra_data = self.extra_data
                db.session.commit()
        else:
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
    
    @staticmethod
    def create_user(name, surname, second_name):
        user = User(name, surname, second_name)
        db_add_objects(user)
        print('Сначала создали юзера = ', user)
        user_info = UserInfo(user.id)
        user_social_pages = UserSocialPages(user.id)
        db_add_objects(user_info, user_social_pages)
        print('Затем создали: ',user,' ',user_info,' ',user_social_pages)
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
        user = User.create_user(name, surname, second_name)
        student = Student(user_id = user.id, educational_group_id=educational_group_id, entry_year=entry_year, degree=degree, tuition_format=tuition_format, tuition_base=tuition_base)
        db_add_objects(student)
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
        user = User.create_user(name, surname, second_name)
        teacher = Teacher(user_id=user.id)
        db_add_objects(teacher)
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

# User_Info.__table__.drop(engine)

""" TEST AREA """
# ivan = db.session.query(User).filter(User.id == 106).first()
# print('reg_password = ', ivan.set_registration_password(password_length = 4))
# new_student = Student.create_student(name='Паша2', surname='Тестовый', second_name='Тестович', educational_group_id=22, entry_year=2016, degree='бакалавр', tuition_format='очная', tuition_base='бюджетная')
    # course = db.session.query(EducationalCourse).filter(EducationalCourse.id == 12).first()
    # group = db.session.query(EducationalGroup).filter(EducationalGroup.id == 15).first()
    # course.add_group(group)
# db_add_objects(course)
# new_student = Student.create_student(name='Андрей_1', surname='Андреев', second_name='Андреевич', educational_group_id=15, entry_year=2017, degree='бакалавр', tuition_format='очная', tuition_base='бюджетная')
# new_student2 = Student.create_student(name='Андрей_2', surname='Андреев', second_name='Андреевич', educational_group_id=1, entry_year=2014, degree='магистр', tuition_format='вечерняя', tuition_base='бюджетная')
# new_student3 = Student.create_student(name='Андрей_3', surname='Андреев', second_name='Андреевич', educational_group_id=22, entry_year=2017, degree='бакалавр', tuition_format='очная', tuition_base='бюджетная')

# db_add_objects(new_student, new_student2, new_student3)

# new_student2 = Student.create_student(name='Сергей', surname='Тестовый', second_name='Сергеевич', educational_group_id=22, entry_year=2017, degree='бакалавр', tuition_format='вечерняя', tuition_base='бюджетная')
    # user = db.session.query(User).filter(User.id == 118).first()
    # print('password = ', user.set_registration_password(password_length=10))
    # db_add_objects(user)

# db_add_objects(new_student, new_student2)

# teacher = Teacher.create_teacher('Петров', 'Петр', 'Предрегистрович')
# db_add_objects(teacher)
# user = db.session.query(User).filter(User.id == 123).first()
# print('password = ', user.set_registration_password(password_length=4))
# db_add_objects(user)
# session.delete(obj)



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