_CLIENT_SCRIPT_TEMPLATE = """<!doctype html>
<script src="/htmx.min.js"></script>
<script>
  htmx.config.defaultSwapStyle = 'none';
  window.pageqlMarkers={};
  function getBodyTextContent(){return document.body?document.body.textContent:'';}
  function pstart(i){var s=document.currentScript,c=document.createComment('pageql-start:'+i);var p=s.parentNode;if(p&&p.tagName==='HEAD'&&document.body){p.removeChild(s);document.body.appendChild(c);}else{s.replaceWith(c);}var a=window.pageqlMarkers[i];if(!a)a=window.pageqlMarkers[i]=[];a.push(c);if(document.currentScript)document.currentScript.remove();}
  function pend(i){var s=document.currentScript,c=document.createComment('pageql-end:'+i);var p=s.parentNode;if(p&&p.tagName==='HEAD'&&document.body){p.removeChild(s);document.body.appendChild(c);}else{s.replaceWith(c);}var a=window.pageqlMarkers[i];if(!a)a=window.pageqlMarkers[i]=[];var m=a[a.length-1];if(m)m.e=c;else{a.push({e:c});}if(document.currentScript)document.currentScript.remove();}
  function pprevioustag(i){var s=document.currentScript,p=s.parentNode,t=s.previousElementSibling;if(p&&p.tagName==='HEAD'&&document.body){p.removeChild(s);t=null;p=document.body;}else{s.remove();}window.pageqlMarkers[i]=t||p;if(document.currentScript)document.currentScript.remove();}
  function pset(i,v){var a=window.pageqlMarkers[i];if(!a||!a.length)return;var s=a[a.length-1],e=s.e,r=document.createRange();r.setStartAfter(s);r.setEndBefore(e);r.deleteContents();var t=document.createElement('template');t.innerHTML=v;var c=t.content;var sc=c.querySelectorAll('script');e.parentNode.insertBefore(c,e);for(var j=0;j<sc.length;j++){var os=sc[j];var ns=document.createElement('script');for(var k=0;k<os.attributes.length;k++){var at=os.attributes[k];ns.setAttribute(at.name,at.value);}ns.text=os.textContent;os.parentNode.replaceChild(ns,os);}if(window.htmx){var x=s.nextSibling;while(x&&x!==e){var nx=x.nextSibling;if(x.nodeType===1)htmx.process(x);x=nx;}}if(document.currentScript)document.currentScript.remove();}
  function pdelete(i){var a=window.pageqlMarkers[i];if(!a||!a.length){if(document.currentScript)document.currentScript.remove();return;}var m=a.pop(),e=m.e,r=document.createRange();r.setStartBefore(m);r.setEndAfter(e);r.deleteContents();if(!a.length)delete window.pageqlMarkers[i];if(document.currentScript)document.currentScript.remove();}
  function pupdate(o,n,v){var ao=window.pageqlMarkers[o];if(!ao||!ao.length){if(document.currentScript)document.currentScript.remove();return;}var m=ao.pop(),e=m.e;m.textContent='pageql-start:'+n;e.textContent='pageql-end:'+n;var an=window.pageqlMarkers[n];if(!an)an=window.pageqlMarkers[n]=[];an.push(m);pset(n,v);if(window.htmx){var x=m.nextSibling;while(x&&x!==e){var nx=x.nextSibling;if(x.nodeType===1)htmx.process(x);x=nx;}}if(document.currentScript)document.currentScript.remove();}
  function pinsert(i,v){var a=window.pageqlMarkers[i];if(!a)a=window.pageqlMarkers[i]=[];var mid=i.split('_')[0];var ca=window.pageqlMarkers[mid];if(!ca||!ca.length){if(document.currentScript)document.currentScript.remove();return;}var c=ca[ca.length-1];var m=document.createComment('pageql-start:'+i);var e=document.createComment('pageql-end:'+i);m.e=e;a.push(m);c.e.parentNode.insertBefore(m,c.e);var t=document.createElement('template');t.innerHTML=v;c.e.parentNode.insertBefore(t.content,c.e);c.e.parentNode.insertBefore(e,c.e);if(window.htmx){var x=m.nextSibling;while(x&&x!==e){var nx=x.nextSibling;if(x.nodeType===1)htmx.process(x);x=nx;}}if(document.currentScript)document.currentScript.remove();}
  function pupdatetag(i,c){var t=window.pageqlMarkers[i];var d=document.createElement('template');d.innerHTML=c;var n=d.content.firstChild;if(!n)return;for(var j=t.attributes.length-1;j>=0;j--){var a=t.attributes[j].name;if(!n.hasAttribute(a))t.removeAttribute(a);}for(var j=0;j<n.attributes.length;j++){var at=n.attributes[j];t.setAttribute(at.name,at.value);}if(document.currentScript)document.currentScript.remove();}
  document.currentScript.remove()
</script>
<script>
  (function() {
    const host = window.location.hostname;
    const port = window.location.port;
    const clientId = "{client_id}";
    function setup() {
      document.body.addEventListener('htmx:configRequest', (evt) => {
        evt.detail.headers['ClientId'] = clientId;
      });
      const proto = window.location.protocol === 'https:' ? 'wss' : 'ws';
      const ws_url = `${proto}://${host}:${port}/reload-request-ws?clientId=${clientId}`;

      function forceReload() {
        const socket = new WebSocket(ws_url);
        socket.onopen = () => {
          window.location.reload();
        };
        socket.onerror = () => {
          setTimeout(forceReload, 100);
        };
      }

      const socket = new WebSocket(ws_url);
      socket.onopen = () => {
        console.log("WebSocket opened with id", clientId);
      };

      socket.onmessage = (event) => {
        if (event.data == "reload") {
          window.location.reload();
        } else if (event.data === "get body text content") {
          socket.send(getBodyTextContent());
        } else {
          try {
            eval(event.data);
          } catch (e) {
            console.error("Failed to eval script", event.data, e);
          }
        }
      };

      socket.onclose = () => {
        setTimeout(forceReload, 100);
      };

      socket.onerror = () => {
        setTimeout(forceReload, 100);
      };
    }
    if (document.body) {
      setup();
    } else {
      window.addEventListener('DOMContentLoaded', setup);
    }
    document.currentScript.remove();

  })();
</script>
"""

def client_script(client_id: str) -> str:
    return _CLIENT_SCRIPT_TEMPLATE.replace("{client_id}", client_id)


