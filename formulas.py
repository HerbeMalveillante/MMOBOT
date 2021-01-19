# This module contains all the functions that calculates the drop rates based on user's stats.

import math
import random



def levelFromXp(xp):
	return math.floor(0.1*(xp**(2/3)))

def xpFromLevel(level):
	return math.ceil((level/0.1)**1.5)

def automaticGold(xp):
	level = levelFromXp(xp)
	
	low = (level/2)
	high = (level*1.5)
	gold = random.randint(int(low) if low >= 1 else 1 , int(high) if high >= 2 else 2)
	return gold
	
if __name__ == "__main__":

	print("Level = 1000")
	xp = xpFromLevel(1000)
	
	for i in range(5):
	
		total = 0
		for i in range(10000):
			total+=automaticGold(xp)
		print(f"Average Gold given : {int(total/10000)}")
