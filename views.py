from application import app#, login_manager
from flask import render_template, request, redirect, url_for, flash, make_response, session, abort, json, jsonify
# from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user,current_user, logout_user
from .models import User, UserInfo, UserSocialPages, Student, Teacher, EducationalGroup, EducationalCourse, CourseMaterial, db, db_add_objects, CourseResponsiblePerson, CourseHometask, StudentHometask
from .forms import LoginForm, RegisterForm, PersonalCabinetForm, ChangePassword, CourseAddMaterialForm, CourseHometaskForm, StudentHometaskForm
from datetime import datetime
 

@app.errorhandler(404)
def error404(error):
    return '<h1>Ошибка 404</h1><p>К сожалению, такой страницы не существет, либо у вас недостаточно прав для ее просмотра</p>'

@app.route('/', methods=['GET'])
@login_required
def index():
    student = db.session.query(Student).filter(Student.user_id == current_user.id).first()
    teacher = db.session.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    groupmates = []
    group_name = ''
    courses = []
    if student:
        educational_group = db.session.query(EducationalGroup).filter(EducationalGroup.id == student.educational_group_id).first()
        group_name = educational_group.group_name
        query_groupmates= db.session.execute('SELECT t2.id as user_id, t2.surname, t2.name, t2.second_name FROM students t1 INNER JOIN users t2 ON (t1.user_id = t2.id) WHERE t1.educational_group_id = :group_id', {'group_id': educational_group.id})
        groupmates = []

        for r in query_groupmates:
            groupmate = {'id':r[0],'surname':r[1],'name':r[2],'second_name':r[3]}
            groupmates.append(groupmate)

        query_courses= db.session.execute('SELECT t1.id as course_id, t1.course_name FROM "EducationalСourse" t1 INNER JOIN "Course_X_Group" t2 ON (t1.id = t2.course_id) WHERE t2.group_id = :group_id', {'group_id': educational_group.id})
        for r in query_courses:
            course = {'id':r[0],'course_name':r[1]}
            courses.append(course)

    if teacher:
        query_courses = db.session.execute(
        """SELECT t1.id as course_id, t1.course_name
        FROM "EducationalСourse" t1
            INNER JOIN teachers t2 ON (t1.teacher_id = t2.id)
        WHERE t2.user_id = :user_id""",
        {'user_id': current_user.id})

        for r in query_courses:
            course = {'id':r[0],'course_name':r[1]}
            courses.append(course)

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
            is_finded = 0
            for checked_user in unregistered_users:
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
    print('go')
    print('URL = ',request.url)
    print('Сервер получил запрос метода',request.method)
    print('request.form = ,', request.form)
    print('request.values = ',request.values)

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

# :<user_id>/edit_user_info

@app.route('/personal_cabinet/user_id/<user_id>', methods=['PUT'])
def edit_user_info(user_id):
    user_id = int(user_id)
    user = db.session.query(User).filter(User.id == user_id).first_or_404()
    form = PersonalCabinetForm(request.form)
    print('form.is_submitted() = ', form.is_submitted())
    form.submit()
    print('form.is_submitted() = ', form.is_submitted())

    print('form.errors = ', form.errors)

    for field in form:
        print('field = ',field.label)
        for error in field.errors:
            print('field = ',field.label,' has error:', error)
    print('form.validate() = ',form.validate())
    print('form.errors = ', form.errors)
    print('URL = ',request.url)
    print('Сервер получил запрос метода',request.method)
    print('user_id = ',user_id)
    print('request.form = ,', request.form)
    print('request.values = ',request.values)
    print('type user_id',type(user_id))
    if current_user.id == user_id:
        if form.validate():
            print('form succussfully validated')
            user_info = db.session.query(UserInfo).filter(UserInfo.user_id == user_id).first()
            user_social_pages = db.session.query(UserSocialPages).filter(UserSocialPages.user_id == user_id).first()

            user_info.set_phone(form.phone.data)
            user_info.set_home_region(form.home_region.data)
            user_info.set_detailed_description(form.detailed_description.data)
            user_social_pages.set_vk_page(form.vk.data)
            print('form.phone.data = ',form.phone.data)
            user_social_pages.set_facebook_page(form.facebook.data)
            user_social_pages.set_linked_in_page(form.linked_in.data)
            user_social_pages.set_instagram_page(form.instagram.data)
            db_add_objects(user_info, user_social_pages)
            print('updated in db')
            print('form.data = ', form.data)
            response_data = {'message': 'null', 'code': 'SUCCESS', 'form_data': form.data}
            response =  make_response(jsonify(response_data), 200)
            flash("Данные обновлены!", 'success')
        else:
            print('ошибка валидации и доступов' )
            response_data = {'message': 'validation error', 'code': 'ERROR', 'form_errors': form.errors}
            # response_data = {'message': 'validation error', 'code': 'ERROR', 'validation_errors': form.data}
            response =  make_response(jsonify(response_data), 400)
            # response.headers 
            #  contentType: "application/json",
            # dataType: 'json'

    print('server response = ',response)
    return response


