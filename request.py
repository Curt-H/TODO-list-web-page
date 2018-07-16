import json
import urllib.parse


class Request(object):
    def __init__(self, request):
        """
        :param request: receieved from server, string and cannot be null
        """
        # Initialize the origin data
        self.method = ''
        self.path = ''
        self.args = dict()
        self.form = dict()

        # Dealing with the request
        self.raw_data = request
        self.header, self.body = request.split('\r\n\r\n')
        self.analyse_header()

    def analyse_header(self):
        request_line = self.header.split('\r\n')[0]
        request_line_element = request_line.split(' ')

        self.method = request_line_element[0]
        path_with_args = request_line_element[1]

        self.analyse_const(path_with_args)

    def analyse_const(self, path_with_args):
        """
        :param path_with_args: path like this '/index?foo=bar'
        :return: None
        """
        self.path = path_with_args
        if self.method == 'GET' and path_with_args.find('?') > 0:
            self.path, args_str = path_with_args.split('?')
            args_str = urllib.parse.unquote_plus(args_str)

            for a in args_str.split('&'):
                k, v = a.split('=')
                self.args[k] = v
        elif self.method == 'POST':
            self.path = path_with_args
            self.body = urllib.parse.unquote_plus(self.body)
            if self.body != '' and self.body.find('=') != -1:
                form_list = self.body.split('&')
                for a in form_list:
                    k, v = a.split('=')
                    self.form[k] = v

    def json(self):
        return json.loads(self.body)
