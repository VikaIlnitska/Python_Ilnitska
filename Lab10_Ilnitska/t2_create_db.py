import psycopg2
from faker import Faker
import random

fake = Faker('uk_UA')

DB_HOST = "localhost"
DB_NAME = "market_db"
DB_USER = "postgres"
DB_PASSWORD = "7481"
DB_PORT = "5433"

def create_tables(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id SERIAL PRIMARY KEY,
                    company_name VARCHAR(150),
                    person_type VARCHAR(20) CHECK (person_type IN ('юридична', 'фізична')),
                    address TEXT,
                    phone VARCHAR(20),
                    contact_person VARCHAR(100),
                    bank_account VARCHAR(50)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    product_name VARCHAR(150) NOT NULL,
                    price NUMERIC(10, 2) NOT NULL,
                    stock_quantity INTEGER NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales (
                    id SERIAL PRIMARY KEY,
                    sale_date DATE NOT NULL,
                    client_id INTEGER REFERENCES clients(id),
                    product_id INTEGER REFERENCES products(id),
                    quantity_sold INTEGER NOT NULL,
                    discount INTEGER CHECK (discount BETWEEN 3 AND 20),
                    payment_method VARCHAR(20) CHECK (payment_method IN ('готівковий', 'безготівковий')),
                    delivery_required BOOLEAN,
                    delivery_cost NUMERIC(10, 2)
                )
            """)
            conn.commit()
            print("Tables successfully created.")
    except Exception as e:
        print(f"Error while creating tables: {e}")
        conn.rollback()

def populate_data(conn):
    try:
        with conn.cursor() as cursor:
            person_types = ['юридична', 'фізична']
            client_ids = []
            for _ in range(4):
                company = fake.company()
                p_type = random.choice(person_types)
                address = fake.address().replace('\n', ', ')
                phone = fake.numerify(text='+380(##)###-##-##')
                contact = fake.name()
                account = fake.iban()
                
                cursor.execute("""
                    INSERT INTO clients (company_name, person_type, address, phone, contact_person, bank_account)
                    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
                """, (company, p_type, address, phone, contact, account))
                client_ids.append(cursor.fetchone()[0])

            product_ids = []
            for _ in range(10):
                name = fake.word().capitalize() + " " + fake.word()
                price = round(random.uniform(10.0, 5000.0), 2)
                quantity = random.randint(10, 100)
                
                cursor.execute("""
                    INSERT INTO products (product_name, price, stock_quantity)
                    VALUES (%s, %s, %s) RETURNING id
                """, (name, price, quantity))
                product_ids.append(cursor.fetchone()[0])

            payment_methods = ['готівковий', 'безготівковий']
            for _ in range(19):
                sale_date = fake.date_this_year()
                client_id = random.choice(client_ids)
                product_id = random.choice(product_ids)
                qty_sold = random.randint(1, 5)
                discount = random.randint(3, 20)
                pay_method = random.choice(payment_methods)
                delivery = fake.boolean()
                delivery_cost = round(random.uniform(50.0, 300.0), 2) if delivery else 0.0

                cursor.execute("""
                    INSERT INTO sales (sale_date, client_id, product_id, quantity_sold, discount, payment_method, delivery_required, delivery_cost)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (sale_date, client_id, product_id, qty_sold, discount, pay_method, delivery, delivery_cost))

            conn.commit()
            print("Data successfully created and loaded to DB.")
    except Exception as e:
        print(f"Error while entering data: {e}")
        conn.rollback()

if __name__ == "__main__":
    connection = None
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        print("The database connection was successful.")
        
        create_tables(connection)
        populate_data(connection)
        
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
    finally:
        if connection:
            connection.close()
            print("The connection is closed.")