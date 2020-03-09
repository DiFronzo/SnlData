<p align="center">
  <a href="https://github.com/DiFronzo/snldata"><img alt="Logo" width="500" height="300" src="https://snldata.readthedocs.io/en/latest/_static/snldata_logo.svg"></a>
</p>
<p align="center">
  <a href="https://github.com/DiFronzo/snldata/actions"><img alt="Actions Status" src="https://github.com/DiFronzo/SnlData/workflows/Test/badge.svg"></a>
  <a href="https://snldata.readthedocs.io/en/latest/?badge=latest"><img alt="Documentation Status" src="https://readthedocs.org/projects/snldata/badge/?version=latest"></a>
<a href="https://app.fossa.io/projects/git%2Bgithub.com%2FDiFronzo%2FSnlData?ref=badge_shield" alt="FOSSA Status"><img src="https://app.fossa.io/api/projects/git%2Bgithub.com%2FDiFronzo%2FSnlData.svg?type=shield"/></a>
  <a href="https://codecov.io/gh/DiFronzo/SnlData"><img alt="Coverage Status" src="https://codecov.io/gh/DiFronzo/SnlData/branch/master/graph/badge.svg"></a>
  <a href="https://travis-ci.com/DiFronzo/SnlData"><img alt="Build Status" src="https://api.travis-ci.com/DiFronzo/SnlData.svg?branch=master"></a>	
  <a href="https://github.com/DiFronzo/SnlData/blob/master/LICENSE"><img alt="License: MIT" src="https://snldata.readthedocs.io/en/latest/_static/license.svg"></a>
  <a href="https://pepy.tech/project/snldata"><img alt="Downloads" src="https://pepy.tech/badge/snldata"></a>
  <a href="https://pypi.org/project/snldata/"><img alt="PyPI" src="https://img.shields.io/pypi/v/snldata"></a>
  <h4>A lightweight Python library for Store norske leksikon APIs</h4>
</p>

## Installation

    pip install snldata

