import { BrowserRouter, Route, Routes } from "react-router"
import Layout from "./pages/Layout"
import ErrorPage from "./pages/ErrorPage"
import FilesPage from "./pages/FilesPage"
import DevicePage from "./pages/DevicePage"
import EmptyPage from "./pages/EmptyPage"
import { AppContext } from "./shared/context/AppContext"
import { useState } from "react"



export default function App() {
  const [server, setServer] = useState<string>("http://192.168.100.44:8955");
  return <AppContext.Provider value={{server, setServer}}>
    <BrowserRouter>
    <Routes>
      <Route path="/" element={<Layout/>} errorElement={<ErrorPage/>}>
        <Route path="/" element={<EmptyPage/>}></Route>
        <Route path="/files" element={<FilesPage/>}></Route>
        <Route path="/device" element={<DevicePage/>}></Route>
      </Route>
    </Routes>
  </BrowserRouter>
  </AppContext.Provider> 
}
