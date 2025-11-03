from app.database import db

class Media:
    def __init__(self, media_type, url, description, entity_id, entity_type, alt_text):
        self.media_type = media_type
        self.url = url
        self.description = description
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.alt_text = alt_text

    def save(self):
        query = """
        INSERT INTO Media (media_type, url, description, entity_id, entity_type, altText)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        return db.execute_query(query, (
            self.media_type,
            self.url,
            self.description,
            self.entity_id,
            self.entity_type,
            self.alt_text
        ))

    @staticmethod
    def get_by_id(media_id):
        query = """SELECT * FROM Media WHERE id = %s"""
        return db.fetch_one(query, (media_id,))

    @staticmethod
    def get_by_entity(entity_type, entity_id):
        query = """
        SELECT * FROM Media 
        WHERE entity_type = %s AND entity_id = %s
        """
        return db.fetch_all(query, (entity_type, entity_id))

    def update(self, media_id, **kwargs):
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = %s")
            values.append(value)
        values.append(media_id)
        
        query = f"""
        UPDATE Media 
        SET {', '.join(fields)}
        WHERE id = %s
        """
        return db.execute_query(query, tuple(values))

    @staticmethod
    def delete(media_id):
        query = """DELETE FROM Media WHERE id = %s"""
        return db.execute_query(query, (media_id,))