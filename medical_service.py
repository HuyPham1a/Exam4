import mysql.connector
from mysql.connector import Error
from datetime import datetime

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='medical_service',
            user='root',  
            password='password'  
        )
        if connection.is_connected():
            print("Connected to the database")
            return connection
    except Error as e:
        print("Error while connecting to database", e)
        return None

def add_patients(connection):
    cursor = connection.cursor()
    patients = [
        ('Nguyen A', '2010-01-01', 'Male', 'Ha Noi', '0123456789', 'a@gmail.com'),
        ('Nguyen B', '1990-02-02', 'Female', 'Ha Noi', '0987654321', 'b@gmail.com'),
        ('Nguyen C', '1985-03-03', 'Male', 'Ha Noi', '0112233445', 'c@gmail.com')
    ]
    for patient in patients:
        query = "INSERT INTO patients (full_name, date_of_birth, gender, address, phone_number, email) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, patient)
    connection.commit()
    print("3 patients added successfully")

def add_doctors(connection):
    cursor = connection.cursor()
    doctors = [
        ('Nguyen Si', 'Cardiology', '0912345678', 'si@gmail.com', 10),
        ('Tran Binh', 'Neurology', '0923456789', 'binh@gmail.com', 12),
        ('Pham Hai', 'Orthopedics', '0934567890', 'hai@gmail.com', 15),
        ('Hoang Minh', 'Pediatrics', '0945678901', 'minh@gmail.com', 8),
        ('Le Cuong', 'Dentistry', '0956789012', 'cuong@gmail.com', 6)
    ]
    for doctor in doctors:
        query = "INSERT INTO doctors (full_name, specialization, phone_number, email, years_of_experience) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, doctor)
    connection.commit()
    print("5 doctors added successfully")

def add_appointments(connection):
    cursor = connection.cursor()
    appointments = [
        (1, 1, '2024-11-29 10:00:00', 'Routine Checkup'),
        (2, 2, '2024-11-29 11:00:00', 'Headache'),
        (3, 3, '2024-11-29 12:00:00', 'Back Pain')
    ]
    for appointment in appointments:
        query = "INSERT INTO appointments (patient_id, doctor_id, appointment_date, reason) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, appointment)
    connection.commit()
    print("3 appointments added successfully")

def generate_report(connection):
    cursor = connection.cursor()
    query = """SELECT p.full_name, p.date_of_birth, p.gender, p.address, d.full_name AS doctor_name, a.reason, a.appointment_date
               FROM appointments a
               JOIN patients p ON a.patient_id = p.patient_id
               JOIN doctors d ON a.doctor_id = d.doctor_id"""
    cursor.execute(query)
    appointments = cursor.fetchall()
    print("No | Patient name | Birthday | Gender | Address | Doctor name | Reason | Date")
    print("-" * 100)
    for idx, row in enumerate(appointments, 1):
        print(f"{idx} | {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]}")

def get_appointments_today(connection):
    cursor = connection.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    query = """SELECT p.full_name, p.date_of_birth, p.gender, d.full_name AS doctor_name, a.status
               FROM appointments a
               JOIN patients p ON a.patient_id = p.patient_id
               JOIN doctors d ON a.doctor_id = d.doctor_id
               WHERE DATE(a.appointment_date) = %s"""
    cursor.execute(query, (today,))
    appointments = cursor.fetchall()
    print("Address | No | Patient name | Birthday | Gender | Doctor name | Status")
    print("-" * 80)
    for idx, row in enumerate(appointments, 1):
        print(f"Ha Noi | {idx} | {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")

def main():
    connection = connect_to_database()
    if connection:
        add_patients(connection)
        add_doctors(connection)
        add_appointments(connection)
        generate_report(connection)
        get_appointments_today(connection)
        connection.close()

if __name__ == '__main__':
    main()
