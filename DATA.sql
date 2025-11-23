
CREATE DATABASE IF NOT EXISTS hospital_db;
USE hospital_db;


CREATE TABLE patients (
    patient_id CHAR(5) PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    age        INT,
    gender     CHAR(1),
    phone      VARCHAR(15),
    address    VARCHAR(255)
);


CREATE TABLE doctors (
    doctor_id     CHAR(5) PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    specialization VARCHAR(100),
    phone         VARCHAR(15)
);


CREATE TABLE rooms (
    room_id      INT PRIMARY KEY,
    room_type    VARCHAR(50),
    is_available TINYINT(1) DEFAULT 1  
);


CREATE TABLE admissions (
    admission_id   INT AUTO_INCREMENT PRIMARY KEY,
    patient_id     CHAR(5),
    room_id        INT,
    admit_date     DATE,
    discharge_date DATE,
    diagnosis      VARCHAR(255),
    CONSTRAINT fk_adm_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    CONSTRAINT fk_adm_room    FOREIGN KEY (room_id)    REFERENCES rooms(room_id)
);


CREATE TABLE appointments (
    appointment_id       INT AUTO_INCREMENT PRIMARY KEY,
    patient_id           CHAR(5),
    doctor_id            CHAR(5),
    appointment_datetime DATETIME,
    reason               VARCHAR(255),
    status               VARCHAR(50),
    CONSTRAINT fk_app_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    CONSTRAINT fk_app_doctor  FOREIGN KEY (doctor_id)  REFERENCES doctors(doctor_id)
);


CREATE TABLE bills (
    bill_id        INT AUTO_INCREMENT PRIMARY KEY,
    admission_id   INT,
    total_amount   DECIMAL(10,2),
    paid_amount    DECIMAL(10,2),
    payment_date   DATE,
    payment_method VARCHAR(50),
    CONSTRAINT fk_bill_admission FOREIGN KEY (admission_id) REFERENCES admissions(admission_id)
);
