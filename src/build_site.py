"""Build standalone, dependency-free editorial case study from the validated dataset."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'data/analysis.json').read_text())
safe=json.dumps(data).replace('<','\\u003c')
template=(ROOT/'site-template.html').read_text()
page=template.replace('/*__PAYLOAD__*/',safe)
(ROOT/'index.html').write_text(page,encoding='utf-8')
print('Built index.html')