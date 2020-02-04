import requests, json, re
from typing import Any, Dict

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
    'nkl': 'https://nkl.snl.no/api/'+api_version+'/search',
    'prototyping': 'https://snl.no/.api/prototyping/search', #UNSTABLE
    }
    assertUser = None
    
    def __init__(
        self,
        user_agent=user_agent,
    ):
        self.headers = {"User-Agent": user_agent}
        self.S = requests.Session()
        
    def search(self, zone="snl", query="", limit=3, offset=0, best=False):
        """
        @param zone: Web site used for the search
        @type zone: str
        @param query: Påkrevd. Spørreord, f.eks. "Tog", "Edvard Munch"
        @type query: str
        @param limit: Ikke påkrevd. Maks. antall resultater, 1-10 er gyldige verdier, standard er 3
        @type limit: int
        @param offset: Ikke påkrevd. Brukes til å vise neste "side" med resultater, default er 0, inkrementer med verdien du satte i limit
        @type offset: int
        @param best: To get the first and best (by rank) result returned.
        @type best: bool
        """
        if (limit > 0 and limit < 11 and zone != "" and offset < limit and query != ""):
            path = self.PATHS[zone.lower()]
            
            PARAMS = {
                "query": query,
                "limit": limit,
                "offset": offset,
            }
            
            getVal = self.get(PARAMS, path)
            
            if best:
                return self.S.get(getVal[0]["article_url_json"]).json()
            elif zone.lower() != "prototyping":
                return self.simple(getVal).json()
            else:
                return getVal.json()
        else:
            raise Exception(
                "Something went wrong with the parametres!"
            )

    def searchV2(self, param: Dict[str, str]) -> Any:
        """
        Dict param: (with "prototyping")
        @param zone: Web site used for the search
        @type zone: str
        @param encyclopedia: Begrens søket til angitt leksikon: snl, sml, nbl eller nkl. Den samme filtreringen kan også oppnås ved gjøre søket i et subdomene.
        @type encyclopedia: str
        @param query: Søketekst, f.eks. "Tog", "Edvard Munch"
        @type query: str
        @param limit: Maksimalt antall resultater. 1-100 er gyldige verdier, standard er 10
        @type limit: int
        @param offset: Brukes for paginering av resultatene. Sett for eksempel offset=100 for å vise søkeresultater utover de første 100.
        @type offset: int
        @param include_metadata: Metadata inkluderes i søkeresultatene hvis dette parameteret settes til true
        @type include_metadata: bool
        @param article_type_id: Filtrer søket til å bare inkludere artikler med angitt artikkeltype
        @type article_type_id: int
        @param author_id: Filtrer søket til å bare inkludere artikler av angitt forfatter
        @type author_id: int
        @param author_name: Filtrer søket til å bare inkludere artikler av forfattere med samsvarende navn
        @type author_name: str
        @param taxonomy_id: Filtrer søket til å bare inkludere artikler i angitt taksonomi
        @type taxonomy_id: int
        @param taxonomy_title: Filtrer søket til å bare inkludere artikler i taksonomier med samsvarende navn
        @type taxonomy_title: str
        @param tagsonomy_id: Filtrer søket til å bare inkludere artikler i angitt tagsonomy
        @type tagsonomy_id: int
        @param tagsonomy_title: Filtrer søket til å bare inkludere artikler i tagsonomyer med samsvarende navn
        @type tagsonomy_title: str
        @param char_count_min: Filtrer søket til å bare inkludere artikler med angitt antall tegn i artikkelteksten, eller flere
        @type char_count_min: int
        @param char_count_max: Filtrer søket til å bare inkludere artikler med angitt antall tegn i artikkelteksten, eller færre
        @type char_count_max: int
        @param media_count_min: Filtrer søket til å bare inkludere artikler med angitt antall media-vedlegg, eller flere
        @type media_count_min: int
        @param media_count_max:Filtrer søket til å bare inkludere artikler med angitt antall media-vedlegg, eller færre
        @type media_count_max: int
        @param version_count_min: Filtrer søket til å bare inkludere artikler med angitt antall historiske versjoner, eller flere
        @type version_count_min: int
        @param version_count_max: Filtrer søket til å bare inkludere artikler med angitt antall historiske versjoner, eller færre
        @type version_count_max: int
        @param license_id: Filtrer søket til å bare inkludere artikler med angitt lisens-id (free eller restricted)
        @type license_id: str
        @param updated_at_or_after: Filtrer søket til å bare inkludere artikler oppdatert på angitt tidspunkt, eller senere. Tidspunktet angis i RFC3339-format.
        @type updated_at_or_after: str (RFC3339 format)
        @param updated_at_or_before: Filtrer søket til å bare inkludere artikler oppdatert på angitt tidspunkt, eller tidligere. Tidspunktet angis i RFC3339-format.
        @type updated_at_or_before: str (RFC3339 format)
        """
        if (param['limit'] > 0 and param['limit'] < 101 and param['offset'] < param['limit'] and param['query'] != ""):
            print("This is an advance API...")
                           
    def get(self, data, path):
        R = self.S.get(path, params=data, headers=self.headers)
        if R.status_code != 200:
            raise Exception(
                "GET was unsuccessfull ({}): {}".format(R.status_code, R.text)
            )
        return R.json()
    
    def simple(self, obj):
        i = 0
        for result in obj:
            sentence = re.search(r'^(.*?(?<!\b\w)[.?!])\s+[A-Z0-9]', result["first_two_sentences"], flags=0)
            obj[i].update( {'simple' : '{}. {} (rank {}): {}'.format(i,result["headword"],round(result["rank"],1),sentence.group(1))} )
            i += 1
            
        return obj
