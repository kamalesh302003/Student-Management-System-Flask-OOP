from datetime import date
from database.db import get_connection
from models.payment import Payment

class PaymentService:
    @staticmethod
    def _row_to_payment(row):
        if row is None:
            return None
        return Payment(
            id=row['id'],
            student_id=row['student_id'],
            amount=row['amount'],
            payment_date=row['payment_date'],
            status=row['status'],
            remarks=row['remarks']
        )

    @staticmethod
    def get_all_payments():
        conn=get_connection()
        rows=conn.execute('SELECT * FROM payments ORDER BY payment_date DESC').fetchall()
        conn.close()
        return [PaymentService._row_to_payment(row) for row in rows]

    @staticmethod
    def get_payment_count():
        conn=get_connection()
        row=conn.execute('SELECT COUNT(*) AS count FROM payments').fetchone()
        conn.close()
        return row['count'] if row else 0

    @staticmethod
    def get_due_amount():
        conn=get_connection()
        row=conn.execute("SELECT IFNULL(SUM(amount), 0) AS total FROM payments WHERE status != 'Paid'").fetchone()
        conn.close()
        return row['total'] if row else 0.0

    @staticmethod
    def get_recent_payments(limit=5):
        conn=get_connection()
        rows=conn.execute('SELECT * FROM payments ORDER BY id DESC LIMIT ?', (limit,)).fetchall()
        conn.close()
        return [PaymentService._row_to_payment(row) for row in rows]

    @staticmethod
    def add_payment(data):
        student_id=data.get('student_id','').strip()
        amount=data.get('amount')
        payment_date=data.get('payment_date') or date.today().isoformat()
        status=data.get('status','Paid').strip() or 'Paid'
        remarks=data.get('remarks','').strip() or None

        if not student_id:
            return False,'Student ID is required.'
        try:
            amount_value=float(amount)
            if amount_value<=0:
                raise ValueError('Amount must be greater than zero.')
        except Exception as exc:
            return False,f'Invalid amount:{exc}'

        conn=get_connection()
        try:
            conn.execute('''
                INSERT INTO payments (student_id,amount,payment_date,status,remarks)
                VALUES (?,?,?,?,?)
            ''', (
                student_id,
                amount_value,
                payment_date,
                status,
                remarks
            ))
            conn.commit()
            return True,'Payment recorded successfully.'
        except Exception as exc:
            return False,str(exc)
        finally:
            conn.close()

    @staticmethod
    def delete_payment(payment_id):
        conn=get_connection()
        cursor=conn.execute('DELETE FROM payments WHERE id=?',(payment_id,))
        conn.commit()
        conn.close()
        return cursor.rowcount>0
