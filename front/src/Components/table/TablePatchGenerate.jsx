import React, { useContext, useEffect, useRef, useState } from "react";
import DisBg from "../DisBg";
import Nav from "../Nav";
import { ThemeContext } from "../../Context/useTheme";
import { TableGenerate } from "../../Context/useGenerate";
import axios from "axios";
import Result from "../Result/Result";

export default function TablePatchGenerate() {
  const { theme } = useContext(ThemeContext);
  const { column, row, data, changeData } = useContext(TableGenerate);

  const [result, setResult] = useState(false);
  const [error, setError] = useState("");

  const nbCout = column * row;

  let x = [];
  let d = [];

  useEffect(() => {
    if (data != "") {
      setResult(!result);
    }
  }, []);

  // Génération des valeurs

  const clientRefs = Array.from({ length: column }).map(() => useRef(""));
  const entrepotRefs = Array.from({ length: row }).map(() => useRef(""));
  const quantitedemandeRefs = Array.from({ length: column }).map(() =>
    useRef("")
  );
  const quantitestockeRefs = Array.from({ length: row }).map(() => useRef(""));

  let coutRefs = Array.from({ length: nbCout }).map(() => {
    x.push(useRef(""));
    if (x.length == column) {
      d = x;
      x = [];
      return d;
    }
  });

  coutRefs = coutRefs.filter((data) => data !== undefined);

  console.log(coutRefs);

  // for (let index = 0; index < nbCout ; index++) {

  //     x.push(useRef(null))

  //     if(x.length == column){
  //         tableCouts.push(x)
  //         x = []
  //     }
  // }

  /************************************** */

  let tableCouts = [];
  let tableEntrepots = [];
  let tableClients = [];
  let tableQuantiteDemande = [];
  let tableQuantiteStocke = [];

  const handleClick = async (e) => {
    e.preventDefault();
    let a = [];
    for (let data of coutRefs) {
      for (let x of data) {
        a.push(parseInt(x.current.value));
      }
      if (tableCouts.length != row) {
        tableCouts.push(a);
        a = [];
      }
    }

    for (let data in entrepotRefs) {
      tableQuantiteStocke.push(
        parseInt(quantitestockeRefs[data].current.value)
      );
      tableEntrepots.push(entrepotRefs[data].current.value);
    }

    for (let data in clientRefs) {
      tableQuantiteDemande.push(
        parseInt(quantitedemandeRefs[data].current.value)
      );
      tableClients.push(clientRefs[data].current.value);
    }

    const data1 = {
      tableCouts: tableCouts,
      tableClients: tableClients,
      tableEntrepots: tableEntrepots,
      tableQuantiteDemande: tableQuantiteDemande,
      tableQuantiteStocke: tableQuantiteStocke,
    };

    try {
      const response = await axios.post("http://localhost:5000/solve", data1);
      console.log(response);
      changeData(JSON.stringify(response.data));
      setResult(true);
    } catch (error) {
      console.log(error);
      setError(error.response.data.error);
      setTimeout(() => {
        setError("");
      }, 3000);
      tableClients = [];
      tableCouts = [];
      tableEntrepots = [];
      tableQuantiteDemande = [];
      tableQuantiteStocke = [];
    }

    // console.log('table quantité demandé: ',tableQuantiteDemande)
    // console.log('table quantité stocké : ',tableQuantiteStocke)
    // console.log('table client : ',tableClients)
    // console.log('table entrepôt : ',tableEntrepots)
    // console.log('table coûts : ',tableCouts)
  };

  /********************************************** */
  return (
    <DisBg>
      <Nav></Nav>
      {!result ? (
        <div className="px-6 py-6">
          <h3 className="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-100 text-center">
            Veuillez compléter le tableau
          </h3>

          {error && (
            <div className="flex justify-center mb-4">
              <p className="alert alert-warning text-center text-sm">{error}</p>
            </div>
          )}

          <div className="flex flex-col lg:flex-row justify-center items-center gap-6">
            {/* Entrepôts */}
            <div className="w-full max-w-xs">
              <h4 className="text-lg font-semibold mb-2 text-center dark:text-white">
                Entrepôts
              </h4>
              <form className="space-y-2">
                {entrepotRefs.map((ref, index) => (
                  <input
                    key={index}
                    ref={ref}
                    type="text"
                    className={`w-full text-center my-2 px-3 py-2 rounded-md ${theme == "dark" ? "text-white bg-gray-600" : "text-black bg-gray-200 "} shadow-sm focus:outline-none focus:ring-2 focus:ring-yellow-500`}
                  />
                ))}
              </form>
            </div>

            {/* Tableau des coûts + clients */}
            <div className="flex flex-col items-center w-full overflow-x-auto">
              <h4 className="text-lg font-semibold mb-2 text-center dark:text-white">
                Clients
              </h4>
              <form className="flex gap-2 mb-4">
                {clientRefs.map((ref, index) => (
                  <input
                    key={index}
                    ref={ref}
                    type="text"
                    className={`w-20 text-center px-2 py-2 ${theme == "dark" ? "text-white bg-gray-600" : "text-black bg-gray-200 "} rounded-md shadow-sm focus:outline-none`}
                  />
                ))}
              </form>

              {/* Matrice des coûts */}
              <table className="table-auto border-collapse">
                <tbody>
                  {coutRefs.map((row, i) => (
                    <tr key={i}>
                      {row.map((ref, j) => (
                        <td key={j} className="p-1">
                          <input
                            ref={ref}
                            type="text"
                            className={`w-20 text-center px-2 py-2 ${theme == "dark" ? "text-white bg-gray-600" : "text-black bg-gray-200 "} rounded-md shadow-sm focus:outline-none`}
                          />
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>

              {/* Quantité demandée */}
              <form className="flex gap-2 mt-3">
                {quantitedemandeRefs.map((ref, index) => (
                  <input
                    key={index}
                    ref={ref}
                    type="text"
                    className={`w-20 text-center px-2 py-2 ${theme == "dark" ? "text-white bg-gray-600" : "text-black bg-gray-200 "} rounded-md shadow-sm focus:outline-none`}
                  />
                ))}
              </form>
              <h4 className="text-lg font-semibold mb-2 text-center dark:text-white">
                Quantités demandés
              </h4>
            </div>

            {/* Quantité stockée */}
            <div className="w-full max-w-xs">
              <h4 className="text-lg font-semibold mb-2 text-center dark:text-white">
                Quantités stockées
              </h4>
              <form className="space-y-2">
                {quantitestockeRefs.map((ref, index) => (
                  <input
                    key={index}
                    ref={ref}
                    type="text"
                    className={`w-full text-center my-2 px-3 py-2 rounded-md ${theme == "dark" ? "text-white bg-gray-600" : "text-black bg-gray-200 "} shadow-sm focus:outline-none focus:ring-2 focus:ring-yellow-500`}
                  />
                ))}
              </form>
            </div>
          </div>

          {/* Bouton de génération */}
          <div className="mt-6 flex justify-end">
            <button
              className={`btn-starting block mb-2 font-medium text-sm tracking-wide  px-3 py-2 transition-all ${theme == 'dark' ? "text-white" : "text-gray-800"}`}
              onClick={handleClick}
            >
              Générer la réponse
            </button>
          </div>
        </div>
      ) : (
        <Result />
      )}
    </DisBg>
  );
}