@app.route('/personal_cabinet/user_id:<user_id>', methods=['POST', 'GET'])
@login_required
def personal_cabinet(user_id):
    user = db.session.query(User).filter(User.id == user_id).first_or_404()
    user_info = db.session.query(UserInfo).filter(UserInfo.user_id == user_id).first()
    user_social_pages = db.session.query(UserSocialPages).filter(UserSocialPages.user_id == user_id).first()
    student = db.session.query(Student).filter(Student.user_id == user_id).first()
    educational_group_name = ''
    if student:
        educational_group = db.session.query(EducationalGroup).filter(EducationalGroup.id == student.educational_group_id).first()
        educational_group_name = educational_group.group_name
    watch_only = True
    if user.id == current_user.id:
        watch_only = False

    form = PersonalCabinetForm(
        email=user.email,
        phone = user_info.phone,
        home_region = user_info.home_region,
        detailed_description = user_info.detailed_description,
        vk = user_social_pages.vk,
        facebook = user_social_pages.facebook,
        linked_in = user_social_pages.linked_in,
        instagram = user_social_pages.instagram
    )

    print('user.email = ',user.email)
    for field in form:
        print('field = ',field.label,' = ',field.data)
        for error in field.errors:
            print('field = ',field.label,' has error:', error)
    print('1')
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
    query_teacher = db.session.execute('SELECT t1.id as teacher_id, t1.surname, t1.name, t1.second_name FROM users t1 INNER JOIN teachers t2 ON (t2.user_id=t1.id) INNER JOIN "EducationalСourse" t3 ON (t3.teacher_id = t2.id)  WHERE t3.id = :course_id  LIMIT 1', {'course_id': course_id})
    teacher_role = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).filter(EducationalCourse.teacher_id == Teacher.id).filter(Teacher.user_id == current_user.id).first()
    # Условие что может редактировать материалы курса
    can_edit_responsible_persons = False
    if (teacher_role):
        can_edit_responsible_persons = True
    
    if can_edit_responsible_persons==True and added_person_id:
        added_person = course.add_responsible_person(added_person_id)
        db_add_objects(added_person)
        flash("Староста курса добавлен!", 'success')

    if can_edit_responsible_persons==True and deleted_person_id:
        deleted_person = course.remove_responsible_person(deleted_person_id)
        db_add_objects(deleted_person)
        flash("Староста курса удален!", 'success')


    teacher = {}
    for r in query_teacher:
        teacher = {'teacher_id':r[0], 'surname':r[1], 'name':r[2], 'second_name':r[3]}
