import psycopg2

# Try to connect

with open("gps_experimentation/"+ str(time) + "-grouped.txt") as f:
    for line in f:
        line = line.rstrip()
        spline = line.split(",")
        array.append(spline)
 # open the file to send
try:
    conn = psycopg2.connect("dbname='phyto' user='postgres' host='192.168.1.202' password='postgres' port='5433'")
except:
    print "unable to connect to the database."

conn = psycopg2.connect("dbname='phyto' user='postgres' host='192.168.1.202' password='postgres' port='5433'") #connect the DB
conn.autocommit = True
cur = conn.cursor()
cur.execute("""INSERT INTO parcelle (nom_parcelle, id_traitement) VALUES (array[1], '8');""") # SQL Query
conn.commit()
cur.execute("""SELECT * from parcelle""")
rows = cur.fetchall()
print "\nShow me the databases:\n"
for row in rows:
    print "   ", row[0],row[1]
