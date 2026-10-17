"""Build data/layers.json from the reusable variety layers (Phase 2, Oct 16, 2026).
Source of truth: /workspace/familygem/listings/variety-layers/<variety>.md (KB-cited there). Run after editing those files."""
import re, json, pathlib
SRC=pathlib.Path('/workspace/familygem/listings/variety-layers')
out={}
for f in sorted(SRC.glob('*.md')):
    t=f.read_text(); body=re.search(r'<!-- layer -->(.*?)<!-- /layer -->',t,re.S).group(1)
    secs=[]
    for m in re.finditer(r'### (.+?)\n(.*?)(?=\n### |\Z)',body,re.S):
        secs.append({'h':m.group(1).strip(),'items':[l[2:].strip() for l in m.group(2).splitlines() if l.startswith('- ')]})
    colors={}
    for m in re.finditer(r'^- (\w+) \([^)]*\): "(.+)"$',t,re.M): colors[m.group(1)]=m.group(2)
    out[f.stem]={'sections':secs,'colors':colors}
bad=re.compile(r'\b(natural|untreated|certified|paraiba|lagoon|rubellite|verdelite|indicolite|watermelon|tiffany|colour)\b',re.I)
for k,v in out.items():
    for s in v['sections']:
        for i in s['items']+[s['h']]:
            assert not bad.search(i), (k,i)
p=pathlib.Path(__file__).resolve().parent.parent/'data'/'layers.json'
p.write_text(json.dumps(out,indent=1,ensure_ascii=False)); print('wrote',p,{k:[len(s['items']) for s in v['sections']] for k,v in out.items()})
