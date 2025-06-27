import React, { useContext } from 'react'
import { ThemeContext } from '../Context/useTheme'

function DisBg({children}) {

    const {theme} = useContext(ThemeContext)

  return (
    <div style={theme == 'dark' ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s'} : {backgroundColor:'white', transition:'0.6s'}}>
        {children}
    </div>
  )
}

export default DisBg