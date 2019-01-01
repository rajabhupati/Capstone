from __future__ import print_function

import pymysql

conn = pymysql.connect(host='retailapp.chhkxmzfw1fy.us-east-1.rds.amazonaws.com', port=3306, user='admin1', passwd='Veri1899$', db='retaildb')

cur = conn.cursor()

cur.execute("SELECT * FROM products")

print(cur.description)

print()

for row in cur:
    print(row)

cur.close()
conn.close()
