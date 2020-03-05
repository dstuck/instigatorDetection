from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from crawlers.crawler_base import CrawlerBase

class CrawlerBaseTestCase(TestCase):
    def setUp(self):
        crawler_mock_calls = MagicMock()
        class TestCrawler(CrawlerBase):
            def _has_finished_crawling(self, api_response):
                return crawler_mock_calls._has_finished_crawling(api_response)

            @classmethod
            def validate_request(cls, request):
                return crawler_mock_calls.validate_request(request)

            def _update_request_data(self, request_data, api_response):
                return crawler_mock_calls._update_request_data(request_data, api_response)

            def _process_response(self, api_response):
                return crawler_mock_calls._process_response(api_response)

            @classmethod
            def get_endpoint(cls):
                return 'fake/endpoint'

            def _get_data_for_initial_request(self):
                return crawler_mock_calls._get_data_for_initial_request()

        self.crawler_mock_calls = crawler_mock_calls
        self.crawler_cls = TestCrawler
        self.request_mock = MagicMock()
        self.crawler = TestCrawler(self.request_mock)
        self.crawler._api = MagicMock()
        self.api_mock = self.crawler._api

    def test_init(self):
        self.crawler_mock_calls.validate_request.assert_called_once_with(self.request_mock)

    def test_crawl(self):
        self.crawler_mock_calls._has_finished_crawling.side_effect = [False, True]

        self.crawler.crawl()

        self.crawler_mock_calls._get_data_for_initial_request.assert_called_once_with()
        self.crawler_mock_calls._process_response.assert_has_calls([
            call(self.api_mock.direct_request.return_value),
            call(self.api_mock.direct_request.return_value),
        ])
        self.crawler_mock_calls._has_finished_crawling.assert_has_calls([
            call(self.crawler_mock_calls._process_response.return_value),
            call(self.crawler_mock_calls._process_response.return_value),
        ])
