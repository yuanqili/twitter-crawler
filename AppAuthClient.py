import base64
import json

import requests

API_ENDPOINT = 'https://api.twitter.com'
API_VERSION = '1.1'


class ClientException(Exception):
    pass


class Client(object):
    """This class implements the Twitter's App-only authentication and supported
    API."""

    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = self._get_access_token()
        self.auth_header = {
            'Authorization': 'Bearer {}'.format(self.access_token)}

    def _get_access_token(self):
        """Obtains a bearer token."""
        resource_url = 'https://api.twitter.com/oauth2/token'
        bearer_token = '{}:{}'.format(self.consumer_key,
                                      self.consumer_secret).encode('ascii')
        encoded_bearer_token = base64.b64encode(bearer_token).decode('utf-8')
        data = {'grant_type': 'client_credentials'}
        headers = {
            'Authorization': 'Basic {}'.format(encoded_bearer_token),
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
        response = requests.post(resource_url, data=data, headers=headers)
        return response.json()['access_token']

    def _twitter_api_request(self, api_url, params={}, headers={}):
        """
        Makes a Twitter API request using given information.

        :param api_url: API resource url.
        :param params: Parameters given to this API requests.
        :param headers: HTTP headers given to this API requests.
        :return: A JSON response returned from Twitter.
        """
        resource_url = '{}/{}/{}'.format(API_ENDPOINT, API_VERSION, api_url)
        headers = headers or self.auth_header
        response = requests.get(resource_url, params=params, headers=headers)
        return response.json()

    def search_tweets(self, q, geocode=None, lang=None, locale=None,
                      result_type=None, count=100, until=None, since_id=None,
                      max_id=None, include_entities=None):
        """
        Returns a collection of relevant Tweets matching a specified query.

        Please note that Twitter’s search service and, by extension, the Search
        API is not meant to be an exhaustive source of Tweets. Not all Tweets
        will be indexed or made available via the search interface.

        In API v1.1, the response format of the Search API has been improved to
        return Tweet objects more similar to the objects you’ll find across the
        REST API and platform. However, perspectival attributes (fields that
        pertain to the perspective of the authenticating user) are not currently
        supported on this endpoint.

        To learn how to use Twitter Search effectively, consult our guide on How
        to build a query. See Working with Timelines to learn best practices for
        navigating results by since_id and max_id.

        :param q: Required. A UTF-8, URL-encoded search query of 500 characters
            maximum, including operators. Queries may additionally be limited by
            complexity.
        :param geocode: Optional. Returns tweets by users located within a given
            radius of the given latitude/longitude. The location is
            preferentially taking from the Geotagging API, but will fall back to
            their Twitter profile. The parameter value is specified by
            "latitude,longitude,radius", where radius units must be specified as
            either "mi" (miles) or "km" (kilometers). Note that you cannot use
            the near operator via the API to geocode arbitrary locations;
            however you can use this geocode parameter to search near geocodes
            directly. A maximum of 1,000 distinct "sub-regions" will be
            considered when using the radius modifier.
        :param lang: Optional. Restricts tweets to the given language, given by
            an ISO 639-1 code. Language detection is best-effort.
        :param locale: Optional. Specify the language of the query you are
            sending (only ja is currently effective). This is intended for
            language-specific consumers and the default should work in the
            majority of cases.
        :param result_type: Optional. Optional. Specifies what type of search
            results you would prefer to receive. The current default is "mixed."
            Valid values include:
            * mixed: Include both popular and real time results in the response.
            * recent: return only the most recent results in the response
            * popular: return only the most popular results in the response.
        :param count: Optional. The number of tweets to return per page, up to a
            maximum of 100. Defaults to 15. This was formerly the "rpp"
            parameter in the old Search API.
        :param until: Optional. Returns tweets created before the given date.
            Date should be formatted as YYYY-MM-DD. Keep in mind that the search
            index has a 7-day limit. In other words, no tweets will be found for
            a date older than one week.
        :param since_id: Returns results with an ID greater than (that is, more
            recent than) the specified ID. There are limits to the number of
            Tweets which can be accessed through the API. If the limit of Tweets
            has occured since the since_id, the since_id will be forced to the
            oldest ID available.
        :param max_id: Optional. Returns results with an ID less than (that is,
            older than) or equal to the specified ID.
        :param include_entities: Optional. The entities node will not be
            included when set to false.
        :return: A collection of relevant Tweets matching a specified query.
        """
        api_url = 'search/tweets.json'
        params = dict(q=q, geocode=geocode, lang=lang, locale=locale,
                      result_type=result_type, count=count, until=until,
                      since_id=since_id, max_id=max_id,
                      include_entities=include_entities)
        return self._twitter_api_request(api_url, params)

    def rate_limit_status(self):
        """
        Returns the current rate limits for methods belonging to the specified
        resource families.

        Each API resource belongs to a “resource family” which is indicated in
        its method documentation. The method’s resource family can be determined
        from the first component of the path after the resource version.

        This method responds with a map of methods belonging to the families
        specified by the resources parameter, the current remaining uses for
        each of those resources within the current rate limiting window, and
        their expiration time in epoch time. It also includes a
        rate_limit_context field that indicates the current access token or
        application-only authentication context.

        You may also issue requests to this method without any parameters to
        receive a map of all rate limited GET methods. If your application only
        uses a few of methods, you should explicitly provide a resources
        parameter with the specified resource families you work with.

        When using application-only auth, this method's response indicates the
        application-only auth rate limiting context.
        """
        api_url = 'application/rate_limit_status.json'
        return self._twitter_api_request(api_url)
