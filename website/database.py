
from sqlalchemy import create_engine, text
from flask_mail import Mail,Message
import os
#from website.email_config import mail  # Import the mail object from email.py

# connection_string=os.environ.get('connection_string')
# print(connection_string)
connection_string="mysql+pymysql://v7ksxyhwiyvck3ehk73z:pscale_pw_UihWfqn6aKIfFKGfV0fPgFjxrlf1GF5InL02NlBjRU1@aws.connect.psdb.cloud/apartments?charset=utf8mb4"

engine = create_engine(connection_string,
                       connect_args={"ssl": {
                           "ssl_ca": "/etc/ssl/cert.pem"
                       }})

def load_apartments_from_db(page_number):
    offset = (page_number - 1) * 12
    query = text(f"SELECT * FROM apartments ORDER BY id LIMIT 12 OFFSET {offset}")

    with engine.connect() as conn:
         result = conn.execute(query)
    aprtments = []
    for apartment in result.all():
        aprtments.append(apartment._asdict())
    return aprtments

def load_apartment_from_db(id):
  with engine.connect() as conn:
    query = text("SELECT * FROM apartments WHERE id = :id")
    result = conn.execute(query.bindparams(id=id))
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return rows[0]._asdict()

def add_new_listings_to_db(data):
    with engine.connect() as conn:
        query = text(
            """INSERT INTO apartments (address, price, beds, bathrooms, property_type, year_built, img_link, sqft, sqft_lot, HOA_fees) VALUES
               (:address, :price, :beds, :bathrooms, :property_type, :year_built, :image, :sqft, :sqft_lot, :HOA_fees)""")
        conn.execute(query.bindparams(
            address=data['address'],
            price=data['price'],
            beds=data['beds'],
            bathrooms=data['bathrooms'],
            property_type=data['property_type'],
            year_built=data['year_built'],
            image=data['image'],
            sqft=data['sqft'],
            sqft_lot=data['sqft_lot'],
            HOA_fees=data['HOA_fees']))
        

def user_filter(user_prefs):
    with engine.connect() as conn:
        sql = "SELECT * FROM apartments WHERE 1=1"
        params = {}
        if user_prefs["location"]:
            sql += " AND address LIKE :location"
            params['location'] = "%"+user_prefs['location']+"%"
        property_types = [value for key, value in user_prefs.items() if key == 'propertyType' and value!='' ]
        if property_types:
            sql += " AND property_type IN :property_types"
            params["property_types"] =tuple(property_types)

        if  user_prefs["min_price"]!='0':
            sql += " AND price >= :min_price"
            params["min_price"] = int(user_prefs["min_price"])
            
        if  user_prefs["max_price"]!='0':
            sql += " AND price <= :max_price"
            params["max_price"] = int(user_prefs["max_price"])

        if user_prefs['min_bedrooms']!='0':
            sql += " AND beds <= :min_bedrooms"
            params["min_bedrooms"] = int(user_prefs["min_bedrooms"])

        if user_prefs['max_bedrooms']!='0':
            sql += " AND beds <= :max_bedrooms"
            params["max_bedrooms"] = int(user_prefs["max_bedrooms"])

        if user_prefs['min_bathrooms']!='0':
            sql += " AND bathrooms <= :min_bathrooms"
            params["min_bathrooms"] = int(user_prefs["min_bathrooms"])
            
        if user_prefs['max_bathrooms']!='0':
            sql += " AND bathrooms <= :max_bathrooms"
            params["max_bathrooms"] = int(user_prefs["max_bathrooms"])
        
        if  user_prefs["min_sqft"]!='0':
            sql += " AND sqft >= :min_sqft"
            params["min_sqft"] = int(user_prefs["min_sqft"])

        if  user_prefs["max_sqft"]!='0':
            sql += " AND sqft <= :max_sqft"
            params["max_sqft"] = int(user_prefs["max_sqft"])

        if user_prefs["min_sqft_lot"]!='0':
            sql += " AND sqft_lot >= :min_sqft_lot"
            params["min_sqft_lot"] = int(user_prefs["min_sqft_lot"])

        if  user_prefs["max_sqft_lot"]!='0':
            sql += " AND sqft_lot <= :max_sqft_lot"
            params["max_sqft_lot"] = int(user_prefs["max_sqft_lot"])

        if user_prefs['min_home_age']!='0':
            sql += " AND year_built >= :min_home_age"
            params["min_home_age"] = int(user_prefs["min_home_age"])

        if user_prefs['hoa_fees_type']!='0':
            if user_prefs['hoa_fees_type']=='no_hoa':
                sql += " AND (HOA_fees IS NULL OR HOA_fees = 0)"
            elif user_prefs['max_HOA_fees']!='0':
                sql += " AND HOA_fees <= :max_HOA_fees"
                params["max_HOA_fees"] = int(user_prefs["max_HOA_fees"])
        
        garage_types = [value for key, value in user_prefs.items() if key == 'garage' and value!='0']
        if garage_types:
            sql += " AND garage IN :garage_types"
            params["garage_types"] =tuple(garage_types)

        if 'id' in user_prefs:
            sql += " AND created_at >:created_at"
            params["created_at"] =user_prefs['created_at']                                                                                                                                                                                                                     


        query = text(sql)
        print ("user prefs",user_prefs,"\n")                                                                                                                                  
        print("sql",sql,"\n")
        print("params",params,"\n")
        result = conn.execute(query.bindparams(**params)) 
        aprtments = []
        for apartment in result.all():
            aprtments.append(apartment._asdict())
        return aprtments

