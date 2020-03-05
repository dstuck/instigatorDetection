from abc import ABCMeta, abstractclassmethod, abstractmethod

from utils.api_utils import get_api


class CrawlerBase(object, metaclass=ABCMeta):
    """
    Base class for crawlers that satisfy a given request
    """
    def __init__(self, request):
        """
        :param request: Request object specific to this Crawler object
        """
        self.validate_request(request)
        self.request = request
        self._api = None

    @classmethod
    @abstractclassmethod
    def validate_request(cls, request):
        raise NotImplementedError()

    @property
    def api(self):
        # TODO: Modify to not use direct api calls
        if self._api is None:
            self._api = get_api()
        return self._api

    def crawl(self):
        """
        Kick off crawling job by making possibly multiple requests to twitter api
        """
        request_data = self._get_data_for_initial_request()
        api_response = self._make_api_request(request_data)
        processed_response = self._process_response(api_response)
        finished_crawling = self._has_finished_crawling(processed_response)

        while not finished_crawling:
            request_data = self._update_request_data(request_data, processed_response)
            api_response = self._make_api_request(request_data)
            processed_response = self._process_response(api_response)
            finished_crawling = self._has_finished_crawling(processed_response)

    @abstractmethod
    def _get_data_for_initial_request(self):
        """
        Returns data for the api request given the Request object
        :return: dict of data for request
        """
        raise NotImplementedError()

    @classmethod
    @abstractclassmethod
    def get_endpoint(cls):
        """
        Get endpoint this request hits, i.e. "search/tweets.json"
        :return: String representing endpoint to request
        """
        raise NotImplementedError()

    @classmethod
    def get_verb(cls):
        """
        Get http verb this request uses, i.e. "search/tweets.json"
        :return: String representing endpoint to request
        """
        return "GET"

    def _make_api_request(self, request_data):
        """
        :param request_data: data to pass to api call
        :return: response from api
        """
        # TODO: Refactor this method to make request to resilient api and wait on response
        return self.api.direct_request(self.get_endpoint(), self.get_verb(), request_data)

    @abstractmethod
    def _process_response(self, api_response):
        """
        Manage processing/storage of response returning cleaned response dict
        :param api_response: dict response from last api call
        :return: Cleaned dict of result
        """
        raise NotImplementedError()

    @abstractmethod
    def _has_finished_crawling(self, api_response):
        """
        Determine if another api call must be made to complete call
        :param api_response: dict response from last api call
        :return: bool determining if the crawler has finished crawling
        """
        raise NotImplementedError()

    @abstractmethod
    def _update_request_data(self, request_data, api_response):
        """
        Update request data for next api request based on previous
        :param request_data: data used for last api call
        :param api_response: response from last api call
        :return: Modified request_data
        """
        raise NotImplementedError()
