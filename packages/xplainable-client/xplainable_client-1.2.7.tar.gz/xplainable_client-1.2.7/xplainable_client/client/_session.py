from functools import cached_property
import xplainable
import json
from requests.adapters import HTTPAdapter
import sys
from urllib3.util import Retry
import requests

class Session:
    """ A client for interfacing with the xplainable web api (xplainable cloud).

    Access models, preprocessors and user data from xplainable cloud. API keys
    can be generated at https://beta.xplainable.io.

    Args:
        api_key (str): A valid api key.
    """

    def __init__(self, api_key=None, hostname='https://api.xplainable.io', org_id=None, team_id=None):
        if not api_key:
            raise ValueError('A valid API Key is required. Generate one from the xplainable app.')

        self.api_key = api_key
        self.hostname = hostname
        self._setup_session()  # Set up the session and other initialization steps
        response = self._session.get(
            url=f'{self.hostname}/client/connect',
        )

        #Create content object
        content = json.loads(response.content)
        self.username = content["username"]
        self.key = content["key"]
        self.expires = content["expires"]

        #Record version info
        version_info = sys.version_info
        self.python_version = f'{version_info.major}.{version_info.minor}.{version_info.micro}'
        self.xplainable_version = xplainable.__version__

        return 


    @cached_property
    def user_data(self):
        """ Retrieves the user data for the active user.
        Returns:
            dict: User data
        """
        response = self._session.get(
            url=f'{self.hostname}/client/connect',
        )
        if response.status_code == 200:
            return self.get_response_content(response)

        else:
            raise Exception(
                f"{response.status_code} Unauthenticated. {response.json()['detail']}"
            )

    def _setup_session(self):
        """ Set up the session with retry strategy and session headers. """
        self._session = requests.Session()
        self._session.headers['api_key'] = self.api_key
        retry_strategy = Retry(total=5, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self._session.mount(self.hostname, adapter)

    def get_response_content(self, response):
        #Print response to console
        print(response)
        if response.status_code == 200:
            return json.loads(response.content)
        elif response.status_code == 401:
            err_string = "401 Unauthorised"
            content = json.loads(response.content)
            if 'detail' in content:
                err_string = err_string + f" ({content['detail']})"

            raise Exception(err_string)
        else:
            raise Exception(response.status_code, json.loads(response.content))

    def _gather_initialization_data(self):
        """ Gather data to display or return upon initialization. """
        version_info = sys.version_info
        self.python_version = f'{version_info.major}.{version_info.minor}.{version_info.micro}'
        self.xplainable_version = xplainable.__version__

        return {
            "xplainable version": self.xplainable_version,
            "python version": self.python_version,
            "user": self.user_data['username'],
            "organisation": self.user_data['organisation_name'],
            "team": self.user_data['team_name'],
        }



