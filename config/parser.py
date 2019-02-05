import logging
import json
import configparser

logger = logging.getLogger(__name__)

def json_extract(json_data):
    """
    function gets the input json and extract the data tag and returns it
    :param json_data:
    :return: data tag of the json.
    """
    if json_data:
        return json.loads(json_data)['data']

def config_parser():
    """
    reads the config.txt and load input file and database connection details.
     
    :return: dictionary having input file and database details
    
    """
    config_dict = {'Input-file' :
                       {
                       'filepath' : "" ,
                       'fileprefix': "",
                       'processing_directory': ""
                        },
                   'database-connection' :
                       {
                        'dbname': '',
                        'host': '',
                        'password': '',
                        'port': 5432,
                        'user': ''
                        }
                   }
    configParser = configparser.RawConfigParser()
    configFilePath = r'.\config\config.txt'
    configParser.read(configFilePath)


    for key,value in config_dict.items():
        for lk in value.keys():
            config_dict[key][lk] = configParser.get(key,lk)

    return config_dict




def get_formatted_dict(data):
    """
    function get input json/dictionary extract all the tag/attribute mentioned in config.txt file and return a dictionary having all the input fields.
    in case a field is not found in the input it will replace it with default value mentioned in mapping.txt

    :param data: a line in input file in json/dict format.
    :return: Dictionary having required fields for table insert.
    """
    tag_to_attr_mapping, col_to_def_value = load_mapping()

    for tag in tag_to_attr_mapping.keys():
        try:
            col_to_def_value[tag_to_attr_mapping[tag]] = data[tag]

        except KeyError:
            pass

    return col_to_def_value

def load_mapping():
    """
    this function will read each colon separated line of config file.
    it will create two dictionary.
        1. Mapping of the json tag to internal attribute name/column name.
        2. Mapping of tag to default value in case tag is not found in json.

    :return:
    tag_to_attr_mapping : type Dict : contains mapping of the json tag to internal attribute name/column name.
    tag_to_def_value : type Dict : Mapping of tag to default value in case tag is not found in json.

    """
    #TODO instead of config file replace it with yaml
    tag_to_attr_mapping = {}
    col_to_def_value = {}
    with open(".\config\mapping.txt","r") as config_file:
        for line in config_file:
            if line[0] == "#": #to ignore comments in the config file.
                continue
            try:
                tag, default_value, column_name = line.rstrip("\n").split(":")
                tag_to_attr_mapping[tag] = column_name
                col_to_def_value[column_name] = default_value

            except ValueError as e:
                logger.error("Got {} for line {}".format(e,line))
                raise
    return tag_to_attr_mapping, col_to_def_value



def business_logic(data):
    """
    place holder to implement business logic related parsing. all the code/calls to functions related to business logic will be here.

    :return:
    data : type dict : modified dictionary after applying logic
    """
    try:
        # append first_name and last_name to store full name
        data['contact_person'] = data['first_name'] + " " + data['last_name']

        #append country code to phone numbers
        if data['mobile_number'] !="" and  data['mobile_number'][0] != '+' :
            data['mobile_number'] = data['mobile_country'] + data['mobile_number'].replace(" ","")
        if data['phone_number'] !="" and data['phone_number'][0] != '+':
            data['phone_number'] = data['phone_country'] + data['phone_number'].replace(" ","")

        # if heating cost is not included in service charge, increment service charge with heating cost
        if data['heating_cost_in_service'] == "NO":
            #print(data['service_charge'],data['heating_cost'])
            data['service_charge'] = int(data['service_charge']) + int(data['heating_cost'])



    except KeyError as e:
        logger.error("Got {} for {}".format(e,e.args))
        raise
    return data

def get_insert_query():
        """
        function to return all the insert query. keeping it inside parser as names of the parameter are mentioned inside query.

        :return:
        query : type string : all the insert query with name of the bind parameters.
        """

        query = """
            
            INSERT into 
                fact_flat 
                (flat_id, city, agency_id,  apartment_type, apartment_size, base_rent, total_rent, rent_scope, number_of_rooms) 
            VALUES 
                (%(flat_id)s, %(city)s, %(agency_id)s, %(apartment_type)s,%(apartment_size)s, %(base_rent)s, %(total_rent)s, %(rent_scope)s, %(number_of_rooms)s);
            INSERT into 
                dim_flat_address 
                (flat_id, house_number, street, quarter, city, region, flat_longitude, flat_latitude, post_code) 
            VALUES 
                (%(flat_id)s, %(house_number)s, %(street)s, %(quarter)s, %(city)s,%(region)s, %(flat_longitude)s, %(flat_latitude)s, %(post_code)s);
            INSERT into 
                dim_agency 
                (agency_id, company, city, house_number, post_code, street, mobile_number, email, contact_person, phone_number) 
            VALUES 
                (%(agency_id)s,%(company)s, %(agency_city)s, %(agency_house_number)s, %(agency_post_code)s, %(agency_street)s, %(mobile_number)s, %(email)s, %(contact_person)s, %(phone_number)s) ON CONFLICT (agency_id) DO NOTHING;
            INSERT into        
                dim_flat_details
                (flat_id, heating_cost, service_charge, construction_year, refurbishment_year, flat_condition, number_of_floor, garden_available, guest_toilet_available, lift_available,pets_allowed) 
            VALUES 
                (%(flat_id)s, %(heating_cost)s, %(service_charge)s, %(construction_year)s, %(refurbishment_year)s, %(flat_condition)s, %(number_of_floor)s, %(garden_available)s, %(guest_toilet_available)s,%(lift_available)s,%(pets_allowed)s);
            INSERT into 
                dim_flat_metadata 
                (flat_id, state, creation_date, modify_date) 
            VALUES 
                (%(flat_id)s, %(state)s, %(creation_date)s, %(modify_date)s);
            
        """
        return query

if __name__ == "__main__":
    #print(load_config())
    #print(business_logic({"first_name":"sachin","last_name":"vyas"}))
    #print(business_logic({"first_name": "sachin", "lst_name": "vyas"}))
    print(config_parser())