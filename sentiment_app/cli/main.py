#!/usr/bin/env python
import argparse
import sys

from sentiment_app import __version__
from sentiment_app.predict import predict as _predict

SEUIL_ABSTENTION = 0.60


def main():
    p = argparse.ArgumentParser(prog='sentiment')
    p.add_argument('--version', action='version', version='sentiment-app ' + __version__)
    s = p.add_subparsers(dest='cmd', required=True)
    sp = s.add_parser('predict')
    sp.add_argument('texte')
    s.add_parser('serve')
    s.add_parser('version')
    a = p.parse_args()
    if a.cmd == 'version':
        print('sentiment-app ' + __version__)
        return 0
    if a.cmd == 'predict':
        try:
            r = _predict(a.texte)
            score = r['score']
            if score >= SEUIL_ABSTENTION:
                lbl = 'POSITIVE' if r['label'] == 'positive' else 'NEGATIVE'
            else:
                lbl = 'INDETERMINE'
            print(lbl + ' (confiance ' + format(score, '.2%') + ')')
            return 0
        except Exception as e:
            print(e, file=sys.stderr)
            return 1
    if a.cmd == 'serve':
        import uvicorn
        uvicorn.run('api.main:app', host='127.0.0.1', port=8000)
        return 0
    p.print_help()
    return 1


if __name__ == '__main__':
    raise SystemExit(main())