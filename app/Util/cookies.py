from flask import current_app

def set_cookie(response, name, token, time):
    response.set_cookie(
        name, 
        token,
        httponly=current_app.config["COOKIE_HTTP"],
        secure=current_app.config["COOKIE_SECURE"],
        max_age=time,
    )
    return response
    
def set_access_cookie(response, token):
    max_age = current_app.config["JWT_TOKEN_TIME"] 
    return set_cookie(response, current_app.config["COOKIE_NAME"], token, max_age)