import sqlite3

conn = sqlite3.connect('userDB.sqlite')
cur = conn.cursor()

distance_1_L = 1
distance_1_R = 2 
distance_2_L = 3 
distance_2_R = 4
distance_3_L = 5
distance_3_R = 6

# insertionQuery_User = 'INSERT 	INTO User (distance_1_L, distance_1_R, distance_2_L, distance_2_R, distance_3_L, distance_3_R) VALUES (?, ?, ?, ?, ?, ?)'
# cur.execute(insertionQuery_User, (distance_1_L, distance_1_R, distance_2_L, distance_2_R, distance_3_L, distance_3_R, ))
# conn.commit()

sql = 'DELETE FROM User WHERE Id=4'
cur.execute(sql)

selectQuery = "SELECT * FROM User"
for row in cur.execute(selectQuery):
	print(row)
cur.close()