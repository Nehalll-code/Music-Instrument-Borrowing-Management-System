-- USERS TABLE
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    userId INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    role ENUM('student', 'faculty', 'admin') NOT NULL
);

-- INSTRUMENTS TABLE
DROP TABLE IF EXISTS instruments;
CREATE TABLE instruments (
    instrumentId INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(100),
    instrument_condition VARCHAR(100),
    available TINYINT(1) DEFAULT 1
);

-- BORROW REQUESTS
DROP TABLE IF EXISTS borrow_requests;
CREATE TABLE borrow_requests (
    requestId INT AUTO_INCREMENT PRIMARY KEY,
    userId INT,
    instrumentId INT,
    date DATE,
    status ENUM('pending', 'approved', 'declined') DEFAULT 'pending',
    FOREIGN KEY (userId) REFERENCES users(userId),
    FOREIGN KEY (instrumentId) REFERENCES instruments(instrumentId)
);

-- RETURN LOGS
DROP TABLE IF EXISTS return_logs;
CREATE TABLE return_logs (
    logId INT AUTO_INCREMENT PRIMARY KEY,
    instrumentId INT,
    returnDate DATE,
    condition_after_return VARCHAR(100),
    FOREIGN KEY (instrumentId) REFERENCES instruments(instrumentId)
);

-- ASSIGNMENT LOG
DROP TABLE IF EXISTS assignment_log;
CREATE TABLE assignment_log (
    assignmentId INT AUTO_INCREMENT PRIMARY KEY,
    facultyId INT,
    instrumentId INT,
    status VARCHAR(50),
    FOREIGN KEY (facultyId) REFERENCES users(userId),
    FOREIGN KEY (instrumentId) REFERENCES instruments(instrumentId)
);

-- NOTIFICATIONS
DROP TABLE IF EXISTS notifications;
CREATE TABLE notifications (
    notificationId INT AUTO_INCREMENT PRIMARY KEY,
    userId INT,
    message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES users(userId)
);

-- REPORTS
DROP TABLE IF EXISTS reports;
CREATE TABLE reports (
    reportId INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT,
    date DATE
);

-- CONDITION LOGS
DROP TABLE IF EXISTS condition_logs;
CREATE TABLE condition_logs (
    logId INT AUTO_INCREMENT PRIMARY KEY,
    instrumentId INT,
    status VARCHAR(100),
    logDate DATE,
    FOREIGN KEY (instrumentId) REFERENCES instruments(instrumentId)
);

-- ROLES
DROP TABLE IF EXISTS roles;
CREATE TABLE roles (
    roleId INT AUTO_INCREMENT PRIMARY KEY,
    roleName VARCHAR(50)
);
