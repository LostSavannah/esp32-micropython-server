import { BrowserRouter, Route, Routes } from "react-router"
import Layout from "./pages/Layout"
import ErrorPage from "./pages/ErrorPage"
import FilesPage from "./pages/FilesPage"
import DevicePage from "./pages/DevicePage"
import EmptyPage from "./pages/EmptyPage"



export default function App() {
  return <BrowserRouter>
    <Routes>
      <Route path="/" element={<Layout/>} errorElement={<ErrorPage/>}>
        <Route path="/" element={<EmptyPage/>}></Route>
        <Route path="/files" element={<FilesPage/>}></Route>
        <Route path="/device" element={<DevicePage/>}></Route>
      </Route>
    </Routes>
  </BrowserRouter>
}
