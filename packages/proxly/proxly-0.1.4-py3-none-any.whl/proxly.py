import curl_cffi as c
import re,random,time,json,html
from base64 import b64decode as d,b64encode as e
from urllib.parse import urlparse as p,urlunparse,parse_qs,urlencode
from typing import Dict,List,Optional,Any,Tuple
from dataclasses import dataclass
from functools import wraps
S=[{"id":146,"url":"https://146.19.24.89/__cp2.php","name":"mevSpaceWarsawE"},{"id":181,"url":"https://208.87.240.35/__cp2.php","name":"psychzLosAngeles2F"},{"id":63,"url":"https://108.181.43.67/__cp2.php","name":"psychzLosAngelesN"},{"id":200,"url":"https://108.181.11.137/__cp2.php","name":"psychzLosAngeles2L"},{"id":149,"url":"https://195.3.222.15/__cp2.php","name":"mevSpaceWarsawF"}]
_server_cache=None;_cache_time=0;_cache_duration=600
class ProxyError(Exception):pass
@dataclass
class ProxyServer:
 id:int;url:str;name:str
@dataclass
class ProxySession:
 session:c.Session;proxy_ip:str;cpo:str;server:ProxyServer
def _fetch_servers_raw(csrf_token:str)->List[Dict[str,Any]]:
 try:
  ps=c.Session(impersonate="chrome",verify=False);r=ps.post("https://www.croxyproxy.com/servers",data={"csrf":csrf_token,"url":"https://example.com"});html_content=r.text;match=re.search(r'<script[^>]*data-ss="\[([^\]]+)\]"[^>]*>',html_content)
  if not match:return S
  array_content=match.group(1);decoded_html=html.unescape(array_content);json_array_str="["+decoded_html+"]";encoded_strings=json.loads(json_array_str);servers=[]
  for encoded_str in encoded_strings:
   try:
    decoded_b64=d(encoded_str).decode('utf-8');decoded_hex=bytes.fromhex(decoded_b64).decode('utf-8');brace_count=0;start_idx=0
    for j,char in enumerate(decoded_hex):
     if char=='{':
      if brace_count==0:start_idx=j
      brace_count+=1
     elif char=='}':
      brace_count-=1
      if brace_count==0:
       try:servers.append(json.loads(decoded_hex[start_idx:j+1]))
       except:pass
   except:continue
  return servers if servers else S
 except:return S
def fetch_servers()->List[Dict[str,Any]]:
 global _server_cache,_cache_time;current_time=time.time()
 if _server_cache and current_time-_cache_time<_cache_duration:return _server_cache
 try:
  ps=c.Session(impersonate="chrome",verify=False);csrf_token=re.findall(r'value="([^"]+)"',ps.get("https://www.croxyproxy.com/").text)[0];servers=_fetch_servers_raw(csrf_token);_server_cache=servers;_cache_time=current_time;return servers
 except:return S
class proxly:
 def __init__(self,timeout=30,max_retries=3):self.timeout=timeout;self.max_retries=max_retries;self.servers=S;self._last_request=0;self._proxy_session=None
 def _create_proxy_session(self,url:str)->ProxySession:
  servers=fetch_servers();ps=c.Session(impersonate="chrome",verify=False);cs=None;a=0
  while a<10:
   sd=random.choice(servers)
   try:
    r=ps.get(sd['url'],timeout=5)
    if r.text.strip()=="OK":cs=ProxyServer(**sd);break
   except:pass
   a+=1
  if not cs:raise ProxyError("No working servers found")
  csrf=re.findall(r'value="([^"]+)"',ps.get("https://www.croxyproxy.com/").text)[0];csrf_two=re.findall(r'data-csrf="&quot;([^&"]+)&quot;"',ps.post("https://www.croxyproxy.com/servers",data={"csrf":csrf,"url":url}).text)[0];proxy_url=re.findall(r'data-r="([^"]+)"',ps.post("https://www.croxyproxy.com/requests",data={"url":url,"proxyServerId":str(cs.id),"csrf":csrf_two,"frontOrigin":"https://www.croxyproxy.com","demo":"0"},params={"fso":""}).text)[0];ps_url=p(cs.url);pi=f"https://{ps_url.netloc}";pu=p(url);to=f"https://{pu.netloc}";cpo=e(to.encode('utf-8')).decode('utf-8').strip("=")
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
 if _global_proxy is None:_global_proxy=proxly()
 return _global_proxy
def get(url,**kwargs):return _get_global_proxy().get(url,**kwargs)
def post(url,**kwargs):return _get_global_proxy().post(url,**kwargs)
def put(url,**kwargs):return _get_global_proxy().put(url,**kwargs)
def delete(url,**kwargs):return _get_global_proxy().delete(url,**kwargs)
def head(url,**kwargs):return _get_global_proxy().head(url,**kwargs)
def patch(url,**kwargs):return _get_global_proxy().patch(url,**kwargs)
def get_server_list()->List[Dict[str,Any]]:return fetch_servers()
def clear_server_cache():global _server_cache,_cache_time;_server_cache=None;_cache_time=0
def create_proxy_session(url:str)->Tuple[c.Session,str,str]:
 proxy=proxly();si=proxy._create_proxy_session(url);return si.session,si.proxy_ip,si.cpo
