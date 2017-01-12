DROP DATABASE IF EXISTS prestashop;
DROP USER IF EXISTS 'prestashop'@'%';

CREATE DATABASE prestashop;
CREATE USER 'prestashop'@'%' IDENTIFIED BY 'prestashop1234';
GRANT SELECT ON prestashop.* TO 'prestashop'@'%';
