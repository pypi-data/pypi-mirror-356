import curl_cffi as c
import re,random,time
from base64 import b64decode as d,b64encode as e
from urllib.parse import urlparse as p,urlunparse,parse_qs,urlencode
from typing import Dict,List,Optional,Any,Tuple
from dataclasses import dataclass
from functools import wraps
S=[{"id":146,"url":"https://146.19.24.89/__cp2.php","name":"mevSpaceWarsawE"},{"id":181,"url":"https://208.87.240.35/__cp2.php","name":"psychzLosAngeles2F"},{"id":63,"url":"https://108.181.43.67/__cp2.php","name":"psychzLosAngelesN"},{"id":200,"url":"https://108.181.11.137/__cp2.php","name":"psychzLosAngeles2L"},{"id":149,"url":"https://195.3.222.15/__cp2.php","name":"mevSpaceWarsawF"},{"id":191,"url":"https://51.158.204.60/__cp2.php","name":"scaleWayAmsterdamB"},{"id":165,"url":"https://51.159.111.35/__cp2.php","name":"scaleWayParisV"},{"id":64,"url":"https://108.181.34.45/__cp2.php","name":"psychzLosAngelesO"},{"id":132,"url":"https://51.159.195.58/__cp2.php","name":"scaleWayParisP"},{"id":164,"url":"https://108.181.6.89/__cp2.php","name":"psychzLosAngelesV"},{"id":223,"url":"https://185.246.86.208/__cp2.php","name":"ikoulaReimsD"},{"id":49,"url":"https://108.181.30.85/__cp2.php","name":"psychzLosAngelesG"},{"id":203,"url":"https://185.16.39.144/__cp2.php","name":"mevSpaceWarsawU"},{"id":48,"url":"https://108.181.34.71/__cp2.php","name":"psychzLosAngelesF"},{"id":233,"url":"https://199.71.214.89/__cp2.php","name":"psychzDallasF"},{"id":219,"url":"https://185.246.84.66/__cp2.php","name":"ikoulaReimsB"},{"id":129,"url":"https://51.159.195.117/__cp2.php","name":"scaleWayParisM"},{"id":199,"url":"https://108.181.11.193/__cp2.php","name":"psychzLosAngeles2K"},{"id":116,"url":"https://51.159.107.230/__cp2.php","name":"scaleWayParisH"},{"id":238,"url":"https://108.181.5.51/__cp2.php","name":"psychzLosAngeles2Q"},{"id":92,"url":"https://108.181.34.157/__cp2.php","name":"psychzLosAngelesR"},{"id":54,"url":"https://108.181.32.61/__cp2.php","name":"psychzLosAngelesL"},{"id":47,"url":"https://108.181.34.57/__cp2.php","name":"psychzLosAngelesE"},{"id":56,"url":"https://108.181.32.59/__cp2.php","name":"psychzLosAngelesM"},{"id":177,"url":"https://108.181.4.237/__cp2.php","name":"psychzLosAngeles2B"},{"id":221,"url":"https://108.181.54.41/__cp2.php","name":"psychzDallasA"},{"id":145,"url":"https://195.3.223.164/__cp2.php","name":"mevSpaceWarsawD"},{"id":185,"url":"https://95.214.53.48/__cp2.php","name":"mevSpaceWarsawP"},{"id":161,"url":"https://108.181.8.179/__cp2.php","name":"psychzLosAngelesS"},{"id":131,"url":"https://51.159.194.250/__cp2.php","name":"scaleWayParisO"},{"id":45,"url":"https://108.181.33.117/__cp2.php","name":"psychzLosAngelesC"},{"id":44,"url":"https://108.181.33.135/__cp2.php","name":"psychzLosAngelesB"},{"id":172,"url":"https://208.87.240.203/__cp2.php","name":"psychzLosAngelesW"},{"id":192,"url":"https://51.158.204.69/__cp2.php","name":"scaleWayAmsterdamC"},{"id":231,"url":"https://199.71.214.121/__cp2.php","name":"psychzDallasD"},{"id":175,"url":"https://108.181.3.54/__cp2.php","name":"psychzLosAngelesZ"},{"id":174,"url":"https://208.87.240.251/__cp2.php","name":"psychzLosAngelesY"},{"id":201,"url":"https://108.181.11.171/__cp2.php","name":"psychzLosAngeles2M"},{"id":213,"url":"https://51.158.204.58/__cp2.php","name":"scaleWayAmsterdamG"},{"id":179,"url":"https://108.181.4.241/__cp2.php","name":"psychzLosAngeles2D"},{"id":117,"url":"https://51.159.195.65/__cp2.php","name":"scaleWayParisI"},{"id":110,"url":"https://51.159.111.24/__cp2.php","name":"scaleWayParisF"},{"id":135,"url":"https://51.159.195.51/__cp2.php","name":"scaleWayParisT"},{"id":229,"url":"https://108.181.90.163/__cp2.php","name":"psychzDallasB"},{"id":46,"url":"https://108.181.33.119/__cp2.php","name":"psychzLosAngelesD"},{"id":197,"url":"https://51.158.204.79/__cp2.php","name":"scaleWayAmsterdamE"},{"id":212,"url":"https://51.158.204.66/__cp2.php","name":"scaleWayAmsterdamF"},{"id":128,"url":"https://51.159.195.110/__cp2.php","name":"scaleWayParisL"},{"id":108,"url":"https://51.159.195.115/__cp2.php","name":"scaleWayParisD"},{"id":230,"url":"https://108.181.90.129/__cp2.php","name":"psychzDallasC"},{"id":144,"url":"https://195.3.223.166/__cp2.php","name":"mevSpaceWarsawC"},{"id":183,"url":"https://208.87.242.233/__cp2.php","name":"psychzLosAngeles2H"},{"id":106,"url":"https://51.158.55.107/__cp2.php","name":"scaleWayParisB"},{"id":168,"url":"https://51.159.194.254/__cp2.php","name":"scaleWayParisY"},{"id":167,"url":"https://51.159.111.59/__cp2.php","name":"scaleWayParisX"},{"id":207,"url":"https://51.159.195.22/__cp2.php","name":"scaleWayParis2A"},{"id":242,"url":"https://51.158.55.99/__cp2.php","name":"scaleWayParis2F"},{"id":210,"url":"https://51.159.107.238/__cp2.php","name":"scaleWayParis2C"},{"id":134,"url":"https://51.159.194.223/__cp2.php","name":"scaleWayParisS"},{"id":178,"url":"https://208.87.241.209/__cp2.php","name":"psychzLosAngeles2C"},{"id":43,"url":"https://108.181.21.229/__cp2.php","name":"psychzLosAngelesA"},{"id":107,"url":"https://51.159.195.9/__cp2.php","name":"scaleWayParisC"},{"id":53,"url":"https://108.181.32.55/__cp2.php","name":"psychzLosAngelesK"},{"id":198,"url":"https://108.181.11.173/__cp2.php","name":"psychzLosAngeles2J"},{"id":69,"url":"https://108.181.34.177/__cp2.php","name":"psychzLosAngelesQ"},{"id":196,"url":"https://51.158.204.2/__cp2.php","name":"scaleWayAmsterdamD"},{"id":224,"url":"https://185.246.86.211/__cp2.php","name":"ikoulaReimsE"},{"id":109,"url":"https://51.158.55.104/__cp2.php","name":"scaleWayParisE"},{"id":202,"url":"https://108.181.11.175/__cp2.php","name":"psychzLosAngeles2N"},{"id":241,"url":"https://51.159.195.121/__cp2.php","name":"scaleWayParis2E"},{"id":182,"url":"https://108.181.5.29/__cp2.php","name":"psychzLosAngeles2G"},{"id":130,"url":"https://51.159.195.89/__cp2.php","name":"scaleWayParisN"},{"id":127,"url":"https://51.159.195.37/__cp2.php","name":"scaleWayParisK"},{"id":205,"url":"https://178.211.139.238/__cp2.php","name":"mevSpaceWarsawW"},{"id":216,"url":"https://185.246.84.18/__cp2.php","name":"ikoulaReimsA"},{"id":163,"url":"https://108.181.11.39/__cp2.php","name":"psychzLosAngelesU"},{"id":162,"url":"https://108.181.9.39/__cp2.php","name":"psychzLosAngelesT"},{"id":173,"url":"https://208.87.240.219/__cp2.php","name":"psychzLosAngelesX"},{"id":118,"url":"https://51.159.195.63/__cp2.php","name":"scaleWayParisJ"},{"id":211,"url":"https://51.159.194.213/__cp2.php","name":"scaleWayParis2D"},{"id":237,"url":"https://108.181.6.9/__cp2.php","name":"psychzLosAngeles2P"},{"id":68,"url":"https://108.181.24.243/__cp2.php","name":"psychzLosAngelesP"},{"id":176,"url":"https://208.87.241.149/__cp2.php","name":"psychzLosAngeles2A"},{"id":209,"url":"https://51.158.54.217/__cp2.php","name":"scaleWayParis2B"},{"id":52,"url":"https://108.181.32.73/__cp2.php","name":"psychzLosAngelesJ"},{"id":133,"url":"https://51.159.111.39/__cp2.php","name":"scaleWayParisR"},{"id":240,"url":"https://208.87.242.51/__cp2.php","name":"psychzLosAngeles2S"},{"id":50,"url":"https://108.181.34.149/__cp2.php","name":"psychzLosAngelesH"},{"id":136,"url":"https://51.159.111.33/__cp2.php","name":"scaleWayParisU"},{"id":204,"url":"https://185.16.39.213/__cp2.php","name":"mevSpaceWarsawV"},{"id":184,"url":"https://208.87.240.67/__cp2.php","name":"psychzLosAngeles2I"},{"id":220,"url":"https://185.246.87.7/__cp2.php","name":"ikoulaReimsC"},{"id":206,"url":"https://51.159.107.232/__cp2.php","name":"scaleWayParisZ"},{"id":150,"url":"https://185.16.39.161/__cp2.php","name":"mevSpaceWarsawG"},{"id":239,"url":"https://108.181.3.225/__cp2.php","name":"psychzLosAngeles2R"},{"id":51,"url":"https://108.181.32.49/__cp2.php","name":"psychzLosAngelesI"},{"id":180,"url":"https://108.181.5.31/__cp2.php","name":"psychzLosAngeles2E"},{"id":186,"url":"https://195.3.222.40/__cp2.php","name":"mevSpaceWarsawQ"},{"id":234,"url":"https://108.181.88.29/__cp2.php","name":"psychzDallasG"},{"id":105,"url":"https://51.159.194.235/__cp2.php","name":"scaleWayParisA"},{"id":190,"url":"https://51.158.204.37/__cp2.php","name":"scaleWayAmsterdamA"},{"id":236,"url":"https://208.87.240.59/__cp2.php","name":"psychzLosAngeles2O"},{"id":143,"url":"https://95.214.53.33/__cp2.php","name":"mevSpaceWarsawB"},{"id":166,"url":"https://51.159.111.23/__cp2.php","name":"scaleWayParisW"},{"id":115,"url":"https://51.159.195.122/__cp2.php","name":"scaleWayParisG"}]
class ProxyError(Exception):pass
@dataclass
class ProxyServer:
 id:int;url:str;name:str
