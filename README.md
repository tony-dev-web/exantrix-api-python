# exantrix-api

Client Python (3.9+, dépendance `requests`) de l'API vendeur de la marketplace [Exantrix](https://exantrix.com) (impression 3D, DTF, textile personnalisé, flocage, découpe) : produits, stock, commandes, expédition, et vérification des webhooks signés.

- Documentation de l'API : https://exantrix.com/extensions/api (FR) · https://exantrix.com/en/extensions/api (EN)
- Jeton API : généré dans votre [espace vendeur](https://exantrix.com/a2/vendeur)

```bash
pip install exantrix-api
```

```python
from exantrix_api import Exantrix, signature_valide

ex = Exantrix("VOTRE_JETON")
ex.moi()                                            # compte, statut, commission
envoyes, erreurs = ex.envoyer([                     # création / mise à jour par référence
    {"reference": "SKU-001", "titre": "Support casque imprimé en 3D", "categorie": "3d", "prix_ttc": 19.90,
     "stock": 12, "images": ["https://maboutique.fr/img/support.jpg"], "description": "Support de casque en PLA"},
])
ex.stock("SKU-001", 7)
commandes = ex.commandes(depuis="2026-01-01")
ex.expedier(commandes[0]["id"], "Colissimo", "6A12345678901")
```

Webhook de commande (Flask) :

```python
@app.post("/webhook-exantrix")
def webhook():
    if not signature_valide(request.get_data(), request.headers.get("X-Exantrix-Signature", ""), JETON):
        abort(401)
    donnees = request.get_json()        # donnees["evenement"] == "commande.payee"
    return {"ok": True}
```

Les nouveaux produits sont validés par Exantrix avant mise en ligne. Limite : 600 requêtes par 10 minutes.

## Les extensions Exantrix

[WordPress / WooCommerce](https://github.com/tony-dev-web/exantrix-marketplace-wordpress) · [PrestaShop](https://github.com/tony-dev-web/exantrix-marketplace-prestashop) · [Shopify](https://github.com/tony-dev-web/exantrix-marketplace-shopify) · [Magento 2](https://github.com/tony-dev-web/exantrix-marketplace-magento) · [Drupal Commerce](https://github.com/tony-dev-web/exantrix-marketplace-drupal) · [CSV, Odoo, Dolibarr](https://github.com/tony-dev-web/exantrix-marketplace-connecteurs) · [Postman / OpenAPI](https://github.com/tony-dev-web/exantrix-api) · [Client Node.js](https://github.com/tony-dev-web/exantrix-api-js) · [Extension navigateur](https://github.com/tony-dev-web/exantrix-extension-navigateur) · https://exantrix.com/extensions/

Licence MIT.
