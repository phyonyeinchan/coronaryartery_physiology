import React, {useState, useEffect} from 'react'

export default function Health(){
  const [status, setStatus] = useState('loading')
  useEffect(()=>{
    fetch('/health')
      .then(r=>r.json())
      .then(j=>setStatus(j.status||'ok'))
      .catch(()=>setStatus('down'))
  },[])
  return (
    <div>
      <h2>API Health</h2>
      <p className={status==='ok'? 'ok' : status==='loading'? 'muted' : 'err'}>Status: {status}</p>
    </div>
  )
}
