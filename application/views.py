from application import app#, login_manager
from flask import render_template, request, redirect, url_for, flash, make_response, session
# from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user,current_user, logout_user
from .models import User, UserInfo, UserSocialPages, Student, Teacher, EducationalGroup, EducationalCourse, db, db_add_objects
from .forms import LoginForm, RegisterForm, PersonalCabinetForm, ChangePassword


@app.route('/', methods=['GET'])
@login_required
def index():
    # user = db.session.query(User).filter(User.id == current_user.id).first_or_404()

    student = db.session.query(Student).filter(Student.user_id == current_user.id).first()
    teacher = db.session.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    print('Вошел на сервер')
    groupmates = []
    group_name = ''
    courses = []
    if student:
        print('Да, студент:',student)
        educational_group = db.session.query(EducationalGroup).filter(EducationalGroup.id == student.educational_group_id).first()
        group_name = educational_group.group_name
        print(group_name)
        query_groupmates= db.session.execute('SELECT t2.id as user_id, t2.surname, t2.name, t2.second_name FROM students t1 INNER JOIN users t2 ON (t1.user_id = t2.id) WHERE t1.educational_group_id = :group_id', {'group_id': educational_group.id})
        print('query_groupmates = ',query_groupmates)
        groupmates = []


        for r in query_groupmates:
            print('r = ',r[0])
            groupmate = {'id':r[0],'surname':r[1],'name':r[2],'second_name':r[3]}
            groupmates.append(groupmate)
        print('groupmates = ',groupmates)

        query_courses= db.session.execute('SELECT t1.id as course_id, t1.course_name FROM "EducationalСourse" t1 INNER JOIN "Course_X_Group" t2 ON (t1.id = t2.course_id) WHERE t2.group_id = :group_id', {'group_id': educational_group.id})
        for r in query_courses:
            print('r = ',r[0])
            course = {'id':r[0],'course_name':r[1]}
            courses.append(course)
        print('courses = ',courses)
        # all_courses = db.session.query(EducationalGroup).filter(EducationalGroup.id == student.educational_group_id).first()
        # educational_group
    if teacher:
        query_courses= db.session.execute('SELECT t1.id as course_id, t1.course_name FROM "EducationalСourse" t1 WHERE t1.teacher_id = :teacher_id', {'teacher_id': current_user.id})
        for r in query_courses:
            print('r = ',r[0])
            course = {'id':r[0],'course_name':r[1]}
            courses.append(course)
        print('courses = ',courses)

    # print('user.id = ',user.id, 'current_user.id = ',current_user.id)

    #     return render_template('personal_cabinet.html', form=form, user = user, user_info=user_info, user_social_pages=user_social_pages, student=student, educational_group_name=educational_group_name, watch_only=watch_only)
    # print('условие не прошло')
    # return render_template('personal_cabinet.html', form=form, user = user, user_info=user_info, user_social_pages=user_social_pages, student=student, educational_group_name=educational_group_name, watch_only=watch_only)



    return render_template('index.html', group_name=group_name, groupmates=groupmates, courses=courses )




@app.route('/admin/')
@login_required
def admin():
    return render_template('admin.html')


