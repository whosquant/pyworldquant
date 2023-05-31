<h1 align="center">PyWorldQuant by whosquant</h1>
<div align="center">
  <img src="https://img.shields.io/readthedocs/pyworldquant/latest?style=for-the-badge" />
  <img src="https://img.shields.io/github/license/whosquant/pyworldquant?style=for-the-badge" />
  <img src="https://img.shields.io/pypi/v/pyworldquant?style=for-the-badge" />
  <img src="https://img.shields.io/github/last-commit/whosquant/pyworldquant?style=for-the-badge" />
</div>
<br>
<div align="center">
  <p>A helper for WorldQuant Brain Consultant to automatically submit alpha factors in the <a href="https://platform.worldquantbrain.com/">WorldQuant Brain</a>.</p>
  <img src="https://platform.worldquantbrain.com/share-logo.png" />
</div>




## Documentation

- **[Quick start guide 🚀](./docs/GETTING-STARTED.md)**
- **[Official API documention 📡](https://platform.worldquantbrain.com/learn/documentation/consultant-information/brain-api)**

## Brief WorkFlow
### alpha workfow
![insample](./doc/c1.png)

### Brain Platform workflow
![insample](./doc/c2.png)

## Installation
 [PyPI](https://pypi.org/project/pyworldquant/) (stable, recommended):
 
```pip install pyworldquant```

## Example
```python
from pyworldquant.spot import Spot as Client
username = 'xxxxx@xxx.com'
password = 'xxxxxxx'
# login
client = Client(username, password)

settings = {'name': 'USA3000',
              'settings': {"nanHandling": "ON", "instrumentType": "EQUITY", "delay": 1, "universe": "TOP3000",
                           "truncation": 0.05, "unitHandling": "VERIFY", "pasteurization": "ON", "region": "USA",
                           "language": "FASTEXPR", "decay": 10, "neutralization": "INDUSTRY", "visualization": False}}
regular = 'close'
# simulate
performance = client.simulate(regular,settings)
print(performance)
# Example output: {"LOW_SHARPE": , "LOW_FITNESS": , "HIGH_TURNOVER": , "LOW_SUB_UNIVERSE_SHARPE": }
```


## To be continued
1,work on how to make the alphapool more effective.
2,work on how to maker better use of the given dataset to formulate better alpha.

## Issue
 If you found a bug or have a question, please open an issue. Email will also be replied.
  
## Warning
 pulling too much requests is dangerous. Never leave your ineffective crawler running on server.

## Contributing
 Pull requests (docs, bug fix, features) are welcomed! Any pull request (documentation, bug fix, features, etc) are welcomed.

