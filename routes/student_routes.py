from flask import Blueprint,render_template,request,redirect,url_for,flash
from services.student_service import StudentService

student_bp=Blueprint('students', __name__)

@student_bp.route('/')
def index():
    count=StudentService.get_student_count()
    return render_template('index.html',count=count)

@student_bp.route('/students')
def list_students():
    students=StudentService.get_all_students()
    student_data=[s.get_details() for s in students]
    return render_template('students.html',students=student_data)

@student_bp.route('/students/add', methods=['GET', 'POST'])
def add_student():
    if request.method=='POST':
        data=request.form.to_dict()
        success,message=StudentService.add_student(data)
        flash(message,'success' if success else 'danger')
        if success:
            return redirect(url_for('students.list_students'))
    return render_template('add_student.html')

@student_bp.route('/students/delete/<student_id>',methods=['POST'])
def delete_student(student_id):
    deleted=StudentService.delete_student(student_id)
    flash('Student deleted.' if deleted else 'Student not found.',
          'success' if deleted else 'warning')
    return redirect(url_for('students.list_students'))

@student_bp.route('/students/edit/<student_id>',methods=['GET','POST'])
def edit_student(student_id):
    student=StudentService.get_student_by_id(student_id)
    if not student:
        flash('Student not found.','warning')
        return redirect(url_for('students.list_students'))

    if request.method=='POST':
        data=request.form.to_dict()
        success,message=StudentService.update_student(student_id,data)
        flash(message,'success' if success else 'danger')
        if success:
            return redirect(url_for('students.list_students'))

    return render_template('add_student.html',student=student.get_details(),edit=True)