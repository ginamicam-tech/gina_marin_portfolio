#!/usr/bin/env python3
"""Build a curated PDF from project portfolio_pdf metadata and portfolio/outline.yml.
Dependencies: reportlab, Pillow, PyYAML, pypdf. No network access required.
"""
from pathlib import Path
import argparse, io, re, html, os
import yaml
from PIL import Image, ImageOps
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
W,H=842,595
INK='#1b2426'; MUTED='#596365'; LINE='#cbd1cc'; PAPER='#f8f7f3'; ACCENT='#485e54'

def read_project(p): return yaml.safe_load(p.read_text().split('---',2)[1])
def plain(s):
 s=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',str(s))
 return s.replace('**','').replace('*','').replace('—','-').replace('–','-').replace('\u2011','-')
def xml(s): return html.escape(plain(s))

def font_dir():
 candidates=[os.environ.get('PORTFOLIO_FONT_DIR',''),'/usr/share/fonts/truetype/dejavu',str(Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype')]
 for directory in candidates:
  if directory and (Path(directory)/'DejaVuSans.ttf').exists():return Path(directory)
 raise RuntimeError('Set PORTFOLIO_FONT_DIR to a directory containing DejaVuSans.ttf, DejaVuSans-Bold.ttf and DejaVuSerif.ttf')

class Portfolio:
 def __init__(self,config,output):
  self.config=config;self.output=output;self.page=0;self.cache={};self.manifest=[]
  fonts=font_dir()
  for name,file in [('Sans','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Serif','DejaVuSerif.ttf')]:pdfmetrics.registerFont(TTFont(name,str(fonts/file)))
  self.c=canvas.Canvas(str(output),pagesize=(W,H),pageCompression=1)
  self.c.setTitle('Gina Marín | '+config['edition']);self.c.setAuthor('Gina Marín');self.c.setSubject('Art & Research; Projects & Production; Design & Communication')
 def text(self,s,x,y,width,size=11,font='Sans',color=INK,leading=None,maxheight=None):
  p=Paragraph(xml(s).replace('\n','<br/>'),ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.43,textColor=color))
  _,h=p.wrap(width,1000)
  if maxheight is not None and h>maxheight:raise ValueError(f'Text overflow on page {self.page}: {h}>{maxheight}: {s[:80]}')
  if y-h<15:raise ValueError(f'Text below margin on page {self.page}: {s[:80]}')
  p.drawOn(self.c,x,y-h);return y-h
 def start(self,label,bookmark=None):
  self.page+=1;self.c.setFillColor(PAPER);self.c.rect(0,0,W,H,fill=1,stroke=0)
  self.text('GINA MARÍN',36,H-25,200,8,font='Bold',color=MUTED)
  self.text(label.upper(),300,H-25,505,8,color=MUTED)
  self.c.setStrokeColor(LINE);self.c.line(36,43,W-36,43)
  self.text('Art, research & shared practice',36,33,400,7.5,color=MUTED)
  self.c.setFont('Sans',8);self.c.setFillColor(MUTED);self.c.drawRightString(W-36,22,f'{self.page:02}')
  if bookmark:self.c.bookmarkPage(bookmark)
 def done(self):self.c.showPage()
 def image(self,src,x,y,w,h):
  path=ROOT/src.lstrip('/')
  if not path.is_file():raise FileNotFoundError(path)
  if src not in self.cache:
   im=ImageOps.exif_transpose(Image.open(path)).convert('RGB');im.thumbnail((1400,1400))
   b=io.BytesIO();im.save(b,'JPEG',quality=76,optimize=True);b.seek(0);self.cache[src]=(ImageReader(b),im.size)
  reader,(iw,ih)=self.cache[src];scale=min(w/iw,h/ih);dw,dh=iw*scale,ih*scale
  self.c.drawImage(reader,x+(w-dw)/2,y+(h-dh)/2,dw,dh,mask='auto')
 def link(self,label,url,x,y,width=220):
  self.text(label,x,y,width,9,font='Bold',color=ACCENT)
  self.c.linkURL(url,(x,y-14,x+width,y+2),relative=0,thickness=0)
 def cover(self):
  self.start('Portfolio')
  self.text('Gina\nMarín',40,465,330,54,leading=59)
  self.text(self.config['subtitle'],43,300,290,20,font='Serif',leading=28)
  self.text(self.config['edition'],43,196,290,10,color=MUTED)
  self.text(self.config['location'],43,173,290,10,color=MUTED)
  self.link(self.config['email'],'mailto:'+self.config['email'],43,120)
  self.link('Full online portfolio ↗',self.config['website']+'/work/',43,96)
  self.image(self.config['cover_image'],380,110,423,420)
  self.text(self.config['cover_caption'],380,88,423,8,color=MUTED,maxheight=35)
  self.done()
 def contents(self,sections):
  self.start('A practice in dialogue','contents');self.c.addOutlineEntry('Contents','contents',0)
  self.text('A practice in dialogue',36,520,750,32)
  self.text(self.config['intro'],36,465,730,12,font='Serif',maxheight=85)
  for n,(section,entries,start) in enumerate(sections):
   x=36+n*260
   self.text(f'0{n+1} / {section["title"]}',x,340,244,15,font='Bold',maxheight=45)
   y=287
   # Compact, two-column art index keeps every project addressable without tiny type.
   columns=2 if len(entries)>14 else 1; cw=118 if columns==2 else 244
   split=(len(entries)+columns-1)//columns
   for j,d in enumerate(entries):
    col=j//split; row=j%split
    title=d['portfolio_pdf'].get('short_title',d['title'])
    title={'They Do Not Save Life, Nor Sustain the Soul':'They Do Not Save Life…','The Revolution of Sovereign Skin Politics':'Sovereign Skin Politics','Women and LGTBIQ+ Altar #LivesInStruggle':'Women and LGTBIQ+ Altar','Trifolium / Impact Festival':'Trifolium / Impact','Trace at The Great Glass':'Trace / The Great Glass','Rituals of Collective Descent':'Rituals of Collective Descent','Ribben: The Resonance Circle':'Ribben'}.get(title,title)
    yy=y-row*19
    # Use a measured single-line abbreviation only in index; full titles on project pages.
    maxw=cw-23; label=title
    while pdfmetrics.stringWidth(label,'Sans',7.3)>maxw:label=label[:-2].rstrip('…')+'…'
    self.text(label,x+col*(cw+8),yy,maxw,7.3)
    self.text(str(start+1+j),x+col*(cw+8)+maxw+4,yy,19,7.3,color=MUTED)
    self.c.linkRect('',d['key'],(x+col*(cw+8),yy-15,x+col*(cw+8)+cw,yy+2),relative=0,thickness=0)
   self.c.linkRect('',section['id'],(x,300,x+244,340),relative=0,thickness=0)
  self.done()
 def divider(self,index,section,description,entries):
  self.start(section['title'],section['id']);self.c.addOutlineEntry(section['title'],section['id'],0)
  self.text(f'0{index}',36,510,220,70,color=ACCENT)
  self.text(section['title'],36,385,315,34,leading=42)
  self.text(f'{len(entries)} projects',36,230,250,11,color=MUTED)
  y=480
  for para in description.split('\n\n'):
   y=self.text(para,390,y,410,13,font='Serif',maxheight=200)-22
  self.done()
 def project(self,section,d):
  p=d['portfolio_pdf'];self.start(section['title'],d['key']);self.c.addOutlineEntry(d['title'],d['key'],1)
  y=self.text(d['title'],36,520,240,23,leading=28,maxheight=140)-14
  years=str(d['year']) if d.get('year_start',d['year'])==d['year'] else f"{d['year_start']}-{d['year']}"
  y=self.text(d.get('context') or d.get('listing_context') or years,36,y,240,9,color=MUTED,maxheight=60)-13
  y=self.text(d.get('role') or 'Artist',36,y,240,9,font='Bold',maxheight=55)-18
  y=self.text(p['summary'],36,y,240,10.4,font='Serif',leading=15.2,maxheight=y-88)
  url=self.config['website']+d['permalink']
  self.link('View full project & documentation ↗',url,36,74,245)
  ims=p['images'];assert 1<=len(ims)<=3
  x=304;rw=502;bottom=170;top=520;rh=top-bottom
  aspects=[Image.open(ROOT/m['src'].lstrip('/')).width/Image.open(ROOT/m['src'].lstrip('/')).height for m in ims]
  side=len(ims)>1 and (sum(aspects)/len(aspects)<1.3 or d['type']=='series')
  for i,m in enumerate(ims):
   if side:
    bw=(rw-14*(len(ims)-1))/len(ims);bx=x+i*(bw+14);by=bottom;bh=rh
   else:
    bh=(rh-38*(len(ims)-1))/len(ims);bw=rw;bx=x;by=top-(i+1)*bh-i*38
   self.image(m['src'],bx,by,bw,bh)
   cap=m.get('caption','')
   self.text(cap,bx,by-6,bw,7.5,color=MUTED,leading=10,maxheight=34)
  credit=p.get('credits','')
  if credit:self.text(credit,x,104,rw,7.6,color=MUTED,leading=10.5,maxheight=55)
  self.manifest.append({'key':d['key'],'page':self.page,'category':section['id'],'images':[m['src'] for m in ims],'url':url})
  self.done()
 def cv(self):
  self.start('Background & contact','cv');self.c.addOutlineEntry('Background & contact','cv',0)
  self.text('Background & contact',36,520,770,32)
  cv=self.config['cv'];y=455
  self.text('EDUCATION',36,y,330,10,font='Bold');y-=30
  for s in cv['education']:y=self.text(s,36,y,330,11,maxheight=65)-18
  y-=8;self.text('PRACTICE & TOOLS',36,y,330,10,font='Bold');y-=25
  y=self.text(cv['skills'],36,y,330,10.5,maxheight=120)-18
  self.text(cv['languages'],36,y,330,10,maxheight=65)
  y=455;self.text('SELECTED EXPERIENCE',420,y,385,10,font='Bold');y-=30
  for s in cv['experience']:y=self.text(s,420,y,385,10.5,maxheight=55)-15
  self.link(self.config['email'],'mailto:'+self.config['email'],420,136)
  self.text(self.config['phone']+' | '+self.config['location'],420,112,385,10)
  self.link('Full CV & online archive ↗',self.config['website']+'/cv/',420,84)
  self.done()

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--outline',default='portfolio/outline.yml');parser.add_argument('--output',default='output/pdf/gina-marin-portfolio.pdf');args=parser.parse_args()
 config=yaml.safe_load((ROOT/args.outline).read_text());projects={d['key']:d for d in map(read_project,(ROOT/'content/_work').glob('*.md'))}
 filters={d['id']:d for d in yaml.safe_load((ROOT/'content/_data/work_filters.yml').read_text())}
 sections=[];seen=set();start=3
 for s in config['sections']:
  entries=[]
  for item in s['projects']:
   if not item.get('include',True):continue
   key=item['key']
   if key in seen:raise ValueError(f'Duplicate project: {key}')
   seen.add(key);d=projects[key];assert d.get('portfolio_pdf'),key
   entries.append(d)
  if entries:sections.append((s,entries,start));start+=len(entries)+1
 out=ROOT/args.output;out.parent.mkdir(parents=True,exist_ok=True)
 b=Portfolio(config,out);b.cover();b.contents(sections)
 for i,(s,entries,_) in enumerate(sections,1):
  b.divider(i,s,filters[s['id']]['description'],entries)
  for d in entries:b.project(s,d)
 b.cv();b.c.save()
 reader=PdfReader(out);assert len(reader.pages)==len(seen)+len(sections)+3
 for item in b.manifest:
  text=reader.pages[item['page']-1].extract_text();assert plain(projects[item['key']]['title']) in plain(text).replace('\n',' '),item['key']
 (out.parent/'portfolio-manifest.yml').write_text(yaml.safe_dump({'pages':len(reader.pages),'projects':b.manifest},allow_unicode=True,sort_keys=False))
 print(f'{out}\n{len(reader.pages)} pages | {len(seen)} unique projects | {out.stat().st_size/1024/1024:.1f} MB')
if __name__=='__main__':main()
