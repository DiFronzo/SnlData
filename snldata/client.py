#!/usr/bin/env python3
import requests
import re
from typing import Any, Dict

name = "SnlData"
api_version = 'v1'
user_agent = "%s %s" % (name, api_version)

script_version = '0.0.5'


class SnlSession:
    """
        Example usage:

            import snldata

            R = snldata.SnlSession()
            R.search(query="aa-", best=True) #Pick the one with the best rank
            print(R.json)
    """

    PATHS = {
        'snl': 'https://snl.no/api/' + api_version + '/search',
        'nbl': 'https://nbl.snl.no/api/' + api_version + '/search',
        'sml': 'https://sml.snl.no/api/' + api_version + '/search',
        'nkl': 'https://nkl.snl.no/api/' + api_version + '/search',
        'prototyping': 'https://snl.no/.api/prototyping/search',  # UNSTABLE
    }

    QUERYQUAL = {
        0: "Match on article text or part of title",
        1: "The search string is equal to the headword, but the article \
has a further clarification",
        2: "The search string is equal to the article's headword and there \
is no further clarification",
    }

    assertUser = None

    def __init__(
        self,
        requests_timeout=None,
        requests_session=True,
        user_agent=user_agent,
    ):
        """
        Creates a Store Norske Leksikon API client.
        :param requests_timeout:
            Tell Requests to stop waiting for a response after a given
            number of seconds
        :param requests_session:
            A Requests session object or a truthy value to create one.
            A falsy value disables sessions.
            It should generally be a good idea to keep sessions enabled
            for performance reasons.
        :param user_agent
            Tell Requests what program is used in the action
        """
        self.headers = {"User-Agent": user_agent}
        self.requests_timeout = requests_timeout

        if isinstance(requests_session, requests.Session):
            self._S = requests_session
        else:
            if requests_session:  # Build a new session.
                self._S = requests.Session()
            else:  # Use the Requests API module as a "session".
                raise NotImplementedError()

    def __enter__(self):
        return self

    def __dir__(self):
         return self.__dict__.keys()

    def search(self, zone="snl", query="", limit=3, offset=0, best=False):
        """
        @param zone: Website used for the search
        @type zone: str
        @param query: Required. Queries, e.g. "Tog", "Edvard Munch".
            Language: Norwegian
        @type query: str
        @param limit: Not required. Max. number of results, 1-10 are valid
             values, default is 3
        @type limit: int
        @param offset: Not required. Used to display the next "page" with
             results, default is 0, increments with the value you set in limit
        @type offset: int
        @param best: To get the first and best (by rank) result returned.
        @type best: bool
        """
        if (limit > 0 and limit < 11 and zone in self.PATHS and
                offset < limit and query != ""):

            PARAMS = {
                "query": query,
                "limit": limit,
                "offset": offset,
            }

            self._get(PARAMS, zone)

            if best:
                self._get(0)
            else:
                self.simple(zone)
        else:
            raise Exception(
                "Something went wrong with the parametres!"
            )

    def searchV2(self, param: Dict[str, str], zone="snl", best = False) -> Any:
        """
        Dict param: (with "prototyping")
        @param encyclopedia: Begrens søket til angitt leksikon: snl, sml, nbl
            eller nkl. Den samme filtreringen kan også oppnås ved gjøre søket i
            et subdomene.
        @type encyclopedia: str
        @param query: Søketekst, f.eks. "Tog", "Edvard Munch"
        @type query: str
        @param limit: Maksimalt antall resultater. 1-100 er gyldige verdier,
            standard er 10
        @type limit: int
        @param offset: Brukes for paginering av resultatene. Sett for eksempel
            offset=100 for å vise søkeresultater utover de første 100.
        @type offset: int
        @param include_metadata: Metadata inkluderes i søkeresultatene hvis
            dette parameteret settes til true
        @type include_metadata: bool
        @param article_type_id: Filtrer søket til å bare inkludere artikler
            med angitt artikkeltype
        @type article_type_id: int
        @param author_id: Filtrer søket til å bare inkludere artikler av angitt
             forfatter
        @type author_id: int
        @param author_name: Filtrer søket til å bare inkludere artikler av
            forfattere med samsvarende navn
        @type author_name: str
        @param taxonomy_id: Filtrer søket til å bare inkludere artikler i
            angitt taksonomi
        @type taxonomy_id: int
        @param taxonomy_title: Filtrer søket til å bare inkludere artikler i
            taksonomier med samsvarende navn
        @type taxonomy_title: str
        @param tagsonomy_id: Filtrer søket til å bare inkludere artikler i
            angitt tagsonomy
        @type tagsonomy_id: int
        @param tagsonomy_title: Filtrer søket til å bare inkludere artikler i
            tagsonomyer med samsvarende navn
        @type tagsonomy_title: str
        @param char_count_min: Filtrer søket til å bare inkludere artikler med
            angitt antall tegn i artikkelteksten, eller flere
        @type char_count_min: int
        @param char_count_max: Filtrer søket til å bare inkludere artikler med
            angitt antall tegn i artikkelteksten, eller færre
        @type char_count_max: int
        @param media_count_min: Filtrer søket til å bare inkludere artikler med
            angitt antall media-vedlegg, eller flere
        @type media_count_min: int
        @param media_count_max:Filtrer søket til å bare inkludere artikler med
            angitt antall media-vedlegg, eller færre
        @type media_count_max: int
        @param version_count_min: Filtrer søket til å bare inkludere artikler
            med angitt antall historiske versjoner, eller flere
        @type version_count_min: int
        @param version_count_max: Filtrer søket til å bare inkludere artikler
            med angitt antall historiske versjoner, eller færre
        @type version_count_max: int
        @param license_id: Filtrer søket til å bare inkludere artikler med
            angitt lisens-id (free eller restricted)
        @type license_id: str
        @param updated_at_or_after: Filtrer søket til å bare inkludere artikler
            oppdatert på angitt tidspunkt, eller senere.
            Tidspunktet angis i RFC3339-format.
        @type updated_at_or_after: str (RFC3339 format)
        @param updated_at_or_before: Filtrer søket til å bare inkludere
            artikler oppdatert på angitt tidspunkt, eller tidligere.
            Tidspunktet angis i RFC3339-format.
        @type updated_at_or_before: str (RFC3339 format)
        @param zone: Website used for the search
        @type zone: str
        @param best: To get the first and best (by query_match_quality)
            result returned.
        @type best: bool
        """
        if (param['limit'] > 0 and param['limit'] < 101 and param['offset'] <
                param['limit'] and param['query'] != "" and
                zone in self.PATHS):

            self._get(param, zone)

            if best:
                self._get(0)
            else:
                self.simple(zone)
        else:
            raise Exception(
                "Something went wrong with the parametres!"
            )

    def _get(self, data, zone=""):
        """
        API GET
        @param data: parametres to be used or key in dict
        @type data: dict/int
        @param zone: Website used for the search
        @type zone: str
        """
        if isinstance(data, int) and isinstance(self.json, list):
            R = self._S.get(
                self.json[data]["article_url_json"], headers=self.headers)
        elif not isinstance(data, int):
            R = self._S.get(
                self.PATHS[zone.lower()], params=data, headers=self.headers)
        else:
            raise NotImplementedError

        if R.status_code != 200:
            raise Exception(
                "GET was unsuccessfull ({}): {}".format(R.status_code, R.text)
            )

        if hasattr(self, 'title'):
            self.delete_var()

        self.json = R.json()

        if not zone:
            self.store_var()

    def simple(self, zone=""):
        """
        Adds a entry to JSON file
        @param zone: Website used for the search (different for "prototyping")
        @type zone: str
        """
        i = 0
        for result in self.json:
            if zone == 'prototyping':
                self.json[i].update(
                    {'query_quality_explain':
                        self.QUERYQUAL[result['query_match_quality']]})
            else:
                sentence = re.search(
                    r'^(.*?(?<!\b\w)[.?!])\s+[A-Z0-9]',
                    result["first_two_sentences"], flags=0)
                if isinstance(sentence, type(None)):
                    # Regex did not work
                    self.json[i].update(
                        {'simple': '{}. {} (rank {}): {}'.format(
                            i, result["headword"], round(result["rank"], 1),
                            result["first_two_sentences"])})
                else:
                    # Regex worked
                    self.json[i].update({
                        'simple': '{}. {} (rank {}): {}'.format(
                            i, result["headword"], round(result["rank"], 1),
                            sentence.group(1))})
            i += 1

    def store_var(self):
        """
        Local storage for easy grabbing of data
        """
        for key in self.json:
            if isinstance(self.json[key], dict):
                for key2 in self.json[key]:
                    setattr(self, key2, self.json[key][key2])
            else:
                setattr(self, key, self.json[key])

    def delete_var(self):
        """
        Remove local storage attributes
        """
        for key in self.json:
            if isinstance(self.json[key], dict):
                for key2 in self.json[key]:
                    delattr(self, key2)
            else:
                delattr(self, key)

    def close(self):
        self._S.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
