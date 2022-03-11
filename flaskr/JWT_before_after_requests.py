@app.errorhandler(401)
def custom_401(error):
    return Response("Missing JWT in header.", 401, {"Authorization": "header is required"})


@app.before_request
def authorization_handler():
    headers = request.headers
    if 'auth' in request.path:
        print(request.path)
        return
    if 'Authorization' in headers:
        token = headers.get('Authorization')
        print(token)
    else:
        abort(401)
