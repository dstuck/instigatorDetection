from twitter import Api, User, Status


class DirectTwitterApi(Api):
    def direct_request(self, endpoint, verb, data=None):
        """Request a twitter api endpoint directly.

        Args:
            endpoint:
                The api endpoint to request. i.e. "search/tweets.json"
            verb:
                Either POST or GET.
            data:
                A dict of (str, unicode) key/value pairs.

        Returns:
            A JSON object.
        """
        full_url = '{}/{}'.format(self.base_url, endpoint)
        resp = self._RequestUrl(full_url, verb, data=data)
        data = self._ParseAndCheckTwitter(resp.content.decode('utf-8'))
        return data
