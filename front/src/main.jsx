import React, { lazy, Suspense, useContext} from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { ThemeContext } from './Context/useTheme.jsx'

const AppLazy = lazy(()=> import('./App.jsx'))

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Suspense fallback={<Spinners/>}>
      <AppLazy/>
    </Suspense>
  </React.StrictMode>
)

function Spinners (){

  const {theme} = useContext(ThemeContext)

  return <div style={{display:'flex', justifyContent:'center', alignItems:'center', height:'100vh'}}>
    {
      theme == "dark" ? 
        <div className="container" style={{display:'flex', justifyContent:'center', alignItems:'center'}}>
      <div className="spinner-grow text-secondary mx-2" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      <div className="spinner-grow text-secondary mx-2" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      <div className="spinner-grow text-secondary mx-2" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      <div className="spinner-grow text-secondary mx-2" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
    </div>
       : 
        <div className="container" style={{display:'flex', justifyContent:'center', alignItems:'center'}}>
        <div className="spinner-grow text-secondary mx-2" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <div className="spinner-grow text-secondary mx-2" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <div className="spinner-grow text-secondary mx-2" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <div className="spinner-grow text-secondary mx-2" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
      }
  </div>
}