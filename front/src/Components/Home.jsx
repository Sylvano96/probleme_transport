import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import DisBg from './DisBg'
import img from '../assets/8365137.png'
import Nav from './Nav'
import { NavLink } from 'react-router-dom'
import { FaGear } from 'react-icons/fa6'
import '../App.css'
import { useContext } from 'react'
import { ThemeContext } from '../Context/useTheme'

function Home(){

    const {theme} = useContext(ThemeContext)
    return <DisBg>
        <Nav></Nav>
        <div style={{display:"flex", justifyContent:'space-around', alignItems:'center', height:'80vh', flexWrap:'wrap'}}>
            <div>
                <img src={img} alt="" style={{maxWidth:'420px', width:'100%', borderRadius:'40px', padding:'10px 10px'}}/>
            </div>
            
            <div style={{display:'block', padding:'30px 20px'}}>
                <p style={{fontFamily:'monospace', fontSize:'1.5rem', width:'100%',maxWidth:'400px', textAlign:'left'}}>Bienvenue dans <span style={{color:'orange', fontSize:'2rem'}}>Solve</span> , l'application qui résouds le problème de transport dans R.O.</p>
                <NavLink to='operation' style={{textDecoration:'none'}} className={`btn-starting w-[250px] block mb-2 font-medium text-sm text-center tracking-wide  px-3 py-2 transition-all ${theme == 'dark' ? "text-white" : "text-gray-800"}`}>Commencer l'opération <FaGear className='mx-1 icon-gear'></FaGear></NavLink>
            </div>
        </div>
    </DisBg>
}

export default Home
