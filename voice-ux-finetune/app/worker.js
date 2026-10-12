importScripts('v60core.js','denoise.js');
onmessage=e=>{const d=e.data;try{
 if(d.cmd==='v60'){const n=V60.extract(d.y,p=>postMessage({p}));postMessage({notes:n})}
 else if(d.cmd==='dn'){const r=DENOISE.process(d.x,d.sr);const y=Float32Array.from(r.y);postMessage({y,f0:r.f0,f1:r.f1,thr:r.thr,f2:r.f2},[y.buffer])}
}catch(err){postMessage({err:String(err&&err.message||err)})}};
