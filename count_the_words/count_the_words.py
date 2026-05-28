import sqlite3
import json

paragraph = """the quick brown fox jumps over the lazy dog
the dog barks at the fox
the fox runs away from the dog
the quick fox is quick and the lazy dog is lazy"""

def convert_doc_string_to_word_list(doc_string):
    word_list = doc_string.split()
    return word_list

def count_words(word_list):
    word_count_dict = {}
    for word in word_list:
        word_count_dict[word] = word_count_dict.get(word, 0) + 1
        
    return word_count_dict

def sort_counted_words(word_count):
    sorted_dict = sorted(word_count.items(), key=lambda item: (-item[1], item[0]))
    return sorted_dict

def python_version():
    word_list = convert_doc_string_to_word_list(paragraph)
    word_count = count_words(word_list)
    sorted_word_count = sort_counted_words(word_count)
    return sorted_word_count

# SQLite

def insert_many_values(table_name, column_name, list_of_values, _cursor):
    for word in list_of_values:    
        _cursor.execute(
            f"""
            INSERT INTO {table_name} ({column_name})
            VALUES (?)
            """, (word, )
        )

def sql_version():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS words(
        word TEXT
        );
        """
    )

    word_list = convert_doc_string_to_word_list(paragraph)
    insert_many_values("words", "word", word_list, cur)

    results = cur.execute(
        """
        SELECT 
        word,
        COUNT(*) AS word_count 
        FROM words
        GROUP BY word
        ORDER BY word_count DESC, word ASC;
        """
    ).fetchall()

    cur.execute("DROP TABLE words;")

    conn.commit()
    conn.close()

    return results

if __name__ == "__main__":
    py_results = python_version()
    sql_results = sql_version()

    print(" ---- PYTHON ---- ")
    print(json.dumps(dict(py_results), indent=4))

    print("\n")
    print(" ---- SQL ---- ")
    print(json.dumps(dict(sql_results), indent=4))

    print("\n")
    print(" ---- Comparison ---- ")
    print("EQUAL" if py_results == sql_results else "DIFFERENT")