def add_user_preferences_to_db(data):
    with engine.connect() as conn:
        query = text(
            """INSERT INTO UserPreferences (location, propertyType, min_price, max_price, min_bedrooms, max_bedrooms, 
                min_bathrooms, max_bathrooms, hoa_fees_type, max_HOA_fees, 
                min_sqft, max_sqft, min_sqft_lot, max_sqft_lot, min_home_age, garage ,email) VALUES 
               (:location, :propertyType, :min_price, :max_price, :min_bedrooms, :max_bedrooms, 
                :min_bathrooms, :max_bathrooms, :hoa_fees_type, :max_HOA_fees, 
                :min_sqft, :max_sqft, :min_sqft_lot, :max_sqft_lot, :min_home_age, :garage, :email)""")

        # Execute the SQL query with the data dictionary
        conn.execute(query.bindparams(
            location=data['location'],
            propertyType=data['propertyType'],
            min_price=data['min_price'],
            max_price=data['max_price'],
            min_bedrooms=data['min_bedrooms'],
            max_bedrooms=data['max_bedrooms'],
            min_bathrooms=data['min_bathrooms'],
            max_bathrooms=data['max_bathrooms'],
            hoa_fees_type=data['hoa_fees_type'],
            max_HOA_fees=data['max_HOA_fees'],
            min_sqft=data['min_sqft'],
            max_sqft=data['max_sqft'],
            min_sqft_lot=data['min_sqft_lot'],
            max_sqft_lot=data['max_sqft_lot'],
            min_home_age=data['min_home_age'],
            garage=data['garage'],
            email=data['email']))


def offLineSerach():
 keys = [
    'id', 'location', 'propertyType', 'min_price', 'max_price',
    'min_bedrooms', 'max_bedrooms', 'min_bathrooms', 'max_bathrooms',
    'hoa_fees_type', 'max_HOA_fees', 'min_sqft', 'max_sqft',
    'min_sqft_lot', 'max_sqft_lot', 'min_home_age', 'garage', 'email','created_at'
]
 with engine.connect() as conn:
    query=text("SELECT * FROM  UserPreferences ")
    result=conn.execute(query)
    for row in result.all():
        print(row)
        string_tuple = [str(item) for item in row]
        property_dict = dict(zip(keys, string_tuple))
        apartment=user_filter(property_dict)
        if apartment:
            msg = Message("Hey", sender='noreply@demo.com', recipients=['kobihazut8@gmail.com']) 
            msg.body = "Hey how are you? Is everything okay?"
            #mail.send(msg)
# def add_user(data):

#     with engine.connect() as conn:
#         query = text(
#             """INSERT INTO note (id, data, date, user_id) VALUES 
#                (:id, :data, :date, :user_id)""")
        
#         conn.execute(query.bindparams(
#             id=data['id'],
#             data=data['data'],
#             date=data['date'],
#             user_id=data['user_id']))



def add_user(data,password1):
    with engine.connect() as conn:
        query = text(
            """INSERT INTO user ( email, password, first_name) VALUES
               (:email, :password1, :firstName)""")
      
        conn.execute(query.bindparams(
            email=data['email'],
            password=password1,
            first_name=data['firstName'],
           
            
            ))