@app.route('/register/', methods=['post', 'get'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # DataBase Logic - check, if user with such validation_password exists
        user_with_equal_email = db.session.query(User).filter(User.email == form.email.data).first()
        if user_with_equal_email != None:
            flash("This E-mail is already reserved", 'danger')
            return redirect(url_for('register'))
        else:
            unregistered_users = db.session.query(User).filter(User.email == None).filter(User.registration_password_hash != None).all()
            print(unregistered_users)
            is_finded = 0
            for checked_user in unregistered_users:
                print('checked_user = ',checked_user)
                if check_password_hash(checked_user.registration_password_hash, form.registration_password.data):
                    checked_user.set_email(form.email.data)
                    checked_user.set_password(form.password.data)
                    db_add_objects(checked_user)
                    login_user(checked_user)
                    is_finded = 1
                    return redirect(url_for('index')) 
            if is_finded == 0:
                flash("Invalid verification code", 'danger')
                return redirect(url_for('register'))   
    return render_template('register.html', form=form)


@app.route('/login/', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
	    return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Вы вошли в систему", 'success')
            return redirect(url_for('index'))

        flash("Invalid email/password", 'danger')
        # flash("Success!", "success")
        # flash("This is a warning", "warning")
        # flash("DANGER DANGER", "danger")
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", 'warning')
    return redirect(url_for('login'))



@app.route('/personal_cabinet/user_id:<user_id>', methods=['POST', 'GET'])
@login_required
def personal_cabinet(user_id):
    user = db.session.query(User).filter(User.id == user_id).first_or_404()
    user_info = db.session.query(UserInfo).filter(UserInfo.user_id == user_id).first()
    user_social_pages = db.session.query(UserSocialPages).filter(UserSocialPages.user_id == user_id).first()
    student = db.session.query(Student).filter(Student.user_id == user_id).first()
    educational_group_name = ''
    if student:
        print(student)
        educational_group = db.session.query(EducationalGroup).filter(EducationalGroup.id == student.educational_group_id).first()
        educational_group_name = educational_group.group_name
    watch_only = True
    if user.id == current_user.id:
        watch_only = False
        print('equal')
    print('user.id = ',user.id, 'current_user.id = ',current_user.id)
    print(watch_only)
    print(student)
    # # user = User.query.filter_by(id=user_id).first_or_404()
    # user_info = User_Info.query.filter_by(user_id=user_id)
    # user_social_pages = User_Social_Pages.query.filter_by(user_id=user_id)
    print('Смотрите на user info:')
    print(user_info)
    print('method = ',request.method)
    # print(user_info.__dict__)

    form = PersonalCabinetForm()
    # print('first errors = ', form.errors)
    print('form.email = ', form.email.data)
    print('form.phone = ', form.phone.data)
    print('form.home_region = ', form.home_region.data)
    print('form.detailed_description = ', form.detailed_description.data)
    print('form.vk = ', form.vk.data)

    print('second errors = ', form.errors)

    print('условие')
    if form.validate_on_submit():
        print('gogogo')

    # DataBase Logic - check, if user with such validation_password exists
        print(user_info.phone)
        user_info.set_phone(form.phone.data)
        user_info.set_home_region(form.home_region.data)
        user_info.set_detailed_description(form.detailed_description.data)

        user_social_pages.set_vk_page(form.vk.data)
        user_social_pages.set_facebook_page(form.facebook.data)
        user_social_pages.set_linked_in_page(form.linked_in.data)
        user_social_pages.set_instagram_page(form.instagram.data)

        db_add_objects(user_info, user_social_pages)
        return render_template('personal_cabinet.html', form=form, user = user, user_info=user_info, user_social_pages=user_social_pages, student=student, educational_group_name=educational_group_name, watch_only=watch_only)
    print('условие не прошло')
    return render_template('personal_cabinet.html', form=form, user = user, user_info=user_info, user_social_pages=user_social_pages, student=student, educational_group_name=educational_group_name, watch_only=watch_only)



@app.route('/change_password/', methods=['POST', 'GET'])
@login_required
def change_password():
    user = db.session.query(User).filter(User.id == current_user.id).first_or_404()
    form = ChangePassword()

    if form.validate_on_submit():
        if user.check_password(form.old_password.data):
            user.set_password(form.new_password.data)
            db_add_objects(user)
            login_user(user)
            flash("Пароль успешно изменен", 'success')
            return redirect(url_for('personal_cabinet', user_id=user.id))
        flash("Неправильный пароль", 'danger')
        return render_template('change_password.html', form=form, user=user)
    return render_template('change_password.html', form=form, user=user)




@app.route('/course/<course_id>/', methods=['POST', 'GET'])
@app.route('/course/<course_id>/description', methods=['POST', 'GET'])
@login_required
def course(course_id):
    active_page = 'course_description'
    course = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).first_or_404()
    return render_template('course.html', active_page=active_page, course=course)


@app.route('/course/<course_id>/program', methods=['POST', 'GET'])
@login_required
def course_program(course_id):
    active_page = 'course_program'
    print('active_page = ',active_page)
    course = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).first_or_404()
    return render_template('course_program.html', active_page=active_page, course=course)


@app.route('/course/<course_id>/hometasks', methods=['POST', 'GET'])
@login_required
def course_hometasks(course_id):
    active_page = 'course_hometasks'
    course = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).first_or_404()
    return render_template('course_hometasks.html', active_page=active_page, course=course)



# @app.route('/user/<username>')
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     posts = [
#         {'author': user, 'body': 'Test post #1'},
#         {'author': user, 'body': 'Test post #2'}
#     ]
#     return render_template('user.html', user=user, posts=posts)