from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.student_service import StudentService
from services.course_service import CourseService
from services.payment_service import PaymentService
from controllers.auth_controller import login_required
from datetime import datetime

def get_time_greeting():
    """Return greeting based on current time of day"""
    hour=datetime.now().hour
    if hour<12:
        return "Good morning"
    elif hour<17:
        return "Good afternoon"
    else:
        return "Good evening"

student_bp=Blueprint('students', __name__)

@student_bp.route('/')
def index():
    total_students=StudentService.get_student_count()
    active_courses=CourseService.get_course_count()
    payments_due=PaymentService.get_due_amount()
    payment_count=PaymentService.get_payment_count()
    recent_students=StudentService.get_recent_students(3)
    recent_payments=PaymentService.get_recent_payments(3)

    activity=[]
    for student in recent_students:
        activity.append({
            'title':f'{student.name} added',
            'subtitle':f'Student ID {student.student_id}',
            'badge':'New',
            'badge_class':'badge-primary'
        })
    for payment in recent_payments:
        activity.append({
            'title':f'Payment {payment.status.lower()}',
            'subtitle':f'{payment.student_id}—₹{payment.amount}',
            'badge':payment.status,
            'badge_class':'badge-secondary' if payment.status=='Paid' else 'badge-warning'
        })

    greeting = get_time_greeting()
    payments_status = 'All cleared' if payments_due == 0 else 'Pending payments'

    return render_template(
        'index.html',
        total_students=total_students,
        active_courses=active_courses,
        payments_due=payments_due,
        payments_status=payments_status,
        payment_count=payment_count,
        avg_attendance=91,
        activity=activity,
        greeting=greeting
    )

@student_bp.route('/students')
def list_students():
    students=StudentService.get_all_students()
    student_data=[s.get_details() for s in students]
    return render_template('students.html',students=student_data)

@student_bp.route('/students/add',methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method=='POST':
        data=request.form.to_dict()
        success,message=StudentService.add_student(data)
        flash(message,'success' if success else 'danger')
        if success:
            return redirect(url_for('students.list_students'))
    return render_template('add_student.html')

@student_bp.route('/students/edit/<student_id>',methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    student=StudentService.get_student_by_id(student_id)
    if not student:
        flash('Student not found.','warning')
        return redirect(url_for('students.list_students'))

    if request.method=='POST':
        data=request.form.to_dict()
        success,message=StudentService.update_student(student_id, data)
        flash(message,'success' if success else 'danger')
        if success:
            return redirect(url_for('students.list_students'))

    return render_template('edit_student.html',student=student.get_details(),edit=True)

@student_bp.route('/students/delete/<student_id>',methods=['POST'])
@login_required
def delete_student(student_id):
    deleted=StudentService.delete_student(student_id)
    flash('Student deleted.' if deleted else 'Student not found.',
          'success' if deleted else 'warning')
    return redirect(url_for('students.list_students'))
