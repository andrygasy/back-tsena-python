# Documentation des API

Cette documentation liste les principales requêtes disponibles pour le backend.

Base URL : https://back-tsena-python-production.up.railway.app

## Authentification

### POST /api/auth/login
- **Entrée** : `{ "email": string, "password": string }`
- **Sortie** : token JWT et informations de l'utilisateur

### POST /api/auth/register
- **Entrée** : `{ "name": string, "email": string, "password": string, "confirmPassword": string }`
- **Sortie** : message de confirmation et utilisateur créé

### POST /api/auth/logout
- **Entrée** : aucun (token dans l'en-tête Authorization)
- **Sortie** : message de déconnexion

## Produits

### GET /api/products
- **Entrée** : paramètres `page`, `limit`, `category`, `search`, `minPrice`, `maxPrice`, `inStock`
- **Sortie** : liste paginée des produits

### GET /api/products/{id}
- **Entrée** : identifiant du produit dans l'URL
- **Sortie** : détails du produit

### POST /api/products
- **Entrée** : données du produit (nom, description, prix, stock, catégorie, image...) avec authentification professionnelle
- **Sortie** : produit créé

### PUT /api/professional/products/{id}
- **Entrée** : champs du produit à modifier
- **Sortie** : produit mis à jour

### DELETE /api/professional/products/{id}
- **Entrée** : identifiant du produit
- **Sortie** : confirmation de suppression

### PUT /api/admin/products/{id}/status
- **Entrée** : nouveau statut et raison
- **Sortie** : message de mise à jour du statut

## Services

### GET /api/services
- **Entrée** : paramètres `page`, `limit`, `category`, `search`, `minPrice`, `maxPrice`
- **Sortie** : liste paginée des services

### GET /api/services/{id}
- **Entrée** : identifiant du service
- **Sortie** : détails du service

### POST /api/services
- **Entrée** : données du service avec authentification professionnelle
- **Sortie** : service créé

### PUT /api/professional/services/{id}
- **Entrée** : champs du service à modifier
- **Sortie** : service mis à jour

### DELETE /api/professional/services/{id}
- **Entrée** : identifiant du service
- **Sortie** : confirmation de suppression

## Panier

### GET /api/cart
- **Entrée** : token d'authentification
- **Sortie** : contenu du panier et total

### POST /api/cart/items
- **Entrée** : `productId`, `quantity`
- **Sortie** : message et total du panier

### PUT /api/cart/items/{itemId}
- **Entrée** : nouvelle quantité
- **Sortie** : panier mis à jour

### DELETE /api/cart/items/{itemId}
- **Entrée** : identifiant de l'article du panier
- **Sortie** : message de suppression

## Commandes

### POST /api/orders
- **Entrée** : items du panier, adresse de livraison, méthode de paiement
- **Sortie** : commande créée avec total et statut

### GET /api/orders
- **Entrée** : token utilisateur, filtres `status` et `page`
- **Sortie** : liste des commandes de l'utilisateur

### GET /api/orders/{id}
- **Entrée** : identifiant de la commande
- **Sortie** : détails de la commande

### GET /api/admin/orders
- **Entrée** : token administrateur
- **Sortie** : liste des commandes

### PUT /api/admin/orders/{id}/status
- **Entrée** : nouveau statut
- **Sortie** : commande mise à jour

## Profil utilisateur

### GET /api/profile
- **Entrée** : token utilisateur
- **Sortie** : informations du profil

### PUT /api/profile
- **Entrée** : champs du profil à mettre à jour
- **Sortie** : profil mis à jour

## Recherche

### GET /api/search
- **Entrée** : paramètre `q` obligatoire, `type`, `page`
- **Sortie** : produits et services correspondants

## Fonctionnalités Professionnels

### POST /api/professional/request
- **Entrée** : informations de la société et du compte
- **Sortie** : message de prise en compte de la demande

### GET /api/professional/products
- **Entrée** : token professionnel
- **Sortie** : produits du professionnel

### GET /api/professional/services
- **Entrée** : token professionnel
- **Sortie** : services du professionnel

### GET /api/professional/orders
- **Entrée** : filtres `status`, `page`
- **Sortie** : commandes reçues

### PUT /api/professional/orders/{id}/status
- **Entrée** : nouveau statut et numéro de suivi
- **Sortie** : confirmation de mise à jour

## Administration

### GET /api/admin/hero-slides
- **Entrée** : token administrateur
- **Sortie** : liste des slides

### POST /api/admin/hero-slides
- **Entrée** : données du slide
- **Sortie** : slide créé

### PUT /api/admin/hero-slides/{id}
- **Entrée** : champs à modifier
- **Sortie** : slide mis à jour

### DELETE /api/admin/hero-slides/{id}
- **Entrée** : identifiant du slide
- **Sortie** : confirmation de suppression

### GET /api/admin/categories
- **Entrée** : filtres `type`, `includeInactive`
- **Sortie** : liste des catégories

### POST /api/admin/categories
- **Entrée** : données de la catégorie
- **Sortie** : catégorie créée

### PUT /api/admin/categories/{id}
- **Entrée** : champs à modifier
- **Sortie** : catégorie mise à jour

### DELETE /api/admin/categories/{id}
- **Entrée** : identifiant
- **Sortie** : confirmation de suppression

### GET /api/admin/products
- **Entrée** : filtres `page`, `limit`, `status`, `category`, `seller`
- **Sortie** : liste des produits

### DELETE /api/admin/products/{id}
- **Entrée** : identifiant du produit
- **Sortie** : produit supprimé

### GET /api/admin/promotions
- **Entrée** : token administrateur
- **Sortie** : liste des promotions

### POST /api/admin/promotions
- **Entrée** : données de la promotion
- **Sortie** : promotion créée

### PUT /api/admin/promotions/{id}
- **Entrée** : champs à modifier
- **Sortie** : promotion mise à jour

### DELETE /api/admin/promotions/{id}
- **Entrée** : identifiant
- **Sortie** : confirmation de suppression

### GET /api/admin/users
- **Entrée** : filtres `page`, `limit`, `role`, `status`, `search`
- **Sortie** : liste des utilisateurs

### PUT /api/admin/users/{id}/status
- **Entrée** : nouveau statut et raison
- **Sortie** : confirmation

### PUT /api/admin/users/{id}/role
- **Entrée** : nouveau rôle
- **Sortie** : confirmation

### DELETE /api/admin/users/{id}
- **Entrée** : identifiant utilisateur
- **Sortie** : utilisateur supprimé

### GET /api/admin/dashboard
- **Entrée** : token administrateur
- **Sortie** : statistiques globales
