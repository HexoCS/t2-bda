import os
import hashlib
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

# Dentro de Docker/Jupyter se usan nombres de servicios del compose.
# Si quieres ejecutar desde fuera, puedes sobreescribir con una variable de entorno MONGO_URI.
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://mongo-primario:27017,mongo-secundario-1:27017,mongo-secundario-2:27017/?replicaSet=rs0"
)

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
client.admin.command("ping")

db = client["Política"]
coleccion = db["Discursos"]

print("Conectado a MongoDB")
print("Cargando modelo de NLP...")
modelo = SentenceTransformer("all-MiniLM-L6-v2")

CARPETA_CORPUS = "./DiscursosOriginales"

def procesar_corpus():
    if not os.path.exists(CARPETA_CORPUS):
        print(f"Error: No se encontró la carpeta '{CARPETA_CORPUS}'.")
        return

    archivos = sorted(f for f in os.listdir(CARPETA_CORPUS) if f.endswith(".txt"))

    if not archivos:
        print("No se encontraron archivos .txt en la carpeta.")
        return

    print(f"Iniciando procesamiento de {len(archivos)} documentos...")

    for archivo in archivos:
        ruta_completa = os.path.join(CARPETA_CORPUS, archivo)

        with open(ruta_completa, "r", encoding="utf-8") as f:
            texto_completo = f.read().strip()

        if not texto_completo:
            continue

        hash_sha256 = hashlib.sha256(texto_completo.encode("utf-8")).hexdigest()
        embedding = modelo.encode(texto_completo).tolist()

        documento = {
            "_id": hash_sha256,
            "archivo": archivo,
            "texto": texto_completo,
            "embedding": embedding
        }

        try:
            coleccion.replace_one({"_id": hash_sha256}, documento, upsert=True)
            print(f"Documento '{archivo}' insertado/actualizado correctamente.")
        except Exception as e:
            print(f"Error al insertar '{archivo}': {e}")

    print("Poblamiento finalizado con éxito")
    print("Total documentos en Discursos:", coleccion.count_documents({}))

if __name__ == "__main__":
    procesar_corpus()
