import React, { useContext } from 'react'
import { createBrowserRouter, RouterProvider, Outlet } from 'react-router-dom'
import Home from './Components/Home'
import Operation from './Components/Operation'
import { ThemeProvider } from './Context/useTheme'
import './App.css'
import Table4x4 from './Components/table/Table4x4'
import TablePatch from './Components/table/TablePatch'
import Result from './Components/Result/Result'
import {TableGenerateProvider } from './Context/useGenerate'
import TablePatchGenerate from './Components/table/TablePatchGenerate'

export default function App() {


  const routes = createBrowserRouter([
    {
      path:'/',
      element: <Home></Home> 
    },
    {
      path:'/operation',
      element: <Outlet></Outlet>,
      children:[
        {
          path:'',
          element: <Operation></Operation>
        },
        {
          path:'table4x4',
          element: <Table4x4></Table4x4>
        },
        {
          path:'tablePatch',
          element: <Outlet></Outlet>,
          children:[
            {
              path:'',
              element: <TablePatch></TablePatch>
            },
            {
              path:'tablePatchGenerate',
              element: <TablePatchGenerate></TablePatchGenerate>
            }
          ]
        }
      ]
    },
  ])


  return (
    <TableGenerateProvider>
      <ThemeProvider>
        <RouterProvider router={routes}/>
      </ThemeProvider>
    </TableGenerateProvider>
  )
}
