from sentiment_app.predict import Prediction, charger_modele, predict

__all__ = ["Prediction", "charger_modele", "predict"]

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python src/predict.py \"texte...\"")
        return 2
    texte = " ".join(sys.argv[1:])
    try:
        res = predict(texte)
        print(f"{res['label']} (confiance {res['score']:.2%})")
        return 0
    except Exception as e:
        print(e, file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
