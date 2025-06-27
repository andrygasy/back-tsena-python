# Documentation API - Marketplace E-commerce

## Table des matières

1. [Authentification](#authentification)
2. [Produits](#produits)
3. [Services](#services)
4. [Panier](#panier)
5. [Commandes](#commandes)
6. [Profil utilisateur](#profil-utilisateur)
7. [Recherche](#recherche)
8. [Professionnels](#professionnels)
9. [Administration Back-Office](#administration-back-office)

---

## Authentification

### Connexion utilisateur

**Méthode** : `POST`
**URL** : `/api/auth/login`

#### Requête

* **En-têtes**
  * `Content-Type: application/json`
  * `Accept: application/json`

* **Corps de la requête**
```json
{
  "email": "user@example.com",
  "password": "motdepasse123"
}
```

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Succès | `{"token": "jwt_token_here", "user": {"id": "user_01", "email": "user@example.com", "name": "Jean Dupont", "isProfessional": false}}` |
| 401  | Identifiants invalides | `{"error": "Email ou mot de passe incorrect."}` |
| 422  | Données invalides | `{"error": "Le format de l'email est invalide."}` |
| 500  | Erreur serveur | `{"error": "Une erreur interne est survenue."}` |

### Inscription utilisateur

**Méthode** : `POST`
**URL** : `/api/auth/register`

#### Requête

* **En-têtes**
  * `Content-Type: application/json`
  * `Accept: application/json`

* **Corps de la requête**
```json
{
  "name": "Jean Dupont",
  "email": "user@example.com",
  "password": "motdepasse123",
  "confirmPassword": "motdepasse123"
}
```

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 201  | Compte créé | `{"message": "Compte créé avec succès.", "user": {"id": "user_01", "email": "user@example.com", "name": "Jean Dupont"}}` |
| 400  | Email déjà utilisé | `{"error": "Cette adresse email est déjà utilisée."}` |
| 422  | Données invalides | `{"error": "Le mot de passe doit contenir au moins 8 caractères."}` |
| 500  | Erreur serveur | `{"error": "Une erreur interne est survenue."}` |

### Déconnexion

**Méthode** : `POST`
**URL** : `/api/auth/logout`

#### Requête

* **En-têtes**
  * `Authorization: Bearer {token}`

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Succès | `{"message": "Déconnexion réussie."}` |
| 401  | Non autorisé | `{"error": "Token invalide."}` |

---

## Produits

### Récupérer la liste des produits

**Méthode** : `GET`
**URL** : `/api/products`

#### Requête

* **En-têtes**
  * `Accept: application/json`

* **Paramètres Query**

| Paramètre | Type | Obligatoire | Description |
|-----------|------|-------------|-------------|
| `page` | integer | non | Numéro de page (défaut : 1) |
| `limit` | integer | non | Nombre d'éléments par page (défaut : 12) |
| `category` | string | non | Filtrer par catégorie |
| `search` | string | non | Recherche par nom ou description |
| `minPrice` | number | non | Prix minimum |
| `maxPrice` | number | non | Prix maximum |
| `inStock` | boolean | non | Filtrer les produits en stock |

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Succès | `{"products": [{"id": "prod_01", "name": "iPhone 15", "description": "Dernier smartphone Apple", "price": 999, "category": "Électronique", "image": "url_image", "stock": 10, "rating": 4.5}], "pagination": {"total": 100, "page": 1, "totalPages": 9}}` |
| 500  | Erreur serveur | `{"error": "Une erreur interne est survenue."}` |

### Récupérer un produit par ID

**Méthode** : `GET`
**URL** : `/api/products/{id}`

#### Requête

* **En-têtes**
  * `Accept: application/json`

* **Paramètres de chemin**

| Paramètre | Type | Description |
|-----------|------|-------------|
| `id` | string | Identifiant unique du produit |

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Succès | `{"id": "prod_01", "name": "iPhone 15", "description": "Description complète...", "price": 999, "category": "Électronique", "images": ["url1", "url2"], "stock": 10, "rating": 4.5, "reviews": [{"user": "Marie", "rating": 5, "comment": "Excellent produit"}]}` |
| 404  | Produit non trouvé | `{"error": "Produit non trouvé."}` |
| 500  | Erreur serveur | `{"error": "Une erreur interne est survenue."}` |

### Créer un produit (Professionnel)

**Méthode** : `POST`
**URL** : `/api/products`

#### Requête

* **En-têtes**
  * `Content-Type: application/json`
  * `Authorization: Bearer {token}`

* **Corps de la requête**
```json
{
  "name": "Nouveau produit",
  "description": "Description du produit",
  "price": 99.99,
  "stock": 50,
  "category": "Électronique",
  "image": "url_image",
  "status": "active"
}
```

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 201  | Produit créé | `{"id": "prod_new", "message": "Produit créé avec succès."}` |
| 401  | Non autorisé | `{"error": "Accès restreint aux professionnels."}` |
| 422  | Données invalides | `{"error": "Le prix doit être positif."}` |
| 500  | Erreur serveur | `{"error": "Une erreur interne est survenue."}` |

---

## Services

### Récupérer la liste des services

**Méthode** : `GET`
**URL** : `/api/services`

#### Requête

* **En-têtes**
  * `Accept: application/json`

* **Paramètres Query**

| Paramètre | Type | Obligatoire | Description |
|-----------|------|-------------|-------------|
| `page` | integer | non | Numéro de page (défaut : 1) |
| `limit` | integer | non | Nombre d'éléments par page (défaut : 6) |
| `category` | string | non | Filtrer par catégorie |
| `search` | string | non | Recherche par titre ou description |
| `minPrice` | number | non | Prix minimum |
| `maxPrice` | number | non | Prix maximum |

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Succès | `{"services": [{"id": "serv_01", "title": "Développement Web", "description": "Sites web modernes", "price": 1500, "category": "Développement", "image": "url", "provider": "Jean Dupont", "rating": 4.8, "deliveryTime": "2-3 semaines"}], "pagination": {"total": 50, "page": 1, "totalPages": 9}}` |
| 500  | Erreur serveur | `{"error": "Une erreur interne est survenue."}` |

### Récupérer un service par ID

**Méthode** : `GET`
**URL** : `/api/services/{id}`

#### Requête

* **En-têtes**
  * `Accept: application/json`

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Succès | `{"id": "serv_01", "title": "Développement Web", "description": "Description complète...", "price": 1500, "category": "Développement", "image": "url", "provider": {"name": "Jean Dupont", "rating": 4.9}, "deliveryTime": "2-3 semaines", "features": ["Responsive", "SEO optimisé"], "options": [{"name": "Design personnalisé", "price": 300}]}` |
| 404  | Service non trouvé | `{"error": "Service non trouvé."}` |
| 500  | Erreur serveur | `{"error": "Une erreur interne est survenue."}` |

### Créer un service (Professionnel)

**Méthode** : `POST`
**URL** : `/api/services`

#### Requête

* **En-têtes**
  * `Content-Type: application/json`
  * `Authorization: Bearer {token}`

* **Corps de la requête**
```json
{
  "title": "Nouveau service",
  "description": "Description du service",
  "pricing": {
    "type": "fixed",
    "amount": 500
  },
  "duration": "1-2 semaines",
  "category": "Développement",
  "image": "url_image",
  "status": "active"
}
```

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 201  | Service créé | `{"id": "serv_new", "message": "Service créé avec succès."}` |
| 401  | Non autorisé | `{"error": "Accès restreint aux professionnels."}` |
| 422  | Données invalides | `{"error": "Le prix doit être positif."}` |
| 500  | Erreur serveur | `{"error": "Une erreur interne est survenue."}` |

---

## Panier

### Récupérer le panier

**Méthode** : `GET`
**URL** : `/api/cart`

#### Requête

* **En-têtes**
  * `Authorization: Bearer {token}`

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Succès | `{"items": [{"id": "cart_01", "productId": "prod_01", "name": "iPhone 15", "price": 999, "quantity": 2, "image": "url"}], "total": 1998}` |
| 401  | Non autorisé | `{"error": "Authentification requise."}` |
| 500  | Erreur serveur | `{"error": "Une erreur interne est survenue."}` |

### Ajouter un article au panier

**Méthode** : `POST`
**URL** : `/api/cart/items`

#### Requête

* **En-têtes**
  * `Content-Type: application/json`
  * `Authorization: Bearer {token}`

* **Corps de la requête**
```json
{
  "productId": "prod_01",
  "quantity": 2
}
```

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 201  | Article ajouté | `{"message": "Article ajouté au panier.", "cartTotal": 1998}` |
| 400  | Stock insuffisant | `{"error": "Stock insuffisant pour ce produit."}` |
| 401  | Non autorisé | `{"error": "Authentification requise."}` |
| 404  | Produit non trouvé | `{"error": "Produit non trouvé."}` |
| 500  | Erreur serveur | `{"error": "Une erreur interne est survenue."}` |

### Mettre à jour la quantité

**Méthode** : `PUT`
**URL** : `/api/cart/items/{itemId}`

#### Requête

* **En-têtes**
  * `Content-Type: application/json`
  * `Authorization: Bearer {token}`

* **Corps de la requête**
```json
{
  "quantity": 3
}
```

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Quantité mise à jour | `{"message": "Quantité mise à jour.", "cartTotal": 2997}` |
| 400  | Stock insuffisant | `{"error": "Stock insuffisant."}` |
| 401  | Non autorisé | `{"error": "Authentification requise."}` |
| 404  | Article non trouvé | `{"error": "Article non trouvé dans le panier."}` |

### Supprimer un article du panier

**Méthode** : `DELETE`
**URL** : `/api/cart/items/{itemId}`

#### Requête

* **En-têtes**
  * `Authorization: Bearer {token}`

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Article supprimé | `{"message": "Article supprimé du panier."}` |
| 401  | Non autorisé | `{"error": "Authentification requise."}` |
| 404  | Article non trouvé | `{"error": "Article non trouvé dans le panier."}` |

---

## Commandes

### Créer une commande

**Méthode** : `POST`
**URL** : `/api/orders`

#### Requête

* **En-têtes**
  * `Content-Type: application/json`
  * `Authorization: Bearer {token}`

* **Corps de la requête**
```json
{
  "items": [
    {
      "productId": "prod_01",
      "quantity": 2,
      "price": 999
    }
  ],
  "shippingAddress": {
    "street": "123 Rue de la Paix",
    "city": "Paris",
    "postalCode": "75001",
    "country": "France"
  },
  "paymentMethod": "stripe"
}
```

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 201  | Commande créée | `{"orderId": "order_01", "total": 1998, "status": "pending", "paymentUrl": "stripe_url"}` |
| 400  | Panier vide | `{"error": "Le panier est vide."}` |
| 401  | Non autorisé | `{"error": "Authentification requise."}` |
| 422  | Données invalides | `{"error": "Adresse de livraison incomplète."}` |

### Récupérer les commandes utilisateur

**Méthode** : `GET`
**URL** : `/api/orders`

#### Requête

* **En-têtes**
  * `Authorization: Bearer {token}`

* **Paramètres Query**

| Paramètre | Type | Obligatoire | Description |
|-----------|------|-------------|-------------|
| `status` | string | non | Filtrer par statut (pending, paid, shipped, delivered) |
| `page` | integer | non | Numéro de page |

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Succès | `{"orders": [{"id": "order_01", "total": 1998, "status": "paid", "createdAt": "2024-01-15", "items": [{"name": "iPhone 15", "quantity": 2}]}]}` |
| 401  | Non autorisé | `{"error": "Authentification requise."}` |

---

## Profil utilisateur

### Récupérer le profil

**Méthode** : `GET`
**URL** : `/api/profile`

#### Requête

* **En-têtes**
  * `Authorization: Bearer {token}`

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Succès | `{"id": "user_01", "name": "Jean Dupont", "email": "jean@example.com", "isProfessional": true, "professionalType": "seller", "avatar": "url", "phone": "+33123456789"}` |
| 401  | Non autorisé | `{"error": "Authentification requise."}` |

### Mettre à jour le profil

**Méthode** : `PUT`
**URL** : `/api/profile`

#### Requête

* **En-têtes**
  * `Content-Type: application/json`
  * `Authorization: Bearer {token}`

* **Corps de la requête**
```json
{
  "name": "Jean Dupont",
  "phone": "+33123456789",
  "avatar": "new_avatar_url"
}
```

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Profil mis à jour | `{"message": "Profil mis à jour avec succès."}` |
| 401  | Non autorisé | `{"error": "Authentification requise."}` |
| 422  | Données invalides | `{"error": "Format de téléphone invalide."}` |

---

## Recherche

### Recherche globale

**Méthode** : `GET`
**URL** : `/api/search`

#### Requête

* **En-têtes**
  * `Accept: application/json`

* **Paramètres Query**

| Paramètre | Type | Obligatoire | Description |
|-----------|------|-------------|-------------|
| `q` | string | oui | Terme de recherche |
| `type` | string | non | Type de résultat (products, services, all) |
| `page` | integer | non | Numéro de page |

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Succès | `{"products": [...], "services": [...], "total": 15}` |
| 400  | Paramètre manquant | `{"error": "Le paramètre 'q' est requis."}` |
| 500  | Erreur serveur | `{"error": "Une erreur interne est survenue."}` |

---

## Professionnels

### Demande de statut professionnel

**Méthode** : `POST`
**URL** : `/api/professional/request`

#### Requête

* **En-têtes**
  * `Content-Type: application/json`
  * `Authorization: Bearer {token}`

* **Corps de la requête**
```json
{
  "companyName": "Ma Société",
  "accountType": "seller",
  "description": "Description de l'activité",
  "email": "contact@masociete.com"
}
```

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 201  | Demande soumise | `{"message": "Demande soumise avec succès.", "status": "pending"}` |
| 400  | Déjà professionnel | `{"error": "Vous êtes déjà professionnel."}` |
| 401  | Non autorisé | `{"error": "Authentification requise."}` |

### Récupérer mes produits (Professionnel)

**Méthode** : `GET`
**URL** : `/api/professional/products`

#### Requête

* **En-têtes**
  * `Authorization: Bearer {token}`

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Succès | `{"products": [{"id": "prod_01", "name": "Mon Produit", "status": "active", "stock": 10, "sales": 25}]}` |
| 401  | Non autorisé | `{"error": "Accès restreint aux professionnels."}` |

### Récupérer mes services (Professionnel)

**Méthode** : `GET`
**URL** : `/api/professional/services`

#### Requête

* **En-têtes**
  * `Authorization: Bearer {token}`

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Succès | `{"services": [{"id": "serv_01", "title": "Mon Service", "status": "active", "orders": 15}]}` |
| 401  | Non autorisé | `{"error": "Accès restreint aux professionnels."}` |

### Gestion des commandes (Professionnel)

**Méthode** : `GET`
**URL** : `/api/professional/orders`

#### Requête

* **En-têtes**
  * `Authorization: Bearer {token}`

* **Paramètres Query**

| Paramètre | Type | Obligatoire | Description |
|-----------|------|-------------|-------------|
| `status` | string | non | Filtrer par statut |
| `page` | integer | non | Numéro de page |

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Succès | `{"orders": [{"id": "order_01", "customer": "Marie Martin", "total": 1500, "status": "pending", "items": [...]}]}` |
| 401  | Non autorisé | `{"error": "Accès restreint aux professionnels."}` |

### Mettre à jour le statut d'une commande

**Méthode** : `PUT`
**URL** : `/api/professional/orders/{orderId}/status`

#### Requête

* **En-têtes**
  * `Content-Type: application/json`
  * `Authorization: Bearer {token}`

* **Corps de la requête**
```json
{
  "status": "shipped",
  "trackingNumber": "1234567890"
}
```

#### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Statut mis à jour | `{"message": "Statut de la commande mis à jour."}` |
| 401  | Non autorisé | `{"error": "Accès restreint aux professionnels."}` |
| 404  | Commande non trouvée | `{"error": "Commande non trouvée."}` |

---

## Administration Back-Office

### Gestion des Slides Héros

#### Récupérer tous les slides

**Méthode** : `GET`
**URL** : `/api/admin/hero-slides`

##### Requête

* **En-têtes**
  * `Authorization: Bearer {admin_token}`

##### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Succès | `{"slides": [{"id": "slide_01", "title": "Découvrez nos produits", "description": "Une sélection exceptionnelle", "image": "url_image", "buttonText": "Explorer", "buttonLink": "/products", "isActive": true, "order": 1}]}` |
| 401  | Non autorisé | `{"error": "Accès administrateur requis."}` |
| 500  | Erreur serveur | `{"error": "Une erreur interne est survenue."}` |

#### Créer un slide héros

**Méthode** : `POST`
**URL** : `/api/admin/hero-slides`

##### Requête

* **En-têtes**
  * `Content-Type: application/json`
  * `Authorization: Bearer {admin_token}`

* **Corps de la requête**
```json
{
  "title": "Nouveau slide",
  "description": "Description du slide",
  "image": "https://example.com/image.jpg",
  "buttonText": "Voir plus",
  "buttonLink": "/new-page",
  "isActive": true,
  "order": 3
}
```

##### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 201  | Slide créé | `{"id": "slide_new", "message": "Slide créé avec succès."}` |
| 401  | Non autorisé | `{"error": "Accès administrateur requis."}` |
| 422  | Données invalides | `{"error": "Le titre est requis."}` |

#### Modifier un slide héros

**Méthode** : `PUT`
**URL** : `/api/admin/hero-slides/{id}`

##### Requête

* **En-têtes**
  * `Content-Type: application/json`
  * `Authorization: Bearer {admin_token}`

* **Corps de la requête**
```json
{
  "title": "Titre modifié",
  "description": "Description modifiée",
  "image": "https://example.com/new-image.jpg",
  "buttonText": "Nouveau texte",
  "buttonLink": "/nouvelle-page",
  "isActive": false
}
```

##### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Slide modifié | `{"message": "Slide modifié avec succès."}` |
| 401  | Non autorisé | `{"error": "Accès administrateur requis."}` |
| 404  | Slide non trouvé | `{"error": "Slide non trouvé."}` |

#### Supprimer un slide héros

**Méthode** : `DELETE`
**URL** : `/api/admin/hero-slides/{id}`

##### Requête

* **En-têtes**
  * `Authorization: Bearer {admin_token}`

##### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Slide supprimé | `{"message": "Slide supprimé avec succès."}` |
| 401  | Non autorisé | `{"error": "Accès administrateur requis."}` |
| 404  | Slide non trouvé | `{"error": "Slide non trouvé."}` |

### Gestion des Catégories (Admin)

#### Récupérer toutes les catégories (Admin)

**Méthode** : `GET`
**URL** : `/api/admin/categories`

##### Requête

* **En-têtes**
  * `Authorization: Bearer {admin_token}`

* **Paramètres Query**

| Paramètre | Type | Obligatoire | Description |
|-----------|------|-------------|-------------|
| `type` | string | non | Filtrer par type (product, service, all) |
| `includeInactive` | boolean | non | Inclure les catégories inactives |

##### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Succès | `{"categories": [{"id": "cat_01", "name": "Électronique", "description": "Produits électroniques", "type": "product", "isActive": true, "image": "url", "productCount": 150}]}` |
| 401  | Non autorisé | `{"error": "Accès administrateur requis."}` |

#### Créer une catégorie (Admin)

**Méthode** : `POST`
**URL** : `/api/admin/categories`

##### Requête

* **En-têtes**
  * `Content-Type: application/json`
  * `Authorization: Bearer {admin_token}`

* **Corps de la requête**
```json
{
  "name": "Nouvelle catégorie",
  "description": "Description de la catégorie",
  "type": "product",
  "image": "https://example.com/category-image.jpg",
  "isActive": true
}
```

##### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 201  | Catégorie créée | `{"id": "cat_new", "message": "Catégorie créée avec succès."}` |
| 401  | Non autorisé | `{"error": "Accès administrateur requis."}` |
| 422  | Données invalides | `{"error": "Le nom est requis."}` |

#### Modifier une catégorie (Admin)

**Méthode** : `PUT`
**URL** : `/api/admin/categories/{id}`

##### Requête

* **En-têtes**
  * `Content-Type: application/json`
  * `Authorization: Bearer {admin_token}`

* **Corps de la requête**
```json
{
  "name": "Nom modifié",
  "description": "Description modifiée",
  "image": "https://example.com/new-image.jpg",
  "isActive": false
}
```

##### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Catégorie modifiée | `{"message": "Catégorie modifiée avec succès."}` |
| 401  | Non autorisé | `{"error": "Accès administrateur requis."}` |
| 404  | Catégorie non trouvée | `{"error": "Catégorie non trouvée."}` |

#### Supprimer une catégorie (Admin)

**Méthode** : `DELETE`
**URL** : `/api/admin/categories/{id}`

##### Requête

* **En-têtes**
  * `Authorization: Bearer {admin_token}`

##### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Catégorie supprimée | `{"message": "Catégorie supprimée avec succès."}` |
| 400  | Catégorie utilisée | `{"error": "Impossible de supprimer une catégorie contenant des produits."}` |
| 401  | Non autorisé | `{"error": "Accès administrateur requis."}` |
| 404  | Catégorie non trouvée | `{"error": "Catégorie non trouvée."}` |

### Gestion des Produits (Admin)

#### Récupérer tous les produits (Admin)

**Méthode** : `GET`
**URL** : `/api/admin/products`

##### Requête

* **En-têtes**
  * `Authorization: Bearer {admin_token}`

* **Paramètres Query**

| Paramètre | Type | Obligatoire | Description |
|-----------|------|-------------|-------------|
| `page` | integer | non | Numéro de page (défaut : 1) |
| `limit` | integer | non | Nombre d'éléments par page (défaut : 20) |
| `status` | string | non | Filtrer par statut (active, inactive, pending) |
| `category` | string | non | Filtrer par catégorie |
| `seller` | string | non | Filtrer par vendeur |

##### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Succès | `{"products": [{"id": "prod_01", "name": "iPhone 15", "price": 999, "status": "active", "category": "Électronique", "seller": "Jean Dupont", "stock": 10, "createdAt": "2024-01-15", "sales": 25}], "pagination": {"total": 500, "page": 1, "totalPages": 25}}` |
| 401  | Non autorisé | `{"error": "Accès administrateur requis."}` |

#### Modifier le statut d'un produit (Admin)

**Méthode** : `PUT`
**URL** : `/api/admin/products/{id}/status`

##### Requête

* **En-têtes**
  * `Content-Type: application/json`
  * `Authorization: Bearer {admin_token}`

* **Corps de la requête**
```json
{
  "status": "inactive",
  "reason": "Produit non conforme aux règles"
}
```

##### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Statut modifié | `{"message": "Statut du produit modifié avec succès."}` |
| 401  | Non autorisé | `{"error": "Accès administrateur requis."}` |
| 404  | Produit non trouvé | `{"error": "Produit non trouvé."}` |

#### Supprimer un produit (Admin)

**Méthode** : `DELETE`
**URL** : `/api/admin/products/{id}`

##### Requête

* **En-têtes**
  * `Authorization: Bearer {admin_token}`

##### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Produit supprimé | `{"message": "Produit supprimé avec succès."}` |
| 401  | Non autorisé | `{"error": "Accès administrateur requis."}` |
| 404  | Produit non trouvé | `{"error": "Produit non trouvé."}` |

### Gestion des Promotions

#### Récupérer toutes les promotions

**Méthode** : `GET`
**URL** : `/api/admin/promotions`

##### Requête

* **En-têtes**
  * `Authorization: Bearer {admin_token}`

##### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Succès | `{"promotions": [{"id": "promo_01", "name": "Soldes d'été", "description": "Réduction sur tous les produits", "discountType": "percentage", "discountValue": 20, "startDate": "2024-06-01", "endDate": "2024-08-31", "isActive": true, "usageCount": 150}]}` |
| 401  | Non autorisé | `{"error": "Accès administrateur requis."}` |

#### Créer une promotion

**Méthode** : `POST`
**URL** : `/api/admin/promotions`

##### Requête

* **En-têtes**
  * `Content-Type: application/json`
  * `Authorization: Bearer {admin_token}`

* **Corps de la requête**
```json
{
  "name": "Promotion Black Friday",
  "description": "Réduction exceptionnelle",
  "discountType": "percentage",
  "discountValue": 30,
  "startDate": "2024-11-24",
  "endDate": "2024-11-30",
  "conditions": {
    "minAmount": 100,
    "categories": ["electronics", "fashion"],
    "maxUsage": 1000
  },
  "isActive": true
}
```

##### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 201  | Promotion créée | `{"id": "promo_new", "message": "Promotion créée avec succès."}` |
| 401  | Non autorisé | `{"error": "Accès administrateur requis."}` |
| 422  | Données invalides | `{"error": "Le nom est requis."}` |

#### Modifier une promotion

**Méthode** : `PUT`
**URL** : `/api/admin/promotions/{id}`

##### Requête

* **En-têtes**
  * `Content-Type: application/json`
  * `Authorization: Bearer {admin_token}`

* **Corps de la requête**
```json
{
  "name": "Nom modifié",
  "discountValue": 25,
  "isActive": false
}
```

##### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Promotion modifiée | `{"message": "Promotion modifiée avec succès."}` |
| 401  | Non autorisé | `{"error": "Accès administrateur requis."}` |
| 404  | Promotion non trouvée | `{"error": "Promotion non trouvée."}` |

#### Supprimer une promotion

**Méthode** : `DELETE`
**URL** : `/api/admin/promotions/{id}`

##### Requête

* **En-têtes**
  * `Authorization: Bearer {admin_token}`

##### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Promotion supprimée | `{"message": "Promotion supprimée avec succès."}` |
| 401  | Non autorisé | `{"error": "Accès administrateur requis."}` |
| 404  | Promotion non trouvée | `{"error": "Promotion non trouvée."}` |

### Gestion des Utilisateurs (Admin)

#### Récupérer tous les utilisateurs

**Méthode** : `GET`
**URL** : `/api/admin/users`

##### Requête

* **En-têtes**
  * `Authorization: Bearer {admin_token}`

* **Paramètres Query**

| Paramètre | Type | Obligatoire | Description |
|-----------|------|-------------|-------------|
| `page` | integer | non | Numéro de page (défaut : 1) |
| `limit` | integer | non | Nombre d'éléments par page (défaut : 20) |
| `role` | string | non | Filtrer par rôle (user, professional, admin) |
| `status` | string | non | Filtrer par statut (active, suspended, pending) |
| `search` | string | non | Recherche par nom ou email |

##### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Succès | `{"users": [{"id": "user_01", "name": "Jean Dupont", "email": "jean@example.com", "role": "professional", "status": "active", "isProfessional": true, "createdAt": "2024-01-15", "lastLogin": "2024-06-25", "orderCount": 12, "totalSpent": 2500}], "pagination": {"total": 1000, "page": 1, "totalPages": 50}}` |
| 401  | Non autorisé | `{"error": "Accès administrateur requis."}` |

#### Modifier le statut d'un utilisateur

**Méthode** : `PUT`
**URL** : `/api/admin/users/{id}/status`

##### Requête

* **En-têtes**
  * `Content-Type: application/json`
  * `Authorization: Bearer {admin_token}`

* **Corps de la requête**
```json
{
  "status": "suspended",
  "reason": "Violation des conditions d'utilisation"
}
```

##### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Statut modifié | `{"message": "Statut de l'utilisateur modifié avec succès."}` |
| 401  | Non autorisé | `{"error": "Accès administrateur requis."}` |
| 404  | Utilisateur non trouvé | `{"error": "Utilisateur non trouvé."}` |

#### Modifier le rôle d'un utilisateur

**Méthode** : `PUT`
**URL** : `/api/admin/users/{id}/role`

##### Requête

* **En-têtes**
  * `Content-Type: application/json`
  * `Authorization: Bearer {admin_token}`

* **Corps de la requête**
```json
{
  "role": "professional",
  "permissions": ["sell_products", "manage_orders"]
}
```

##### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Rôle modifié | `{"message": "Rôle de l'utilisateur modifié avec succès."}` |
| 401  | Non autorisé | `{"error": "Accès administrateur requis."}` |
| 404  | Utilisateur non trouvé | `{"error": "Utilisateur non trouvé."}` |

#### Supprimer un utilisateur

**Méthode** : `DELETE`
**URL** : `/api/admin/users/{id}`

##### Requête

* **En-têtes**
  * `Authorization: Bearer {admin_token}`

##### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Utilisateur supprimé | `{"message": "Utilisateur supprimé avec succès."}` |
| 401  | Non autorisé | `{"error": "Accès administrateur requis."}` |
| 404  | Utilisateur non trouvé | `{"error": "Utilisateur non trouvé."}` |

### Statistiques du Back-Office

#### Tableau de bord administrateur

**Méthode** : `GET`
**URL** : `/api/admin/dashboard`

##### Requête

* **En-têtes**
  * `Authorization: Bearer {admin_token}`

##### Réponses

| Code | Description | Corps (JSON) |
|------|-------------|--------------|
| 200  | Succès | `{"stats": {"totalUsers": 1250, "totalProducts": 350, "totalOrders": 890, "totalRevenue": 125000, "newUsersToday": 15, "ordersToday": 25, "revenueToday": 3500, "pendingOrders": 12, "lowStockProducts": 8, "activePromotions": 3}}` |
| 401  | Non autorisé | `{"error": "Accès administrateur requis."}` |

---

## Codes d'erreur génériques

| Code | Description |
|------|-------------|
| 400  | Requête malformée |
| 401  | Non authentifié |
| 403  | Accès interdit |
| 404  | Ressource non trouvée |
| 422  | Données non valides |
| 429  | Trop de requêtes |
| 500  | Erreur serveur interne |
| 503  | Service indisponible |

## Notes d'implémentation

- Tous les endpoints nécessitant une authentification utilisent un token JWT dans l'en-tête `Authorization: Bearer {token}`
- Les réponses d'erreur suivent un format standardisé avec un champ `error` contenant le message
- La pagination utilise les paramètres `page` et `limit` avec des métadonnées retournées dans `pagination`
- Les prix sont en euros et les dates au format ISO 8601
- Les images utilisent des URLs absolues vers le système de stockage