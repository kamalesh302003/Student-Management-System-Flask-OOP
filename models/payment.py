class Payment:
    def __init__(self,student_id,amount,payment_date,status='Paid',remarks=None,id=None):
        self.id=id
        self.student_id=student_id
        self.amount=amount
        self.payment_date=payment_date
        self.status=status
        self.remarks=remarks

    def get_details(self):
        return {
            'id':self.id,
            'student_id':self.student_id,
            'amount':self.amount,
            'payment_date':self.payment_date,
            'status':self.status,
            'remarks':self.remarks
        }
