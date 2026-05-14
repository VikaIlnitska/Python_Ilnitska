import psycopg2

DB_HOST = "localhost"
DB_NAME = "market_db"
DB_USER = "postgres"
DB_PASSWORD = "7481"
DB_PORT = "5433"

ukr_alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
letter_weights = {char: idx for idx, char in enumerate(ukr_alphabet)}

def ukrainian_sort_key(item):
    name = str(item).lower()
    return [letter_weights.get(char, 999) for char in name]

def print_formatted_table(headers, rows):
    if not rows:
        print("No data to display.\n")
        return
    
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell) if cell is not None else ""))

    row_format = " | ".join([f"{{:<{w}}}" for w in col_widths])
    
    separator = "-" * (sum(col_widths) + 3 * len(headers) - 1)
    print(separator)
    print(row_format.format(*headers))
    print(separator)
    for row in rows:
        formatted_row = ["" if cell is None else str(cell) for cell in row]
        print(row_format.format(*formatted_row))
    print(separator)
    print()

def main():
    try:
        with psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT) as conn:
            with conn.cursor() as cursor:

                print("\nDisplay tables:")
                tables = ['clients', 'products', 'sales']
                for table in tables:
                    print(f"Table {table}:")
                    cursor.execute(f"""
                        SELECT column_name, data_type 
                        FROM information_schema.columns 
                        WHERE table_name = '{table}'
                    """)
                    cols = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    print_formatted_table(cols, rows)

                print("\nData:")
                for table in tables:
                    print(f"\nДані таблиці {table}:")
                    cursor.execute(f"SELECT * FROM {table}")
                    cols = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    print_formatted_table(cols, rows)

                print("\nQueries")

                print("\n1. Продажі, оплачені готівкою (відсортовано за назвою клієнта):")
                cursor.execute("""
                    SELECT s.id, s.sale_date, c.company_name, p.product_name, s.payment_method
                    FROM sales s
                    JOIN clients c ON s.client_id = c.id
                    JOIN products p ON s.product_id = p.id
                    WHERE s.payment_method = 'готівковий'
                """)
                cols = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()               
                rows.sort(key=lambda x: ukrainian_sort_key(x[2]))
                print_formatted_table(cols, rows)

                print("\n2. Продажі, по яких потрібна була доставка:")
                cursor.execute("""
                    SELECT s.id, s.sale_date, c.company_name, p.product_name, s.delivery_required, s.delivery_cost
                    FROM sales s
                    JOIN clients c ON s.client_id = c.id
                    JOIN products p ON s.product_id = p.id
                    WHERE s.delivery_required = TRUE
                """)
                print_formatted_table([desc[0] for desc in cursor.description], cursor.fetchall())

                print("\n3. Сума та сума з урахуванням знижки для кожного клієнта:")
                cursor.execute("""
                    SELECT c.company_name,
                           ROUND(SUM(s.quantity_sold * p.price + COALESCE(s.delivery_cost, 0)), 2) AS total_sum,
                           ROUND(SUM((s.quantity_sold * p.price * (1 - s.discount / 100.0)) + COALESCE(s.delivery_cost, 0)), 2) AS total_discounted
                    FROM sales s
                    JOIN clients c ON s.client_id = c.id
                    JOIN products p ON s.product_id = p.id
                    GROUP BY c.company_name
                """)
                print_formatted_table([desc[0] for desc in cursor.description], cursor.fetchall())

                print("\n4. Всі покупки вказаного клієнта (запит з параметром, ID=1):")
                target_client_id = 1
                cursor.execute("""
                    SELECT s.id, s.sale_date, p.product_name, s.quantity_sold
                    FROM sales s
                    JOIN products p ON s.product_id = p.id
                    WHERE s.client_id = %s
                """, (target_client_id,))
                print_formatted_table([desc[0] for desc in cursor.description], cursor.fetchall())

                print("\n5. Кількість покупок, які здійснив кожен клієнт:")
                cursor.execute("""
                    SELECT c.company_name, COUNT(s.id) AS purchases_count
                    FROM sales s
                    JOIN clients c ON s.client_id = c.id
                    GROUP BY c.company_name
                """)
                print_formatted_table([desc[0] for desc in cursor.description], cursor.fetchall())

                print("\n6. Сума розрахунку готівкою та безготівково (перехресний запит):")
                cursor.execute("""
                    SELECT c.company_name,
                           ROUND(SUM(CASE WHEN s.payment_method = 'готівковий' 
                                          THEN (s.quantity_sold * p.price * (1 - s.discount / 100.0)) + COALESCE(s.delivery_cost, 0) 
                                          ELSE 0 END), 2) AS cash_total,
                           ROUND(SUM(CASE WHEN s.payment_method = 'безготівковий' 
                                          THEN (s.quantity_sold * p.price * (1 - s.discount / 100.0)) + COALESCE(s.delivery_cost, 0) 
                                          ELSE 0 END), 2) AS cashless_total
                    FROM sales s
                    JOIN clients c ON s.client_id = c.id
                    JOIN products p ON s.product_id = p.id
                    GROUP BY c.company_name
                """)
                print_formatted_table([desc[0] for desc in cursor.description], cursor.fetchall())

    except psycopg2.Error as e:
        print(f"Error while work with DB: {e}")

if __name__ == "__main__":
    main()