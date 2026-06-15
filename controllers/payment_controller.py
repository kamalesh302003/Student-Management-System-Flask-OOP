from flask import Blueprint,render_template,request,redirect,url_for,flash
from services.payment_service import PaymentService
from controllers.auth_controller import login_required

payment_bp=Blueprint('payments',__name__,url_prefix='/payments')

@payment_bp.route('/')
def list_payments():
    payments=PaymentService.get_all_payments()
    payment_data=[p.get_details() for p in payments]
    return render_template('payments.html',payments=payment_data)

@payment_bp.route('/add',methods=['GET','POST'])
@login_required
def add_payment():
    if request.method=='POST':
        data=request.form.to_dict()
        success,message=PaymentService.add_payment(data)
        flash(message,'success' if success else 'danger')
        if success:
            return redirect(url_for('payments.list_payments'))
    return render_template('payments.html',payments=[p.get_details() for p in PaymentService.get_all_payments()])

@payment_bp.route('/delete/<int:payment_id>',methods=['POST'])
@login_required
def delete_payment(payment_id):
    deleted=PaymentService.delete_payment(payment_id)
    flash('Payment deleted.'if deleted else 'Payment not found.',
          'success' if deleted else 'warning')
    return redirect(url_for('payments.list_payments'))
