from connexion.exceptions import OAuthProblem

import config


def apikey_auth(token):
    if not config.TOKEN.__eq__(token) or config.TOKEN is None:
        raise OAuthProblem("Invalid Token")

    return {"uid": 1}
