from application import app#, login_manager
from flask import render_template, request, redirect, url_for, flash, make_response, session, abort
# from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user,current_user, logout_user
from .models import User, UserInfo, UserSocialPages, Student, Teacher, EducationalGroup, EducationalCourse, CourseMaterial, db, db_add_objects
from .forms import LoginForm, RegisterForm, PersonalCabinetForm, ChangePassword, CourseAddMaterialForm

@app.errorhandler(404)
def error404(error):
    return '<h1>Ошибка 404</h1><p>К сожалению, такой страницы не существет, либо у вас недостаточно прав для ее просмотра</p>'

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

    form = PersonalCabinetForm(detailed_description = user_info.detailed_description)
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
@app.route('/course/<course_id>/description/added_responsible_person:<added_person_id>', methods=['POST', 'GET'])
@app.route('/course/<course_id>/description/deleted_responsible_person:<deleted_person_id>', methods=['POST', 'GET'])
@login_required
def course(course_id, added_person_id=None, deleted_person_id=None):
    active_page = 'course_description'
    course = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).first_or_404()
    query_teacher = db.session.execute('SELECT t1.id as teacher_id, t1.surname, t1.name, t1.second_name FROM users t1 INNER JOIN teachers t2 ON (t2.user_id=t1.id) INNER JOIN "EducationalСourse" t3 ON (t3.teacher_id = t2.user_id)  WHERE t3.id = :course_id  LIMIT 1', {'course_id': course_id})
    
    # Условие что может редактировать материалы курса
    teacher_role = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).filter(EducationalCourse.teacher_id == current_user.id).first()
    can_edit_responsible_persons = False
    if (teacher_role):
        can_edit_responsible_persons = True

    if can_edit_responsible_persons==True and added_person_id:
        print('we will add responsible person id = ', added_person_id )
        added_person = course.add_responsible_person(added_person_id)
        db_add_objects(added_person)
        flash("Староста курса добавлен!", 'success')

    if can_edit_responsible_persons==True and deleted_person_id:
        print('we will deleted responsible person id = ', deleted_person_id )
        deleted_person = course.remove_responsible_person(deleted_person_id)
        db_add_objects(deleted_person)
        flash("Староста курса удален!", 'success')


    teacher = {}
    for r in query_teacher:
        teacher = {'teacher_id':r[0], 'surname':r[1], 'name':r[2], 'second_name':r[3]}
        print('teacher = ',teacher)

    query_responsible_persons = db.session.execute(
    """SELECT t3.id as user_id, t3.surname, t3.name, t3.second_name
    FROM "EducationalСourse" t1 
        INNER JOIN "Course_Responsible_Person" t2 ON (t1.id=t2.course_id)
        INNER JOIN users t3 ON (t3.id=t2.person_id)
    WHERE t2.is_active = 1
    and t1.id = :course_id
    ORDER BY t2.updated_on""", 
    {'course_id': course_id})
    responsible_persons = []
    for r in query_responsible_persons:
        person = {'user_id':r[0], 'surname':r[1], 'name':r[2], 'second_name':r[3]}
        print('person = ', person)
        responsible_persons.append(person)


    query_possible_responsible_persons = db.session.execute(
    """SELECT t5.id as user_id, t5.surname, t5.name, t5.second_name
    FROM "EducationalСourse" t1 
        INNER JOIN "Course_X_Group" t2 ON (t1.id=t2.course_id)
        INNER JOIN "EducationalGroup" t3 ON (t3.id=t2.group_id)
        INNER JOIN students t4 ON (t4.educational_group_id=t3.id)
        INNER JOIN users t5 ON (t5.id=t4.user_id)
        LEFT JOIN "Course_Responsible_Person" t6 ON ( (t6.course_id=t1.id) and (t6.person_id=t5.id) and (t6.is_active=1) )

    WHERE t1.id = :course_id
    and t2.is_active = 1
    and t6.id IS NULL
    ORDER BY t5.surname, t5.name, t5.second_name""", 
    {'course_id': course_id})

    possible_responsible_persons = []
    for r in query_possible_responsible_persons:
        person = {'user_id':r[0], 'surname':r[1], 'name':r[2], 'second_name':r[3]}
        print('person = ', person)
        possible_responsible_persons.append(person)
    print('len(myArray) = ',len(possible_responsible_persons))


    return render_template('course.html', active_page=active_page, course=course, teacher=teacher, responsible_persons=responsible_persons, can_edit_responsible_persons=can_edit_responsible_persons, possible_responsible_persons=possible_responsible_persons)


