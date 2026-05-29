import os
import hashlib
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer


MONGO_URI = "mongodb://localhost:27017/?directConnection=true"
client = MongoClient(MONGO_URI)
db = client["Política"]
coleccion = db["Discursos"]


print("Cargando modelo de NLP...")
modelo = SentenceTransformer('all-MiniLM-L6-v2')


CARPETA_CORPUS = "./DiscursosOriginales"

def procesar_corpus():
    if not os.path.exists(CARPETA_CORPUS):
        print(f"Error: No se encontró la carpeta '{CARPETA_CORPUS}'.")
        return

    archivos = [f for f in os.listdir(CARPETA_CORPUS) if f.endswith('.txt')]
    
    if not archivos:
        print("No se encontraron archivos .txt en la carpeta.")
        return

    print(f"Iniciando procesamiento de {len(archivos)} documentos...")

    for archivo in archivos:
        ruta_completa = os.path.join(CARPETA_CORPUS, archivo)
        
        with open(ruta_completa, 'r', encoding='utf-8') as f:
            texto_completo = f.read().strip()
            
        if not texto_completo:
            continue
        
        hash_sha256 = hashlib.sha256(texto_completo.encode('utf-8')).hexdigest()
        

        embedding = modelo.encode(texto_completo).tolist()
        

        documento = {
            "_id": hash_sha256,
            "texto": texto_completo,
            "embedding": embedding
        }
        

        try:
            #upsert para no duplicar llave primaria en caso de accidente jiji
            coleccion.replace_one({"_id": hash_sha256}, documento, upsert=True)
            print(f"Documento '{archivo}' insertado correctamente.")
        except Exception as e:
            print(f"Error al insertar '{archivo}': {e}")

    print("Poblamiento finalizado con éxito")

if __name__ == '__main__':
    procesar_corpus()