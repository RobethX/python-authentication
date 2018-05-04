import bcrypt
import getpass
import sqlite3
import sys
import time
import os
import base64

dbpath = 'accounts.db'

if os.path.isfile(dbpath):
    db = sqlite3.connect(dbpath)
else:
    print("Database could not be found.")
    time.sleep(3)
    sys.exit(0)

c = db.cursor()

username = input("Username: ")
password = base64.b64encode((getpass.getpass("Password: ") + "NaCl").encode()) #b64 to prevent it from ever being in plain (readable) text - is this useless?
hash = bcrypt.hashpw(password, bcrypt.gensalt(12))

c.execute("SELECT * FROM accounts WHERE username = ? COLLATE NOCASE", (username,))
data = c.fetchone()
if not data:
    if "y" in input('Account with username %s not found. Would you like to create a new account? [y/n]' %username).lower():
        email = input("Email address: ")
        c.execute("INSERT INTO accounts values (?,?,?,?,?)", [username, hash, email, int(time.time()), int(time.time())]) #set date accessed and date created to current time
        print("Account created.")
else:
    if bcrypt.checkpw(password, data[1]):
        print("Successfully authenticated credentials.")
        c.execute("UPDATE accounts SET time_last_accessed = ? WHERE username = ? COLLATE NOCASE", (int(time.time()), username,)) #update time accessed
    else:
        print("Password incorrect.")

password = None #clear out the password variable just to be safe

db.commit()
db.close()