import mysql.connector
import random



def get_connection():
    
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="lisa@1234@mondal",  
        database="hospital_db"
    )
    return conn



def generate_unique_id(table_name, id_column):
    """
    Generate a 5-digit ID with all different digits (e.g., 10527),
    and make sure it does not already exist in the given table.
    """
    conn = get_connection()
    cursor = conn.cursor()

    while True:
        digits = list('0123456789')
        random.shuffle(digits)
        new_id = ''.join(digits[:5])

        query = f"SELECT COUNT(*) FROM {table_name} WHERE {id_column} = %s"
        cursor.execute(query, (new_id,))
        (count,) = cursor.fetchone()
        if count == 0:
            cursor.close()
            conn.close()
            return new_id

def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")



def add_patient():
    conn = get_connection()
    cursor = conn.cursor()

    patient_id = generate_unique_id("patients", "patient_id")
    print(f"Generated Patient ID: {patient_id}")

    name = input("Enter patient name: ")
    age = input_int("Enter age: ")
    gender = input("Enter gender (M/F/O): ")
    phone = input("Enter phone: ")
    address = input("Enter address: ")

    query = """
        INSERT INTO patients (patient_id, name, age, gender, phone, address)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (patient_id, name, age, gender, phone, address)
    cursor.execute(query, values)
    conn.commit()

    print("Patient added successfully!\n")

    cursor.close()
    conn.close()

def view_patients():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT patient_id, name, age, gender, phone FROM patients")
    rows = cursor.fetchall()

    print("\n--- All Patients ---")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Gender: {row[3]}, Phone: {row[4]}")
    print()

    cursor.close()
    conn.close()

def search_patient():
    conn = get_connection()
    cursor = conn.cursor()

    pid = input("Enter patient ID to search: ")
    cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (pid,))
    row = cursor.fetchone()

    if row:
        print("\n--- Patient Details ---")
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Age: {row[2]}")
        print(f"Gender: {row[3]}")
        print(f"Phone: {row[4]}")
        print(f"Address: {row[5]}\n")
    else:
        print("Patient not found.\n")

    cursor.close()
    conn.close()



def add_doctor():
    conn = get_connection()
    cursor = conn.cursor()

    doctor_id = generate_unique_id("doctors", "doctor_id")
    print(f"Generated Doctor ID: {doctor_id}")

    name = input("Enter doctor name: ")
    specialization = input("Enter specialization: ")
    phone = input("Enter phone: ")

    query = """
        INSERT INTO doctors (doctor_id, name, specialization, phone)
        VALUES (%s, %s, %s, %s)
    """
    values = (doctor_id, name, specialization, phone)
    cursor.execute(query, values)
    conn.commit()

    print("Doctor added successfully!\n")

    cursor.close()
    conn.close()

def view_doctors():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT doctor_id, name, specialization, phone FROM doctors")
    rows = cursor.fetchall()

    print("\n--- All Doctors ---")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Specialization: {row[2]}, Phone: {row[3]}")
    print()

    cursor.close()
    conn.close()



def create_appointment():
    conn = get_connection()
    cursor = conn.cursor()

    print("\nTo create an appointment you need:")
    print("- Patient ID")
    print("- Doctor ID")

    patient_id = input("Enter existing Patient ID: ")
    doctor_id = input("Enter existing Doctor ID: ")

    
    cursor.execute("SELECT COUNT(*) FROM patients WHERE patient_id = %s", (patient_id,))
    (p_count,) = cursor.fetchone()
    if p_count == 0:
        print("Invalid Patient ID. Please add the patient first.\n")
        cursor.close()
        conn.close()
        return

    
    cursor.execute("SELECT COUNT(*) FROM doctors WHERE doctor_id = %s", (doctor_id,))
    (d_count,) = cursor.fetchone()
    if d_count == 0:
        print("Invalid Doctor ID. Please add the doctor first.\n")
        cursor.close()
        conn.close()
        return

    date = input("Enter appointment date (YYYY-MM-DD): ")
    time = input("Enter appointment time (HH:MM, 24-hr): ")
    reason = input("Enter reason for visit: ")

    datetime_str = f"{date} {time}:00"

    query = """
        INSERT INTO appointments (patient_id, doctor_id, appointment_datetime, reason, status)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (patient_id, doctor_id, datetime_str, reason, "Scheduled")
    cursor.execute(query, values)
    conn.commit()

    print("Appointment created successfully!\n")

    cursor.close()
    conn.close()

def view_appointments():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT a.appointment_id, p.name, d.name, a.appointment_datetime, a.reason, a.status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        ORDER BY a.appointment_datetime
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    print("\n--- All Appointments ---")
    for row in rows:
        print(f"ID: {row[0]}, Patient: {row[1]}, Doctor: {row[2]}, DateTime: {row[3]}, Reason: {row[4]}, Status: {row[5]}")
    print()

    cursor.close()
    conn.close()



