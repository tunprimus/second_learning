CREATE TABLE airlines (
    airline_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    country VARCHAR(50)
);

INSERT INTO airlines (name, country) VALUES
('Pakistan International Airlines', 'Pakistan'),
('Airblue', 'Pakistan'),
('SereneAir', 'Pakistan'),
('Qatar Airways', 'Qatar'),
('Emirates', 'UAE');

CREATE TABLE passengers (
    passenger_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    passport_number VARCHAR(20) UNIQUE,
    nationality VARCHAR(50),
    dob DATE
);

INSERT INTO passengers (name, email, phone, passport_number, nationality, dob) VALUES
('Sahil', 'sahil@example.com', '+923011234567', 'PK1234567', 'Pakistani', '1995-08-12'),
('Shivani', 'shivani@example.com', '+923024567890', 'PK2345678', 'Pakistani', '1998-04-23'),
('Aryan', 'aryan@example.com', '+923035678901', 'PK3456789', 'Pakistani', '1992-11-05'),
('Kashish', 'kashish@example.com', '+923046789012', 'PK4567890', 'Pakistani', '1999-01-17'),
('Laiba', 'laiba@example.com', '+923057890123', 'PK5678901', 'Pakistani', '2001-07-30');

CREATE TABLE airports (
    airport_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50)
);

INSERT INTO airports (airport_id, name, city, country) VALUES
('KHI', 'Karachi International Airport', 'Karachi', 'Pakistan'),
('LHE', 'Lahore International Airport', 'Lahore', 'Pakistan'),
('ISB', 'Islamabad International Airport', 'Islamabad', 'Pakistan'),
('PEW', 'Peshawar International Airport', 'Peshawar', 'Pakistan'),
('UET', 'Quetta International Airport', 'Quetta', 'Pakistan');

CREATE TABLE aircrafts (
    aircraft_id SERIAL PRIMARY KEY,
    model VARCHAR(50),
    manufacturer VARCHAR(50),
    capacity INT,
    registration_number VARCHAR(50) UNIQUE,
    airline_id INT REFERENCES airlines(airline_id)
);

INSERT INTO aircrafts (model, manufacturer, capacity, registration_number, airline_id) VALUES
('Boeing 777', 'Boeing', 300, 'REG-PIA-001', 1),
('Airbus A320', 'Airbus', 180, 'REG-PIA-002', 1),
('ATR 72', 'ATR', 70, 'REG-PIA-003', 1),
('Boeing 737', 'Boeing', 215, 'REG-PIA-004', 1),
('Airbus A310', 'Airbus', 280, 'REG-PIA-005', 1);

CREATE TABLE flights (
    flight_id SERIAL PRIMARY KEY,
    flight_code VARCHAR(10) UNIQUE,
    origin_airport VARCHAR(10) REFERENCES airports(airport_id),
    destination_airport VARCHAR(10) REFERENCES airports(airport_id),
    aircraft_id INT REFERENCES aircrafts(aircraft_id),
    airline_id INT REFERENCES airlines(airline_id)
);

INSERT INTO flights (flight_code, origin_airport, destination_airport, aircraft_id, airline_id) VALUES
('PIA101', 'KHI', 'LHE', 1, 1),
('PIA102', 'LHE', 'ISB', 2, 1),
('PIA103', 'ISB', 'PEW', 3, 1),
('PIA104', 'PEW', 'UET', 4, 1),
('PIA105', 'UET', 'KHI', 5, 1);

CREATE TABLE flight_schedules (
    schedule_id SERIAL PRIMARY KEY,
    flight_id INT REFERENCES flights(flight_id),
    departure_time TIMESTAMP,
    arrival_time TIMESTAMP,
    status VARCHAR(20)
);

INSERT INTO flight_schedules (flight_id, departure_time, arrival_time, status) VALUES
(1, '2025-06-01 08:00:00', '2025-06-01 10:00:00', 'Scheduled'),
(2, '2025-06-01 11:00:00', '2025-06-01 13:00:00', 'Scheduled'),
(3, '2025-06-02 09:00:00', '2025-06-02 11:00:00', 'Scheduled'),
(4, '2025-06-02 14:00:00', '2025-06-02 16:00:00', 'Scheduled'),
(5, '2025-06-03 07:00:00', '2025-06-03 09:30:00', 'Scheduled');

CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE
);

INSERT INTO roles (role_name) VALUES
('Pilot'),
('Co-Pilot'),
('Flight Attendant'),
('Ground Staff'),
('Technician');

CREATE TABLE staff (
    staff_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    role_id INT REFERENCES roles(role_id),
    phone VARCHAR(20),
    email VARCHAR(100) UNIQUE
);

INSERT INTO staff (name, role_id, phone, email) VALUES
('Sahil', 1, '+923011234567', 'sahil@pia.pk'),
('Hitesh', 4, '+923022345678', 'hitesh@pia.pk'),
('Ali', 2, '+923033456789', 'ali@pia.pk'),
('Varsha', 3, '+923044567890', 'varsha@pia.pk'),
('Sandhya', 3, '+923055678901', 'sandhya@pia.pk');

CREATE TABLE flight_staff_assignment (
    assignment_id SERIAL PRIMARY KEY,
    flight_id INT REFERENCES flights(flight_id),
    staff_id INT REFERENCES staff(staff_id)
);

INSERT INTO flight_staff_assignment (flight_id, staff_id) VALUES
(1, 1),
(1, 2),
(2, 3),
(3, 4),
(4, 5);

CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    passenger_id INT REFERENCES passengers(passenger_id),
    schedule_id INT REFERENCES flight_schedules(schedule_id),
    booking_date DATE,
    status VARCHAR(20)
);

INSERT INTO bookings (passenger_id, schedule_id, booking_date, status) VALUES
(1, 1, '2025-05-15', 'Confirmed'),
(2, 2, '2025-05-16', 'Confirmed'),
(3, 3, '2025-05-17', 'Pending'),
(4, 4, '2025-05-18', 'Cancelled'),
(5, 5, '2025-05-19', 'Confirmed');

CREATE TABLE tickets (
    ticket_id SERIAL PRIMARY KEY,
    booking_id INT REFERENCES bookings(booking_id),
    seat_number VARCHAR(10),
    class VARCHAR(20),
    price DECIMAL(10,2)
);

INSERT INTO tickets (booking_id, seat_number, class, price) VALUES
(1, '12A', 'Economy', 150.00),
(2, '14B', 'Business', 300.00),
(3, '20C', 'Economy', 150.00),
(4, '1A', 'First Class', 500.00),
(5, '15D', 'Economy', 150.00);

CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    ticket_id INT REFERENCES tickets(ticket_id),
    amount DECIMAL(10,2),
    payment_date DATE,
    payment_method VARCHAR(50)
);

INSERT INTO payments (ticket_id, amount, payment_date, payment_method) VALUES
(1, 150.00, '2025-05-16', 'Credit Card'),
(2, 300.00, '2025-05-17', 'Debit Card'),
(3, 150.00, '2025-05-18', 'Cash'),
(4, 500.00, '2025-05-19', 'Credit Card'),
(5, 150.00, '2025-05-20', 'Mobile Payment');
