import os
import requests
from requests.auth import HTTPBasicAuth

class AgentAPI:
    def __init__(self, ampa_url=None, username=None, password=None, api_token=None):
        if ampa_url is None:
            ampa_url = os.getenv("AMPA_API_URL", "https://ampa-api.the37lab.com/")
        if username is None:
            username = os.getenv("AMPA_API_USERNAME")
        if password is None:
            password = os.getenv("AMPA_API_PASSWORD")
        if api_token is None:
            api_token = os.getenv("AMPA_API_TOKEN")
        self.base_url = ampa_url.rstrip('/')
        if username and password:
            self.auth = HTTPBasicAuth(username, password)
            self.api_token = None
        elif api_token:
            self.auth = None
            self.api_token = api_token
        else:
            raise ValueError("Either username and password or api_token must be provided")

    def _get_headers(self):
        if self.api_token:
            return {"X-API-Token": self.api_token}
        return {}

    def create_agent(self, **kwargs):
        url = f"{self.base_url}/api/v1/agents"
        response = requests.post(url, params=kwargs, auth=self.auth, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def list_agents(self):
        url = f"{self.base_url}/api/v1/agents"
        response = requests.get(url, auth=self.auth, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def get_agent(self, agent):
        url = f"{self.base_url}/api/v1/agents/{agent}"
        response = requests.get(url, auth=self.auth, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def get_agent_versions(self, agent):
        url = f"{self.base_url}/api/v1/agents/{agent}/versions"
        response = requests.get(url, auth=self.auth, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def call_agent(self, agent, variables=None, prompt=None):
        url = f"{self.base_url}/api/v1/agents/{agent}/call"
        params = []
        if variables:
            for k, v in variables.items():
                params.append(('var', f"{k}={v}"))
        if prompt:
            params.append(('prompt', prompt))
        response = requests.post(url, params=params, auth=self.auth, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def update_agent(self, agent_id, **kwargs):
        url = f"{self.base_url}/api/v1/agents/{agent_id}/update_agent"
        response = requests.put(url, params=kwargs, auth=self.auth, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def delete_agent(self, agent_id):
        url = f"{self.base_url}/api/v1/agents/{agent_id}"
        response = requests.delete(url, auth=self.auth, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def delete_agent_version(self, agent_id, version_id):
        url = f"{self.base_url}/api/v1/agents/{agent_id}/versions/{version_id}"
        response = requests.delete(url, auth=self.auth, headers=self._get_headers())
        response.raise_for_status()
        return response.json()