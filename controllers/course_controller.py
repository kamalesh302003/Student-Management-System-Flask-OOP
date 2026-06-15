from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.course_service import CourseService
from controllers.auth_controller import login_required

course_bp = Blueprint('courses', __name__, url_prefix='/courses')

@course_bp.route('/')
def list_courses():
    courses = CourseService.get_all_courses()
    course_data = [c.get_details() for c in courses]
    return render_template('courses.html', courses=course_data)

@course_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_course():
    if request.method == 'POST':
        data = request.form.to_dict()
        success, message = CourseService.add_course(data)
        flash(message, 'success' if success else 'danger')
        if success:
            return redirect(url_for('courses.list_courses'))
    return render_template('add_course.html')

@course_bp.route('/edit/<int:course_id>', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    course = CourseService.get_course_by_id(course_id)
    if not course:
        flash('Course not found.', 'warning')
        return redirect(url_for('courses.list_courses'))

    if request.method == 'POST':
        data = request.form.to_dict()
        success, message = CourseService.update_course(course_id, data)
        flash(message, 'success' if success else 'danger')
        if success:
            return redirect(url_for('courses.list_courses'))

    return render_template('edit_course.html', course=course.get_details(), edit=True)

@course_bp.route('/delete/<int:course_id>', methods=['POST'])
@login_required
def delete_course(course_id):
    deleted = CourseService.delete_course(course_id)
    flash('Course deleted.' if deleted else 'Course not found.',
          'success' if deleted else 'warning')
    return redirect(url_for('courses.list_courses'))
