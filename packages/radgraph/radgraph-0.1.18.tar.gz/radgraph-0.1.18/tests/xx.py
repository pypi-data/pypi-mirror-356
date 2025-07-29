from radgraph import RadGraph, F1RadGraph
from tqdm import tqdm

rg = RadGraph(model_type="modern-radgraph-xl")


import json
import os

expected_path = os.path.join(os.path.dirname(__file__), 'chexbert_test_set.json')

with open(expected_path, "r") as f:
    data = json.load(f)

l = []

for k,v in tqdm(data.items()):
    out = rg([v])
    l.append(out)

with open("chexbert_test_set_modern_radgraph_xl.json", "w") as f:
    json.dump(l, f)