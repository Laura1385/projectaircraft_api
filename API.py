#pip install fastapi
#pip install uvicorn

from fastapi import FastAPI

app = FastAPI()

dati = {
    'luoghi': [
        'Milano',
        'Roma',
        'Riva del Garda',
        'Sanremo',
        'Taggia',
        'Biot',
        'Cerami']
}

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
    
    