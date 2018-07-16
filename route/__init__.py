import json


def generate_header(content_type='text/html', state_code=200):
    sc = str(state_code)
    state_dict = {
        '200': 'OK',
        '404': 'Not Found'
    }
    header = f'HTTP/1.1 {sc} {state_dict[sc]}\r\n' \
             f'Content-Type: {content_type}\r\n' \
             f'\r\n'
    return header


def json_response(data):
    body = json.dumps(data, ensure_ascii=False, indent=2)
    header = generate_header('application/json')

    response = header + body
    return response


if __name__ == '__main__':
    pass
