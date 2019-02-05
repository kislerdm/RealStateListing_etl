# RealstateListing
Programs reads the input json file having details of flat ad listing on immobilienscout24 and loads it to database for furthur processing.

# Tools and Languages
  - language - Python 3.7.0
  - database - postgres10

## How to run
```
to start the process
> python main.py

to stop the process
> python stop.py

```


# Functionality :
## HighLevel :
1. This programs reads the input json file having details of flat ad listing on immobilienscout24.
2. Extracts the necessary (see below table structure ) information  from file and insert into
    postgresql database for further analysis.
## Prerequisite:
1. Configure the input directory, file prefix and processing directory in config.txt under Input-file section.
2. Configure postgresql db details in config.txt under database-connection section.
3. For this exercise already done but if changes needed - please populate mapping.txt with the mapping
    of tag in input to internal column name  with default value.
    this file have list of attribute to be extracted from input file for transformation and load.
    - tag => The tag or the key in the input whose value we want to extract and use. e.g. realEstate_baseRent
    - default value => if tag is not found what is the default value to be assigned and persisted in database.
    - internal column name => we are mapping tag to internal column name to be able to have descriptive
                            name for them. Also if attribute is directly inserted into the database without
                            any manipulation than column name is same as database column name.
4. Have mapping of query to binding variable in parser.get_insert_query() if there are any changes done in
    table structure/mapping.txt/parser.business_logic
5. Install the packages mentioned in requirements.txt
6. Install postgresql db. and run create_table.sql to create tables.

 ## Detailed :
1. Program runs as a daemon, use stop.py to stop it. it will only stops after processing current batch
    of files.
2. It continuously ( sleeps for 90 secs in between) polls the input directory (filepath) for file
    prefix pattern (fileprefix). (filepath and fileprefix are configured in the config.txt)
3. If file is found, it moves the file to a different directory for processing. (processing_directory)
4. It opens the file and reads it line by line.
5. For each line use call parser.get_formatted_dict which will extract the necessary information from input
    have a dictionary populated (column_data) with internal column name and value of it.
6. Call parser.business_logic, this function is place holder for any transformation needed on input data
    and new attribute population logic will reside (or other function will be called from here) in this function.
7. Get the insert query from parser.get_insert_query() and call execute with query and dictionary column_data.
8. Once all the records are inserted into database call commit.
9. Sleep for 90 seconds and then poll the input directory for new file.


## Table Structure :

### fact_flat
            
Fact table in star schema, contains most important details related to flat, can be used alone to do analytics on available flats in a price range etc.



|Column_name      | Data type   | Constraint    | Default   | comment                                  |
|-----------------|-------------|---------------|-----------|------------------------------------------|
|flat_id          | INTEGER     |  PRIMARY KEY  |           | unique id for property                       |
|agency_id        | varchar(60) | NOT NULL      |           | unique id for agency posting ad          |
|sys_creation_date| date        | not null      |CURRENT_DATE| date when record is inserted in table   |
|city varchar(60) |             |               |           | city when property is located                |
|apartment_type   |varchar(20)  |               |           | type of property e.g. APARTMENT,ROOF_STOREY, PENTHOUSE etc.|
|apartment_size   |INTEGER      |               |           | size of property in sqr mtr             |
|base_rent        |decimal(10,2)|               |           | base rent flat                           |
|total_rent       |decimal(10,2)|               |           | total rent of flat                       |
|rent_scope       |varchar(40)  |               |           | scope of rent warm,cold etc              |
|number_of_rooms  |INTEGER      |               |           | number of rooms in property             |


### dim_flat_address

This dimension table contains address information of flat listed in fact_flat table.

|Column_name      | Data type   | Constraint    | Default   | comment                      |
|-----------------|-------------|---------------|-----------|------------------------------|
|flat_id          |INTEGER      |PRIMARY KEY FOREIGN KEY REFERENCES fact_flat (flat_id)||unique id for property|
|sys_creation_date| date        |not null       | CURRENT_DATE|date when record is inserted in table       |
|house_number     |varchar(20)  |               |           | house number of property     |
|street           |varchar(60)  |               |           | street name fof property     |
|quarter          | varchar(40) |               |           | quarter name of property     |
|city             |varchar(60)  |               |           | city name of property        |
|region           |varchar(60)  |               |           | region name of property      |
|flat_longitude   |INTEGER      |               |           | longitude of property        |
|flat_latitude    |INTEGER      |               |           | latitude of property         |
|post_code        |varchar(11)  |               |           | postcode of property         |


