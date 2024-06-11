 create database restaurant;
  use  restaurant;

CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
   );
insert into admins values (1,'lali','12345');
CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
    );


  insert into items values(4,"Item 4",20.00,30);