# Добавить переход с юзеров на студентов
    query_responsible_persons = db.session.execute(
    """SELECT t3.id as user_id, t3.surname, t3.name, t3.second_name, t4.id as student_id
    FROM "EducationalСourse" t1 
        INNER JOIN "Course_Responsible_Person" t2 ON (t1.id=t2.course_id)
        INNER JOIN students t4 ON (t4.id=t2.person_id)
        INNER JOIN users t3 ON (t3.id=t4.user_id)

    WHERE t2.is_active = 1
    and t1.id = :course_id
    ORDER BY t2.updated_on""", 
    {'course_id': course_id})
    responsible_persons = []
    for r in query_responsible_persons:
        person = {'user_id':r[0], 'surname':r[1], 'name':r[2], 'second_name':r[3], 'student_id':r[4]}
        responsible_persons.append(person)


    query_possible_responsible_persons = db.session.execute(
    """SELECT t4.id as student_id, t5.surname, t5.name, t5.second_name
    FROM "EducationalСourse" t1 
        INNER JOIN "Course_X_Group" t2 ON (t1.id=t2.course_id)
        INNER JOIN "EducationalGroup" t3 ON (t3.id=t2.group_id)
        INNER JOIN students t4 ON (t4.educational_group_id=t3.id)
        INNER JOIN users t5 ON (t5.id=t4.user_id)
        LEFT JOIN "Course_Responsible_Person" t6 ON ( (t6.course_id=t1.id) and (t6.person_id=t4.id) and (t6.is_active=1) )

    WHERE t1.id = :course_id
    and t2.is_active = 1
    and t6.id IS NULL
    ORDER BY t5.surname, t5.name, t5.second_name""", 
    {'course_id': course_id})

    possible_responsible_persons = []
    for r in query_possible_responsible_persons:
        person = {'student_id':r[0], 'surname':r[1], 'name':r[2], 'second_name':r[3]}
        possible_responsible_persons.append(person)

    return render_template('course.html', active_page=active_page, course=course, teacher=teacher, responsible_persons=responsible_persons, can_edit_responsible_persons=can_edit_responsible_persons, possible_responsible_persons=possible_responsible_persons)


@app.route('/course/<course_id>/program',  methods=['POST', 'GET'])
@app.route('/course/<course_id>/program/deleted_material_id:<material_id>', methods=['POST', 'GET'])
@login_required
def course_program(course_id, material_id=None):
    active_page = 'course_program'
    course = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).first_or_404()
    can_add_material = False

    teacher = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).filter(EducationalCourse.teacher_id == Teacher.id).filter(Teacher.user_id == current_user.id).first()
    responsible_person = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).filter(CourseResponsiblePerson.course_id == course_id).filter(CourseResponsiblePerson.person_id == Student.id).filter(current_user.id == Student.user_id).filter(CourseResponsiblePerson.is_active == 1).first()
    # if (teacher or student):
    if (teacher or responsible_person):
        can_add_material = True

    if can_add_material==True and material_id:
        deleted_material = db.session.query(CourseMaterial).filter(CourseMaterial.id == material_id).first()
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

    return render_template('course_program.html', active_page=active_page, course=course, course_materials=course_materials, can_add_material=can_add_material)


