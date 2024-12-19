# THIS FILE IS DEPRECATED. DEDICATED DAO SERVICE IN DOCKER CONTAINER USED INSTEAD.
#
# class DAO:
#     def __init__(self, mysql):
#         self.mysql = mysql

#     def insert(self, table_name, data) -> bool:
#         """ Insert data into a table """
#         columns = ', '.join(data.keys())
#         values = ', '.join(['%s'] * len(data))  # Prepare for parameterized query
#         sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
#         cursor = self.mysql.connection.cursor()
#         try:
#             cursor.execute(sql, tuple(data.values()))
#             self.mysql.connection.commit()
#             return True
#         except Exception as e:
#             self.mysql.connection.rollback()
#             raise e
#         finally:
#             cursor.close()

#     def read(self, table_name, filters):
#         """ Get a record from a table based on multiple search fields (filters) """
#         conditions = ' AND '.join([f"{key} = %s" for key in filters.keys()])
#         sql = f"SELECT * FROM {table_name} WHERE {conditions}"
#         cursor = self.mysql.connection.cursor()
#         cursor.execute(sql, tuple(filters.values()))
#         result = cursor.fetchone()  # Use fetchall() for multiple results
#         cursor.close()
#         return result

#     def list_list(self, table_name, field, value):
#         """ Get all records based on a field and its value """
#         sql = f"SELECT * FROM {table_name} WHERE {field} = %s"
#         cursor = self.mysql.connection.cursor()
#         cursor.execute(sql, (value,))
#         results = cursor.fetchall()  # Fetch all rows
#         cursor.close()
#         return results

#     def update(self, table_name, key, value, data):
#         """ Update a record in a table based on key-value pair """
#         set_clause = ', '.join([f"{column} = %s" for column in data.keys()])
#         sql = f"UPDATE {table_name} SET {set_clause} WHERE {key} = %s"
#         cursor = self.mysql.connection.cursor()
#         try:
#             cursor.execute(sql, tuple(data.values()) + (value,))
#             self.mysql.connection.commit()
#         except Exception as e:
#             self.mysql.connection.rollback()
#             raise e
#         finally:
#             cursor.close()

#     def delete(self, table_name, key, value):
#         """ Delete a record from a table based on key-value pair """
#         sql = f"DELETE FROM {table_name} WHERE {key} = %s"
#         cursor = self.mysql.connection.cursor()
#         try:
#             cursor.execute(sql, (value,))
#             self.mysql.connection.commit()
#         except Exception as e:
#             self.mysql.connection.rollback()
#             raise e
#         finally:
#             cursor.close()
