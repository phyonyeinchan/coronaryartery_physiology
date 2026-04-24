import React, {useState} from 'react'

export default function PredictForm(){
  const [patientId, setPatientId] = useState('p1')
  const [age, setAge] = useState(65)
  const [hr, setHr] = useState(80)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const submit = async (e)=>{
    e.preventDefault()
    setLoading(true)
    const payload = {patient_id: patientId, features: {age: Number(age), heart_rate: Number(hr)}}
    try{
      const r = await fetch('/predict', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)})
      const j = await r.json()
      setResult(j)
    }catch(err){
      setResult({error: String(err)})
    }finally{setLoading(false)}
  }

  return (
    <div>
      <h2>Predict Risk</h2>
      <form onSubmit={submit} className="form">
        <label>Patient ID<input value={patientId} onChange={e=>setPatientId(e.target.value)} /></label>
        <label>Age<input type="number" value={age} onChange={e=>setAge(e.target.value)} /></label>
        <label>Heart rate<input type="number" value={hr} onChange={e=>setHr(e.target.value)} /></label>
        <button type="submit" disabled={loading}>{loading? 'Running...' : 'Predict'}</button>
      </form>
      {result && (
        <pre className="result">{JSON.stringify(result, null, 2)}</pre>
      )}
    </div>
  )
}
