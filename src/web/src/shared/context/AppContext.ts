import { createContext, useContext } from "react"

export interface IAppContext{
    server:string,
    setServer:(server: string) => void
}

export const AppContext = createContext<IAppContext>({
    server: "",
    setServer(server:string){
        this.server = server;
    }
})

export const useAppContext = () => useContext(AppContext);