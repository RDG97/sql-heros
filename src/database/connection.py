import psycopg
from psycopg import OperationalError

def create_connection(db_name, db_user, db_password, db_host = "localhost", db_port = "5432"):
    connection = None
    try:
        connection = psycopg.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(query, params=None):
    connection = create_connection("postgres", "postgres", "postgres")
    cursor = connection.cursor()
    # try:
    cursor.execute(query, params)
    connection.commit()
    print("Query executed successfully")
    connection.close()
    return cursor
    # except OSError as e:
    #     print(f"The error '{e}' occurred or the hero name is already taken")

# create_connection('postgres', 'postgres', 'postgres')

# ====================================== EDIT BELOW HERE


def select_all():
    query = """
        SELECT * from heroes
    """

    list_of_heroes = execute_query(query).fetchall()
    print(list_of_heroes)
    for record in list_of_heroes:
        print(record[1])

# select_all()

def create_new_hero():
    newName = input('New hero name: ')
    newAbout = input('now give them a brief description: ')
    newBio = input('Lastley, give them a bio: ')
    print('new name will be: ', newName)
    print('new about_me will be: ', newAbout)
    print('bio will be: ', newBio)
    query = """
        INSERT INTO heroes (name, about_me, biography)
        VALUES (%s, %s, %s);
    """
    try: 
        execute_query(query, (newName, newAbout, newBio))
        print(f"Hero {newName} was born!")
    except:
        print('Sorry that didnt work')
        


create_new_hero()

def kill_hero():
    dyingStar = input('who should die?: ')
    test = ''
    print(dyingStar, "'s time has come")
    query = """
        DELETE FROM heroes WHERE name=%s;
    """
    kill_hero = execute_query(query, (dyingStar,)).fetchall()

# kill_hero()