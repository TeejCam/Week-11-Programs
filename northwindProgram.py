import sqlite3

def displayTables():
    try:
        conn = sqlite3.connect('/Users/melissachamalan/Documents/northwind.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        print("Tables in Northwind database:")
        for index, table in enumerate(tables, start=1):
            print(f"{index}. {table[0]}")

        return tables
    except sqlite3.Error as e:
        print(f"Error fetching tables: {e}")
    finally:
        if conn:
            conn.close()

# displays the records to the user
def displayTableRecords(tableName):
    try:
        conn = sqlite3.connect('/Users/melissachamalan/Documents/northwind.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {tableName}")
        rows = cursor.fetchall()

        columns = [description[0] for description in cursor.description]

        print(f"\nRecords from {tableName} table: ")
        print(columns)

        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(f"Error fetching records from {tableName}: {e}")
    finally:
        if conn:
            conn.close()

# User can insert a record into the table
def insertRecord(tableName):
    try:
        conn = sqlite3.connect('/Users/melissachamalan/Documents/northwind.db')
        cursor = conn.cursor()

        columns = input(f"Enter column names for {tableName} (comma separated): ")
        values = input(f"Enter values for {tableName} (comma separated): ")

        columnsList = [column.strip() for column in columns.split(",")]
        valuesList = [value.strip() for value in values.split(",")]

        if len(columnsList) != len(valuesList):
            print("Column names and values must be of the same length")
            return

        # using placeholders for the values
        placeholders = ', '.join(['?'] * len(valuesList))
        data = f"INSERT INTO {tableName} ({', '.join(columnsList)}) VALUES ({placeholders})"
        cursor.execute(data, valuesList)

        conn.commit()
        print(f"Record inserted into {tableName} table.")
    except sqlite3.Error as e:
        print(f"Error inserting record into {tableName}: {e}")
    finally:
        if conn:
            conn.close()

# User can update records
def updateRecord(tableName):
    try:
        conn = sqlite3.connect('/Users/melissachamalan/Documents/northwind.db')
        cursor = conn.cursor()

        cursor.execute(f"PRAGMA table_info({tableName})")
        columns = cursor.fetchall()
        columnNames = [column[1] for column in columns]

        print("Existing columns: ", columnNames)

        recordID = input("\nEnter ID of what you want to update: ")
        columnName = input("Enter column name: ")
        if columnName not in columnNames:
            print(f"Column '{columnName}' does not exist in the table.")
            return

        newValue = input(f"Enter new value for {columnName}: ")

        cursor.execute(f"PRAGMA table_info({tableName});")
        #getting the primary key column name
        pkColumn = [col for col in cursor.fetchall() if col[5] == 1][0][1]

        data = f"UPDATE {tableName} SET {columnName} = ? WHERE {pkColumn} = ?"
        cursor.execute(data, (newValue, recordID))

        conn.commit()
        print(f"Record in {tableName} table updated.")
    except sqlite3.Error as e:
        print(f"Error updating record in {tableName}: {e}")
    finally:
        if conn:
            conn.close()

# User can delete record
def deleteRecord(tableName):
    try:
        conn = sqlite3.connect('/Users/melissachamalan/Documents/northwind.db')
        cursor = conn.cursor()

        cursor.execute(f"PRAGMA table_info({tableName});")
        columns = cursor.fetchall()
        columnNames = [column[1] for column in columns]

        print("Existing columns: ", columnNames)

        recordID = input("\nEnter ID of what you want to delete: ")

        cursor.execute(f"PRAGMA table_info({tableName});")
        pkColumn = [col for col in cursor.fetchall() if col[5] == 1][0][1]

        data = f"DELETE FROM {tableName} WHERE {pkColumn} = ?"
        cursor.execute(data, (recordID,))

        conn.commit()
        print(f"Record in {tableName} table deleted.")
    except sqlite3.Error as e:
        print(f"Error deleting record from {tableName}: {e}")
    finally:
        if conn:
            conn.close()


def main():
    tables = displayTables()

    # Ensuring user enters a valid table index
    while True:
        try:
            tableChoice = int(input("\nSelect a table to see contents (enter number): ")) - 1
            selectedTable = tables[tableChoice][0]
            break
        except (ValueError, IndexError):
            print("Invalid input, please select a valid table number.")

    displayTableRecords(selectedTable)

    insertRecord(selectedTable)
    updateRecord(selectedTable)
    deleteRecord(selectedTable)

# entry point of program
if __name__ == "__main__":
    main()