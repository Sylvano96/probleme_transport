import React, { useContext, useEffect, useState } from 'react'
import DisBg from '../DisBg'
import Spinner from '../Spinner'
import { TableGenerate } from '../../Context/useGenerate'
import { Link } from 'react-router-dom'
import { FaArrowRightLong, FaPencil } from 'react-icons/fa6'
import { ThemeContext } from '../../Context/useTheme'

export default function Result() {
  const [etat, setEtat] = useState(true)
  const [dataResult, setDataResult] = useState({})
  const { data, changeData } = useContext(TableGenerate)
  const { theme } = useContext(ThemeContext)

  useEffect(() => {
    if (data !== "") { // Changed from data != "" for strict equality
      try {
        setDataResult(JSON.parse(data))
      } catch (error) {
        console.error("Failed to parse data from context:", error)
        setDataResult({}) // Set to empty object on error
      }
    }
  }, [data]) // Added data to dependency array

  console.log('Result en Json dans dataResult : ', dataResult)

  const handleRemove = () => {
    changeData("")
  }

  // Use a proper cleanup for setTimeout if component unmounts before timeout
  useEffect(() => {
    const timer = setTimeout(() => {
      setEtat(false)
    }, 2000)

    return () => clearTimeout(timer) // Cleanup the timer
  }, [])

  const textColorClass = theme === 'dark' ? 'text-white' : 'text-dark';
  const tableBgClass = theme === 'dark' ? 'bg-dark text-white' : 'bg-white text-dark';
  const buttonVariant = theme === 'dark' ? 'btn-outline-warning' : 'btn-warning';

  return (
    <DisBg>
      {etat ? (
        <div className="d-flex justify-content-center align-items-center vh-50">
          <Spinner />
        </div>
      ) : (
        <div className="container py-4">
          {/* Header and Modify Button */}
          <div className="d-flex flex-wrap justify-content-between align-items-center mb-4">
            <h2 className="mb-0">Résultats des Opérations</h2>
            <Link
              to={'/operation'}
              className={`btn ${buttonVariant} d-flex align-items-center`}
              onClick={handleRemove}
            >
              MODIFIER <FaPencil className="ms-2" />
            </Link>
          </div>

          <hr className="my-4" />

          {/* MINITAB Section */}
          <section className="mb-5">
            <h3 className={`text-center mb-4 ${textColorClass}`}>MINITAB</h3>
            <div className="row g-4 justify-content-around align-items-start">
              {/* Table after minimization */}
              <div className="col-md-6">
                <h4 className={`fs-5 fw-bold mb-3 ${textColorClass}`}>
                  Tableau après minimalisation
                </h4>
                {dataResult[0]?.solution_table ? (
                  <div className={`table-responsive rounded shadow ${tableBgClass}`}>
                    <table className="table mb-0">
                      <tbody>
                        {dataResult[0].solution_table.map((row, rowIndex) => (
                          <tr key={rowIndex} className="text-center">
                            {row.map((cell, cellIndex) => (
                              <td key={cellIndex} className={`${tableBgClass}`}>
                                {cell}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <p className={`alert alert-info ${textColorClass}`}>Aucune donnée de tableau à afficher pour MINITAB.</p>
                )}
              </div>

              {/* Solution de base and Assignments */}
              <div className="col-md-5">
                <h4 className={`fs-5 fw-bold mb-3  ${textColorClass}`}>
                  Solution de base : <span className="badge bg-success">{dataResult[0]?.solution_base_cost}</span>
                </h4>
                
                <h4 className={`fs-5 fw-bold mb-3 mt-4 ${textColorClass}`}>
                  Assignation de chaque entrepôt vers les clients
                </h4>
                <div className="list-group">
                  {dataResult[0]?.initial_assignments?.length > 0 ? (
                    dataResult[0].initial_assignments.map((assignment, index) => (
                      <div 
                        key={index} 
                        className={`list-group-item d-flex align-items-center justify-content-between ${tableBgClass} ${textColorClass}`}
                      >
                        <span className="me-2">
                          Entrepôt <strong className="text-primary">{assignment.source}</strong> vers Client <strong className="text-info">{assignment.destination}</strong>
                        </span>
                        <span className="d-flex align-items-center">
                          Coût <FaArrowRightLong className="mx-2" /> <span className="badge bg-dark mx-2">{assignment.amount}</span>
                        </span>
                      </div>
                    ))
                  ) : (
                    <p className={`alert alert-info ${textColorClass}`}>Aucune assignation initiale à afficher.</p>
                  )}
                </div>
              </div>
            </div>
          </section>

          <hr className="my-4" />

          {/* Stepping Stone Algorithm Section */}
          <section className="mb-5">
            <h3 className={`text-center mb-4 ${textColorClass}`}>Algorithme de Stepping Stone</h3>
            <div className="row g-4 justify-content-around align-items-center">
              {/* Table after Stepping Stone */}
              <div className="col-md-6">
                <h4 className={`fs-5 fw-bold mb-3 ${textColorClass}`}>
                  Tableau après de l'algorithme de Stepping Stone
                </h4>
                {dataResult[1]?.optimal_solution_table ? (
                  <div className={`table-responsive rounded shadow ${tableBgClass}`}>
                    <table className="table mb-0">
                      <tbody>
                        {dataResult[1].optimal_solution_table.map((row, rowIndex) => (
                          <tr key={rowIndex} className="text-center">
                            {row.map((cell, cellIndex) => (
                              <td key={cellIndex} className={`${tableBgClass}`}>
                                {cell}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <p className={`alert alert-info ${textColorClass}`}>Aucune donnée de tableau à afficher pour Stepping Stone.</p>
                )}
              </div>

              {/* Optimal Solution */}
              <div className="col-md-5">
                <h4 className={`fs-5 fw-bold mb-3 ${textColorClass}`}>
                  Solution optimale trouvée : <span className="badge bg-primary">{dataResult[1]?.optimal_cost}</span>
                </h4>
              </div>
            </div>
          </section>
        </div>
      )}
    </DisBg>
  )
}