import React , { useContext } from 'react'
import { ThemeContext } from '../Context/useTheme'
import { FaRegSun, FaRegMoon } from 'react-icons/fa6'
import { useNavigate } from 'react-router-dom'

export default function Nav() {
 
    const {theme, toogleTheme} = useContext(ThemeContext)
    const navigate = useNavigate()

    const handleNavigate = (e) => {
        e.preventDefault()
        navigate('/')
    }
  
    return (
    <nav style={{display:"flex", justifyContent:'space-between', alignItems:'center'}}>
        <h3 className='mx-4 my-2' style={{color:'orange', fontSize:'2rem'}} onClick={handleNavigate}>
            Solve
        </h3>
        <span onClick={toogleTheme} className='mx-4 my-2' style={{fontSize:'1.3rem', transition:"0.6s"}}> {theme == "dark" ? <FaRegMoon/> : <FaRegSun/> } </span>
    </nav>
  )
}
