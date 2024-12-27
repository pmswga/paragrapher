# import json
# from pprint import pprint

# with open('result.json') as fp:
#     _json = fp.read()

# pars_by_page = json.loads(_json)

# pprint(
#     list(enumerate(pars_by_page))
# )


def compare_list(a: list, b: list) -> list:
    return [x for x in a + b if x not in a or x not in b]


res = compare_list(
    ['a', 'b'],
    ['b', 'c']
)

print(res)