def add_room():
    conn = get_connection()
    cursor = conn.cursor()

    room_id = input_int("Enter room number (e.g., 101): ")
    room_type = input("Enter room type (General/ICU/Private): ")

    query = """
        INSERT INTO rooms (room_id, room_type, is_available)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (room_id, room_type, 1))
    conn.commit()

    print("Room added successfully!\n")

    cursor.close()
    conn.close()

def view_rooms():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT room_id, room_type, is_available FROM rooms")
    rows = cursor.fetchall()

    print("\n--- All Rooms ---")
    for row in rows:
        status = "Available" if row[2] == 1 else "Occupied"
        print(f"Room: {row[0]}, Type: {row[1]}, Status: {status}")
    print()

    cursor.close()
    conn.close()

def admit_patient():
    conn = get_connection()
    cursor = conn.cursor()

    patient_id = input("Enter Patient ID to admit: ")

    
    cursor.execute("SELECT COUNT(*) FROM patients WHERE patient_id = %s", (patient_id,))
    (p_count,) = cursor.fetchone()
    if p_count == 0:
        print("Invalid Patient ID.\n")
        cursor.close()
        conn.close()
        return

   
    cursor.execute("SELECT room_id, room_type FROM rooms WHERE is_available = 1")
    rooms = cursor.fetchall()
    if not rooms:
        print("No rooms available.\n")
        cursor.close()
        conn.close()
        return

    print("\nAvailable rooms:")
    for r in rooms:
        print(f"Room {r[0]} ({r[1]})")

    room_id = input_int("Enter room number to assign: ")
    diagnosis = input("Enter diagnosis: ")
    admit_date = input("Enter admit date (YYYY-MM-DD): ")

    
    cursor.execute("SELECT is_available FROM rooms WHERE room_id = %s", (room_id,))
    row = cursor.fetchone()
    if not row or row[0] == 0:
        print("Room not available.\n")
        cursor.close()
        conn.close()
        return

    query = """
        INSERT INTO admissions (patient_id, room_id, admit_date, diagnosis)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (patient_id, room_id, admit_date, diagnosis))

   
    cursor.execute("UPDATE rooms SET is_available = 0 WHERE room_id = %s", (room_id,))
    conn.commit()

    print("Patient admitted successfully!\n")

    cursor.close()
    conn.close()

def discharge_patient():
    conn = get_connection()
    cursor = conn.cursor()

    admission_id = input_int("Enter Admission ID to discharge: ")
    discharge_date = input("Enter discharge date (YYYY-MM-DD): ")

    
    cursor.execute("SELECT room_id FROM admissions WHERE admission_id = %s", (admission_id,))
    row = cursor.fetchone()
    if not row:
        print("Invalid Admission ID.\n")
        cursor.close()
        conn.close()
        return

    room_id = row[0]

   
    cursor.execute(
        "UPDATE admissions SET discharge_date = %s WHERE admission_id = %s",
        (discharge_date, admission_id)
    )

    
    cursor.execute("UPDATE rooms SET is_available = 1 WHERE room_id = %s", (room_id,))
    conn.commit()

    print("Patient discharged successfully!\n")

    cursor.close()
    conn.close()



def create_bill():
    conn = get_connection()
    cursor = conn.cursor()

    admission_id = input_int("Enter Admission ID for billing: ")
    total_amount = float(input("Enter total amount: "))
    paid_amount = float(input("Enter paid amount: "))
    payment_date = input("Enter payment date (YYYY-MM-DD): ")
    payment_method = input("Enter payment method (Cash/Card/UPI): ")

    query = """
        INSERT INTO bills (admission_id, total_amount, paid_amount, payment_date, payment_method)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (admission_id, total_amount, paid_amount, payment_date, payment_method))
    conn.commit()

    print("Bill created successfully!\n")

    cursor.close()
    conn.close()

def view_bills():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT b.bill_id, b.admission_id, p.name, b.total_amount, b.paid_amount, b.payment_date, b.payment_method
        FROM bills b
        JOIN admissions a ON b.admission_id = a.admission_id
        JOIN patients p ON a.patient_id = p.patient_id
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    print("\n--- All Bills ---")
    for row in rows:
        print(f"Bill ID: {row[0]}, Admission ID: {row[1]}, Patient: {row[2]}, Total: {row[3]}, Paid: {row[4]}, Date: {row[5]}, Method: {row[6]}")
    print()

    cursor.close()
    conn.close()



def main_menu():
    while True:
        print("======== HOSPITAL MANAGEMENT SYSTEM ========")
        print("1. Add Patient")
        print("2. View Patients")
        print("3. Search Patient by ID")
        print("4. Add Doctor")
        print("5. View Doctors")
        print("6. Create Appointment")
        print("7. View Appointments")
        print("8. Add Room")
        print("9. View Rooms")
        print("10. Admit Patient")
        print("11. Discharge Patient")
        print("12. Create Bill")
        print("13. View Bills")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_patient()
        elif choice == "2":
            view_patients()
        elif choice == "3":
            search_patient()
        elif choice == "4":
            add_doctor()
        elif choice == "5":
            view_doctors()
        elif choice == "6":
            create_appointment()
        elif choice == "7":
            view_appointments()
        elif choice == "8":
            add_room()
        elif choice == "9":
            view_rooms()
        elif choice == "10":
            admit_patient()
        elif choice == "11":
            discharge_patient()
        elif choice == "12":
            create_bill()
        elif choice == "13":
            view_bills()
        elif choice == "0":
            print("Exiting... Bye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main_menu()
