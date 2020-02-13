import requests, json, re
from typing import Any, Dict
import iso8601
import pytz

name = "SnlData"
api_version = 'v1'
user_agent = "%s %s" % (name, api_version)

script_version = '0.0.5'


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
    
    QUERYQUAL = {
        0: 'Treff på artikkeltekst eller deler av tittel',
        1: 'Søkestrengen er lik artikkelens tittel (headword), men artikkelen har en ytterligere presisering (clarification)',
        2: 'Søkestrengen er lik artikkelens tittel (headword) og det er ingen ytterligere presisering (clarification)',
    }
    
    assertUser = None
    
    def __init__(
        self,
        user_agent=user_agent,
    ):
        self.headers = {"User-Agent": user_agent}
        self.S = requests.Session()
        self.results = {}
        
    def search(self, zone="snl", query="", limit=3, offset=0, best=False):
    """
    @param zone: Website used for the search
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
            
            PARAMS = {
                "query": query,
                "limit": limit,
                "offset": offset,
            }
            
            getVal = self._get(PARAMS, zone)
            
            if best:
                self.results = self._getSpecific(getVal[0]["article_url_json"]).json()
                self.store_var()
            else:
                self.json = self.simple(getVal)
        else:
            raise Exception(
                "Something went wrong with the parametres!"
            )

    def searchV2(self, param: Dict[str, str], zone="snl", best = False) -> Any:
    """
    Dict param: (with "prototyping")
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
    
    @param zone: Website used for the search
    @type zone: str
    @param best: To get the first and best (by query_match_quality) result returned.
    @type best: bool
    """
         if (param['limit'] > 0 and param['limit'] < 101 and param['offset'] < param['limit'] and param['query'] != ""):
            
            getVal = self._get(param, zone)
            
            if best:
                self.results = self._getSpecific(getVal[0]["article_url_json"])
                self.store_var()
            else:
                self.json = self.simple(getVal,zone)
        #else: #BUG - IndentationError: unindent does not match any outer indentation level
         #   raise Exception("Something went wrong with the parametres!")

    def _get(self, data, zone="snl"):
    """
    API GET
    @param data: parametres to be used
    @type data: dict
    @param zone: Website used for the search
    @type zone: str
    """
        R = self.S.get(self.PATHS[zone.lower()], params=data, headers=self.headers)
        if R.status_code != 200:
            raise Exception(
                "GET was unsuccessfull ({}): {}".format(R.status_code, R.text)
            )
        return R.json()
    
    def _getSpecific(self, data):
    """
    API GET from JSON site
    @param data: JSON page/file/attribute to get
    @type data: Json
    """
        R = self.S.get(data, headers=self.headers)
        if R.status_code != 200:
            raise Exception(
                "GET was unsuccessfull ({}): {}".format(R.status_code, R.text)
            )
        self.results = R.json()
        self.store_var()
        return self.results
    
    def simple(self, obj, zone=""):
    """
    Adds a entry to JSON file
    @param obj: JSON page/file/attribute
    @type obj: Json
    @param zone: Website used for the search (different for "prototyping")
    @type zone: str
    """
        i = 0
        for result in obj:
            if zone == 'prototyping':
                obj[i].update( {'query_quality_explain' : self.QUERYQUAL[result['query_match_quality']]} )
            else:
                sentence = re.search(r'^(.*?(?<!\b\w)[.?!])\s+[A-Z0-9]', result["first_two_sentences"], flags=0)
                obj[i].update( {'simple' : '{}. {} (rank {}): {}'.format(i,result["headword"],round(result["rank"],1),sentence.group(1))} )
            i += 1
            
        return obj
    
    def date_format(self, dateRFC):
    """
    Human-readable date
    @param dateRFC: date in RFC3339 format
    @type dateRFC: str
    """
        _date_obj=iso8601.parse_date(dateRFC)
        _date_utc=_date_obj.astimezone(pytz.utc)
        return _date_utc.strftime('%b %d, %Y; %H:%M:%S')
    
    def taxonomy(self):
        page = str(self.results["subject_url"])+'.json'
        self._getSpecific(page)
    
    def store_var(self):
    """
    Local storage for easy grabbing of data
    """
        if 'taxonomy' in self.results:
            self.tax_json = self.results
            self.tax_title = str(self.results["taxonomy"]["title"])
            self.tax_primary_article = self.results["taxonomy"]["primary_article"] #list
            self.tax_articles = self.results["taxonomy"]["articles"] #list
            self.tax_ancestors = self.results["taxonomy"]["ancestors"] #list
        else:
            try:
                self.json = self.results
                self.title = str(self.results["title"])
                self.url = str(self.results["url"])
                self.subject_url = str(self.results["subject_url"])
                self.subject_title = str(self.results["subject_title"])
                self.xhtml_body = self.results["xhtml_body"]
                self.created_at = self.date_format(self.results["created_at"])
                self.changed_at = self.date_format(self.results["changed_at"])
                self.license_name = str(self.results["license_name"])
                self.metadata_license_name = str(self.results["metadata_license_name"])
                
                for val in self.results["metadata"]:
                    if val == "headword":
                        self.meta_headword = self.results["metadata"]["headword"]
                    
                    if val == "lastname":
                        self.meta_lastname = self.results["metadata"]["lastname"]
                    
                    if val == "firstname":
                        self.meta_firstname = self.results["metadata"]["firstname"]
                    
                    if val == "birth_date":
                        self.meta_birth_date = self.results["metadata"]["birth_date"]
                    
                    if val == "birthplace":
                        self.meta_birthplace = self.results["metadata"]["birthplace"]
                    
                    if val == "firstname":
                        self.meta_firstname = self.results["metadata"]["firstname"]
                    
                    if val == "death_date":
                        self.meta_death_date = self.results["metadata"]["death_date"]
                        
                    if val == "article_type":
                        self.meta_article_type = self.results["metadata"]["article_type"]
                        
                    if val == "authorized": #1 = true 0 = false
                        self.meta_authorized = self.results["metadata"]["authorized"]
                        
                    if val == "pronunciation":
                        self.meta_pronunciation = self.results["metadata"]["pronunciation"]
                        
                    if val == "place_of_death":
                        self.meta_place_of_death = self.results["metadata"]["place_of_death"]
                        
                    if val == "alternative_form":
                        self.meta_alternative_form = self.results["metadata"]["alternative_form"]
                    
                    if val == "epoch_start":
                        self.meta_epoch_start = self.results["metadata"]["epoch_start"]
                
                self.authors = self.results["authors"]    
                self.images = self.results["images"]
    
            except AttributeError:
                print("There's no item with that code")
