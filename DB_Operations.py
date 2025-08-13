import sqlite3
import pandas as pd

# conn = sqlite3.connect('Trading.db')

# Cur = conn.cursor()

# Cur.execute("""select * from Employees""")

# # Cur.execute("""CREATE TABLE Employees (
# #             first text,
# #             last text,
# #             pay integer)""")

# conn.commit()
# conn.close()


data = {'col1': [1, 2], 'col2': ['A', 'B']}
df = pd.DataFrame(data)

conn = sqlite3.connect("Trading.db")

# Insert the DataFrame into a table named 'flags'
df.to_sql("flags", conn, if_exists="replace", index=False)

# Optional: Fetch and print inserted data
cursor = conn.cursor()
cursor.execute("SELECT * FROM flags")
for row in cursor.fetchall():
    print(row)