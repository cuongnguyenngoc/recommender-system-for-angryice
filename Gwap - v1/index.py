
describers = {1: {"img1": {"d1": "des1"}, "img2": {"d2": "des2"}}, 2: {"img1": {"d3": "des3"}, "img2": {"d4": "des4"}}}
a = 3
b = "img1"
describers[a] = {b: {"d5": "des5"}, "img2": {"d6": "des6"}}
des = {}
for v in describers.values():
    for i in v.values():
        des.update(i)


for i, k in des.items():
    print(i + ":" + k)