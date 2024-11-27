# ### link >>> https://www.geeksforgeeks.org/python-sqlite/?ref=shm
import sqlite3

try:

	# Connect to DB and create a cursor
    sqliteConnection = sqlite3.connect('temp.db')


    # Get cursor
    cursor = sqliteConnection.cursor()


    # # make query phrase for createing a table called 'tsetmc' with 3 columns and then execute it
    # query = "CREATE TABLE tsetmc(title, volume, price)"
    # cursor.execute(query)


    # get name of tables in database
    result = cursor.execute("SELECT name from sqlite_master")
    print("tables: ", result.fetchall())

    # # serach for a table name in database
    # result = cursor.execute("SELECT name from sqlite_master WHERE name='test1'")
    # print("tables: ", result.fetchall())


    # # Insert some data to database 'tsetmc' using 'execute' and 'executemany' commands
    # cursor.execute("""
    #     INSERT INTO tsetmc VALUES
    #     ('one', 2365855, 2365),
    #     ('two', 32365652, 235.9),
    #     ('three', 566666, 2361.5)
    # """)
    # sqliteConnection.commit()

    # new_rows = [
    #     ('four', 346543, 1256),
    #     ('five', 965352, 32.26),
    #     ('six', 154696, 25684.9)
    # ]
    # cursor.executemany("INSERT INTO tsetmc VALUES(?, ?, ?)", new_rows)
    # sqliteConnection.commit()


    # # some queries to get data from 'tsetmc' table
    # result = cursor.execute("SELECT * FROM tsetmc")
    # print("data: ", result.fetchall())

    # result = cursor.execute("SELECT title FROM tsetmc")
    # print("data: ", result.fetchall())

    # result = cursor.execute("SELECT title, volume FROM tsetmc ORDER BY volume")
    # print("data: ", result.fetchall())

    # result = cursor.execute("SELECT title, price FROM tsetmc ORDER BY price")
    # for row in result:
    #     print(row[0], "\t ===> \t", row[1])
    
    result = cursor.execute("SELECT title, volume, price FROM tsetmc ORDER BY volume DESC")
    for row in result:
        print(row[0],"(", row[2],")\t ===> \t", row[1])


	# Close the cursor
    cursor.close()

# Handle errors
except sqlite3.Error as error:
	print('Error occurred - ', error)

# Close DB Connection irrespective of success
# or failure
finally:

	if sqliteConnection:
		sqliteConnection.close()
		print('SQLite Connection closed')
