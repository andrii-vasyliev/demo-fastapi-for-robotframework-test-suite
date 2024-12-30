/*
It's assumed that "postgres" is a superuser and db.sql, tables.sql scrpts have been ran
*/

/*--------- FUNCTION: robotfw.get_catalog_items ------------*/
CREATE OR REPLACE FUNCTION robotfw.get_catalog_items(
	)
    RETURNS TABLE(items json)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
BEGIN
	RETURN QUERY
	SELECT json_object('id' VALUE i.id,
						'name' VALUE i.name,
						'price' VALUE i.price
		   )
	  FROM ecommerce.items i;
END;
$BODY$;

ALTER FUNCTION robotfw.get_catalog_items() OWNER TO postgres;

REVOKE ALL ON FUNCTION robotfw.get_catalog_items() FROM PUBLIC;
REVOKE ALL ON FUNCTION robotfw.get_catalog_items() FROM api;

GRANT EXECUTE ON FUNCTION robotfw.get_catalog_items() TO postgres WITH GRANT OPTION;
GRANT EXECUTE ON FUNCTION robotfw.get_catalog_items() TO robotfw;

/*--------- FUNCTION: ecommerce.get_customer_by ------------*/
-- DROP FUNCTION IF EXISTS ecommerce.get_customer_by(character varying, character varying);
CREATE OR REPLACE FUNCTION ecommerce.get_customer_by(
	customer_name character varying DEFAULT NULL::character varying,
	customer_email character varying DEFAULT 'ANY'::character varying)
    RETURNS json
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
	customers json;
BEGIN
	IF NULLIF(customer_name, '') IS NULL AND (customer_email IS NULL OR UPPER(customer_email) IN ('', 'ANY')) THEN
		RAISE assert_failure USING MESSAGE = 'At least one search parameter is required';
	END IF;

	SELECT json_arrayagg(
			 json_object('id' VALUE c.id,
						 'name' VALUE c.name,
						 'email' VALUE c.email)
		   )
	  INTO customers
	  FROM ecommerce.customers c
 	 WHERE (NULLIF(customer_name, '') IS NULL
			OR c.name = customer_name)
	   AND (UPPER(COALESCE(customer_email, 'ANY')) = 'ANY'
		    OR (customer_email = '' AND c.email IS NULL)
			OR c.email = customer_email);

	IF customers IS NULL THEN
		RAISE no_data_found USING MESSAGE = 'query returned no rows';
	END IF;

	RETURN json_object('customers': customers);
END;
$BODY$;

ALTER FUNCTION ecommerce.get_customer_by(character varying, character varying) OWNER TO postgres;

REVOKE ALL ON FUNCTION ecommerce.get_customer_by(character varying, character varying) FROM PUBLIC;
REVOKE ALL ON FUNCTION ecommerce.get_customer_by(character varying, character varying) FROM robotfw;

GRANT EXECUTE ON FUNCTION ecommerce.get_customer_by(character varying, character varying) TO postgres WITH GRANT OPTION;
GRANT EXECUTE ON FUNCTION ecommerce.get_customer_by(character varying, character varying) TO api;

/*--------- FUNCTION: ecommerce.get_customer_by_id ------------*/
-- DROP FUNCTION IF EXISTS ecommerce.get_customer_by_id(uuid);
CREATE OR REPLACE FUNCTION ecommerce.get_customer_by_id(
	customer_id uuid)
    RETURNS json
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
	customer json;
BEGIN
	IF customer_id IS NULL THEN
		RAISE assert_failure USING MESSAGE = 'Field required: "id"';
	END IF;

	SELECT json_object('id' VALUE c.id,
						'name' VALUE c.name,
						'email' VALUE c.email)
	  INTO STRICT customer
	  FROM ecommerce.customers c
	 WHERE c.id = customer_id;

	RETURN customer;
END;
$BODY$;

ALTER FUNCTION ecommerce.get_customer_by_id(uuid) OWNER TO postgres;

REVOKE ALL ON FUNCTION ecommerce.get_customer_by_id(uuid) FROM PUBLIC;
REVOKE ALL ON FUNCTION ecommerce.get_customer_by_id(uuid) FROM robotfw;

GRANT EXECUTE ON FUNCTION ecommerce.get_customer_by_id(uuid) TO postgres WITH GRANT OPTION;
GRANT EXECUTE ON FUNCTION ecommerce.get_customer_by_id(uuid) TO api;

/*--------- FUNCTION: ecommerce.create_customer ------------*/
-- DROP FUNCTION IF EXISTS ecommerce.create_customer(jsonb);
CREATE OR REPLACE FUNCTION ecommerce.create_customer(
	customer_json jsonb)
    RETURNS json
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
	customer json;
	customer_name character varying(256);
	customer_email character varying(256);
	customer_id uuid;
BEGIN
	BEGIN
		SELECT c.name,
			   c.email
		  INTO customer_name,
			   customer_email
		  FROM jsonb_to_record(customer_json) c
				 (
					"name" character varying(256),
					email character varying(256)
				 );

		IF customer_name IS NULL THEN
			RAISE assert_failure USING MESSAGE = 'Field required: "name"';
		END IF;

		customer = ecommerce.get_customer_by(customer_name, COALESCE(customer_email, ''));

		RAISE assert_failure USING MESSAGE = 'customer already exist';
	EXCEPTION
		WHEN no_data_found THEN
			NULL;
	END;

	INSERT INTO ecommerce.customers ("name", email)
		 VALUES (customer_name, NULLIF(customer_email, ''))
	  RETURNING customers.id
		   INTO customer_id;

	customer = ecommerce.get_customer_by_id(customer_id);
	RETURN customer;
END;
$BODY$;

ALTER FUNCTION ecommerce.create_customer(jsonb) OWNER TO postgres;

REVOKE ALL ON FUNCTION ecommerce.create_customer(jsonb) FROM PUBLIC;
REVOKE ALL ON FUNCTION ecommerce.create_customer(jsonb) FROM robotfw;

GRANT EXECUTE ON FUNCTION ecommerce.create_customer(jsonb) TO postgres WITH GRANT OPTION;
GRANT EXECUTE ON FUNCTION ecommerce.create_customer(jsonb) TO api;
