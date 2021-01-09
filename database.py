import sqlite3
import json
from log import log


def create_table():
	curseur.execute("""CREATE TABLE IF NOT EXISTS userdata
	(id integer, Exp integer, Gold integer, Energy integer, Diamonds integer,
	 Weapon integer, Armor integer, Backpack integer, 
	 Attack integer, Defense integer, Stamina integer,
	 Wood integer, Fabric integer, Iron integer, Rock integer, Orb integer, Emerald integer, Oil integer, Obsidian integer, Seeds int, Antimatter int)""")
	connexion.commit()

def get_userdata(user_id, stat):
	if does_account_exists(user_id):
		curseur.execute(f"SELECT {stat} FROM userdata WHERE id = {user_id}")
		return curseur.fetchone()
	else :
		log(f"[DATABASE] can't get userdata from {user_id} : account not found")
		return "We could not retrieve any informations about the user or the stat you're searching for.\nPlease check your command or create a profile to get started."

def _force_get_userdata(user_id, stat):
	curseur.execute(f"SELECT {stat} FROM userdata WHERE id = {user_id}")
	return curseur.fetchone()

def get_profile(user_id):
	if does_account_exists(user_id):
		curseur.execute(f"SELECT * FROM userdata WHERE id = ?", (user_id,))
		return curseur.fetchone()
	else:
		log(f"[DATABASE] can't get userdata from {user_id} : account not found")
		return ["We could not retrieve any informations about the user or the stat you're searching for.\nPlease check your command or create a profile to get started."]

def _get_whole_database():
	curseur.execute("SELECT * from userdata")
	return curseur.fetchall()

def print_whole_database():
	for i in _get_whole_database():
		print(str(i))

def modify_userdata(user_id, stat, value, print=True):
	curseur.execute(f"UPDATE userdata SET {stat} = {value} WHERE id = {user_id}")
	connexion.commit()
	if print:
		log(f"[DATABASE] modified userdata for user {user_id} : {stat} got a value of {value}")

def increment_energy(print=True):
	curseur.execute("UPDATE userdata SET Energy = Energy +1 WHERE Energy < Stamina*10")
	connexion.commit()

def does_account_exists(user_id):
	curseur.execute(f"SELECT * FROM userdata WHERE id = ?", (user_id,))
	result = curseur.fetchone()
	return not result == None

def delete_user_account(user_id):
	if does_account_exists(user_id):
		curseur.execute(f"DELETE FROM userdata WHERE id = {user_id}")
		connexion.commit()
		log(f"[DATABASE] deleted account number {user_id}")
	else : 
		log(f"[DATABASE] Could not delete : user {user_id} not found in the database")


def create_account(user_id):
	if not does_account_exists(user_id):
		curseur.execute("INSERT INTO userdata VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, 0, 0, 10, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
		log(f"[DATABASE] Created account for user {user_id}")
		connexion.commit()
	else :
		log(f"[DATABASE] The user {user_id} already is in the database")

def get_all_ids():
	curseur.execute("SELECT id FROM userdata")
	listIds = curseur.fetchall()
	return listIds

def get_player_number():
	curseur.execute("SELECT COUNT(*) FROM userdata")
	number = curseur.fetchone()[0]
	return number

def increase_userdata(user_id, stat, value, print=True):
	curseur.execute(f"UPDATE userdata SET {stat} = {stat}+{value} WHERE id = {user_id}")
	connexion.commit()
	if print:
		log(f"[DATABASE] increased userdata for user {user_id} : {stat} increased by {value}")


log("[DATABASE] database module loaded")

connexion = sqlite3.connect("database.db")
log("[DATABASE] connected to the database")
curseur = connexion.cursor()
log("[DATABASE] cursor created")
create_table()
log("[DATABASE] table created/loaded")
