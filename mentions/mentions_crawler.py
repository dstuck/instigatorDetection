from utils.api_utils import get_api


class MentionsCrawler(object):
    """
    Class to crawl back through a single user's mentions (non-retweet @ mentions)
    """
    def __init__(self, user, api=None, last_id=None):
        """
        :param user: twitter handle to check mentions for
        :param api: twitter.Api object
        :param last_id: int, status id of oldest status already pulled
        """
        self.user = user
        self.request_count = 100
        self._api = api
        self.mentions = []
        self.last_id = last_id

    @property
    def api(self):
        if self._api is None:
            self._api = get_api()
        return self._api

    def crawl_mentions_in_range(self, since_id=None, max_id=None):
        """Crawl tweets mentioning the user for a given range

        :param since_id: Exclusive min id to search
        :param max_id: Inclusive max id to search
        :return: List of twitter.Status
        """
        return self.api.GetSearch(
            term='@{} -filter:retweets'.format(self.user),
            result_type='recent',
            count=self.request_count,
            since_id=since_id,
            max_id=max_id
        )

    def crawl(self):
        max_id = self.last_id
        if max_id:
            max_id = max_id - 1
        new_mentions = self.crawl_mentions_in_range(max_id=max_id)
        if new_mentions:
            self.last_id = new_mentions[-1].id
            self.mentions.extend(new_mentions)
            return True
        return False


if __name__ == "__main__":
    import argparse

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('user')
    PARSER.add_argument('-n', '--n-mentions', required=False)
    PARSED_ARGS = PARSER.parse_args()

    mention_crawler = MentionsCrawler(PARSED_ARGS.user)
    if PARSED_ARGS.n_mentions:
        mention_crawler.request_count = PARSED_ARGS.n_mentions
    recent_mentions = mention_crawler.crawl_mentions_in_range()
    for mention in recent_mentions:
        print(repr(mention))
