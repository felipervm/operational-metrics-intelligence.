"""Render a standalone, reproducible editorial case with local assets."""
import base64
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def data_uri(path,mime):
    return f'data:{mime};base64,'+base64.b64encode(path.read_bytes()).decode('ascii')

def json_script(data):
    return json.dumps(data,ensure_ascii=True).replace('<','\\u003c')

def render(data):
    template=(ROOT/'site-template.html').read_text(encoding='utf-8')
    fonts=''.join("@font-face{font-family:Poppins;font-style:normal;font-weight:"+str(weight)+";font-display:swap;src:url("+data_uri(ROOT/f'site/assets/fonts/poppins-{weight}.woff2','font/woff2')+") format('woff2')}" for weight in [400,500,600,700])
    replacements={
      '/*__PAYLOAD__*/':json_script(data),
      '/*__STYLES__*/':fonts+(ROOT/'site/styles.css').read_text(encoding='utf-8'),
      '/*__APP__*/':(ROOT/'site/app.js').read_text(encoding='utf-8'),
      '/*__HERO_IMAGE__*/':data_uri(ROOT/'site/assets/decision-lens.jpg','image/jpeg'),
      '/*__PORTRAIT__*/':data_uri(ROOT/'site/assets/felipe-mattos.jpg','image/jpeg'),
    }
    for token,value in replacements.items():
        if template.count(token)!=1:
            raise ValueError(f'Expected one presentation token: {token}')
        template=template.replace(token,value)
    return template

def main():
    data=json.loads((ROOT/'data/analysis.json').read_text(encoding='utf-8'))
    (ROOT/'index.html').write_bytes(render(data).encode('utf-8'))
    print('Built standalone index.html from validated data and local assets')

if __name__=='__main__':main()
