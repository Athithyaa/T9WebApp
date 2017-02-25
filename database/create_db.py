from sqlalchemy import create_engine


# fill out the path to sqlite engine
def get_username(file):
    f = open(file)
    uname = ""
    pword = ""
    host = ""
    for line in f:
        split_str = line.split("=")
        if split_str[0] == "username":
            uname = split_str[1]
        if split_str[0] == "password":
            pword = split_str[1]
        if split_str[0] == "host":
            host = split_str[1]
    return [uname, pword, host]


file = "../database/config.properties"
config = get_username(file)
engine = create_engine('postgresql+psycopg2://' + config[0].replace("\n", "") + ':' + config[1].replace("\n", "") +
                       '@' + config[2].replace("\n", "") + '/postgres')
conn = engine.connect()
conn.execute("commit")
conn.execute("create database t9_db")
conn.close()