### dim_agency

This dimension table contains information of agency posted the ad for property and their address.

|Column_name      | Data type   | Constraint    | Default   | comment              |
|-----------------|-------------|---------------|-----------|----------------------|
|agency_id        |varchar(60)  |PRIMARY KEY    |           | unique id for agency |
|sys_creation_date| date        |not null       | CURRENT_DATE|date when record is inserted in table|
|company          |varchar(100) |               |            | name of the company/agency|
|contact_person   |varchar(100) |               |           | full name of the contact person of agency|
|house_number     |varchar(40)  |               |           | house number of agency location |
|street           |varchar(60)  |               |           | street name of agency location|
|city             |varchar(60)  |               |           | city name of agency location|
|post_code        |varchar(11)  |               |           | post_code of agency location |
|email            |varchar(60)  |               |           | email of agency |
|mobile_number    |varchar(50)  |               |           | mobile number of agency|
|phone_number     |varchar(50)  |               |           | phone number of agency|


### dim_flat_details

This dimension table contains additional details for property which will be useful for analysis.


|Column_name      | Data type   | Constraint    | Default   | comment                     |
|-----------------|-------------|---------------|-----------|-----------------------------|
|flat_id          |INTEGER      |PRIMARY KEY FOREIGN KEY REFERENCES fact_flat (flat_id)|| unique id for property|
|sys_creation_date| date        |not null       | CURRENT_DATE|date when record is inserted in table|
|heating_cost     |decimal(10,2)|               |           |heating cost of property|
|service_charge   |decimal(10,2)|               |           |total service charge including heating cost|
|construction_year| INTEGER     |               |           |year of construction of property|
|refurbishment_year| INTEGER    |               |           |refurbishment year|
|flat_condition   |varchar(40)  |               |           |condition of flat e.g. MODERNIZED, MINT_CONDITION etc.|
|number_of_floor  |INTEGER      |               |           |number of floors in the property|
|garden_available |varchar(20)  |               |           | if garden is available|
|guest_toilet_available|varchar(20)|            |           |if guest toilet is available|
|lift_available   |varchar(20)  |               |           |if lift is available|
|pets_allowed     |varchar(20)  |               |           |if pets are allowed on property|



### dim_flat_metadata

This dimension table contains metadata information of ad posted on site.


|Column_name      | Data type   | Constraint    | Default   | comment                |
|-----------------|-------------|---------------|-----------|------------------------|
|flat_id          |INTEGER      |PRIMARY KEY FOREIGN KEY REFERENCES fact_flat (flat_id)||unique id for flat|
|sys_creation_date| date        |not null       |CURRENT_DATE|date when record is inserted in table|
|state            |varchar(10)  |               |           |state of ad ACTIVE/INACTIVE|
|creation_date    |timestamptz  |               |           |date when ad was created|
|modify_date      |timestamptz  |               |           |date when ad was modified|


## Configuration
### config.txt (./RealstateListing/config/config.txt)
Used to configure details for input file under Input-file section
    - input file path (filepath)
    - input file prefix (fileprefix)
    - processing directory to which file will be moved from input directory (processing_directory)
    
and database details for postgres under database-connection section

```
[Input-file]
filepath = C:\Users\sachin.vyas\Documents\ds_training\
fileprefix = immobilienscout24
processing_directory = C:\\Users\\sachin.vyas\\Documents\\ds_training\\processing_dir\\

[database-connection]
dbname=postgres
host=localhost
password=unix11
port=5432
user=postgres

```

### mapping.txt (./RealstateListing/config/mapping.txt)
Mapping file provide function to map input tag directly to column name and if tag is not found populate the default value.


```
###############################
# mapping file
# Please add the data in below format
# tag_in_json:default_value_if_tag_not_found:column_name
####################################
#fact_flat
contactDetails_id:ERROR:flat_id
realEstate_apartmentType:NA:apartment_type
realEstate_livingSpace:0:apartment_size
realEstate_baseRent:0:base_rent

```