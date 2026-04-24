import React, {useState, useEffect} from 'react'
import Health from './components/Health'
import PredictForm from './components/PredictForm'
import AdminReload from './components/AdminReload'

export default function App(){
  return (
    <div className="app">
      <header className="header">
        <h1>Cardio Risk Dashboard</h1>
      </header>
      <main className="grid">
        <div className="card">
          <Health />
        </div>
        <div className="card">
          <PredictForm />
        </div>
        <div className="card">
          <AdminReload />
        </div>
      </main>
      <footer className="footer">Built on the Cardio Risk API</footer>
    </div>
  )
}
