import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

class HospitalManagementMySQL:
    def __init__(self, host='localhost', user='root', password='root', database='hospital_management'):
        try:
         
            self.conn = mysql.connector.connect(host=host, user=user, password=password)
            self.cursor = self.conn.cursor(dictionary=True)
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            self.cursor.execute(f"USE {database}")
            self._initialize_tables()
            print("Connected to MySQL database and tables verified successfully.")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Error: Invalid MySQL credentials (check user/password).")
            else:
                print(f"Database Initialization Error: {err}")
            exit(1)

    def _initialize_tables(self):
        """Creates the required tables automatically if they do not exist."""
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INT NOT NULL,
                gender VARCHAR(10) NOT NULL,
                phone VARCHAR(15),
                address TEXT)""")
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                specialization VARCHAR(100) NOT NULL,
                phone VARCHAR(15),
                email VARCHAR(100))""")
        
      
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INT AUTO_INCREMENT PRIMARY KEY,
                patient_id INT,
                doctor_id INT,
                appointment_date DATETIME NOT NULL,
                remarks TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
                FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE)""")
        self.conn.commit()

    def add_patient(self, name, age, gender, phone=None, address=None):
        query = "INSERT INTO patients (name, age, gender, phone, address) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (name, age, gender, phone, address))
        self.conn.commit()
        print(f"Patient '{name}' added successfully.")

    def view_patients(self):
        self.cursor.execute("SELECT * FROM patients")
        patients = self.cursor.fetchall()
        if not patients:
            print("No patient records found.")
            return
        print("\n--- Patients List ---")
        for p in patients:
            print(f"ID: {p['patient_id']} | Name: {p['name']} | Age: {p['age']} | Gender: {p['gender']} | Phone: {p['phone']} | Address: {p['address']}")

    def update_patient(self, patient_id, **fields):
        if not fields:
            print("No fields provided to update.")
            return
        set_clause = ", ".join(f"{k} = %s" for k in fields)
        values = list(fields.values())
        values.append(patient_id)
        query = f"UPDATE patients SET {set_clause} WHERE patient_id = %s"
        self.cursor.execute(query, tuple(values))
        self.conn.commit()
        print(f"Patient ID {patient_id} updated.")

    def delete_patient(self, patient_id):
        self.cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
        self.conn.commit()
        print(f"Patient ID {patient_id} deleted.")

    def add_doctor(self, name, specialization, phone=None, email=None):
        query = "INSERT INTO doctors (name, specialization, phone, email) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (name, specialization, phone, email))
        self.conn.commit()
        print(f"Doctor '{name}' added.")

    def view_doctors(self):
        self.cursor.execute("SELECT * FROM doctors")
        doctors = self.cursor.fetchall()
        if not doctors:
            print("No doctor records found.")
            return
        print("\n--- Doctors List ---")
        for d in doctors:
            print(f"ID: {d['doctor_id']} | Name: {d['name']} | Specialization: {d['specialization']} | Phone: {d['phone']} | Email: {d['email']}")

    def update_doctor(self, doctor_id, **fields):
        if not fields:
            print("No fields provided to update.")
            return
        set_clause = ", ".join(f"{k} = %s" for k in fields)
        values = list(fields.values())
        values.append(doctor_id)
        query = f"UPDATE doctors SET {set_clause} WHERE doctor_id = %s"
        self.cursor.execute(query, tuple(values))
        self.conn.commit()
        print(f"Doctor ID {doctor_id} updated.")

    def delete_doctor(self, doctor_id):
        self.cursor.execute("DELETE FROM doctors WHERE doctor_id = %s", (doctor_id,))
        self.conn.commit()
        print(f"Doctor ID {doctor_id} deleted.")

    def add_appointment(self, patient_id, doctor_id, appointment_date_str, remarks=None):
        try:
            appointment_date = datetime.strptime(appointment_date_str, '%Y-%m-%d %H:%M')
        except ValueError:
            print("Invalid datetime format. Use YYYY-MM-DD HH:MM")
            return
        query = "INSERT INTO appointments (patient_id, doctor_id, appointment_date, remarks) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (patient_id, doctor_id, appointment_date, remarks))
        self.conn.commit()
        print("Appointment scheduled successfully.")

    def view_appointments(self):
        self.cursor.execute('''
            SELECT a.appointment_id, p.name AS patient_name, d.name AS doctor_name, a.appointment_date, a.remarks 
            FROM appointments a 
            JOIN patients p ON a.patient_id = p.patient_id 
            JOIN doctors d ON a.doctor_id = d.doctor_id 
            ORDER BY a.appointment_date
        ''')
        appointments = self.cursor.fetchall()
        if not appointments:
            print("No scheduled appointments found.")
            return
        print("\n--- Appointments Schedule ---")
        for a in appointments:
            print(f"ID: {a['appointment_id']} | Patient: {a['patient_name']} | Doctor: {a['doctor_name']} | Date: {a['appointment_date']} | Remarks: {a['remarks']}")

    def close(self):
        self.cursor.close()
        self.conn.close()
        print("MySQL connection closed.")
        
if __name__ == "__main__":
    system = HospitalManagementMySQL(host='localhost', user='root', password='root', database='hospital_management')

    while True:
        print("\n=== Hospital Management System ===")
        print("1. Add Patient")
        print("2. View Patients")
        print("3. Add Doctor")
        print("4. View Doctors")
        print("5. Schedule Appointment")
        print("6. View Appointments")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            name = input("Enter Patient Name: ")
            age = int(input("Enter Patient Age: "))
            gender = input("Enter Gender (M/F/Other): ")
            phone = input("Enter Phone (or leave blank): ") or None
            address = input("Enter Address (or leave blank): ") or None
            system.add_patient(name, age, gender, phone, address)

        elif choice == '2':
            system.view_patients()

        elif choice == '3':
            name = input("Enter Doctor Name: ")
            specialization = input("Enter Specialization: ")
            phone = input("Enter Phone (or leave blank): ") or None
            email = input("Enter Email (or leave blank): ") or None
            system.add_doctor(name, specialization, phone, email)

        elif choice == '4':
            system.view_doctors()

        elif choice == '5':
            try:
                p_id = int(input("Enter Patient ID: "))
                d_id = int(input("Enter Doctor ID: "))
                dt_str = input("Enter Date & Time (YYYY-MM-DD HH:MM): ")
                remarks = input("Enter Remarks (or leave blank): ") or None
                system.add_appointment(p_id, d_id, dt_str, remarks)
            except ValueError:
                print("Error: IDs must be numeric integers.")

        elif choice == '6':
            system.view_appointments()

        elif choice == '7':
            system.close()
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice! Please select an option between 1 and 7.")

