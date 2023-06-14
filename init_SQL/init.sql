-- public.dcd_car_params definition

-- Drop table

-- DROP TABLE public.dcd_car_params;

CREATE TABLE public.dcd_car_params (
	id serial4 NOT NULL,
	car_type varchar NOT NULL,
	params text NOT NULL,
	"operator" varchar NOT NULL,
	create_time timestamp NOT NULL DEFAULT now()::timestamp without time zone,
	status int2 NOT NULL DEFAULT 1,
	update_time timestamp NULL,
	CONSTRAINT dcd_car_params_pkey PRIMARY KEY (id)
);