@app.route('/course/<course_id>/hometasks', methods=['POST', 'GET', 'DELETE'])
@app.route('/course/<course_id>/hometasks/deleted_hometask_id:<hometask_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def course_hometasks(course_id, hometask_id=None):
    active_page = 'course_hometasks'
    course = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).first_or_404()
    
    can_edit_hometask = False
    teacher = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).filter(EducationalCourse.teacher_id == Teacher.id).filter(Teacher.user_id == current_user.id).first()
    if (teacher):
        can_edit_hometask = True

    if can_edit_hometask==True and hometask_id:
        deleted_hometask = db.session.query(CourseHometask).filter(CourseHometask.id == hometask_id).first()
        deleted_hometask.delete()
        db_add_objects(deleted_hometask)
        flash("Домашнее задание удалено!", 'success')

    is_student = False
    student = db.session.execute(
    """SELECT t4.id as student_id, t5.surname, t5.name, t5.second_name
    FROM "EducationalСourse" t1 
        INNER JOIN "Course_X_Group" t2 ON (t1.id=t2.course_id)
        INNER JOIN "EducationalGroup" t3 ON (t3.id=t2.group_id)
        INNER JOIN students t4 ON (t4.educational_group_id=t3.id)
        INNER JOIN users t5 ON (t5.id=t4.user_id)
    WHERE t1.id = :course_id
    and t2.is_active = 1
    and t5.id = :current_user_id
    LIMIT 1
    """, 
    {'course_id': course_id, 'current_user_id':current_user.id}).first()
    current_dttm = datetime.utcnow()
    if student:
        is_student = True

    query_course_hometasks = db.session.execute(
    """SELECT t1.id as course_hometask_id, t1.name, t1.content, t1.start_dttm, t1.end_dttm, to_char(t1.end_dttm, 'dd-Mon-YYYY,HH24:MM') as trunced_end_dttm
    FROM course_hometask t1 
        INNER JOIN "EducationalСourse" t2 
        ON (t2.id=t1.course_id)  
    WHERE t2.id = :course_id and (t1.deleted !=1 or t1.deleted is null)
    ORDER BY t1.created_on""", 
    {'course_id': course_id})

    course_hometasks = []
    for r in query_course_hometasks:
        course_hometask = {'course_hometask_id':r[0], 'name':r[1], 'content':r[2], 'start_dttm':r[3], 'end_dttm':r[4], 'trunced_end_dttm':r[5]}
        course_hometasks.append(course_hometask)

    return render_template('course_hometasks.html', active_page=active_page, course=course, can_edit_hometask=can_edit_hometask, course_hometasks=course_hometasks, is_student=is_student, current_dttm=current_dttm)


@app.route('/course/<course_id>/add_hometasks/', methods=['POST', 'GET'])
@login_required
def course_add_hometasks(course_id):
    active_page = 'course_hometasks'
    course = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).first_or_404()
    teacher = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).filter(EducationalCourse.teacher_id == Teacher.id).filter(Teacher.user_id == current_user.id).first()
    if not (teacher):
        abort(403)
    form = CourseHometaskForm()

    if form.validate_on_submit():
        new_hometask = course.add_hometask(form.name.data, form.content.data, form.start_dttm.data, form.end_dttm.data)
        db_add_objects(new_hometask)
        flash("Домашнее задание успешно добавлено", 'success')
        return redirect(url_for('course_hometasks', course_id=course_id))
    
    return render_template('course_add_hometask.html', course=course, active_page=active_page, form=form)


@app.route('/course/<course_id>/edit_hometask/<hometask_id>', methods=['POST', 'GET'])
@login_required
def course_edit_hometask(course_id, hometask_id):
    active_page = 'course_hometasks'
    course = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).first_or_404()
    hometask = db.session.query(CourseHometask).filter(CourseHometask.id == hometask_id).first_or_404()
    teacher = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).filter(EducationalCourse.teacher_id == Teacher.id).filter(Teacher.user_id == current_user.id).first()

    if not (teacher):
        abort(403)
    form = CourseHometaskForm(content = hometask.content, start_dttm=hometask.start_dttm, end_dttm=hometask.end_dttm)
    # Непослушный TextArea требует заранее костыльно задавать ему изначальное значение. Потому что placeholder не работает =(

    if form.validate_on_submit():
        hometask.name = form.name.data
        hometask.content = form.content.data
        hometask.start_dttm = form.start_dttm.data
        hometask.end_dttm = form.end_dttm.data
        db_add_objects(hometask)
        flash("Задание успешно обновлено", 'success')
        return redirect(url_for('course_hometasks', course_id=course_id))
    
    return render_template('course_edit_hometask.html', course=course, active_page=active_page, form=form, hometask=hometask)


