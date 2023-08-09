
def send_cookie(response, access_token=None, refresh_token=None):
    response.set_cookie(key='myCookie', value="bkl")
    if refresh_token is not None:
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            max_age=86400,
            secure=True,
            httponly=True,
            path='/',
            samesite='None'
        )

    if access_token is not None:
        response.set_cookie(
            key='access_token',
            value=access_token,
            max_age=86400,
            secure=True,
            httponly=True,
            path='/',
            samesite='None'
        )

    response.status_code = 201