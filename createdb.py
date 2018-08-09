import sqlite3

conn = sqlite3.connect("temp.db")

c = conn.cursor()

c.execute('''CREATE TABLE "companies" (
    [companyId] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [name] VARCHAR(20)
)''')

c.execute('''CREATE TABLE "employees" (
    [employeeId] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    [name] VARCHAR(20),
    [companyId] INTEGER,
    FOREIGN KEY ([companyId]) REFERENCES "companies" ([companyId])
)''')

companies = [(1, 'OpenBet'), (2, 'Facebook'), (3, 'Google')]
employees = [(1, 'Dimitris', 1), (2, 'Billos', 2), (3, 'Ilibee', 3)]

c.executemany('insert into companies values (?, ?)', companies)
c.executemany('insert into employees values (?, ?, ?)', employees)

conn.commit()
conn.close()
