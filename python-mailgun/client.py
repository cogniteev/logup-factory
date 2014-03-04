import requests

class Client(object):
    def __init__(self, key, domain):
        self.api_key = key
        self.domain = domain

    def _request(self, method, resource, data=None, files=None):

        url = 'https://api.mailgun.net/v2/%s/%s' % (self.domain, resource)

        auth = ('api', self.api_key)

        return requests.request(method, url, data=data, auth=auth, files=files)

    def send_mail(self, sender, to, subject, text, html=None, cc=None, bcc=None,
                  files=None):
        data = {'from': sender, 'to': to, 'subject': subject, 'text': text,
                'html': html if html else text}

        if cc:
            data['cc'] = cc
        if bcc:
            data['bcc'] = bcc

        if files and isinstance(files, list):
            attached_files = []
            for f in files:
                attached_files.append(('attachment', open(f)))
            return self._request('post', 'messages', data=data,
                                 files=attached_files)

        return self._request('post', 'messages', data=data)