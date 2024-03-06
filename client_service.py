import psycopg2


class Database:

    def __init__(self, db_name: str, user: str, password: str):
        self.conn = psycopg2.connect(
            database=db_name, user=user, password=password
        )
    
    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute(
                '''
                DROP TABLE IF EXISTS
                       clients,
                       phone_numbers;
                '''
            )
            cur.execute(
                '''
                CREATE TABLE IF NOT EXISTS Clients (
                    client_id  SERIAL      PRIMARY KEY,
                    first_name VARCHAR(30) NOT NULL,
                    last_name  VARCHAR(30) NOT NULL,
                    email      VARCHAR(30) NOT NULL UNIQUE
                );
                '''
            )
            cur.execute(
                '''
                CREATE TABLE IF NOT EXISTS Phone_numbers (
                    number_id    SERIAL      PRIMARY KEY,
                    phone_number VARCHAR(20) DEFAULT NULL,
                    client_id    INTEGER     NOT NULL,
                                 CONSTRAINT client_id
                                 FOREIGN KEY (client_id)
                                 REFERENCES clients
                                 ON DELETE CASCADE
                );
                '''
            )
        self.conn.commit()

    def add_client(self, name: str, surname: str, email: str):
        with self.conn.cursor() as cur:
            cur.execute(
                '''
                   INSERT INTO clients (first_name, last_name, email)
                   VALUES (%s, %s, %s)
                RETURNING client_id, first_name, last_name, email;
                ''',
                (name, surname, email)
            )
            print('Добавлен пользователь:')
            print(*cur.fetchone())
        self.conn.commit()
    
    def add_phone_number(self, phone_number: str, client_id: int):
        with self.conn.cursor() as cur:
            cur.execute(
                '''
                   INSERT INTO phone_numbers (phone_number, client_id)
                   VALUES (%s, %s)
                RETURNING number_id, phone_number, client_id;
                ''',
                (phone_number, client_id)
            )
            print('Добавлен телефон:')
            print(*cur.fetchone())
        self.conn.commit()

    def change_client_data(self, client_id: int, new_name: str):
        with self.conn.cursor() as cur:
            cur.execute(
                '''
                   UPDATE clients
                      SET first_name = %s
                    WHERE client_id = %s
                RETURNING first_name;
                ''',
                (new_name, client_id)
            )
            print('Новое имя клиента:', end=' ')
            print(*cur.fetchone())
        self.conn.commit()

    def del_phone_number(self, phone_number: str):
        with self.conn.cursor() as cur:
            cur.execute(
                '''
                   DELETE FROM phone_numbers
                    WHERE phone_number = %s
                RETURNING number_id, phone_number;
                ''',
                (phone_number,)
            )
            print('Удалён номер телефона:')
            print(*cur.fetchone())
        self.conn.commit()

    def del_client(self, client_id):
        with self.conn.cursor() as cur:
            cur.execute(
                '''
                DELETE FROM clients
                WHERE client_id = %s
                RETURNING first_name, last_name, email;
                ''',
                (client_id,)
            )
            print('Удалён клиент:')
            print(*cur.fetchone())
        self.conn.commit()

    def get_client_data(self, client_id: int) -> tuple:
        with self.conn.cursor() as cur:
            cur.execute(
                '''
                SELECT c.first_name, c.last_name, c.email, pn.phone_number
                  FROM clients c
                       LEFT JOIN phone_numbers pn
                       ON c.client_id = pn.client_id
                WHERE c.client_id = %s;
                ''',
                (client_id,)
            )
            return cur.fetchone()

    def show_all_data(self):
        with self.conn.cursor() as cur:
            cur.execute(
                '''
                SELECT *
                  FROM clients c
                       LEFT JOIN phone_numbers pn
                       ON c.client_id = pn.client_id
                 ORDER BY c.client_id;
                '''
            )
            print('Данные всех таблиц:')
            print('-' * 100)
            for person in cur.fetchall():
                print('|', end=' ')
                print(*person, sep=' | ', end='')
                print(' |')
                print('-' * 100)
        self.conn.commit()

    def __del__(self) -> None:
        self.conn.close()
        print('База закрыта')


if __name__ == '__main__':
    db_name, user, password = 'client_db', 'postgres', 'KiaPostgre1809',
    db = Database(db_name, user, password)
    print('Доступ к базе открыт:', '\n')
    
    db.create_tables()
    
    db.add_client('Igor', 'First', 'dasfa@con')
    db.add_client('Sasha', 'Second', 'iasiffa@con')
    db.add_client('Tania', 'Matiania', 'sdfsd@con')
    
    db.add_phone_number('823943243', 1)
    db.add_phone_number('239342383', 1)
    db.add_phone_number('234234324', 3)
    db.add_phone_number('234322355', 3)

    print('\nДанные клиента №1 до изменения:')
    print(*db.get_client_data(1))
    print('\nМеняем имя клиента №1 на Ivan...')
    db.change_client_data(1, 'Ivan')
    print('\nДанные клиента №1 после изменения:')
    print(*db.get_client_data(1))
    print()
    db.show_all_data()
    db.del_phone_number('234234324')
    print()
    db.show_all_data()
    db.del_client(1)
    print()
    db.show_all_data()
