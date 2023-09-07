#pip install fastapi
#pip install uvicorn

#uvicorn API:app --reload (modalità sviluppo)
#uvicorn app:app  (modalità x distribuzione/normale)

#http://127.0.0.1:8000/redoc
#http://127.0.0.1:8000/docs#/


import json
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException

app = FastAPI()

#read data from file JSON 
with open("df_airfleets_clean.json", "r") as file:
    dati = json.load(file)

#1____ - http://127.0.0.1:8000/airlines_db
@app.get("/airlines_db")
async def get_airlines_db():
    #initialise a list to store data rows side by side
    result = []

    #iterate over the data and create a string for each row
    for index, airline_data in dati['AIRLINE'].items():
        airline_name = airline_data
        country = dati['COUNTRY'][index]
        information = dati['INFORMATION/N.AIRCRAFT'][index]
        row_string = f"{airline_name}, {country}, {information}"
        result.append(row_string)

    #Join strings using semicolons as separators
    result_string = "; ".join(result)
    return {"Airlines Data Base": result_string}




#2____ http://127.0.0.1:8000/airline_info/Airfrance
@app.get("/airline_info/{airline_name}")
async def get_airline_info(airline_name: str):
    try:
        #removes spaces from the airline name
        airline_name = airline_name.replace(" ", "").lower()

        #search for the airline (also converting existing names to lowercase and removing spaces)
        for index, existing_airline in dati['AIRLINE'].items():
            if existing_airline.replace(" ", "").lower() == airline_name:
                country = dati['COUNTRY'][index]
                information = dati['INFORMATION/N.AIRCRAFT'][index]
                return {'AIRLINE': existing_airline, 'COUNTRY': country, 'INFORMATION/N.AIRCRAFT': information}

        #if the airline doesn't exist return a error message
        return {'error': f"Airline '{airline_name}' not found"}
    except KeyError as e:
        return {'error': f"Missing field: {e}"}
    
    
    
    
#3____ http://127.0.0.1:8000/get_airlines_by_country/Italy   
@app.get("/airlines_info_by_country/{country_name}")
async def get_airlines_info_by_country(country_name: str):
    try:
        #transform country name into uppercase
        country_name = country_name.capitalize()

        #initialize a list to store airlines and their related data
        compagnie_aeree = []
        num = 0

        #loop to search for the country
        for key, row in dati['COUNTRY'].items():
            if row.lower() == country_name.lower():
                airline_name = dati['AIRLINE'][key]
                information = dati['INFORMATION/N.AIRCRAFT'][key]
                compagnia_aerea = f"{airline_name}, {row}, {information}"
                compagnie_aeree.append(compagnia_aerea)
        
        #calculate the number of found airlines
        num = len(compagnie_aeree)

        #check if the country has been found
        if compagnie_aeree:
            #concatenate the airlines into a string separated by semicolons
            result_string = "; ".join(compagnie_aeree)
            return {"Airline find": num, "Airline Details": result_string}
        else:
            raise HTTPException(status_code=404, detail=f"Nessuna compagnia aerea trovata per il paese {country_name}")

    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Missing field: {e}")
