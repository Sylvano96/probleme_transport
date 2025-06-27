import { createContext, useState } from "react";

 export const TableGenerate = createContext({
    row : null,
    column : null,
    changeTableGenerate : (x,y) => {},
    data : '',
    changeData : (x) => {}
})

 export function TableGenerateProvider({children}) {

    const [row, setRow] = useState(localStorage.getItem('nbLi') ? parseInt(localStorage.getItem('nbLi')) : 4)
    const [column, setColumn] = useState(localStorage.getItem('nbCol') ? parseInt(localStorage.getItem('nbCol')) : 6)
    const [data, setData] = useState(localStorage.getItem('data') ? localStorage.getItem('data') :'')

    const changeTableGenerate = (x, y) => {
        setRow(x)
        setColumn(y)
        localStorage.setItem('nbLi', x)
        localStorage.setItem('nbCol', y)
    } 

    const changeData = (x) => {
        setData(x)
        localStorage.setItem('data', x)
        console.log(data)
    }


    return <TableGenerate.Provider value={{row,column,changeTableGenerate,data,changeData}}>
        {children}
    </TableGenerate.Provider>
}