@app.route('/course/<course_id>/hometasks/<hometask_id>', methods=['POST', 'GET'])
@login_required
def course_hometask(course_id, hometask_id):
    course = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).first_or_404()
    hometask = db.session.query(CourseHometask).filter(CourseHometask.id == hometask_id).first_or_404()
    deadline = hometask.end_dttm.strftime('%d-%m-%Y %H:%M')
    
    can_edit_hometask = False
    groups = []
    student_hometasks = []
    teacher = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).filter(EducationalCourse.teacher_id == Teacher.id).filter(Teacher.user_id == current_user.id).first()
    if (teacher):
        can_edit_hometask = True

        query_students_hometasks = db.session.execute(
        """SELECT t4.id as student_id, t5.surname, t5.name, t5.second_name, t3.group_name,
        case when t7.id IS NOT NULL THEN 1 ELSE 0 end as is_hometask_passed,
        to_char(t7.updated_on, 'dd-Mon-YYYY, HH24:mi') as hometask_pass_dttm,
        t7.id as student_hometask_id
            FROM "EducationalСourse" t1 
            INNER JOIN "Course_X_Group" t2 ON (t1.id=t2.course_id)
            INNER JOIN "EducationalGroup" t3 ON (t3.id=t2.group_id)
            INNER JOIN students t4 ON (t4.educational_group_id=t3.id)
            INNER JOIN users t5 ON (t5.id=t4.user_id)
            INNER JOIN course_hometask t6 ON (t6.course_id = t1.id)
            LEFT JOIN student_hometask t7 ON ((t7.course_hometask_id = t6.id) AND (t7.student_id = t4.id))
        WHERE t1.id = :course_id
        and t2.is_active = 1
        and t6.id = :hometask_id
        ORDER BY t3.group_name, t5.surname, t5.name, t5.second_name
        """, 
        {'course_id': course_id, 'hometask_id':hometask_id })
        
        
        for r in query_students_hometasks:
            student_hometask = {'student_id':r[0], 'surname':r[1], 'name':r[2], 'second_name':r[3], 'group_name':r[4], 'is_hometask_passed':r[5], 'hometask_pass_dttm':r[6], 'student_hometask_id':r[7] }
            student_hometasks.append(student_hometask)
            # Список групп обучающихся на курсе
            if student_hometask['group_name'] not in groups:
                groups.append(student_hometask['group_name'])


    is_student = False
    query_student = db.session.execute(
    """SELECT t4.id as student_id, t5.surname, t5.name, t5.second_name
    FROM "EducationalСourse" t1 
        INNER JOIN "Course_X_Group" t2 ON (t1.id=t2.course_id)
        INNER JOIN "EducationalGroup" t3 ON (t3.id=t2.group_id)
        INNER JOIN students t4 ON (t4.educational_group_id=t3.id)
        INNER JOIN users t5 ON (t5.id=t4.user_id)
    WHERE t1.id = :course_id
    and t2.is_active = 1
    and t5.id = :current_user_id
    LIMIT 1
    """, 
    {'course_id': course_id, 'current_user_id':current_user.id}).first()


    current_dttm = datetime.utcnow()

    student_hometask = None
    form = StudentHometaskForm()
    if query_student:
        student_id = query_student[0]
        student = db.session.query(Student).filter(Student.id == student_id).first()
        is_student = True
        student_hometask = db.session.query(StudentHometask).filter(StudentHometask.course_hometask_id == hometask_id).filter(StudentHometask.student_id == Student.id).filter(Student.user_id == current_user.id).first()
        if student_hometask:
            form = StudentHometaskForm(content = student_hometask.content)
        
    if is_student and current_dttm < hometask.start_dttm:
        abort(403)

    if form.validate_on_submit():
        if not student_hometask:
            student_hometask = StudentHometask(course_hometask_id=hometask.id, student_id=student.id, content=form.content.data)
        else:
            student_hometask.content = form.content.data
        db_add_objects(student_hometask)
        flash("Решение задания сохранено", 'success')
        return redirect(url_for('course_hometasks', course_id=course_id))
    return render_template('course_hometask.html', course=course, hometask=hometask, form=form, can_edit_hometask=can_edit_hometask,
    student_hometask=student_hometask, is_student=is_student, deadline=deadline, current_dttm=current_dttm, groups=groups, student_hometasks=student_hometasks)


