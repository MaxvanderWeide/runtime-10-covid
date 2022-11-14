from connexion.exceptions import OAuthProblem


def apikey_auth(token):
    if not "token".__eq__(token):
        raise OAuthProblem("Invalid Token")

    return {"uid": 1}
