import { useContext, useState } from "react"
import DisBg from "./DisBg"
import Nav from "./Nav"
import { FaXmark, FaTableCells, FaRegSquarePlus, FaPencil } from "react-icons/fa6"
import { useNavigate } from "react-router-dom"
import { TableGenerate } from "../Context/useGenerate"

function Operation(){

    const navigate = useNavigate()
    const {data} = useContext(TableGenerate)

    const handleNavigate = (link) => {
        navigate(link)
    }

    return <DisBg>
        <Nav></Nav>

        <div className="container">
            <h3 className="my-3">Choisissez votre tableau</h3>
            <div style={{display:'flex',justifyContent:'space-around', flexWrap:'wrap', height:'50vh',alignItems:'center', textAlign:'center'}}>
                <div className="card-table" style={{cursor:'pointer'}} onClick={(e)=> {
                    e.preventDefault()
                    handleNavigate('table4x4')
                    }}>
                    <span ><FaTableCells style={{fontSize:'150px'}}></FaTableCells></span>
                    <p>Tableau 4 * 4</p>
                </div>
                <div className="card-table" style={{cursor:'pointer'}} onClick={(e)=> {
                    e.preventDefault()
                    handleNavigate('tablePatch')
                    }}>
                    <span className="flex justify-center"><FaRegSquarePlus style={{fontSize:'150px'}}></FaRegSquarePlus></span>
                    <p>Tableau personnalisé <FaPencil className="inline"></FaPencil></p>
                </div>
            </div>
        </div>
    </DisBg>

}

export default Operation