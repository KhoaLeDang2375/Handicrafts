from app.database import db

class Shipment:
    def __init__(self, order_id, carrier='GHTK', status='Pending'):
        self.order_id = order_id
        self.carrier = carrier
        self.status = status

    def save(self):
        query = """
        INSERT INTO Shipment (order_id, carrier, status)
        VALUES (%s, %s, %s)
        """
        return db.execute_query(query, (
            self.order_id,
            self.carrier,
            self.status
        ))

    @staticmethod
    def get_by_id(shipment_id):
        query = """
        SELECT s.*, o.date as order_date 
        FROM Shipment s
        JOIN Orders o ON s.order_id = o.id
        WHERE s.id = %s
        """
        return db.fetch_one(query, (shipment_id,))

    @staticmethod
    def get_by_order(order_id):
        query = """SELECT * FROM Shipment WHERE order_id = %s"""
        return db.fetch_one(query, (order_id,))

    def update_status(self, shipment_id, status):
        query = """
        UPDATE Shipment 
        SET status = %s 
        WHERE id = %s
        """
        return db.execute_query(query, (status, shipment_id))

    @staticmethod
    def get_all_by_status(status):
        query = """
        SELECT s.*, o.date as order_date 
        FROM Shipment s
        JOIN Orders o ON s.order_id = o.id
        WHERE s.status = %s
        """
        return db.fetch_all(query, (status,))