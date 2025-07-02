#!/bin/sh
set -e

sleep 15

# Attente de la disponibilité de PostgreSQL
until PGPASSWORD=adminpassword psql -h 51.38.237.164 -p 6969 -U admin -d mydatabase -c '\q'; do
  >&2 echo "⏳ PostgreSQL est indisponible - attente..."
  >&2 echo "🔁 Tentative de connexion avec :"
  >&2 echo "    HOST=51.38.237.164"
  >&2 echo "    PORT=6969"
  >&2 echo "    USER=admin"
  >&2 echo "    DB=mydatabase"
  sleep 5
done

# Vérification de l'existence de la base de données
if ! PGPASSWORD=adminpassword psql -h "51.38.237.164" -p "6969" -U "admin" -d "mydatabase" -c '\q' 2>/dev/null; then
  >&2 echo "⚠️ La base de données 'mydatabase' n'existe pas - création..."
  PGPASSWORD=adminpassword psql -h "51.38.237.164" -p "6969" -U "admin" -d postgres -c "CREATE DATABASE mydatabase;"
fi

# Application des migrations Alembic
alembic -c /app/alembic.ini upgrade head

>&2 echo "✅ PostgreSQL est opérationnel - exécution de la commande : $@"
exec "$@"
