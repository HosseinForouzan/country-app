import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel

# set database
conn = psycopg2.connect(database="hossein",
                        host="localhost",
                        user="hossein",
                        password="password",
                        port="5432")

cursor = conn.cursor()

cursor.execute("select exists(select * from information_schema.tables where table_name=%s)", ('country',))

if (not cursor.fetchone()[0]):

    cursor.execute("CREATE TABLE country(\
                id INTEGER PRIMARY KEY, \
                name VARCHAR(55) NOT NULL,\
                capital VARCHAR(55),\
                currency VARCHAR(55)\
                );\
                ")
    conn.commit()

app = FastAPI()

@app.get("/")
def get_countries():
    cursor.execute("SELECT * FROM country;")
    countries = cursor.fetchall()
    result = []

    for country in countries:
        result.append({'id': country[0], 'name': country[1], 'capital': country[2], 'currency': country[3]})
    
    return result

@app.get("/country/{country_id}")
def get_country(country_id: int):
    cursor.execute("SELECT id FROM country;")
    ids = cursor.fetchall()
    result_ids = []
    for id in ids:
        result_ids.append(id[0])
        
    if country_id in result_ids:
        cursor.execute(f"SELECT * FROM country WHERE id = {country_id} ")
        country = cursor.fetchone()
        result = {'id': country[0], 'name': country[1], 'capital': country[2], 'currency': country[3]}
    
    return result


class Country(BaseModel):
    id: int
    name: str
    capital: str | None
    currency: str | None

@app.post("/countries/")
def create_country(country: Country):
    country_dict = country.dict()
    cursor.execute(f"INSERT INTO country VALUES( {country_dict['id']},\
                                                '{country_dict['name']}',\
                                                '{country_dict['capital']}', \
                                                '{country_dict['currency']}')")
    conn.commit()

    return country_dict


@app.delete("/countries/{country_id}")
def delete_country(country_id: int):
   cursor.execute(f"DELETE FROM country WHERE id= {country_id};")
   conn.commit()

   return {"id": country_id}

@app.put("/countries/{country_id}")
def update_country(country_id: int, country: Country):
    country_dict = country.dict()
    cursor.execute(f"UPDATE country SET name='{country_dict['name']}',\
                                        capital='{country_dict['capital']}', \
                                        currency='{country_dict['currency']}' \
                                         WHERE id= {country_id}")

    conn.commit()

    return {"update_status": "OK"}