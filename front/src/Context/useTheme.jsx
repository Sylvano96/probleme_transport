import { createContext, useState } from "react";


export const ThemeContext = createContext({
    theme : null,
    toogleTheme : () => {}
})

export function ThemeProvider({children}){

    const [theme, SetTheme] = useState(localStorage.getItem('bg') == null ? getThemeColor() : localStorage.getItem('bg'))
    stateBg(theme)

    const toogleTheme = () => {
        SetTheme(theme === 'dark' ? 'light' : 'dark')
        localStorage.setItem('bg', theme === 'dark' ? 'light' : 'dark')
        stateBg(theme)
    }

    return <ThemeContext.Provider value={{theme, toogleTheme}}>
        {children}
    </ThemeContext.Provider>
}

const stateBg = (theme) => {
    if(theme === 'dark'){
        const body = document.body
        body.style.opacity = 0
        body.style.transition ='0.6s'
        body.style.backgroundColor = 'rgb(41, 39, 39)'
        body.style.color = 'white'
        body.style.opacity = 1
        body.style.transition ='0.6s'
    }else{
        const body = document.body
        body.style.opacity = 0
        body.style.transition ='0.6s'
        body.style.backgroundColor = 'white'
        body.style.color = 'black'
        body.style.opacity = 1
        body.style.transition ='0.6s'
    }
}

function getThemeColor(){
    return window.matchMedia && window.matchMedia('(prefers-color-scheme : dark)').matches? 'dark' : 'light'
}