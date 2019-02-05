drop table  IF EXISTS dim_agency;
drop table  IF EXISTS dim_flat_details;
drop table  IF EXISTS dim_flat_metadata;
drop table  IF EXISTS dim_flat_address;
drop table  IF EXISTS fact_flat cascade;
CREATE TABLE fact_flat
    (flat_id INTEGER ,
    agency_id varchar(60) NOT NULL,
    sys_creation_date date not null default CURRENT_DATE,
    city varchar(60),
    apartment_type varchar(20),
    apartment_size INTEGER,
    base_rent decimal(10,2),
    total_rent decimal(10,2),
    rent_scope varchar(40),
    number_of_rooms INTEGER,
    PRIMARY KEY (flat_id));

CREATE TABLE dim_flat_address
    (flat_id INTEGER ,
    sys_creation_date date not null default CURRENT_DATE,
    house_number varchar(20),
    street varchar(60),
    quarter varchar(40),
    city varchar(60),
    region varchar(60),
    flat_longitude INTEGER,
    flat_latitude INTEGER,
    post_code varchar(11),
    PRIMARY KEY (flat_id),
    FOREIGN KEY (flat_id) REFERENCES fact_flat (flat_id));



 CREATE TABLE dim_agency
   (agency_id varchar(60) NOT NULL,
   sys_creation_date date not null default CURRENT_DATE,
   company varchar(100),
   contact_person varchar(100),
   house_number varchar(40),
   street varchar(60),
   city varchar(60),
   post_code varchar(11),
   email varchar(60),
   mobile_number varchar(50),
   phone_number varchar(50),
   PRIMARY KEY (agency_id))
   ;

  CREATE TABLE dim_flat_details
    (flat_id INTEGER NOT NULL,
     sys_creation_date date not null default CURRENT_DATE,
     heating_cost decimal(10,2) ,
     service_charge decimal(10,2) ,
     construction_year INTEGER,
     refurbishment_year INTEGER,
     flat_condition varchar(40),
     number_of_floor INTEGER,
     garden_available varchar(20),
     guest_toilet_available varchar(20),
     lift_available varchar(20),
     pets_allowed varchar(20),
     PRIMARY KEY (flat_id),
     FOREIGN KEY (flat_id) REFERENCES fact_flat (flat_id));


  CREATE TABLE dim_flat_metadata
        (flat_id INTEGER NOT NULL,
        sys_creation_date date not null default CURRENT_DATE,
        state varchar(10),
        creation_date timestamptz,
        modify_date timestamptz,
        FOREIGN KEY (flat_id) REFERENCES fact_flat (flat_id));