@dataclass
class ProxySession:
 session:c.Session;proxy_ip:str;cpo:str;server:ProxyServer
class FreeProxy:
 def __init__(self,timeout=30,max_retries=3):
  self.timeout=timeout;self.max_retries=max_retries;self.servers=[ProxyServer(**s)for s in S];self._last_request=0;self._proxy_session=None
 def _create_proxy_session(self,url:str)->ProxySession:
  ps=c.Session(impersonate="chrome",verify=False);cs=None;a=0
  while a<10:
   sd=random.choice(S)
   try:
    r=ps.get(sd['url'],timeout=5)
    if r.text.strip()=="OK":cs=ProxyServer(**sd);break
   except:pass
   a+=1
  if not cs:raise ProxyError("No working servers found")
  csrf=re.findall(r'value="([^"]+)"',ps.get("https://www.croxyproxy.com/").text)[0]
  csrf_two=re.findall(r'data-csrf="&quot;([^&"]+)&quot;"',ps.post("https://www.croxyproxy.com/servers",data={"csrf":csrf,"url":url}).text)[0]
  proxy_url=re.findall(r'data-r="([^"]+)"',ps.post("https://www.croxyproxy.com/requests",data={"url":url,"proxyServerId":str(cs.id),"csrf":csrf_two,"frontOrigin":"https://www.croxyproxy.com","demo":"0"},params={"fso":""}).text)[0]
  ps_url=p(cs.url);pi=f"https://{ps_url.netloc}";pu=p(url);to=f"https://{pu.netloc}";cpo=e(to.encode('utf-8')).decode('utf-8').strip("=")
  return ProxySession(session=ps,proxy_ip=pi,cpo=cpo,server=cs)
 def _get_proxy_session(self,url:str)->ProxySession:
  if self._proxy_session is None:self._proxy_session=self._create_proxy_session(url)
  return self._proxy_session
 def _request(self,method:str,url:str,**kwargs):
  now=time.time()
  if now-self._last_request<0.5:time.sleep(0.5-(now-self._last_request))
  self._last_request=now;pa=p(url)
  for a in range(self.max_retries):
   try:
    px=self._get_proxy_session(url);pu=px.proxy_ip+pa.path
    if pa.query:pu+="?"+pa.query
    if 'params'not in kwargs:kwargs['params']={}
    kwargs['params']['__cpo']=px.cpo
    if 'timeout'not in kwargs:kwargs['timeout']=self.timeout
    return px.session.request(method,pu,**kwargs)
   except Exception as ex:
    if a==self.max_retries-1:raise
    self._proxy_session=None;time.sleep(1)
 def get(self,url:str,**kwargs):return self._request("GET",url,**kwargs)
 def post(self,url:str,**kwargs):return self._request("POST",url,**kwargs)
 def put(self,url:str,**kwargs):return self._request("PUT",url,**kwargs)
 def delete(self,url:str,**kwargs):return self._request("DELETE",url,**kwargs)
 def head(self,url:str,**kwargs):return self._request("HEAD",url,**kwargs)
 def patch(self,url:str,**kwargs):return self._request("PATCH",url,**kwargs)
 def get_session_info(self)->Optional[Dict[str,str]]:
  if self._proxy_session:return {"proxy_ip":self._proxy_session.proxy_ip,"server_name":self._proxy_session.server.name,"cpo":self._proxy_session.cpo}
  return None
 def close(self):
  if self._proxy_session and self._proxy_session.session:self._proxy_session.session.close()
  self._proxy_session=None
 def __enter__(self):return self
 def __exit__(self,*args):self.close()
_global_proxy=None
def _get_global_proxy():
 global _global_proxy
 if _global_proxy is None:_global_proxy=FreeProxy()
 return _global_proxy
def get(url,**kwargs):return _get_global_proxy().get(url,**kwargs)
def post(url,**kwargs):return _get_global_proxy().post(url,**kwargs)
def put(url,**kwargs):return _get_global_proxy().put(url,**kwargs)
def delete(url,**kwargs):return _get_global_proxy().delete(url,**kwargs)
def head(url,**kwargs):return _get_global_proxy().head(url,**kwargs)
def patch(url,**kwargs):return _get_global_proxy().patch(url,**kwargs)
def create_proxy_session(url:str)->Tuple[c.Session,str,str]:
 proxy=FreeProxy();si=proxy._create_proxy_session(url);return si.session,si.proxy_ip,si.cpo
