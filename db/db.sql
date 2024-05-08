/*
It's assumed that "admin" administrator user exists in the PostgreSQL
*/

-- Database: ecommerce
-- DROP DATABASE IF EXISTS ecommerce;
CREATE DATABASE ecommerce
    WITH
    OWNER = admin
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

CREATE SCHEMA IF NOT EXISTS ecommerce AUTHORIZATION pg_database_owner;
GRANT ALL ON SCHEMA ecommerce TO pg_database_owner WITH GRANT OPTION;

ALTER ROLE admin IN DATABASE ecommerce SET search_path TO ecommerce, public;

-- create role "api" if it doesn't exist
CREATE ROLE api WITH
  LOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  NOBYPASSRLS;

ALTER ROLE api WITH PASSWORD 'password';
ALTER ROLE api IN DATABASE ecommerce SET search_path TO ecommerce;

-- create role "robotfw" if it doesn't exist
CREATE ROLE robotfw WITH
  LOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION
  NOBYPASSRLS;

ALTER ROLE robotfw WITH PASSWORD 'password';
ALTER ROLE robotfw IN DATABASE ecommerce SET search_path TO ecommerce;

GRANT USAGE ON SCHEMA ecommerce TO api;
GRANT USAGE ON SCHEMA ecommerce TO robotfw;
