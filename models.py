import sqlite3


class Schema:
   def __init__(self):
       self.conn = sqlite3.connect('items.db')
       self.create_item_table()
       # Why are we calling user table before to_do table
       # what happens if we swap them?

   def __del__(self):
       # body of destructor
       self.conn.commit()
       self.conn.close()

   def create_item_table(self):

       query = """
       CREATE TABLE IF NOT EXISTS "Items" (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         Name TEXT,
         Type TEXT,
         Price REAL,
         Quantity INTEGER
       );
       """

       self.conn.execute(query)


class ItemModel:
   TABLENAME = "Items"

   def __init__(self):
       self.conn = sqlite3.connect('items.db')
       self.conn.row_factory = sqlite3.Row

   def __del__(self):
       # body of destructor
       self.conn.commit()
       self.conn.close()

   def get_by_id(self, _id):
       where_clause = f"AND id={_id}"
       return self.list_items(where_clause)

   def create(self, params):
       print (params)
       query = f'insert into {self.TABLENAME} ' \
               f'(Name, Type, Price, Quantity) ' \
               f'values ("{params.get("Name")}","{params.get("Type")}",' \
               f'"{params.get("Price")}","{params.get("Quantity")}")'

       """insert into todo (Title, Description, DueDate, UserId) values ("todo1","todo1", "2018-01-01", 1)"""
      
       result = self.conn.execute(query)
       return self.get_by_id(result.lastrowid)

   def delete(self, item_id):
       query = f"DELETE FROM {self.TABLENAME} " \
               f"WHERE id = {item_id}"
       print (query)
       self.conn.execute(query)
       return self.list_items()

   def update(self, item_id, update_dict):
       """
       column: value
       Title: new title
       """
       set_query = ", ".join([f'{column} = "{value}"'
                    for column, value in update_dict.items()])

       query = f"UPDATE {self.TABLENAME} " \
               f"SET {set_query} " \
               f"WHERE id = {item_id}"
  
       self.conn.execute(query)
       return self.get_by_id(item_id)

   def list_items(self, where_clause=""):
       query = f"SELECT id, Name, Type, Price, Quantity " \
               f"from {self.TABLENAME}"
               # WHERE _is_deleted != {1} " + where_clause
       print (query)
       result_set = self.conn.execute(query).fetchall()
       print (result_set)
       result = [{column: row[i]
                 for i, column in enumerate(result_set[0].keys())}
                 for row in result_set]
       return result
