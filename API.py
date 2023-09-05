#pip install fastapi
#pip install uvicorn


from fastapi import FastAPI
import json

app = FastAPI()

#read data from file JSON 
with open("df_airfleets_clean.json", "r") as file:
    dati = json.load(file)

#1Ok - http://127.0.0.1:8000/airfleets
@app.get("/airfleets")
async def get_airfleets():
    #initialise a list to store data rows side by side
    result = []

    #iterate over the data and create a string for each row
    for index, airline_data in dati['AIRLINE'].items():
        airline_name = airline_data
        country = dati['COUNTRY'][index]
        information = dati['INFORMATION'][index]
        row_string = f"{airline_name}, {country}, {information}"
        result.append(row_string)

    #Join strings using semicolons as separators
    result_string = "; ".join(result)

    return result_string


#2Ok - http://127.0.0.1:8000/airline/Air%20France'
@app.get("/airline/{airline_name}")
async def get_airline_info(airline_name: str):
    try:
        #removes spaces from the airline name
        airline_name = airline_name.replace(" ", "").lower()

        #search for the airline (also converting existing names to lowercase and removing spaces)
        for index, existing_airline in dati['AIRLINE'].items():
            if existing_airline.replace(" ", "").lower() == airline_name:
                country = dati['COUNTRY'][index]
                information = dati['INFORMATION'][index]
                return {'AIRLINE': existing_airline, 'COUNTRY': country, 'INFORMATION': information}

        #if the airline doesn't exist return a error message
        return {'error': f"Airline '{airline_name}' not found"}
    except KeyError as e:
        return {'error': f"Missing field: {e}"}


#3 - 

def contains_category(text, category):
    # Rimuovi gli spazi all'inizio e alla fine del testo e convertilo in minuscolo
    cleaned_text = text.strip().lower()
    
    # Controlla se il testo contiene la categoria specificata
    return category in cleaned_text

@app.get("/airline_categories")
async def get_airline_categories(country: str):
    try:
        # Converte il paese inserito dall'utente in minuscolo
        country = country.lower()

        # Inizializza i contatori per le tre categorie
        aircraft_count = 0
        inactive_with_aircraft_count = 0
        inactive_merged_count = 0

        # Scorre i dati e conta le compagnie aeree nelle tre categorie
        for index in dati['AIRLINE']:
            airline_info = dati['INFORMATION'][index].lower()
            if dati['COUNTRY'][index].lower() == country:
                if contains_category(airline_info, "aircraft"):
                    aircraft_count += 1
                if contains_category(airline_info, "inactive (with supported aircraft)"):
                    inactive_with_aircraft_count += 1
                if contains_category(airline_info, "inactive (with supported aircraft)renamed / merged"):
                    inactive_merged_count += 1

        return {
            'country': country,
            'aircraft_count': aircraft_count,
            'inactive_with_aircraft_count': inactive_with_aircraft_count,
            'inactive_merged_count': inactive_merged_count
        }
    except Exception as e:
        return {'error': str(e)}








'''

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

#read data from file JSON
with open("df_airfleets_clean.json", "r") as file:
    dati = json.load(file)

#http://127.0.0.1:8000/all_airlines 
@app.get("/all_airlines", response_class=HTMLResponse) #return all data
async def get_airlines():
    html_response = "<html><body><table>"
    html_response += "<tr><th>AIRLINE</th><th>COUNTRY</th><th>INFORMATION</th></tr>"

    for key, value in dati["AIRLINE"].items():
        airline = value
        country = dati["COUNTRY"][key]
        information = dati["INFORMATION"][key]
        html_response += f"<tr><td>{airline}</td><td>{country}</td><td>{information}</td></tr>"

    html_response += "</table></body></html>"
    
    return HTMLResponse(content=html_response)



@app.post("/luoghi")
async def post_paesi(paese: str):
    if paese in dati['luoghi']:
        return {'dati': dati, 'message': "Località già esistente"}
    else:
        dati['luoghi'].append(paese)
        return {'dati': dati, 'message': "Località aggiunta"}
    
@app.delete("/luoghi")
async def delete_paesi(paese: str):
    if paese in dati['luoghi']:
        dati['luoghi'].remove(paese)
        return {'data': dati, 'message':"Località eliminata"}
    else:
        return {'data': dati, 'message': "La località non esiste"}
    
'''