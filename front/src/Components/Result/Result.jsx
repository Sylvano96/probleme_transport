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
    if (data !== "") {
      try {
        const parsedData = JSON.parse(data)
        // Adapter la structure de la réponse Flask pour inclure toutes les itérations
        const formattedData = {
          initial: {
            solution_table: parsedData[0]?.tableau || [],
            solution_base_cost: parsedData[0]?.solution_base || 0,
            initial_assignments: parsedData[0]?.direction_client.map(item => ({
              source: item[0],
              destination: item[1],
              amount: parsedData[0].tableau[entrepots.indexOf(item[0])][clients.indexOf(item[1])] || 0
            })) || []
          },
          iterations: parsedData.slice(1).map((iteration, index) => ({
            iteration_number: index + 1,
            solution_table: iteration.tableau || [],
            solution_base_cost: iteration.solution_base || 0,
            initial_assignments: iteration.direction_client.map(item => ({
              source: item[0],
              destination: item[1],
              amount: iteration.tableau[entrepots.indexOf(item[0])][clients.indexOf(item[1])] || 0
            })) || []
          }))
        }
        // Filtrer les itérations pour éviter les redondances
        const uniqueIterations = formattedData.iterations.filter((iteration, index, self) =>
          index === self.findIndex((t) => 
            JSON.stringify(t.solution_table) === JSON.stringify(iteration.solution_table) &&
            JSON.stringify(t.initial_assignments) === JSON.stringify(iteration.initial_assignments)
          )
        );
        formattedData.iterations = uniqueIterations;
        setDataResult(formattedData)
      } catch (error) {
        console.error("Failed to parse data from context:", error)
        setDataResult({})
      }
    }
  }, [data])

  // Définir entrepots et clients comme variables globales (à adapter selon votre contexte)
  const entrepots = ['A', 'B', 'C', 'D'] // Remplacez par la logique pour obtenir ces valeurs dynamiquement si nécessaire
  const clients = ['1', '2', '3', '4', '5', '6'] // Remplacez par la logique pour obtenir ces valeurs dynamiquement si nécessaire

  console.log('Result en Json dans dataResult : ', dataResult)

  const handleRemove = () => {
    changeData("")
  }

  useEffect(() => {
    const timer = setTimeout(() => {
      setEtat(false)
    }, 2000)

    return () => clearTimeout(timer)
  }, [])

  const textColorClass = theme === 'dark' ? 'text-white' : 'text-dark'
  const tableBgClass = theme === 'dark' ? 'bg-dark text-white' : 'bg-white text-dark'
  const buttonVariant = theme === 'dark' ? 'btn-outline-warning' : 'btn-warning'

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
                {dataResult.initial?.solution_table && dataResult.initial.solution_table.length > 0 ? (
                  <div className={`table-responsive rounded shadow ${tableBgClass}`}>
                    <table className="table mb-0">
                      <tbody>
                        {dataResult.initial.solution_table.map((row, rowIndex) => (
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
                <h4 className={`fs-5 fw-bold mb-3 ${textColorClass}`}>
                  Solution de base : <span className="badge bg-success">{dataResult.initial?.solution_base_cost || 0}</span>
                </h4>
                
                <h4 className={`fs-5 fw-bold mb-3 mt-4 ${textColorClass}`}>
                  Assignation de chaque entrepôt vers les clients
                </h4>
                <div className="list-group">
                  {dataResult.initial?.initial_assignments?.length > 0 ? (
                    dataResult.initial.initial_assignments.map((assignment, index) => (
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
              {dataResult.iterations && dataResult.iterations.length > 0 ? (
                dataResult.iterations.map((iteration, index) => (
                  <div key={index} className="col-12 mb-4">
                    <h4 className={`fs-5 fw-bold mb-3 ${textColorClass}`}>
                      Itération {iteration.iteration_number}
                    </h4>
                    <div className="row">
                      {/* Table after Stepping Stone for this iteration */}
                      <div className="col-md-6">
                        <h5 className={`fs-6 fw-bold mb-3 ${textColorClass}`}>
                          Tableau après itération
                        </h5>
                        {iteration.solution_table && iteration.solution_table.length > 0 ? (
                          <div className={`table-responsive rounded shadow ${tableBgClass}`}>
                            <table className="table mb-0">
                              <tbody>
                                {iteration.solution_table.map((row, rowIndex) => (
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
                          <p className={`alert alert-info ${textColorClass}`}>Aucune donnée de tableau pour cette itération.</p>
                        )}
                      </div>

                      {/* Cost and Assignments for this iteration */}
                      <div className="col-md-5">
                        <h5 className={`fs-6 fw-bold mb-3 ${textColorClass}`}>
                          Coût après itération : <span className="badge bg-primary">{iteration.solution_base_cost || 0}</span>
                        </h5>
                        <h5 className={`fs-6 fw-bold mb-3 mt-4 ${textColorClass}`}>
                          Assignations
                        </h5>
                        <div className="list-group">
                          {iteration.initial_assignments.length > 0 ? (
                            iteration.initial_assignments.map((assignment, idx) => (
                              <div
                                key={idx}
                                className={`list-group-item d-flex align-items-center justify-content-between ${tableBgClass} ${textColorClass}`}
                              >
                                <span className="me-2">
                                  Entrepôt <strong className="text-primary">{assignment.source}</strong> vers Client{' '}
                                  <strong className="text-info">{assignment.destination}</strong>
                                </span>
                                <span className="d-flex align-items-center">
                                  Coût <FaArrowRightLong className="mx-2" />{' '}
                                  <span className="badge bg-dark mx-2">{assignment.amount}</span>
                                </span>
                              </div>
                            ))
                          ) : (
                            <p className={`alert alert-info ${textColorClass}`}>Aucune assignation pour cette itération.</p>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <p className={`alert alert-info ${textColorClass}`}>Aucune itération de Stepping Stone à afficher.</p>
              )}
            </div>
          </section>
        </div>
      )}
    </DisBg>
  )
}