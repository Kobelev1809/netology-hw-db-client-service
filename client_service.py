from database import Database


class ClientService:

    def __init__(self, db_name: str) -> None:
        self.db = Database(db_name)
        self.clients = {}
        self.phone_numbers = {}
        


if __name__ == '__main__':
    pass