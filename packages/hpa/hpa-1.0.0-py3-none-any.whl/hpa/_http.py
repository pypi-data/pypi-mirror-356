import requests


def post(url, req_body, headers=None):
    """ post http request to slb service
        :param url: url path
        :param req_body: http request body
        :param headers: http headers
        :return:
            success return response
            fali return None
    """
    try:
        response = requests.post(url, data=req_body, headers=headers, timeout=10, verify=False)
        return response

    except Exception as e:
        raise ValueError('caught exception when post {0}. {1}'.format(url, e))


def _format_http_text(method, url, headers, body):
    """
    print http head and body for request or response

    For examples: _format_http_text('', title, response.headers, response.text)
    """
    result = method + ' ' + url + '\n'

    if headers is not None:
        for key, value in headers.items():
            result = result + key + ': ' + value + '\n'

    result = result + body
    return result