# @user.route('/<user_id>')
@app.route('/course/<course_id>/program',  methods=['POST', 'GET'])
@app.route('/course/<course_id>/program/deleted_material_id:<material_id>', methods=['POST', 'GET'])
@login_required
def course_program(course_id, material_id=None):
    active_page = 'course_program'
    print('active_page = ',active_page)
    course = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).first_or_404()
    
    can_add_material = False
    # Условие что студент может редактировать материалы курса
    # student = db.session.query(Student).filter(Student.id == course_id).first_or_404()
    teacher = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).filter(EducationalCourse.teacher_id == current_user.id).first()
    # if (teacher or student):
    if (teacher):
        can_add_material = True

        # print('deleted_material_id = ',deleted_material_id)
    if can_add_material==True and material_id:
        print('we will delete material_id = ', material_id )
        deleted_material = db.session.query(CourseMaterial).filter(CourseMaterial.id == material_id).first()
        print('Имя материала = ', deleted_material.name)
        deleted_material.delete()
        db_add_objects(deleted_material)
        flash("Материал удален!", 'success')

    query_course_materials = db.session.execute(
    """SELECT t1.id as course_material_id, t1.name, t1.content, date_trunc('second', t1.created_on) 
    FROM "Course_Material" t1 
        INNER JOIN "EducationalСourse" t2 
        ON (t2.id=t1.course_id)  
    WHERE t2.id = :course_id and (t1.deleted !=1 or t1.deleted is null)
    ORDER BY t1.created_on""", 
    {'course_id': course_id})

    course_materials = []
    for r in query_course_materials:
        course_material = {'course_material_id':r[0], 'name':r[1], 'content':r[2], 'created_dttm':r[3]}
        course_materials.append(course_material)
    # print('course_materials = ',course_materials)

    return render_template('course_program.html', active_page=active_page, course=course, course_materials=course_materials, can_add_material=can_add_material)


@app.route('/course/<course_id>/hometasks', methods=['POST', 'GET'])
@login_required
def course_hometasks(course_id):
    active_page = 'course_hometasks'
    course = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).first_or_404()
    return render_template('course_hometasks.html', active_page=active_page, course=course)



@app.route('/course/<course_id>/add_material/', methods=['POST', 'GET'])
@login_required
def course_add_material(course_id):
    # Условие что студент может редактировать материалы курса
    # student = db.session.query(Student).filter(Student.id == course_id).first_or_404()
    active_page = 'course_program'
    course = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).first_or_404()
    teacher = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).filter(EducationalCourse.teacher_id == current_user.id).first()
    # if not (teacher or student):
    if not (teacher):
        abort(404)
    print('succes you can edit')
    form = CourseAddMaterialForm()
    print('form.name.data = ', form.name.data)
    print('form.content.data = ', form.content.data)

    if form.validate_on_submit():
        print('succesful add new material to course ',course.course_name)
        new_material = course.add_course_material(form.name.data, form.content.data)
        db_add_objects(new_material)
        flash("Материал успешно добавлен", 'success')
        return redirect(url_for('course_program', course_id=course_id))
    
    return render_template('course_add_material.html', course=course, active_page=active_page, form=form)


@app.route('/course/<course_id>/edit_material/<material_id>', methods=['POST', 'GET'])
@login_required
def course_edit_material(course_id, material_id):
    # Условие что студент может редактировать материалы курса
    # student = db.session.query(Student).filter(Student.id == course_id).first_or_404()
    active_page = 'course_program'
    course = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).first_or_404()
    material = db.session.query(CourseMaterial).filter(CourseMaterial.id == material_id).first_or_404()
    teacher = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).filter(EducationalCourse.teacher_id == current_user.id).first()
    # if not (teacher or student):
    if not (teacher):
        abort(404)
    print('succes you can edit')
    form = CourseAddMaterialForm(content = material.content)
    # Непослушный TextArea требует заранее костыльно задавать ему изначальное значение. Потому что placeholder не работает =(
    # form.content.data = '123'# material.content
    # form.content.data = '1235'# material.content

    if form.validate_on_submit():
        print('succesful edit material to course ',course.course_name, 'material = ',material.name)
        material.name = form.name.data
        material.content = form.content.data
        print('material.name = ', material.name)
        print('material.content = ', material.content)
        print('form.content.data = ', form.content.data)
        db_add_objects(material)
        flash("Материал успешно обновлен", 'success')
        return redirect(url_for('course_program', course_id=course_id))
    
    return render_template('course_edit_material.html', course=course, active_page=active_page, form=form, material=material)
    

    
# @app.route('/user/<username>')
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     posts = [
#         {'author': user, 'body': 'Test post #1'},
#         {'author': user, 'body': 'Test post #2'}
#     ]
#     return render_template('user.html', user=user, posts=posts)