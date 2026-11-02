"""Paquet de prédiction du sentiment."""
from .predict import Prediction, charger_modele, predict

__all__ = ["Prediction", "charger_modele", "predict"]
__version__ = "0.6.0"
