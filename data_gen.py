import mysql.connector
import random
import time
from datetime import datetime


#mysql connection config
config = {
    "user": "",
    "password" : "",
    "host" : "localhost",
    "database" : "dog_wash_V2",
}

def connect_db():
    return mysql.connector.connect(**config)

def product_levels(machine_id):
    return{
        "water_level" : round(random.uniform(10, 100),2),
        "soap_level": round(random.uniform(5,50), 2),
        "tick_remover_level": round(random.uniform(1, 30), 2),
    }

def sale(machine_id):
    amount = random.choice([10.0, 11.0, 12.0, 13.5])
    payment_type = random.choice(['cash', 'card', 'mobile'])
    return amount, payment_type

def insert_product_log(cursor, machine_id, water, soap, tick_remover_level):
    sql = """
    INSERT INTO product_log (machine_id, water_level, soap_level, tick_remover_level, timestamp)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (machine_id, water, soap, tick_remover_level, datetime.now()))

def insert_sale(cursor, machine_id, amount, payment_type):
    sql = """
    INSERT INTO sales_table (machine_id, amount, timestamp, payment_type)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (machine_id, amount, datetime.now(), payment_type))

def main():
    conn = connect_db()
    cursor = conn.cursor()

    machine_ids = [1,2,3]

    try:
        for _ in range(10):
            for machine_id in machine_ids:
                levels = product_levels(machine_id)
                insert_product_log(cursor, machine_id,
                                   levels["water_level"], levels["soap_level"], levels["tick_remover_level"])
                if random.random() < 0.5:
                    amount, payment_type = sale(machine_id)
                    insert_sale(cursor, machine_id, amount, payment_type)

            conn.commit()
            print("Cycle completed and data commmiteed.")
            time.sleep(5)
    except Exception as e:
        print("Error:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__== "__main__":
    main()

































                
