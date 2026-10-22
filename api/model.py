"""Raccord entre l'API et le modèle entraîné au TP2.

L'API n'entraîne rien et ne connaît pas scikit-learn : elle appelle la fonction
predict() de src/predict.py, qui charge models/sentiment.joblib une seule fois.
"""
import sys
from pathlib import Path
from typing import Literal, TypedDict

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))
from predict import charger_modele  # noqa: E402  (fonctions du TP2)
from predict import predict as _predict  # noqa: E402

SEUIL_ABSTENTION = 0.60  # sous cette confiance, le modèle préfère s'abstenir (TP4, étape C)

Label = Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]
ETIQUETTES: dict[str, Label] = {"negative": "NEGATIVE", "positive": "POSITIVE"}


class PredictionAPI(TypedDict):
    """Réponse de l'API : étiquette du contrat, confiance, aperçu du texte."""
    label: Label
    score: float
    text: str


class SentimentClassifier:
    """Enveloppe du modèle TP2 avec l'interface attendue par l'API."""

    model_name = "tfidf-logreg (TP2, models/sentiment.joblib)"

    def __init__(self) -> None:
        pipeline = charger_modele()  # échoue immédiatement si le joblib manque
        classes = set(pipeline.classes_)
        if not classes <= ETIQUETTES.keys():
            raise RuntimeError(
                f"classes du modèle inconnues du contrat : {sorted(classes)}"
            )
        self.classes = classes

    def predict(self, text: str) -> PredictionAPI:
        """Renvoie {'label': POSITIVE|NEGATIVE|INDETERMINE, 'score': float, 'text': aperçu}."""
        r = _predict(text)  # lève ValueError si le texte est vide
        score = r["score"]
        etiquette = ETIQUETTES[r["label"]]
        label: Label = etiquette if score >= SEUIL_ABSTENTION else "INDETERMINE"
        return {"label": label, "score": score, "text": text[:100]}


def load_model() -> SentimentClassifier:
    """Construit le classifier (le cache de chargement est dans src/predict.py)."""
    return SentimentClassifier()
