"""Tests aux limites du contrat d'entrée (TP4, étape B).

PredictRequest promet un champ « text », chaîne de 1 à 2000 caractères.
Ce fichier vérifie cette promesse à ses frontières, puis au hasard (hypothesis).
"""
import json
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")

LABELS = {"POSITIVE", "NEGATIVE", "INDETERMINE"}


@pytest.fixture(scope="module")
def client():
    """Portée « module » : l'API démarre une fois pour tout le fichier (hypothesis l'exige)."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as c:  # le « with » exécute le lifespan : le modèle est chargé
        yield c


def en_json(valeur: object) -> bytes:
    """Corps de requête JSON, sous forme d'octets : permet aussi d'envoyer un corps invalide."""
    return json.dumps(valeur).encode("utf-8")


# Étape B.1 : au moins huit cas, chacun avec son code attendu. Deux sont donnés.
CAS = [
    pytest.param(en_json({"text": ""}), 422, id="texte-vide"),
    pytest.param(en_json({"text": "   "}), 422, id="texte-blancs"),
    pytest.param(en_json({"text": "a"}), 200, id="un-caractere"),
    pytest.param(en_json({"text": "a" * 2000}), 200, id="2000-caracteres"),
    pytest.param(en_json({"text": "a" * 2001}), 422, id="2001-caracteres"),
    pytest.param(en_json({}), 422, id="champ-absent"),
    pytest.param(en_json({"text": 42}), 422, id="champ-mauvais-type"),
    pytest.param(b"pas du json", 422, id="corps-non-json"),
]


@pytest.mark.parametrize("corps, code_attendu", CAS)
def test_frontieres_du_contrat(client, corps, code_attendu):
    reponse = client.post("/predict", content=corps, headers={"Content-Type": "application/json"})
    assert reponse.status_code == code_attendu
    # Étape B.2 : pour chaque 422, la forme standard de FastAPI (liste de loc/msg/type).
    if code_attendu == 422:
        detail = reponse.json()["detail"]
        assert isinstance(detail, list) and detail, f"detail non standard : {detail!r}"
        for erreur in detail:
            assert {"loc", "msg", "type"} <= erreur.keys()


# Étape B.5 : deux tests de propriété avec hypothesis, dans ce fichier.
@settings(deadline=None)
@given(st.text(min_size=1, max_size=2000).filter(lambda t: t.strip()))
def test_propriete_texte_valide(client, texte):
    """Tout texte de 1 à 2000 caractères non blancs est classifié avec un label du contrat."""
    reponse = client.post("/predict", json={"text": texte})
    assert reponse.status_code == 200
    corps = reponse.json()
    assert corps["label"] in LABELS
    assert 0.0 <= corps["score"] <= 1.0


BLANCS = st.characters(whitelist_categories=("Zs", "Zl", "Zp"))


@settings(deadline=None)
@given(st.text(alphabet=BLANCS, min_size=1, max_size=2000))
def test_propriete_texte_blanc(client, texte):
    """Tout texte fait uniquement de blancs (au sens de str.strip()) est refusé, forme standard."""
    assert texte and not texte.strip()  # pré-condition : ce que str.strip() considère blanc
    reponse = client.post("/predict", json={"text": texte})
    assert reponse.status_code == 422
    detail = reponse.json()["detail"]
    assert isinstance(detail, list) and detail
    for erreur in detail:
        assert {"loc", "msg", "type"} <= erreur.keys()
