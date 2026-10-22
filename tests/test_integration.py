"""Tests d'intégration : l'API telle qu'elle tourne vraiment (TP4, étape D).

Les tests du TP3 vérifient des réponses ; ceux-ci vérifient le démarrage de l'API
et son comportement quand le modèle manque ou tombe en panne.
"""
from pathlib import Path

import pytest

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


def test_demarrage_reel_charge_le_modele():
    """D.1 (donné en exemple) : un client ouvert par « with » exécute le lifespan."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        reponse = client.get("/health")
    assert reponse.status_code == 200
    assert "TP2" in reponse.json()["model"]


def test_modele_absent_l_api_refuse_de_demarrer(monkeypatch, tmp_path):
    """D.2 : chemin du modèle redirigé, cache vidé : le démarrage échoue."""
    from fastapi.testclient import TestClient

    import predict
    from api.main import app

    monkeypatch.setattr(predict, "MODELE", tmp_path / "absent.joblib")
    predict.charger_modele.cache_clear()
    try:
        with pytest.raises(FileNotFoundError):
            with TestClient(app):
                pass
    finally:
        predict.charger_modele.cache_clear()


def test_modele_non_charge_renvoie_503():
    """D.3 : modèle retiré de app.state : /health et /predict répondent 503."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        sauve = app.state.classifier
        del app.state.classifier
        try:
            assert client.get("/health").status_code == 503
            assert client.post("/predict", json={"text": "bonjour"}).status_code == 503
        finally:
            app.state.classifier = sauve


@pytest.mark.parametrize("erreur", [RuntimeError("panne"), ValueError("bug interne")])
def test_panne_du_modele_renvoie_500_sans_message_interne(erreur):
    """D.4 : toute exception du modèle répond 500, sans le message interne."""
    from fastapi.testclient import TestClient

    from api.main import app

    class ModeleEnPanne:
        model_name = "en panne"

        def predict(self, text):
            raise erreur

    with TestClient(app) as client:
        sauve = app.state.classifier
        app.state.classifier = ModeleEnPanne()
        try:
            reponse = client.post("/predict", json={"text": "bonjour"})
        finally:
            app.state.classifier = sauve

    assert reponse.status_code == 500
    assert "Erreur interne du serveur" in reponse.text
    assert str(erreur) not in reponse.text


def test_classes_du_modele_connues():
    """E.3 : le modèle chargé n'expose que des classes de la correspondance du contrat."""
    import predict
    from api.model import ETIQUETTES

    predict.charger_modele.cache_clear()
    pipeline = predict.charger_modele()
    assert set(pipeline.classes_) <= ETIQUETTES.keys()
