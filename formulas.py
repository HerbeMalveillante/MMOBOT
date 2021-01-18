import math



def levelFromXp(xp):
	return math.floor(0.1*(xp**(2/3)))

def xpFromLevel(level):
	return math.ceil((level/0.1)**1.5)
	
if __name__ == "__main__":

	print(levelFromXp(1000000))
	print(xpFromLevel(5000))

	for i in range(50):
		print(f"{xpFromLevel(i*20+1)-xpFromLevel(i*20)} xp from level {i*20} to level {i*20+1}")
