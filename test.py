# import json
# from pprint import pprint

# with open('result.json') as fp:
#     _json = fp.read()

# pars_by_page = json.loads(_json)

# pprint(
#     list(enumerate(pars_by_page))
# )


import pandas as pd

s = pd.DataFrame([
    (1, 'asffas', [124,124,124])
])

s.to_csv('test.csv', header=False)
