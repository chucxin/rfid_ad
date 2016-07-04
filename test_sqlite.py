import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


conn = sqlite3.connect('userdata.db')
conn.row_factory = dict_factory

c = conn.cursor()

# c.execute('''INSERT INTO test (name, phone) VALUES("Lhasa", "0937173775")''')

# conn.commit()


c.execute('SELECT * FROM test')
r = c.fetchall()

for i in r:
    print(i["name"])


#for row in c:
#    print(row['name'])


conn.close()
