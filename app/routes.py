from flask import request as flask_request, Response, stream_with_context
from app import app, methods


@app.route('/<path:url>', methods=methods.requests_mapping.keys())
def proxy(url):
    requests_function = methods.requests_mapping[flask_request.method]
    headers = dict(flask_request.headers)
    request = requests_function(url, stream=True, params=flask_request.args, headers=headers)
    response = Response(
        stream_with_context(request.iter_content()),
        content_type=request.headers['content-type'],
        status=request.status_code)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
