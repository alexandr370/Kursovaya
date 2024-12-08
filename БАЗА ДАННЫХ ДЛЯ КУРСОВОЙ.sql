-- Создание базы данных TouristVouchers
CREATE DATABASE "TouristVouchers";
CREATE SCHEMA "TouristSchema";

-- Таблица Пользователи
CREATE TABLE "TouristSchema"."users" (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Таблица Паспортные данные
CREATE TABLE "TouristSchema"."passport_data" (
    passport_data_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    patronymic VARCHAR(100),
    passport_series_and_number VARCHAR(20) NOT NULL UNIQUE,
    gender CHAR(1) NOT NULL CHECK (gender IN ('M', 'F')),
    validity_period DATE NOT NULL,
    date_of_birth DATE NOT NULL,
    citizenship VARCHAR(100) NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES "TouristSchema"."users"(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Таблица Локации
CREATE TABLE "TouristSchema"."locations" (
    locations_id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL
);

-- Таблица Туристические путевки
CREATE TABLE "TouristSchema"."tours" (
    tour_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    departure_location INT NOT NULL,
    arrival_location INT NOT NULL,
    departure_date TIMESTAMP NOT NULL,
    arrival_date TIMESTAMP NOT NULL,
    return_date TIMESTAMP,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    services TEXT,
    available_places INT NOT NULL CHECK (available_places >= 0),
    FOREIGN KEY (departure_location) REFERENCES "TouristSchema"."locations"(locations_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (arrival_location) REFERENCES "TouristSchema"."locations"(locations_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Таблица История бронирований
CREATE TABLE "TouristSchema"."booking_history" (
    id SERIAL PRIMARY KEY,
    tour_id INT NOT NULL,
    user_id INT NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    number_of_places INT NOT NULL CHECK (number_of_places > 0),
    total_price DECIMAL(10, 2) NOT NULL CHECK (total_price >= 0),
    FOREIGN KEY (tour_id) REFERENCES "TouristSchema"."tours"(tour_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES "TouristSchema"."users"(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);
