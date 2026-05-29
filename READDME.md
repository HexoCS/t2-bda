# Tarea Laboratorio 2 MongoDB 

## Requisitos Previos


* **Docker Desktop** (Asegurarse de que esté corriendo).
* **Python 3.8+**.
* **MongoDB Compass** 

---

## Levantar la Infraestructura (Docker)

El proyecto utiliza un clúster de MongoDB compuesto por 1 nodo primario y 2 secundarios.

1. **Iniciar los contenedores:**
   Abre una terminal en la raíz del proyecto y ejecuta:
   ```bash
   docker compose up -d
    ```
2. **Iniciar replica set:**
    Ejecuta el siguiente comando en la misma terminal
    ```bash
    docker exec -it mongo-primario mongosh --eval "
            rs.initiate({
            _id: 'rs0',
            members: [
                { _id: 0, host: 'mongo-primario:27017', priority: 2 },
                { _id: 1, host: 'mongo-secundario-1:27017', priority: 1 },
                { _id: 2, host: 'mongo-secundario-2:27017', priority: 1 }
            ]
            })
            "
    ```
3. **Verificar en mongoDB Compass:**
     ```bash
   mongodb://localhost:27017/?directConnection=true
    ```

## Configurar entorno python

1. **Crear y activar el entorno virtual:**
   Abre una terminal en la raíz del proyecto y ejecuta:
   ```bash
    # Crear entorno
    python -m venv venv

    # Activar 
    .\venv\Scripts\Activate.ps1
    ```
2. **Instalar dependencias:**
   ```bash
    pip install pymongo sentence-transformers torch
    ```
3. **Poblar DB:**
    ```bash
   python poblar_db.py
    ```