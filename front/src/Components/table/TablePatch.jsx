import { useContext, useRef, useState } from "react"
import DisBg from "../DisBg"
import Nav from "../Nav"
import { TableGenerate } from "../../Context/useGenerate"
import { ThemeContext } from "../../Context/useTheme"
import { Link, useNavigate } from "react-router-dom"

function TablePatch(){

    const {theme} = useContext(ThemeContext)

    const {changeTableGenerate} = useContext(TableGenerate)
    const {column} = useContext(TableGenerate)
    const {row} = useContext(TableGenerate)

    const [rowTable, setRowTable] = useState(row)
    const [columnTable, setColumnTable] = useState(column)

    const navigate = useNavigate()
    
    const handleNavigate = (link) => {
        navigate(link)
    }

    const handleGenerate = (e) => {
        e.preventDefault()
        changeTableGenerate(rowTable, columnTable)
        handleNavigate('tablePatchGenerate')
    }


    return <DisBg>
        <Nav></Nav>
        <h3 className="my-3 mx-5">Tableau personnalisé</h3>
        <div style={{display:'flex', justifyContent:'center', alignItems:'center', height:'60vh'}}>
            <form style={{width:'300px'}}>
                <label htmlFor="" className="my-1">Nombre de ligne</label>
                <input type="number" style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}} onChange={(e)=> setRowTable(e.target.value)}  className="form-control" min={3} max={8}/>

                <label htmlFor="" className="my-1">Nombre de colonne</label>
                <input type="number" style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}} onChange={(e)=> setColumnTable(e.target.value)}  className="form-control" min={3} max={8}/>

                <div style={{display:'flex', justifyContent:'flex-end'}}>
                    <button className="btn btn-warning my-2" onClick={handleGenerate}>Générer le tableau</button>
                </div>
            </form>
        </div>
    </DisBg>
}

export default TablePatch