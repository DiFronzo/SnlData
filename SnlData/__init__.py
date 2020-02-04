import requests, json

name = "SnlData"
api_version = 'v1'
user_agent = "%s %s" % (name, api_version)

script_version = '0.0.1'


class SnlSession:
    """
    Work with SNL
    """
    
    PATHS = {
    'snl': 'https://snl.no/api/'+api_version+'/search',
    'nbl': 'https://nbl.snl.no/api/'+api_version+'/search',
    'sml': 'https://sml.snl.no/api/'+api_version+'/search',
    'prototyping': 'https://snl.no/.api/prototyping/search', #UNSTABLE
    }
    
    assertUser = None
    
    def __init__(
        self,
        user_agent=user_agent,
    ):
        self.headers = {"User-Agent": user_agent}
        self.S = requests.Session()
        
    def search(self, zone="snl", query="", limit=3, offset=0):
        if (limit > 0 and limit < 11 and zone != "" and offset < limit):
            path = self.PATHS[zone.lower()]
            PARAMS = {
                "query": query,
                "limit": limit,
                "offset": offset,
            }
            return self.get(PARAMS, path)
        else:
            raise Exception(
                "Something went wrong with the parametres!"
            )

    def get(self, data, path):
        R = self.S.get(path, params=data, headers=self.headers)
        if R.status_code != 200:
            raise Exception(
                "GET was unsuccessfull ({}): {}".format(R.status_code, R.text)
            )
        return R.json()
