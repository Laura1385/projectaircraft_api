#pip install fastapi
#pip install uvicorn

#In terminale
#uvicorn api:app --reload (modalità sviluppo)
#uvicorn api:app  (modalità x distribuzione/normale)
#CTRL+C (per uscire/interrompere)
#http://127.0.0.1:8000/redoc (documentazione)
#http://127.0.0.1:8000/docs#/ (documentazione)

#In terminale con container 
#docker build -t api_airlines .  (crea immagine)
#docker run -p 8000:8000 -d api_airlines   (lancia)
#docker ps (mostra container attivi)
#docker --version
#netstat -tuln (mostra porte in ascolto)
#http://localhost:8080/airlines_db


import json
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse
from fastapi.responses import JSONResponse
from pydantic import BaseModel

#for documented error 404 e 500
class Message(BaseModel):
    message: str


app = FastAPI()

#1____ http://127.0.0.1:8000/show_map
@app.get("/show_map")
async def show_map():
    # Specifica il nome del tuo file HTML nella stessa directory dell'applicazione
    html_file_name = "world_map.html"
    
    # Restituisci il file HTML come risposta
    return FileResponse(html_file_name, media_type="text/html")


#read data from file JSON 
with open("df_airfleets_clean.json", "r") as file:
    data = json.load(file)

#2____ http://127.0.0.1:8000/airlines_db
@app.get("/airlines_db")
async def get_airlines_db():
    # Initialize a set to store unique countries and airlines
    unique_countries = set()
    unique_airlines = set()

    # Initialize a list to store data rows side by side
    result = []

    # Iterate over the data and create a string for each row
    for index, airline_data in data['AIRLINE'].items():
        airline_name = airline_data
        country = data['COUNTRY'][index]
        information = data['INFORMATION/N.AIRCRAFT'][index]
        row_string = f"{airline_name}, {country}, {information}"
        result.append(row_string)

        # Add the country and airline to the set to count unique values
        unique_countries.add(country)
        unique_airlines.add(airline_name)

    # Join strings using semicolons as separators
    result_string = "; ".join(result)

    # Get the count of unique countries and airlines
    num_unique_countries = len(unique_countries)
    num_unique_airlines = len(unique_airlines)

    return {
        "Number of Countries with Airlines": num_unique_countries,
        "Number of Airlines in Db": num_unique_airlines,
        "Airlines Data Base": result_string
    }


#3____ http://127.0.0.1:8000/airline_info/Airfrance
@app.get("/airline_info/{airline_name}", responses={404: {"model": Message}, 500: {"model": Message}})
async def get_airline_info(airline_name: str):
    try:
        #removes spaces from the airline name
        airline_name = airline_name.replace(" ", "").lower()

        #search for the airline (also converting existing names to lowercase and removing spaces)
        for index, existing_airline in data['AIRLINE'].items():
            if existing_airline.replace(" ", "").lower() == airline_name:
                country = data['COUNTRY'][index]
                information = data['INFORMATION/N.AIRCRAFT'][index]
                if information.strip() == "":
                    return JSONResponse(status_code=404, content={"404 - Warning!": f"Airline '{airline_name}'name is empty"})
                
                return {'AIRLINE': existing_airline, 'COUNTRY': country, 'INFORMATION/N.AIRCRAFT': information}
            
        return JSONResponse(status_code=404, content={"404 - Warning!": f"Airline '{airline_name}' not found"})
    
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"500 - Missing field: {e}")
    
    
    
#4____ http://127.0.0.1:8000/get_airlines_by_country/Italy   
@app.get("/airlines_info_by_country/{country_name}", responses={404: {"model": Message}, 500: {"model": Message}})
async def get_airlines_info_by_country(country_name: str):
    try:
        #transform country name into uppercase
        country_name = country_name.capitalize()

        #initialize a list to store airlines and their related data
        airlines = []
        num = 0

        #loop to search for the country
        for key, row in data['COUNTRY'].items():
            if row.lower() == country_name.lower():
                airline_name = data['AIRLINE'][key]
                information = data['INFORMATION/N.AIRCRAFT'][key]
                #airline = f"{airline_name}, {row}, {information}"
                airline = {'Airline name':airline_name, 'Country' : row, 'info': information}
                airlines.append(airline)
        
        #calculate the number of found airlines
        num = len(airlines)

        #check if the country has been found
        if airlines:
            #concatenate the airlines into a string separated by semicolons
            #result_string = "; ".join(airlines)
            return {"Total": num, "Details": airlines}
        else:
            raise HTTPException(status_code=404, detail=f"404 - Warning! No airlines found for the country {country_name}")

    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"500 - Missing field: {e}")
        
       
    
#5____ http://127.0.0.1:8000/airlines_summary_by_country/italy
@app.get("/airlines_summary_by_country/{country_name}",responses={404: {"model": Message}, 500: {"model": Message}})
async def get_airlines_summary_by_country(country_name: str):
    try:
        #transform country name into uppercase
        country_name = country_name.capitalize()
        
        trovato = False  # Flag per verificare se il paese è stato trovato

        #initialize a list to store airlines and their related data
        active_count = 0
        disappeared_count = 0
        absorbed_count = 0

        #ciclo for per cercare il paese
        for key, row in data['COUNTRY'].items():
            if row.lower() == country_name.lower(): 
                trovato = True
                information = data['INFORMATION/N.AIRCRAFT'][key]

                if information.isdigit():  #controllo se è un numero (compagnia attiva)
                    active_count += 1
                elif information == 'inactive (with supported aircraft)':  #compagnia scomparsa
                    disappeared_count += 1
                elif information.startswith('inactive (with supported aircraft)Renamed / Merged to'):  #compagnia assorbita
                    absorbed_count += 1

        #verifica se il paese è stato trovato
        if trovato:
            return{
                'Found for': country_name,
                'Number of active airlines': active_count,
                'Number of failed airlines': disappeared_count,
                'Number of airlines absorbed': absorbed_count
            }
        else:
            raise HTTPException(status_code=404, detail=f"404 - Warning! No airlines found for the country {country_name}")

    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"500 - Missing field: {e}")
        
