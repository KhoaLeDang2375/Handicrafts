from app.database.database import db
from datetime import datetime

class ContactForm:
    def __init__(self, content, contact_type, employee_id=None, customer_id=None):
        self.employee_id = employee_id
        self.customer_id = customer_id
        self.content = content
        self.contact_type = contact_type
        self.create_time = datetime.now()

    def save(self):
        query = """
        INSERT INTO ContactForm (employee_id, customer_id, content, create_time, contact_type)
        VALUES (%s, %s, %s, %s, %s)
        """
        return db.execute_query(query, (
            self.employee_id,
            self.customer_id,
            self.content,
            self.create_time,
            self.contact_type
        ))

    @staticmethod
    def get_by_id(form_id):
        query = """
        SELECT cf.*, 
               COALESCE(e.name, c.name) as sender_name
        FROM ContactForm cf
        LEFT JOIN Employee e ON cf.employee_id = e.id
        LEFT JOIN customers c ON cf.customer_id = c.id
        WHERE cf.id = %s
        """
        return db.fetch_one(query, (form_id,))

    @staticmethod
    def get_customer_messages(customer_id):
        query = """
        SELECT * FROM ContactForm 
        WHERE customer_id = %s 
        ORDER BY create_time DESC
        """
        return db.fetch_all(query, (customer_id,))

    @staticmethod
    def get_employee_messages(employee_id):
        query = """
        SELECT * FROM ContactForm 
        WHERE employee_id = %s 
        ORDER BY create_time DESC
        """
        return db.fetch_all(query, (employee_id,))