<p align="center">
  <img width="500" height="300" src="https://github.com/DiFronzo/SnlData/blob/master/docs/_static/snldata_logo.svg">
</p>
<p align="center">
  <a href="https://github.com/DiFronzo/snldata/actions"><img alt="Actions Status" src="https://github.com/DiFronzo/SnlData/workflows/Test/badge.svg"></a>
  <a href="https://snldata.readthedocs.io/en/latest/?badge=latest"><img alt="Documentation Status" src="https://readthedocs.org/projects/snldata/badge/?version=latest"></a>
  <a href="https://coveralls.io/github/psf/snldata?branch=master"><img alt="Coverage Status" src="https://coveralls.io/repos/github/psf/snldata/badge.svg?branch=master"></a>
  <a href="https://github.com/DiFronzo/SnlData/blob/master/LICENSE"><img alt="License: MIT" src="https://github.com/DiFronzo/SnlData/blob/master/docs/_static/license.svg"></a>
  <a href="https://pypi.org/project/snldata/"><img alt="PyPI" src="https://img.shields.io/pypi/v/snldata"></a>
</p>

##### A light weight Python library for the Store norske leksikon API

## Documentation

UNDER CONSTRUCTION

## Installation

    pip install snldata

## Quick Start
Raw JSON
```python
import snldata

R = snldata.SnlSession()
R.search(query="aa-", best=True) #Pick the one with the best rank
print(R.json)

```
Outputs: the JSON object
```
{
	"title": "aa-",
	"url": "http://snl.no/aa-",
	"subject_url": "http://snl.no/.taxonomy/3959",
	"subject_title": "Prefikser og suffikser",
	"xhtml_body": "\u003cdiv\u003e\u003cp\u003efor ord som uttales \u003cem\u003ea-\u003c/em\u003e, se også ord på a-.\u003c/p\u003e\u003c/div\u003e\n",
	"created_at": "2009-02-14T00:11:33.711+01:00",
	"changed_at": "2015-11-19T21:18:52.285+01:00",
	"license_name": "begrenset",
	"metadata_license_name": "fri",
	"metadata": {
		"author": "1660",
		"subject": "253",
		"headword": "aa-",
		"article_type": "general",
		"is_authorized": "1"
	},
	"authors": [{
		"full_name": "Store norske leksikon (2005 - 2007)"
	}],
	"images": []
}
```
## Overview of sites/zones
|     code    |       Website       |   Note  |
|:-----------:|:-------------------:|:-------:|
|     snl     |   https://snl.no/   | Default |
|     nbl     | https://nbl.snl.no/ |         |
|     sml     | https://sml.snl.no/ |         |
|     nkl     | https://nkl.snl.no/ |         |
| prototyping |          -          | Unstable |
### Easy Query
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
0. Dr. Dre: Søkestrengen er lik artikkelens tittel (headword) og det er ingen ytterligere presisering (clarification)
1. hiphop: Treff på artikkeltekst eller deler av tittel
2. Eminem: Treff på artikkeltekst eller deler av tittel
###Explaining of the values: (the prototyping api allows you to send a lot of parametres)
<index of the json file> <title>: <rank as text>
```
Pick the article you want from the example above:
```python
R._get(1)
print("Title: {}, Created: {}".format(R.title, R.created_at))
```
Outputs: `Title: hiphop, Created: 2009-02-14T05:15:20.546+01:00`

## To-do
- [ ] Fully support taxonomy

## Reporting Issues

If you have suggestions, bugs or other issues specific to this library, file them [here](https://github.com/DiFronzo/SnlData/issues). Or just send me a pull request.