@app.route('/course/<course_id>/hometask/<hometask_id>/student_hometask/<student_hometask_id>', methods=['POST', 'GET'])
@login_required
def course_student_hometask(course_id, hometask_id, student_hometask_id):
    teacher = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).filter(EducationalCourse.teacher_id == Teacher.id).filter(Teacher.user_id == current_user.id).first_or_404()
    course = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).first_or_404()
    hometask = db.session.query(CourseHometask).filter(CourseHometask.id == hometask_id).first_or_404()
    student_hometask = db.session.query(StudentHometask).filter(StudentHometask.id == student_hometask_id).first_or_404()
    student = db.session.query(Student).filter(Student.id == StudentHometask.student_id).filter(StudentHometask.id == student_hometask_id).first_or_404()
    user_student = db.session.query(User).filter(Student.id == student.id).filter(User.id == Student.user_id).first_or_404()
    deadline = hometask.end_dttm.strftime('%d-%m-%Y %H:%M')
    return render_template('course_student_hometask.html', course=course, hometask=hometask, student_hometask=student_hometask, deadline=deadline, user_student=user_student)


@app.route('/course/<course_id>/add_material/', methods=['POST', 'GET'])
@login_required
def course_add_material(course_id):
    active_page = 'course_program'
    course = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).first_or_404()
    teacher = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).filter(EducationalCourse.teacher_id == Teacher.id).filter(Teacher.user_id == current_user.id).first()
    responsible_person = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).filter(CourseResponsiblePerson.course_id == course_id).filter(CourseResponsiblePerson.person_id == Student.id).filter(current_user.id == Student.user_id).filter(CourseResponsiblePerson.is_active == 1).first()

    if not (teacher or responsible_person):
        abort(403)
    form = CourseAddMaterialForm()

    if form.validate_on_submit():
        new_material = course.add_course_material(form.name.data, form.content.data)
        db_add_objects(new_material)
        flash("Материал успешно добавлен", 'success')
        return redirect(url_for('course_program', course_id=course_id))
    
    return render_template('course_add_material.html', course=course, active_page=active_page, form=form)


@app.route('/course/<course_id>/edit_material/<material_id>', methods=['POST', 'GET'])
@login_required
def course_edit_material(course_id, material_id):
    # Условие что студент может редактировать материалы курса
    active_page = 'course_program'
    course = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).first_or_404()
    material = db.session.query(CourseMaterial).filter(CourseMaterial.id == material_id).first_or_404()
    teacher = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).filter(EducationalCourse.teacher_id == Teacher.id).filter(Teacher.user_id == current_user.id).first()
    responsible_person = db.session.query(EducationalCourse).filter(EducationalCourse.id == course_id).filter(CourseResponsiblePerson.course_id == course_id).filter(CourseResponsiblePerson.person_id == Student.id).filter(current_user.id == Student.user_id).filter(CourseResponsiblePerson.is_active == 1).first()
    # if not (teacher or student):
    if not (teacher or responsible_person):
        abort(403)
    form = CourseAddMaterialForm(content = material.content)
    # Непослушный TextArea требует заранее костыльно задавать ему изначальное значение. Потому что placeholder не работает =(

    if form.validate_on_submit():
        material.name = form.name.data
        material.content = form.content.data
        db_add_objects(material)
        flash("Материал успешно обновлен", 'success')
        return redirect(url_for('course_program', course_id=course_id))
    
    return render_template('course_edit_material.html', course=course, active_page=active_page, form=form, material=material)