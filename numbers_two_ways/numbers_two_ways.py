num_list = [12, 7, 22, 3, 14, 9, 31, 5, 18, 7]

def count(_list):
    _count = 0
    for num in _list:
        _count += 1

    return _count

def my_sum(_list):
    total = 0
    for num in _list:
        total += num

    return total

def avg(_list):
    _count = count(_list)
    total = my_sum(_list)
    avg = total / _count
    return avg

def minimum(_list):
    _minimum = _list[0]
    for num in _list:
        if _minimum > num:
            _minimum = num
    
    return _minimum

def maximum(_list):
    _maximum = _list[0]
    for num in _list:
        if _maximum < num:
            _maximum = num
    
    return _maximum

def python_version():
    result = (count(num_list), my_sum(num_list), avg(num_list), minimum(num_list), maximum(num_list))
    return result

# SQLite Version

import sqlite3

def insert_many_values(table_name, column_name, list_of_values, _cursor):
    for num in list_of_values:    
        _cursor.execute(
            f"""
            INSERT INTO {table_name} ({column_name})
            VALUES (?)
            """, (num, )
        )

def sqlite_version():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS numbers (
        value INTEGER
        );
        """
    )
        
    insert_many_values("numbers", "value", num_list, cur)

    result = cur.execute(
        """
        SELECT 
        COUNT(value) as Count,
        SUM(value) as Sum,
        AVG(value) as Average,
        MIN(value) as Minimum,
        MAX(value) as Maximum
        FROM numbers;
        """
    ).fetchone()

    cur.execute(
        """
        DROP TABLE numbers;
        """
    )

    conn.commit()
    conn.close()

    return result

if __name__ == "__main__":
    py_result = python_version()
    sql_result = sqlite_version()

    from math import isclose

    print(" ---- Comparison between Python and SQLite ---- ")
    print(f"Count: {"EQUAL" if py_result[0] == sql_result[0] else "DIFFERENT"}")
    print(f"Sum: {"EQUAL" if py_result[1] == sql_result[1] else "DIFFERENT"}")
    print(f"Average: {"EQUAL" if isclose(py_result[2], sql_result[2]) else "DIFFERENT"}")
    print(f"Minimum: {"EQUAL" if py_result[3] == sql_result[3] else "DIFFERENT"}")
    print(f"Maximum: {"EQUAL" if py_result[4] == sql_result[4] else "DIFFERENT"}")