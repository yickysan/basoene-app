import sqlite3
from basoene_api.models.rooms import create_tables as room_tables
from basoene_api.models.products import create_tables as product_tables

query = """
        DROP TABLE productsales
        """

if __name__ == "__main__":
    with sqlite3.connect("rooms.db") as conn:
        cursor = conn.execute(query)
    
    
    


