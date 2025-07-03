# Documentation des API

Cette documentation liste les principales requêtes disponibles pour le backend.

Base URL : https://back-tsena-python-production.up.railway.app

## Authentification

### POST /api/auth/login
- **Description** : Connecte un utilisateur et retourne un token JWT.
- **Entrée** : `application/json`
  - `email` (string, requis) : L'adresse e-mail de l'utilisateur.
  - `password` (string, requis) : Le mot de passe de l'utilisateur.
- **Sortie** : `application/json`
  - `access_token` (string) : Le token JWT.
  - `token_type` (string) : Le type de token (ex: "bearer").
  - Le token décodé contient également : `sub` (string, user ID) et `user` (objet User).

### POST /api/auth/register
- **Description** : Enregistre un nouvel utilisateur.
- **Entrée** : `application/json`
  - `email` (string, requis) : L'adresse e-mail du nouvel utilisateur.
  - `password` (string, requis) : Le mot de passe du nouvel utilisateur.
- **Sortie** : `application/json`
  - `id` (UUID) : L'identifiant unique de l'utilisateur.
  - `email` (string) : L'adresse e-mail de l'utilisateur.

### POST /api/auth/logout
- **Description** : Déconnecte l'utilisateur (côté client).
- **Entrée** : Aucun (le token est envoyé dans l'en-tête `Authorization`).
- **Sortie** : Message de confirmation.

## Catégories

### GET /api/categories
- **Description** : Récupère une liste paginée de catégories.
- **Entrée (Query Params)** :
  - `page` (integer, optionnel, défaut: 1) : Le numéro de la page.
  - `limit` (integer, optionnel, défaut: 10) : Le nombre d'éléments par page.
  - `search` (string, optionnel) : Terme de recherche pour filtrer les catégories par nom.
- **Sortie** : `application/json`
  - `categories` (array) : Liste des objets catégories.
  - `total` (integer) : Nombre total de catégories.
  - `page` (integer) : Page actuelle.
  - `limit` (integer) : Limite d'éléments par page.

### GET /api/categories/tree
- **Description** : Récupère les catégories sous forme d'arborescence.
- **Entrée** : Aucun.
- **Sortie** : `application/json` - Une liste d'objets catégories, chacun pouvant contenir une liste `children`.

### GET /api/categories/{id}
- **Description** : Récupère les détails d'une catégorie spécifique.
- **Entrée (Path Param)** :
  - `id` (UUID, requis) : L'identifiant de la catégorie.
- **Sortie** : `application/json` - L'objet de la catégorie.

### POST /api/categories
- **Permissions** : Administrateur requis.
- **Description** : Crée une nouvelle catégorie.
- **Entrée** : `application/json`
  - `name` (string, requis) : Nom de la catégorie.
  - `description` (string, optionnel) : Description de la catégorie.
  - `parent_id` (UUID, optionnel) : ID de la catégorie parente.
- **Sortie** : `application/json` - L'objet de la catégorie créée.

### PUT /api/categories/{id}
- **Permissions** : Administrateur requis.
- **Description** : Met à jour une catégorie existante.
- **Entrée (Path Param)** :
  - `id` (UUID, requis) : L'identifiant de la catégorie à mettre à jour.
- **Entrée (Body)** : `application/json`
  - `name` (string, optionnel) : Nouveau nom de la catégorie.
  - `description` (string, optionnel) : Nouvelle description.
  - `parent_id` (UUID, optionnel) : Nouvel ID de la catégorie parente.
- **Sortie** : `application/json` - L'objet de la catégorie mise à jour.

### DELETE /api/categories/{id}
- **Permissions** : Administrateur requis.
- **Description** : Supprime une catégorie.
- **Entrée (Path Param)** :
  - `id` (UUID, requis) : L'identifiant de la catégorie.
- **Sortie** : `204 No Content`.

## Produits

### GET /api/products
- **Description** : Récupère une liste paginée de produits.
- **Entrée (Query Params)** :
  - `page` (integer, optionnel, défaut: 1)
  - `limit` (integer, optionnel, défaut: 12)
  - `category_id` (UUID, optionnel)
  - `search` (string, optionnel)
  - `min_price` (float, optionnel)
  - `max_price` (float, optionnel)
- **Sortie** : `application/json`
  - `products` (array) : Liste des objets produits.
  - `total` (integer) : Nombre total de produits.
  - `page` (integer) : Page actuelle.
  - `limit` (integer) : Limite par page.

### GET /api/products/{id}
- **Description** : Récupère les détails d'un produit spécifique.
- **Entrée (Path Param)** :
  - `id` (UUID, requis) : L'identifiant du produit.
- **Sortie** : `application/json` - L'objet du produit.

### POST /api/products
- **Permissions** : Utilisateur authentifié requis.
- **Description** : Crée un nouveau produit. Si l'utilisateur est un professionnel, il est assigné comme vendeur. Les images sont uploadées sur MinIO.
- **Entrée** : `multipart/form-data`
  - `name` (string, requis)
  - `description` (string, optionnel)
  - `price` (float, requis)
  - `stock` (integer, requis)
  - `category_id` (UUID, optionnel)
  - `files` (array[File], optionnel) : Fichiers images à uploader.
- **Sortie** : `application/json` - L'objet du produit créé, incluant les URLs des images.

### PUT /api/products/{id}
- **Permissions** : Administrateur ou propriétaire du produit.
- **Description** : Met à jour un produit. Gère la mise à jour des images sur MinIO.
- **Entrée (Path Param)** :
  - `id` (UUID, requis) : L'identifiant du produit.
- **Entrée (Body)** : `multipart/form-data`
  - Champs du produit à modifier (ex: `name`, `price`, etc.).
  - `files` (array[File], optionnel) : Nouveaux fichiers images.
- **Sortie** : `application/json` - L'objet du produit mis à jour.

### DELETE /api/products/{id}
- **Permissions** : Administrateur ou propriétaire du produit.
- **Description** : Supprime un produit et ses images associées de MinIO.
- **Entrée (Path Param)** :
  - `id` (UUID, requis) : L'identifiant du produit.
- **Sortie** : `204 No Content`.

## Profil utilisateur

### GET /api/profile
- **Description** : Récupère le profil de l'utilisateur authentifié.
- **Entrée** : Token d'authentification.
- **Sortie** : `application/json`
  - `id` (UUID)
  - `name` (string, optionnel)
  - `email` (string)
  - `is_professional` (boolean)
  - `professional_type` (string, optionnel)
  - `avatar` (string, optionnel)
  - `phone` (string, optionnel)

### PUT /api/profile
- **Description** : Met à jour le profil de l'utilisateur authentifié.
- **Entrée** : `application/json`
  - `name` (string, optionnel)
  - `phone` (string, optionnel)
  - `avatar` (string, optionnel)
- **Sortie** : `application/json` - L'objet du profil mis à jour.

---
*Le reste de la documentation peut être mis à jour de manière similaire si nécessaire.*

