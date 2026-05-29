import numpy as np
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Configuración de conexión a MongoDB
MONGO_URI = "mongodb://localhost:27017/?directConnection=true"
client = MongoClient(MONGO_URI)
db = client["Política"]
coleccion = db["Discursos"]

# 2. Cargar el mismo modelo de NLP usado para poblar la BD
print("Cargando modelo de NLP (all-MiniLM-L6-v2)...")
modelo = SentenceTransformer('all-MiniLM-L6-v2')

def buscar_discursos(consulta_texto, top_k=5):
    # Generar el embedding de la consulta del usuario
    embedding_consulta = modelo.encode([consulta_texto])
    
    # Recuperar todos los documentos de la base de datos
    documentos = list(coleccion.find({}))
    if not documentos:
        print("La base de datos está vacía. Ejecuta el poblamiento primero.")
        return

    # Extraer los embeddings y prepararlos para el cálculo matemático
    embeddings_db = [doc["embedding"] for doc in documentos]
    
    # Calcular similitud coseno usando scikit-learn
    # Esto compara la consulta contra TODOS los documentos a la vez
    similitudes = cosine_similarity(embedding_consulta, embeddings_db)[0]
    
    # Asociar cada documento con su puntaje de similitud
    resultados = []
    for i, doc in enumerate(documentos):
        resultados.append({
            "id": doc["_id"],
            "texto": doc["texto"][:200] + "...", # Mostramos solo un extracto de 200 caracteres
            "similitud": similitudes[i]
        })
        
    # Ordenar de mayor a menor similitud y tomar el Top K
    resultados_ordenados = sorted(resultados, key=lambda x: x["similitud"], reverse=True)[:top_k]
    
    # Imprimir los resultados por consola
    print(f"\nResultados Top {top_k} para: '{consulta_texto}'")
    print("="*60)
    for i, res in enumerate(resultados_ordenados, 1):
        print(f"{i}. Similitud Coseno: {res['similitud']:.4f} | ID (SHA-256): {res['id']}")
        print(f"   Extracto: {res['texto']}\n")

if __name__ == '__main__':
    while True:
        consulta = input("Ingresa tu consulta textual (o 'salir' para terminar): ")
        if consulta.lower() == 'salir':
            break
        if consulta.strip():
            buscar_discursos(consulta)