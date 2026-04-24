import React, {useState} from 'react'

export default function AdminReload(){
  const [token, setToken] = useState('')
  const [msg, setMsg] = useState(null)
  const [loading, setLoading] = useState(false)

  const reload = async (e)=>{
    e && e.preventDefault()
    setLoading(true)
    try{
      const headers = {}
      if(token) headers['X-Reload-Token'] = token
      const r = await fetch('/reload-model', {method:'POST', headers})
      const j = await r.json()
      if(!r.ok) throw new Error(j.detail || JSON.stringify(j))
      setMsg({type:'ok', text:`Reloaded: ${j.path}`})
    }catch(err){
      setMsg({type:'err', text: String(err)})
    }finally{setLoading(false)}
  }

  return (
    <div>
      <h2>Admin: Reload Model</h2>
      <form onSubmit={reload} className="form-inline">
        <input placeholder="X-Reload-Token (if set)" value={token} onChange={e=>setToken(e.target.value)} />
        <button type="submit" disabled={loading}>{loading? 'Reloading...' : 'Reload'}</button>
      </form>
      {msg && <p className={msg.type==='ok'? 'ok' : 'err'}>{msg.text}</p>}
    </div>
  )
}
