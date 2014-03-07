import PlcStructre;

dt = PlcStructre.PlcDataType('pair');
dt.setData(
{'a2': [False, False, True, True, True, True, True, True, True, True],
 'lc': {'alt': {'al': 1, 'ti': 2}, 'temp': {'C': 1, 'F': 3}}})

assert(dt.lc.alt.al ==1)


dt.setByStringAddress('lc.alt.al',5)
assert(dt.getByStringAddress('lc.alt.al') ==5)
