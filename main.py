import discord, sqlite3

class DB:
    # Class Initialization
    def __init__(self, id: int):
        self.id = id

        # SQLite Database Connection
        self.connection = sqlite3.connect("data.db", isolation_level=None)
        self.cursor = self.connection.cursor()

        # Create table if not exist
        self.cursor.execute("""CREATE TABLE if not Exists Gumpu
               (ID INTEGER, Coins INTEGER, BTC INTEGER, ETH INTEGER, Date INTEGER)""")
        self.cursor.execute(f"SELECT EXISTS(SELECT Coins FROM Gumpu WHERE ID={id})")

        # Create row if not exist
        if not self.cursor.fetchone():
            self.cursor.execute(f"INSERT INTO Gumpu VALUES({id}, 0, 0, 0, 0)")

    # Fetching Data
    def fetch(self, key: str) -> int:
        self.cursor.execute(f"SELECT {key} FROM Gumpu WHERE ID={self.id}")
        return self.cursor.fetchone()

    # Updating Data
    def update(self, key: str, value: str):
        self.cursor.execute(f"UPDATE Gumpu SET {key}={value} WHERE ID={self.id}")

    # Auto-closing SQLite Database
    def __exit__(self):
        self.connection.close()

client = discord.Client()
token = ''

@client.event
async def on_ready():
    print(client.user.name + ", Starting Now...")
    await client.change_presence(activity = discord.Game("공놀이"))

client.run(token)