## Quick Start
Raw JSON
```python
import snldata

R = snldata.SnlSession()
R.search(query="fortolket programmeringsspråk", best=True) #Pick the one with the best rank
print(R.json)

```
Outputs: the JSON object
```
{
	"title": "fortolket programmeringsspråk",
	"url": "http://snl.no/fortolket_programmeringsspr%C3%A5k",
	"subject_url": "http://snl.no/.taxonomy/3689",
	"subject_title": "Programmering",
	"xhtml_body": "\u003cdiv\u003e\r\n\u003cp\u003eprogrammeringsspråk som ikke blir kompilert til objekt- eller maskinkode, men fortolket av et eget program på vertsmaskinen.\u003c/p\u003e\r\n\u003cp\u003eFordelen med slike språk er at man kan lage programmer som kan gjøre på mange forskjellige \u003ca class=\"crossref\" href=\"https://snl.no/datamaskin\"\u003edatamaskiner\u003c/a\u003e og \u003ca class=\"crossref\" href=\"https://snl.no/operativsystem\"\u003eoperativsystemer\u003c/a\u003e uten å skreddersy dem for hver enkelt plattform.\u003c/p\u003e\r\n\u003cp\u003eEksempler på fortolkede språk:\u003c/p\u003e\r\n\u003cul\u003e\r\n\u003cli\u003e\u003ca class=\"crossref\" href=\"https://snl.no/Python_-_programmeringsspr%C3%A5k\"\u003ePython\u003c/a\u003e\u003c/li\u003e\r\n\u003cli\u003eJavascript\u003c/li\u003e\r\n\u003cli\u003e\u003ca class=\"crossref\" href=\"https://snl.no/Perl_-_IT\"\u003ePHP\u003c/a\u003e\u003c/li\u003e\r\n\u003cli\u003e\u003ca class=\"crossref\" href=\"https://snl.no/Perl_-_IT\"\u003ePerl\u003c/a\u003e\u003c/li\u003e\r\n\u003c/ul\u003e\r\n\u003c/div\u003e",
	"created_at": "2017-12-12T10:34:18.189+01:00",
	"changed_at": "2017-12-12T10:38:37.626+01:00",
	"license_name": "fri",
	"metadata_license_name": "fri",
	"metadata": {
		"lastname": "",
		"firstname": ""
	},
	"authors": [{
		"full_name": "Henrik Dvergsdal"
	}],
	"images": []
}
```
## Licenses for content from Store norske leksikon
| Licence | Description | Read more
| --- | --- | --- |
| `fri` | [Creative Commons](https://creativecommons.org/) **[CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0/)** license. Everyone is allowed to **share, use, copy and adapt** the text as long as **the author and Store norske leksikon** continues to be credited and the article retains the same free license for further use. | [Meta](https://meta.snl.no/fri_gjenbruk)
| `begrenset gjenbruk` | You **can't reuse, republish, or adapt** the article without first obtaining the author's permission.| [Meta](https://meta.snl.no/begrenset_gjenbruk)

## Overview of sites/zones
|     code    |       Website       |   Note 
| --- | --- | --- |
|     `snl`     |   https://snl.no/   | Default
|     `nbl`     | https://nbl.snl.no/ |        
|     `sml`     | https://sml.snl.no/ |        
|     `nkl`     | https://nkl.snl.no/ |        
| `prototyping` |          -          | Unstable

## Query
### Easy Query
- Main documentation: [API-dokumentasjon](https://meta.snl.no/API-dokumentasjon)

```python
import snldata

R = snldata.SnlSession()
R.search(query="Ole Ivars", best=True) #Pick the one with the best rank
print(R.url)

```
Outputs: `https://snl.no/Ole_Ivars`

```python
import snldata

R = snldata.SnlSession()
R.search(query="Ole Ivars") #Pick the three best results
for val in R.json:
    print(val["simple"] #Summery for each index

```
Outputs: 
```
0. Ole Ivars (rank 576.6): Ole Ivars er et norsk danseband fra Hamar.
1. Spellemannprisen (rank 25.9): Spellemannprisen er den norske platebransjens årlige prisutdeling for å stimulere og markere plateproduksjonen i Norge.
2. danseband (rank 25.1): Danseband, ensemble som spiller til dans, betegner i dag vanligvis en instrumentbesetning som i pop og rock (vokal, elektrisk gitar og bass, keyboards, trommer, eventuelt også saksofon eller andre blåsere).
###Explaining of the values:
<index of the json file> <title> (rank <rank id>): <first sentence>
```
Pick the article you want from the example above:
```python
R._get(1)
print(R.title)
```
Outputs: `Spellemannprisen`

### Advance Query (best for prototyping api)
- Main documentation: [API-dokumentasjon - prototyping](https://meta.snl.no/API-dokumentasjon_-_prototyping)

```python
import snldata

R = snldata.SnlSession()
R.searchV2({"encyclopedia": "snl", "query": "dr. dre", "limit": 3, "offset": 0 }, zone="prototyping", best=True)
print(R.title)

```
Outputs: `Dr. Dre`

```python
import snldata

R = snldata.SnlSession()
R.searchV2({"encyclopedia": "snl", "query": "dr. dre", "limit": 3, "offset": 0 }, zone="prototyping")
i = 0
for val in R.json:
    print('{}. {}: {}'.format(i, val['headword'], val["query_quality_explain"]))
    i += 1

```
Outputs:
```
0. Dr. Dre: The search string is equal to the article's headword and there is no further clarification
1. hiphop: Match on article text or part of title
2. Eminem: Match on article text or part of title
###Explaining of the values: (the prototyping api allows you to send a lot of parametres)
<index of the json file> <title>: <rank as text>
```
Pick the article you want from the example above:
```python
R._get(1)
print("Title: {}, Created: {}".format(R.title, R.created_at))
```
Outputs: `Title: hiphop, Created: 2009-02-14T05:15:20.546+01:00`

<sup>All of the examples uses text that is [CC-BY-SA-3.0](https://creativecommons.org/licenses/by-sa/3.0). By at least one of the following authors: Henrik Dvergsdal, Jon Vidar Bergan, and Audun Kjus Aahlin. Read more about the license: [fri gjenbruk](https://meta.snl.no/fri_gjenbruk).</sup>

## To-do
- [ ] Fully support taxonomy

## Reporting Issues

If you have suggestions, bugs or other issues specific to this library, file them [here](https://github.com/DiFronzo/SnlData/issues). Or just send me a pull request.
