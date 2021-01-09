import datetime

def log(content):  # modified print() function that adds the hour to the print. More convenient for logging purposes.
    print(str(datetime.datetime.utcnow())[11:19] + " : " + content)