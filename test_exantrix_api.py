import hashlib, hmac, unittest
from unittest.mock import patch, MagicMock
from exantrix_api import Exantrix, ExantrixError, signature_valide


class Tests(unittest.TestCase):
    def test_signature(self):
        corps = b'{"evenement":"commande.payee"}'
        sig = "sha256=" + hmac.new(b"jeton", corps, hashlib.sha256).hexdigest()
        self.assertTrue(signature_valide(corps, sig, "jeton"))
        self.assertFalse(signature_valide(corps, "sha256=00", "jeton"))
        self.assertTrue(Exantrix("jeton").signature_valide(corps, sig))

    def test_envoyer_par_lots(self):
        ex = Exantrix("J")
        rep = MagicMock(status_code=200, content=b"x"); rep.json = lambda: {"produits": [{}] * 2, "erreurs": []}
        with patch.object(ex.s, "request", return_value=rep) as m:
            n, err = ex.envoyer([{"reference": str(i)} for i in range(5)], lot=2)
        self.assertEqual(m.call_count, 3)
        self.assertEqual(m.call_args_list[0].kwargs["json"]["produits"][0]["reference"], "0")

    def test_erreur(self):
        ex = Exantrix("J")
        rep = MagicMock(status_code=401, content=b"x"); rep.json = lambda: {"erreur": "jeton invalide"}
        with patch.object(ex.s, "request", return_value=rep):
            with self.assertRaises(ExantrixError) as c:
                ex.moi()
        self.assertEqual(c.exception.status, 401)


if __name__ == "__main__":
    unittest.main()
