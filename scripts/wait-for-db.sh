#!/bin/sh
set -e

sleep 15


# Attente de la disponibilité de PostgreSQL
until PGPASSWORD=adminpassword psql -h 51.38.237.164 -p 6969 -U admin -d mydatabase -c '\q'; do
  >&2 echo "⏳ PostgreSQL est indisponible - attente..."
  >&2 echo "🔁 Tentative de connexion avec :"
  >&2 echo "    HOST=$POSTGRES_HOST"
  >&2 echo "    PORT=$POSTGRES_PORT"
  >&2 echo "    USER=$POSTGRES_USER"
  >&2 echo "    DB=$POSTGRES_DB"
  sleep 5
done

# Vérification de l'existence de la base de données
if ! PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' 2>/dev/null; then
  >&2 echo "⚠️ La base de données '$POSTGRES_DB' n'existe pas - création..."
  PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE $POSTGRES_DB;"
fi

# Application des migrations Alembic
alembic -c /app/alembic.ini upgrade head

>&2 echo "✅ PostgreSQL est opérationnel - exécution de la commande : $@"
exec "$@"
