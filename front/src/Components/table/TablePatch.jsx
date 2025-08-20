import { useContext, useState } from "react"
import DisBg from "../DisBg"
import Nav from "../Nav"
import { TableGenerate } from "../../Context/useGenerate"
import { ThemeContext } from "../../Context/useTheme"
import { useNavigate } from "react-router-dom"
import { motion } from "framer-motion"

function TablePatch() {
  const { theme } = useContext(ThemeContext)
  const { changeTableGenerate, column, row } = useContext(TableGenerate)

  const [rowTable, setRowTable] = useState(row)
  const [columnTable, setColumnTable] = useState(column)

  const navigate = useNavigate()

  const handleNavigate = (link) => {
    navigate(link)
  }

  const handleGenerate = (e) => {
    e.preventDefault()
    changeTableGenerate(rowTable, columnTable)
    handleNavigate("tablePatchGenerate")
  }

  const isDark = theme === "dark"

  return (
    <DisBg>
      <Nav />

      <div className="max-w-xl mx-auto py-12 px-6">
        <h3 className="text-3xl font-bold mb-8 text-center font-sans text-gray-800 dark:text-gray-100">
          Tableau personnalisé
        </h3>

        <motion.form
          onSubmit={handleGenerate}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className={`rounded-2xl shadow-xl p-8 transition-all duration-500 ${
            isDark
              ? "bg-zinc-800 border border-zinc-700 text-white"
              : "bg-white border border-gray-200 text-gray-800"
          }`}
        >
          {/* Ligne */}
          <div className="mb-6">
            <label
              htmlFor="rows"
              className="block mb-2 font-medium text-sm tracking-wide"
            >
              Nombre de lignes
            </label>
            <input
              id="rows"
              type="number"
              min={3}
              max={8}
              required
              value={rowTable}
              onChange={(e) => setRowTable(e.target.value)}
              className={`w-full px-4 py-2 rounded-md shadow-sm border text-sm outline-none focus:ring-2 ${
                isDark
                  ? "bg-zinc-700 border-zinc-600 text-white focus:ring-yellow-500"
                  : "bg-gray-50 border-gray-300 text-gray-800 focus:ring-yellow-400"
              }`}
            />
          </div>

          {/* Colonne */}
          <div className="mb-6">
            <label
              htmlFor="columns"
              className="block mb-2 font-medium text-sm tracking-wide"
            >
              Nombre de colonnes
            </label>
            <input
              id="columns"
              type="number"
              min={3}
              max={8}
              required
              value={columnTable}
              onChange={(e) => setColumnTable(e.target.value)}
              className={`w-full px-4 py-2 rounded-md shadow-sm border text-sm outline-none focus:ring-2 ${
                isDark
                  ? "bg-zinc-700 border-zinc-600 text-white focus:ring-yellow-500"
                  : "bg-gray-50 border-gray-300 text-gray-800 focus:ring-yellow-400"
              }`}
            />
          </div>

          {/* Bouton */}
          <div className="flex justify-end">
            <button
              type="submit"
              className={`btn-starting block mb-2 font-medium text-sm tracking-wide  px-3 py-2 transition-all ${theme == 'dark' ? "text-white" : "text-gray-800"}`}
            >
              Générer le tableau
            </button>
          </div>
        </motion.form>
      </div>
    </DisBg>
  )
}

export default TablePatch
