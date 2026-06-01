#!/usr/bin/env bash
set -e

docker exec mongo-primario mongosh --eval "
rs.initiate({
  _id: 'rs0',
  members: [
    { _id: 0, host: 'mongo-primario:27017', priority: 2 },
    { _id: 1, host: 'mongo-secundario-1:27017', priority: 1 },
    { _id: 2, host: 'mongo-secundario-2:27017', priority: 1 }
  ]
})
"

echo "Esperando elección de PRIMARY..."
sleep 8

docker exec mongo-primario mongosh --eval "
rs.status().members.map(m => ({
  name: m.name,
  stateStr: m.stateStr,
  health: m.health
}))
"
