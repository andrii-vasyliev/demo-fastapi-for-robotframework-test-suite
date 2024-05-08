/*
It's assumed that 'admin' administrator user exists in the PostgreSQL
Connect to the created ecommerce DB as 'admin' user and create following objects:
*/

/*--------- Table: ecommerce.order_statuses ------------*/
-- DROP TABLE IF EXISTS ecommerce.order_statuses;
CREATE TABLE IF NOT EXISTS ecommerce.order_statuses
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    status character varying(128) COLLATE pg_catalog."default" NOT NULL,
    created timestamp(3) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP(0),
    created_by character varying(256) COLLATE pg_catalog."default" NOT NULL DEFAULT CURRENT_USER,
    CONSTRAINT "PK_ORDER_STATUS_ID" PRIMARY KEY (id)
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS ecommerce.order_statuses OWNER to admin;

REVOKE ALL ON TABLE ecommerce.order_statuses FROM api;
REVOKE ALL ON TABLE ecommerce.order_statuses FROM robotfw;

GRANT ALL ON TABLE ecommerce.order_statuses TO admin WITH GRANT OPTION;
GRANT SELECT ON TABLE ecommerce.order_statuses TO api;
GRANT DELETE, INSERT, UPDATE, SELECT ON TABLE ecommerce.order_statuses TO robotfw;

INSERT INTO ecommerce.order_statuses(status) VALUES ('New'), ('Approved'), ('Voided'), ('Closed');
COMMIT;

/*--------- Table: ecommerce.items ------------*/
-- DROP TABLE IF EXISTS ecommerce.items;
CREATE TABLE IF NOT EXISTS ecommerce.items
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    name character varying(512) COLLATE pg_catalog."default" NOT NULL,
    price real NOT NULL DEFAULT 0,
    created timestamp(3) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP(0),
    created_by character varying(256) COLLATE pg_catalog."default" NOT NULL DEFAULT CURRENT_USER,
    CONSTRAINT "PK_ITEM_ID" PRIMARY KEY (id)
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS ecommerce.items OWNER to admin;

REVOKE ALL ON TABLE ecommerce.items FROM api;
REVOKE ALL ON TABLE ecommerce.items FROM robotfw;

GRANT ALL ON TABLE ecommerce.items TO admin WITH GRANT OPTION;
GRANT UPDATE, SELECT, DELETE, INSERT ON TABLE ecommerce.items TO api;
GRANT UPDATE, SELECT, DELETE, INSERT ON TABLE ecommerce.items TO robotfw;

INSERT INTO ecommerce.items (id, "name", price)
	 VALUES ('41c8ba6b-d87d-4186-b5a7-67e0859f9930', 'AsRock B650M PG Riptide AM5', 704.99),
			('8989d984-b4d2-4593-bc46-d6d041691b03', 'G.Skill DDR5-6000 32GB (2x16GB) CL36', 509.00),
			('42fe5cab-1d68-4dcd-83f3-9210a705bcec', 'Thermalright contact frame AM5', 52.50),
			('c3688919-9a8b-41f3-a7f6-71a070c525aa', 'AMD Ryzen 5 7600 3.8GHz BOX', 931.06);
COMMIT;

/*--------- Table: ecommerce.customers ------------*/
-- DROP TABLE IF EXISTS ecommerce.customers;
CREATE TABLE IF NOT EXISTS ecommerce.customers
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    name character varying(256) COLLATE pg_catalog."default" NOT NULL,
    email character varying(256) COLLATE pg_catalog."default",
    created timestamp(3) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP(0),
    created_by character varying(256) COLLATE pg_catalog."default" NOT NULL DEFAULT CURRENT_USER,
    CONSTRAINT "PK_CUSTOMER_ID" PRIMARY KEY (id)
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS ecommerce.customers OWNER to admin;

REVOKE ALL ON TABLE ecommerce.customers FROM api;
REVOKE ALL ON TABLE ecommerce.customers FROM robotfw;

GRANT ALL ON TABLE ecommerce.customers TO admin WITH GRANT OPTION;
GRANT UPDATE, SELECT, DELETE, INSERT ON TABLE ecommerce.customers TO api;
GRANT UPDATE, SELECT, DELETE, INSERT ON TABLE ecommerce.customers TO robotfw;

/*--------- Table: ecommerce.orders ------------*/
-- DROP TABLE IF EXISTS ecommerce.orders;
CREATE TABLE IF NOT EXISTS ecommerce.orders
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    customer_id uuid NOT NULL,
    status uuid NOT NULL,
    created timestamp(3) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP(0),
    created_by character varying(256) COLLATE pg_catalog."default" NOT NULL DEFAULT CURRENT_USER,
    CONSTRAINT "PK_ORDER_ID" PRIMARY KEY (id),
    CONSTRAINT "FK_ORDERS_CUSTOMER" FOREIGN KEY (customer_id)
        REFERENCES ecommerce.customers (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT "FK_ORDERS_STATUS" FOREIGN KEY (status)
        REFERENCES ecommerce.order_statuses (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS ecommerce.orders OWNER to admin;

REVOKE ALL ON TABLE ecommerce.orders FROM api;
REVOKE ALL ON TABLE ecommerce.orders FROM robotfw;

GRANT ALL ON TABLE ecommerce.orders TO admin WITH GRANT OPTION;
GRANT UPDATE, SELECT, DELETE, INSERT ON TABLE ecommerce.orders TO api;
GRANT UPDATE, SELECT, DELETE, INSERT ON TABLE ecommerce.orders TO robotfw;

/*--------- Table: ecommerce.order_items ------------*/
-- DROP TABLE IF EXISTS ecommerce.order_items;
CREATE TABLE IF NOT EXISTS ecommerce.order_items
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    order_id uuid NOT NULL,
    item_id uuid NOT NULL,
    quantity integer NOT NULL DEFAULT 0,
    created timestamp(3) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP(0),
    created_by character varying(256) COLLATE pg_catalog."default" NOT NULL DEFAULT CURRENT_USER,
    CONSTRAINT "PK_ORDER_ITEM_ID" PRIMARY KEY (id),
    CONSTRAINT "FK_ORDER_ITEM_ITEM" FOREIGN KEY (item_id)
        REFERENCES ecommerce.items (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "FK_ORDER_ITEM_ORDER" FOREIGN KEY (order_id)
        REFERENCES ecommerce.orders (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS ecommerce.order_items OWNER to admin;

REVOKE ALL ON TABLE ecommerce.order_items FROM api;
REVOKE ALL ON TABLE ecommerce.order_items FROM robotfw;

GRANT ALL ON TABLE ecommerce.order_items TO admin WITH GRANT OPTION;
GRANT UPDATE, SELECT, DELETE, INSERT ON TABLE ecommerce.order_items TO api;
GRANT UPDATE, SELECT, DELETE, INSERT ON TABLE ecommerce.order_items TO robotfw;
