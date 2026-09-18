"""Client Python de l'API vendeur Exantrix (https://exantrix.com/extensions/api).

Produits, stock, commandes, expedition et verification des webhooks signes de la marketplace
exantrix.com (impression 3D, DTF, textile). Python 3.9+, dependance : requests.
"""
import hashlib
import hmac

import requests

BASE = "https://exantrix.com/api/v1"


class ExantrixError(RuntimeError):
    """Erreur renvoyee par l'API (message et code HTTP)."""

    def __init__(self, message, status=0, body=None):
        super().__init__(message)
        self.status = status
        self.body = body


class Exantrix:
    def __init__(self, jeton, base=BASE):
        self.s = requests.Session()
        self.s.headers.update({"Authorization": f"Bearer {jeton}", "Content-Type": "application/json", "User-Agent": "exantrix-api-python/1.0"})
        self.base = base
        self.jeton = jeton

    def _appel(self, methode, chemin, **kw):
        r = self.s.request(methode, self.base + chemin, timeout=60, **kw)
        donnees = r.json() if r.content else {}
        if r.status_code >= 400:
            raise ExantrixError(donnees.get("erreur") or f"HTTP {r.status_code}", r.status_code, donnees)
        return donnees

    def moi(self):
        return self._appel("GET", "/moi")

    def produits(self):
        return self._appel("GET", "/produits")["produits"]

    def envoyer(self, fiches, lot=100):
        """Envoie les fiches par lots ; retourne (nb_envoyes, erreurs)."""
        envoyes, erreurs = 0, []
        for i in range(0, len(fiches), lot):
            r = self._appel("PUT", "/produits", json={"produits": fiches[i:i + lot]})
            envoyes += len(r.get("produits", []))
            erreurs += [f"{e.get('reference')}: {e.get('erreur')}" for e in r.get("erreurs", [])]
        return envoyes, erreurs

    def stock(self, reference, stock):
        return self._appel("PATCH", f"/produits/{reference}/stock", json={"stock": int(stock)})

    def commandes(self, depuis=None):
        return self._appel("GET", "/commandes", params={"depuis": depuis} if depuis else None)["commandes"]

    def expedier(self, commande_id, transporteur, suivi):
        return self._appel("POST", f"/commandes/{commande_id}/expedier", json={"transporteur": transporteur, "suivi": suivi})

    def signature_valide(self, corps_brut: bytes, entete: str) -> bool:
        return signature_valide(corps_brut, entete, self.jeton)


def signature_valide(corps_brut: bytes, entete: str, jeton: str) -> bool:
    """Verifie X-Exantrix-Signature (sha256= + HMAC-SHA256 hex du corps brut, cle = jeton)."""
    attendu = "sha256=" + hmac.new(jeton.encode(), corps_brut, hashlib.sha256).hexdigest()
    return hmac.compare_digest(attendu, entete or "")


__all__ = ["Exantrix", "ExantrixError", "signature_valide", "BASE"]
__version__ = "1.0.0"
