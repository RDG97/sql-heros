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
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def select_all():
    query = """
        SELECT * from heroes
    """

    list_of_heroes = execute_query(query).fetchall()
    
    for record in list_of_heroes:
        print(record[1])



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
        

#select_all()
#create_new_hero()
#kill_hero()

def kill_hero():
    dyingStar = input('who should die?: ')
    test = ''
    print(dyingStar, "'s time has come")
    query = """
        DELETE FROM heroes WHERE name=%s;
    """
    kill_hero = execute_query(query, (dyingStar,)).fetchall()


def list_friendships():
    query = """
            SELECT * FROM heroes, relationships
            WHERE heroes.id = relationships.hero1_id               
            """
    buddybuddy = execute_query(query).fetchall()
    print(buddybuddy[1][1])
    for x in range(len(buddybuddy)):
        if buddybuddy[x][8] == 1:
            relStat = f"{bcolors.OKCYAN} friends{bcolors.ENDC}"
        else:
            relStat = f"{bcolors.FAIL}enemies{bcolors.ENDC}"
        hero1Name = str(buddybuddy[x][1])
        hero2id = int(buddybuddy[x][7])
        hero2Name = str(buddybuddy[hero2id][1])
        print(hero1Name, f"{bcolors.WARNING} and{bcolors.ENDC}", hero2Name, f"{bcolors.WARNING} and{bcolors.ENDC}", relStat)

#list_friendships()

def make_friends():
    query = """
            SELECT * FROM heroes
            """
    heroes = execute_query(query).fetchall()
    for record in heroes:
        print(record[1], 'id:', record[0])
    print(f"{bcolors.WARNING} here is a list of heroes and their ids{bcolors.ENDC}")
    firsthero = input(f"{bcolors.WARNING}enter the first heroes ID: {bcolors.ENDC}")
    secondhero = input(f"{bcolors.WARNING}now enter the second heroes id: {bcolors.ENDC}")
    stat = input(f"{bcolors.WARNING}now how do they feel about each other? (1 for friends 2 for enemies): {bcolors.ENDC}")

    query = """
        INSERT INTO relationships (hero1_id, hero2_id, relationship_type_id)
        VALUES (%s, %s, %s);
            """
    execute_query(query, (firsthero, secondhero, stat))
    print(f"{bcolors.OKGREEN}Success! do {bcolors.ENDC}{bcolors.OKBLUE}'list_friendships'{bcolors.ENDC}{bcolors.OKGREEN} to see the new connection{bcolors.ENDC}")




def king_prompt():
    whatdo = input(f"{bcolors.WARNING}What would you like to do? (type 'help' for options): ")
    if whatdo == 'list_friendships':
        list_friendships()
        king_prompt()
    elif whatdo == 'kill_hero':
        kill_hero()
        king_prompt()
    elif whatdo == 'create_new_hero':
        create_new_hero()
        king_prompt()
    elif whatdo == 'help':
        mls = """function option(s):
            list_friendships(),
            kill_hero(),
            create_new_hero(),
            make_friends(),
            stop
            """
        print(mls)
        king_prompt()
    elif whatdo == 'make_friends':
        make_friends()
        king_prompt()
    elif whatdo == 'stop':
        print(f"{bcolors.OKGREEN}STOPPED{bcolors.ENDC}")
    else:
        print(f"{bcolors.FAIL}oops i dont think you typed what you meant to type. type 'help' for options{bcolors.ENDC}")
        king_prompt()

king_prompt()

