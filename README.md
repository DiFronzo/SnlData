[![Documentation Status](https://readthedocs.org/projects/snldata/badge/?version=latest)](https://snldata.readthedocs.io/en/latest/?badge=latest)

# SnlData

##### A light weight Python library for the Store norske leksikon API

## Documentation

UNDER CONSTRUCTION

## Installation

    pip install snldata

## Quick Start

### Query
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
<index in the file> <title> (rank <rank id>): <first sentence>
```
Pick the article you want from the example above: (this will maybe change in the future)
```python
R._getSpecific(R.json[1]["article_url_json"])
print(R.title)
```
Outputs: `Spellemannprisen`

## Reporting Issues

If you have suggestions, bugs or other issues specific to this library, file them [here](https://github.com/DiFronzo/SnlData/issues). Or just send me a pull request.
