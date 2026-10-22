"""Contrats d'entrée et de sortie de l'API (Pydantic v2)."""
from typing import Literal

from pydantic import BaseModel, Field, field_validator

Label = Literal["POSITIVE", "NEGATIVE", "INDETERMINE"]


class PredictRequest(BaseModel):
    """Requête de prédiction."""
    text: str = Field(..., min_length=1, max_length=2000, description="Texte à classifier",
                      examples=["Livraison rapide, produit conforme, très satisfait"])

    @field_validator("text")
    @classmethod
    def _pas_de_blancs_seuls(cls, valeur: str) -> str:
        """Même règle que predict() du TP2 : un texte réduit à des blancs est un texte vide."""
        if not valeur.strip():
            raise ValueError("Le texte ne peut pas être vide ou ne contenir que des espaces")
        return valeur


class PredictResponse(BaseModel):
    """Réponse de prédiction."""
    label: Label = Field(..., description="POSITIVE, NEGATIVE, ou INDETERMINE sous le seuil")
    score: float = Field(..., ge=0, le=1, description="Confiance de la classe prédite")
    text: str = Field(..., description="Aperçu du texte analysé (100 caractères)")


class HealthResponse(BaseModel):
    """Réponse de l'endpoint de santé."""
    status: str = Field(..., description="OK si le modèle est chargé")
    model: str = Field(..., description="Nom du modèle servi")


class ErrorResponse(BaseModel):
    """Format standard des erreurs FastAPI."""
    detail: str
