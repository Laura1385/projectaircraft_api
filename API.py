#pip install fastapi
#pip install uvicorn

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

#read data from file JSON
with open("df_airfleets_clean.json", "r") as file:
    dati = json.load(file)

@app.get("/airlines", response_class=HTMLResponse)
async def get_airlines():
    try:
        html_response = "<html><body><table>"
        html_response += "<tr><th>AIRLINE</th><th>COUNTRY</th><th>INFORMATION</th></tr>"

        for row in dati:
            html_response += f"<tr><td>{row['AIRLINE']}</td><td>{row['COUNTRY']}</td><td>{row['INFORMATION']}</td></tr>"

        html_response += "</table></body></html>"
        
        return HTMLResponse(content=html_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


'''
@app.get("/luoghi")
async def get_paesi():
    return {'dati': dati}

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