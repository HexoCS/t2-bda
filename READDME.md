# Tarea Laboratorio 2 MongoDB 

## Requisitos Previos


* **Docker Desktop** (Asegurarse de que esté corriendo).
* **Python 3.8+**.
* **MongoDB Compass** 

---

## Levantar la Infraestructura (Docker)

El proyecto utiliza un clúster de MongoDB compuesto por 1 nodo primario y 2 secundarios.

1. **Iniciar los contenedores:**
   Desde la raíz del proyecto, ejecutar:

    ```bash
    docker compose up -d --build
    ```

    Luego verificar que los contenedores estén corriendo:

    ```bash
    docker ps
    ```

    Deberían aparecer al menos:

    ```text
    mongo-primario
    mongo-secundario-1
    mongo-secundario-2
    jupyter-mongo
    ```

2. **Iniciar replica set:**
    Una vez que los contenedores estén activos, inicializar el replica set desde el nodo primario inicial: 
    ```bash
    chmod +x init_replica_set.sh # para darle permiso de ejecución
    init_replica_set.sh
    ```
    El resultado esperado es similar a:

    ```text
    mongo-primario:27017        PRIMARY
    mongo-secundario-1:27017    SECONDARY
    mongo-secundario-2:27017    SECONDARY
    ```
3. **Verificar en mongoDB Compass:**
     ```bash
   mongodb://localhost:27017/?directConnection=true
    ```

4. Acceder a Jupyter Notebook

Para obtener la URL de Jupyter:

```bash
docker logs jupyter-mongo
```

Abrir en el navegador la URL indicada, normalmente:

```text
http://127.0.0.1:8888/lab
```

Si el contenedor fue configurado sin token, bastará con abrir esa URL directamente.


5. URI de conexión correcta

Como el notebook y el script se ejecutan dentro del contenedor `jupyter-mongo`, deben conectarse usando los nombres internos de Docker:

```python
MONGO_URI = "mongodb://mongo-primario:27017,mongo-secundario-1:27017,mongo-secundario-2:27017/?replicaSet=rs0"
```

No usar para las pruebas de tolerancia a fallos:

```python
mongodb://localhost:27017/?directConnection=true
```

Esa URI conecta solo a un nodo específico y no permite demostrar correctamente el cambio automático de primario.

---

6. Poblar la base de datos

Para ejecutar el poblamiento:

```bash
docker exec -it jupyter-mongo python poblar_db.py
```

Verificar el número de documentos insertados:

```python
from pymongo import MongoClient

MONGO_URI = "mongodb://mongo-primario:27017,mongo-secundario-1:27017,mongo-secundario-2:27017/?replicaSet=rs0"
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)

db = client["Política"]
coleccion = db["Discursos"]

print("Documentos en Discursos:", coleccion.count_documents({}))
```