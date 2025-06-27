import { Quantum } from 'ldrs/react'
import 'ldrs/react/Quantum.css'
import { useContext } from 'react'
import { ThemeContext } from '../Context/useTheme'

function Spinner(){
    const {theme} = useContext(ThemeContext)
    return <div style={{display:'flex', justifyContent:'center', alignItems:'center', height:'80vh'}}>
    
    <Quantum
    size="70"
    speed="1.75"
    color={theme == "dark" ? 'white' : 'black'} 
    />

    </div>
}

export default Spinner