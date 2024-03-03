import psycopg2


class Database:

    def __init__(self, db_name: str,
                 user='postgres',
                 password='KiaPostgre1809') -> None:
        self.conn = psycopg2.connect(database='client_db',
                                   user=user,
                                   password=password)
    
    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute(
                '''DROP TABLE IF EXISTS
                       clients,
                       phone_numbers;
                CREATE TABLE IF NOT EXISTS Clients (
                    client_id  SERIAL      PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name  VARCHAR(50) NOT NULL,
                    email      VARCHAR(70) NOT NULL UNIQUE
                );
                CREATE TABLE IF NOT EXISTS Phone_numbers (
                    number_id    SERIAL      PRIMARY KEY,
                    phone_number VARCHAR(20) DEFAULT NULL,
                    client_id    INTEGER     NOT NULL,
                                CONSTRAINT client_id
                                FOREIGN KEY (client_id)
                                REFERENCES clients
                                ON DELETE CASCADE
                );'''
            )
        self.conn.commit()
    
    def add_client(self, name: str, surname: str, email: str):
        pass
    
    def add_phone_number(self, client_id):
        pass
    
    def change_client_data(self, **kwarg):
        pass
    
    def del_phone_number(self):
        pass
    
    def del_client(self):
        pass
    
    def get_client_data(self):
        pass    
    
    def __del__(self) -> None:
        self.conn.close()
        print('База закрыта')


if __name__ == '__main__':
    db = Database('client_id')
    print('создали объект базы')
    db.create_tables()

