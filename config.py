username = ''
key = ''

settings1 = {'name': '1',
              'settings': {"nanHandling": "ON", "instrumentType": "EQUITY", "delay": 1, "universe": "TOP3000",
                           "truncation": 0.03, "unitHandling": "VERIFY", "pasteurization": "ON", "region": "USA",
                           "language": "FASTEXPR", "decay": 3, "neutralization": "INDUSTRY", "visualization": False}}
settings2 = {'name': '2',
              'settings': {"nanHandling": "ON", "instrumentType": "EQUITY", "delay": 1, "universe": "TOP3000",
                           "truncation": 0.04, "unitHandling": "VERIFY", "pasteurization": "ON", "region": "USA",
                           "language": "FASTEXPR", "decay": 3, "neutralization": "INDUSTRY", "visualization": False}}
settings3 = {'name': '3',
              'settings': {"nanHandling": "ON", "instrumentType": "EQUITY", "delay": 1, "universe": "TOP1200",
                           "truncation": 0.02, "unitHandling": "VERIFY", "pasteurization": "ON", "region": "EUR",
                           "language": "FASTEXPR", "decay": 3, "neutralization": "SUBINDUSTRY", "visualization": False}}
settings4 = {'name': '4',
              'settings': {"nanHandling": "ON", "instrumentType": "EQUITY", "delay": 1, "universe": "TOP3000",
                           "truncation": 0.01, "unitHandling": "VERIFY", "pasteurization": "ON", "region": "USA",
                           "language": "FASTEXPR", "decay": 17, "neutralization": "SUBINDUSTRY", "visualization": False}}
settings5 = {'name': '5',
              'settings': {"nanHandling": "ON", "instrumentType": "EQUITY", "delay": 1, "universe": "TOP3000",
                           "truncation": 0.01, "unitHandling": "VERIFY", "pasteurization": "ON", "region": "USA",
                           "language": "FASTEXPR", "decay":17, "neutralization": "INDUSTRY", "visualization": False}}
settingslist = [settings1,settings2,settings3,settings4,settings5]