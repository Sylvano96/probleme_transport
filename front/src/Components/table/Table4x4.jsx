import Nav from '../Nav'
import DisBg from "../DisBg"
import { FaXmark } from 'react-icons/fa6'
import { useContext, useEffect, useRef, useState } from 'react'
import { ThemeContext } from '../../Context/useTheme'
import Result from '../Result/Result'
import axios from 'axios'
import { TableGenerate } from '../../Context/useGenerate'

function Table4x4(){

    const {theme} = useContext(ThemeContext)
    const {data, changeData} = useContext(TableGenerate)

    const [result, setResult] = useState(false)
    const [error, setError] = useState("")

    useEffect(() => {
        if (data != "") {
            setResult(!result)
        }
    }, [])
    

    /* *********************** Entrepôts ***************************** */


    const entrepot1Ref = useRef("")
    const entrepot2Ref = useRef("")
    const entrepot3Ref = useRef("")
    const entrepot4Ref = useRef("")


    /* *********************** Clients ***************************** */


    const client1Ref = useRef("")
    const client2Ref = useRef("")
    const client3Ref = useRef("")
    const client4Ref = useRef("")


    /****************************  Les coûts  *************************/



    const cout1Ref = useRef("")
    const cout2Ref = useRef("")
    const cout3Ref = useRef("")
    const cout4Ref = useRef("")
    const cout5Ref = useRef("")
    const cout6Ref = useRef("")
    const cout7Ref = useRef("")
    const cout8Ref = useRef("")
    const cout9Ref = useRef("")
    const cout10Ref = useRef("")
    const cout11Ref = useRef("")
    const cout12Ref = useRef("")
    const cout13Ref = useRef("")
    const cout14Ref = useRef("")
    const cout15Ref = useRef("")
    const cout16Ref = useRef("")



    /***************************  Quantités stockées  *************************** */
    
    const quantiteStocke1Ref = useRef("")
    const quantiteStocke2Ref = useRef("")
    const quantiteStocke3Ref = useRef("")
    const quantiteStocke4Ref = useRef("")


    /***************************  Quantités demandés  *************************** */
    
    const quantitedemande1Ref = useRef("")
    const quantitedemande2Ref = useRef("")
    const quantitedemande3Ref = useRef("")
    const quantitedemande4Ref = useRef("")


    /****************************************************************** */

    const handleClick = async() => {
        const data = {
            tableEntrepots: [
                entrepot1Ref.current.value.trim(),
                entrepot2Ref.current.value.trim(),
                entrepot3Ref.current.value.trim(),
                entrepot4Ref.current.value.trim(),
            ],
            tableCouts: [
                [
                parseInt(cout1Ref.current.value.trim()),
                parseInt(cout2Ref.current.value.trim()),
                parseInt(cout3Ref.current.value.trim()),
                parseInt(cout4Ref.current.value.trim()),
                ],
                [
                parseInt(cout5Ref.current.value.trim()),
                parseInt(cout6Ref.current.value.trim()),
                parseInt(cout7Ref.current.value.trim()),
                parseInt(cout8Ref.current.value.trim()),
                ],
                [
                parseInt(cout9Ref.current.value.trim()),
                parseInt(cout10Ref.current.value.trim()),
                parseInt(cout11Ref.current.value.trim()),
                parseInt(cout12Ref.current.value.trim()),
                ],
                [
                parseInt(cout13Ref.current.value.trim()),
                parseInt(cout14Ref.current.value.trim()),
                parseInt(cout15Ref.current.value.trim()),
                parseInt(cout16Ref.current.value.trim()),
                ],
            ],
            tableClients: [
                client1Ref.current.value.trim(),
                client2Ref.current.value.trim(),
                client3Ref.current.value.trim(),
                client4Ref.current.value.trim(),
            ],
            tableQuantiteDemande: [
                parseInt(quantitedemande1Ref.current.value.trim()),
                parseInt(quantitedemande2Ref.current.value.trim()),
                parseInt(quantitedemande3Ref.current.value.trim()),
                parseInt(quantitedemande4Ref.current.value.trim()),
            ],
            tableQuantiteStocke: [
                parseInt(quantiteStocke1Ref.current.value.trim()),
                parseInt(quantiteStocke2Ref.current.value.trim()),
                parseInt(quantiteStocke3Ref.current.value.trim()),
                parseInt(quantiteStocke4Ref.current.value.trim()),
            ],
        };


        try {
    
            const response = await axios.post('http://localhost:5000/solve', data)
            changeData(JSON.stringify(response.data))
            setResult(!result)
        } catch (error) {
            setError(error.response.data.error)
            setTimeout(()=>{
                setError('')
            },4000)
        }
    }

    

    return <DisBg>
        <Nav></Nav>
        {
            !result ? <div>
                <h3 className="my-3 mx-5">Veuillez compléter le tableau</h3>
                <div style={{display:'flex', justifyContent:'center'}}>
                    <div style={{display:'flex', justifyContent:'center', alignItems:'center'}}>
                        <div style={{display:'flex', justifyContent:'center', alignItems:'center', width:'30%'}}>
                            <h3>Entrepôts</h3>
                            <form action="" className='mx-2'>
                                <input type="text" ref={entrepot1Ref} className='form-control m-1 text-center' style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/>
                                <input type="text" ref={entrepot2Ref} className='form-control m-1 text-center' style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/>
                                <input type="text" ref={entrepot3Ref} className='form-control m-1 text-center' style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/>
                                <input type="text" ref={entrepot4Ref} className='form-control m-1 text-center' style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/>
                            </form>
                        </div>
                        <div style={{position:'absolute', top:'50px', right:'60px'}}>
                            {
                                error && <div style={{display:'flex', justifyContent:'center'}} className='m-1' >
                                            <p className='alert alert-warning text-center'>{error}</p>
                                        </div>
                            }
                        </div>
                        <div>
                            <div>
                                <h3 className='text-center'>Clients</h3>
                                <form action="" className='mx-2 d-flex'>
                                    <input type="text" ref={client1Ref} className='form-control mx-1 text-center' style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/>
                                    <input type="text" ref={client2Ref} className='form-control mx-1 text-center' style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/>
                                    <input type="text" ref={client3Ref} className='form-control mx-1 text-center' style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/>
                                    <input type="text" ref={client4Ref} className='form-control mx-1 text-center' style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/>
                                </form>
                            </div>
                            <table className='table' style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', margin:'0px'} : {backgroundColor:'white', transition:'0.6s', margin:'0px'}}> 
                                <tbody>
                                    <tr>
                                        <td style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s'} : {backgroundColor:'white', transition:'0.6s'}}><input type="text" ref={cout1Ref}  className="form-control text-center" style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/></td>
                                        <td style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s'} : {backgroundColor:'white', transition:'0.6s'}}><input type="text" ref={cout2Ref}  className="form-control text-center" style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/></td>
                                        <td style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s'} : {backgroundColor:'white', transition:'0.6s'}}><input type="text" ref={cout3Ref}  className="form-control text-center" style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/></td>
                                        <td style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s'} : {backgroundColor:'white', transition:'0.6s'}}><input type="text" ref={cout4Ref}  className="form-control text-center" style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/></td>
                                    </tr>
                                    <tr>
                                        <td style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s'} : {backgroundColor:'white', transition:'0.6s'}}><input type="text" ref={cout5Ref}  className="form-control text-center" style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/></td>
                                        <td style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s'} : {backgroundColor:'white', transition:'0.6s'}}><input type="text" ref={cout6Ref}  className="form-control text-center" style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/></td>
                                        <td style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s'} : {backgroundColor:'white', transition:'0.6s'}}><input type="text" ref={cout7Ref}  className="form-control text-center" style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/></td>
                                        <td style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s'} : {backgroundColor:'white', transition:'0.6s'}}><input type="text" ref={cout8Ref}  className="form-control text-center" style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/></td>
                                    </tr>
                                    <tr>
                                        <td style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s'} : {backgroundColor:'white', transition:'0.6s'}}><input type="text" ref={cout9Ref}  className="form-control text-center" style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/></td>
                                        <td style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s'} : {backgroundColor:'white', transition:'0.6s'}}><input type="text" ref={cout10Ref}  className="form-control text-center" style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/></td>
                                        <td style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s'} : {backgroundColor:'white', transition:'0.6s'}}><input type="text" ref={cout11Ref}  className="form-control text-center" style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/></td>
                                        <td style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s'} : {backgroundColor:'white', transition:'0.6s'}}><input type="text" ref={cout12Ref} className="form-control text-center" style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/></td>
                                    </tr>
                                    <tr>
                                        <td style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s'} : {backgroundColor:'white', transition:'0.6s'}}><input type="text" ref={cout13Ref}  className="form-control text-center" style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/></td>
                                        <td style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s'} : {backgroundColor:'white', transition:'0.6s'}}><input type="text" ref={cout14Ref}  className="form-control text-center" style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/></td>
                                        <td style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s'} : {backgroundColor:'white', transition:'0.6s'}}><input type="text" ref={cout15Ref}  className="form-control text-center" style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/></td>
                                        <td style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s'} : {backgroundColor:'white', transition:'0.6s'}}><input type="text" ref={cout16Ref}  className="form-control text-center" style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/></td>
                                    </tr>
                                </tbody>
                            </table>
                            <div>
                                <form action="" className='mx-2 d-flex'>
                                    <input type="text" ref={quantitedemande1Ref} className='form-control mx-1 text-center' style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/>
                                    <input type="text" ref={quantitedemande2Ref} className='form-control mx-1 text-center' style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/>
                                    <input type="text" ref={quantitedemande3Ref} className='form-control mx-1 text-center' style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/>
                                    <input type="text" ref={quantitedemande4Ref} className='form-control mx-1 text-center' style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/>
                                </form>
                                <h3 className='text-center my-1'>Quantités demandés</h3>
                            </div>
                        </div>
                        <div style={{display:'flex', justifyContent:'center', alignItems:'center', width:'30%'}}>
                            <form action="" className='mx-2'>
                                <input type="text" ref={quantiteStocke1Ref} className='form-control m-1 text-center' style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/>
                                <input type="text" ref={quantiteStocke2Ref} className='form-control m-1 text-center' style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/>
                                <input type="text" ref={quantiteStocke3Ref} className='form-control m-1 text-center' style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/>
                                <input type="text" ref={quantiteStocke4Ref} className='form-control m-1 text-center' style={theme == "dark" ? {backgroundColor:'rgb(41, 39, 39)', transition:'0.6s', color:'white'} : {backgroundColor:'white', transition:'0.6s', color:'black'}}/>
                            </form>
                            <h3 className='mx-2'>Quantités stockées</h3>
                        </div>
                    </div>
                </div>
                
                <div style={{display:'flex', justifyContent:'flex-end', marginRight:'40px'}}>
                    <button className="btn btn-warning" onClick={handleClick}>Générer la réponse</button>
                </div>
            </div> : <div>
                <Result></Result>
            </div>
        }
        
        
    </DisBg>
}



export default Table4x4