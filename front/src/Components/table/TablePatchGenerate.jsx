import React, { useContext, useEffect, useRef, useState } from 'react'
import DisBg from '../DisBg'
import Nav from '../Nav'
import { ThemeContext } from '../../Context/useTheme'
import { TableGenerate } from '../../Context/useGenerate'
import axios from 'axios'
import Result from '../Result/Result'

export default function TablePatchGenerate() {


    const { theme } = useContext(ThemeContext)
    const { column, row, data, changeData } = useContext(TableGenerate)

    const [result, setResult] = useState(false)
    const [error, setError] = useState("")

    const nbCout = column * row

    let x = []
    let d = []

    useEffect(() => {
        if (data != "") {
            setResult(!result)
        }
    }, [])

    // Génération des valeurs 

    const clientRefs = Array.from({ length: column }).map(() => useRef(''))
    const entrepotRefs = Array.from({ length: row }).map(() => useRef(''))
    const quantitedemandeRefs = Array.from({ length: column }).map(() => useRef(''))
    const quantitestockeRefs = Array.from({ length: row }).map(() => useRef(''))

    let coutRefs = Array.from({ length: nbCout }).map(() => {
        x.push(useRef(''))
        if (x.length == column) {
            d = x
            x = []
            return d
        }
    })

    coutRefs = coutRefs.filter(data => data !== undefined)

    console.log(coutRefs)

    // for (let index = 0; index < nbCout ; index++) {

    //     x.push(useRef(null))

    //     if(x.length == column){
    //         tableCouts.push(x)
    //         x = []
    //     }
    // }  


    /************************************** */

    let tableCouts = []
    let tableEntrepots = []
    let tableClients = []
    let tableQuantiteDemande = []
    let tableQuantiteStocke = []

    const handleClick = async (e) => {
        e.preventDefault()
        let a = []
        for (let data of coutRefs) {
            for (let x of data) {
                a.push(parseInt(x.current.value))
            }
            if (tableCouts.length != row) {
                tableCouts.push(a)
                a = []
            }
        }

        for (let data in entrepotRefs) {
            tableQuantiteStocke.push(parseInt(quantitestockeRefs[data].current.value))
            tableEntrepots.push(entrepotRefs[data].current.value)
        }

        for (let data in clientRefs) {
            tableQuantiteDemande.push(parseInt(quantitedemandeRefs[data].current.value))
            tableClients.push(clientRefs[data].current.value)
        }

        const data1 = {
            tableCouts: tableCouts,
            tableClients: tableClients,
            tableEntrepots: tableEntrepots,
            tableQuantiteDemande: tableQuantiteDemande,
            tableQuantiteStocke: tableQuantiteStocke
        }

        try {
            const response = await axios.post('http://localhost:5000/solve', data1)
            changeData(JSON.stringify(response.data))
            setResult(true)
        } catch (error) {
            console.log(error)
            setError(error.response.data.error)
            setTimeout(() => {
                setError('')
            }, 3000)
            tableClients = []
            tableCouts = []
            tableEntrepots = []
            tableQuantiteDemande = []
            tableQuantiteStocke = []
        }

        // console.log('table quantité demandé: ',tableQuantiteDemande)
        // console.log('table quantité stocké : ',tableQuantiteStocke)
        // console.log('table client : ',tableClients)
        // console.log('table entrepôt : ',tableEntrepots)
        // console.log('table coûts : ',tableCouts)

    }

    /********************************************** */
    return (
        <DisBg>
            <Nav></Nav>
            {
                !result ? <div>
                    <h3 className="my-3 mx-5">Veuillez compléter le tableau</h3>
                    <div style={{ display: 'flex', justifyContent: 'center' }}>
                        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', width: '40%', maxWidth:'350px' }}>
                                <h3>Entrepôts</h3>
                                <form action="" className='mx-2'>
                                    {
                                        entrepotRefs.map((value, key) => (
                                            <div key={key}>
                                                <input type="text" ref={value} className='form-control m-1 text-center' style={theme == "dark" ? { backgroundColor: 'rgb(41, 39, 39)', transition: '0.6s', color: 'white' } : { backgroundColor: 'white', transition: '0.6s', color: 'black' }} />
                                            </div>
                                        ))
                                    }
                                </form>
                            </div>
                            <div style={{ position: 'absolute', top: '50px', right: '60px' }}>
                                {
                                    error && <div style={{ display: 'flex', justifyContent: 'center' }} className='m-1' >
                                        <p className='alert alert-warning text-center'>{error}</p>
                                    </div>
                                }
                            </div>
                            <div>
                                <div>
                                    <h3 className='text-center'>Clients</h3>
                                    <form action="" className='mx-2 d-flex'>
                                        {
                                            clientRefs.map((value, key) => (
                                                <div key={key} className='mx-1'>
                                                    <input type="text" ref={value} className='form-control mx-1 text-center' style={theme == "dark" ? { backgroundColor: 'rgb(41, 39, 39)', transition: '0.6s', color: 'white' } : { backgroundColor: 'white', transition: '0.6s', color: 'black' }} />
                                                </div>
                                            ))
                                        }
                                    </form>
                                </div>
                                <table className='table' style={theme == "dark" ? { backgroundColor: 'rgb(41, 39, 39)', transition: '0.6s', margin: '0px' } : { backgroundColor: 'white', transition: '0.6s', margin: '0px' }}>
                                    <tbody>
                                        {
                                            coutRefs.map((value, key) => (
                                                <tr key={key}>
                                                    {
                                                        value.map((val, key) => (
                                                            <td key={key} style={theme == "dark" ? { backgroundColor: 'rgb(41, 39, 39)', transition: '0.6s' } : { backgroundColor: 'white', transition: '0.6s' }}><input type="text" ref={val} className="form-control text-center" style={theme == "dark" ? { backgroundColor: 'rgb(41, 39, 39)', transition: '0.6s', color: 'white' } : { backgroundColor: 'white', transition: '0.6s', color: 'black' }} /></td>
                                                        ))
                                                    }
                                                </tr>
                                            ))
                                        }
                                    </tbody>
                                </table>
                                <div>
                                    <form action="" className='mx-2 d-flex'>
                                        {
                                            quantitedemandeRefs.map((value, key) => (
                                                <div key={key} className='mx-1'>
                                                    <input type="text" ref={value} className='form-control mx-1 text-center' style={theme == "dark" ? { backgroundColor: 'rgb(41, 39, 39)', transition: '0.6s', color: 'white' } : { backgroundColor: 'white', transition: '0.6s', color: 'black' }} />
                                                </div>
                                            ))
                                        }
                                    </form>
                                    <h3 className='text-center my-1'>Quantités demandés</h3>
                                </div>
                            </div>
                            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', width: '40%', maxWidth:'350px' }}>
                                <form action="" className='mx-2'>
                                    {
                                        quantitestockeRefs.map((value, key) => (
                                            <div key={key}>
                                                <input type="text" ref={value} className='form-control m-1 text-center' style={theme == "dark" ? { backgroundColor: 'rgb(41, 39, 39)', transition: '0.6s', color: 'white' } : { backgroundColor: 'white', transition: '0.6s', color: 'black' }} />
                                            </div>
                                        ))
                                    }
                                </form>
                                <h3 className='mx-2'>Quantités stockées</h3>
                            </div>
                        </div>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'flex-end', marginRight: '40px' }}>
                        <button className="btn btn-warning" onClick={handleClick}>Générer la réponse </button>
                    </div>
                </div> : <Result></Result>
            }
        </DisBg>
    )
}
