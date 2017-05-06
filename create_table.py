import psycopg2

conn = psycopg2.connect(host="localhost", dbname="testpython",
                        user="vaibhavs10", password="v9811045972")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS employees (employee_id INT PRIMARY KEY, dependent_id INT REFERENCES employees);")
conn.commit()
c.execute("INSERT INTO employees VALUES (1,2), (2,4), (4,5), (8, NULL), (6, 26), (26,4), (5,8)")
conn.commit()
c.execute("CREATE TABLE IF NOT EXISTS employee_detail (employee_id INT PRIMARY KEY, join_date VARCHAR)")
conn.commit()
c.execute("INSERT INTO employee_detail VALUES (1, '10/11/2002'), (2, '10/11/2001'), (4, '10/11/2000'), (5, '10/11/1999'), (8, '10/11/1998'), (6, '10/11/2004'), (26, '10/11/2003') ")
conn.commit()
c.close()