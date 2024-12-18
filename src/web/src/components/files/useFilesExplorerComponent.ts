import { useEffect, useState } from "react";
import { DeviceAmpyService } from "../../services/DeviceAmpyService";
import { useAppContext } from "../../shared/context/AppContext";

export function useFilesExplorerComponents(){
    let context = useAppContext();

    let [files, setFiles] = useState<string[]>([]);
    const service = new DeviceAmpyService(context.server);
    
    useEffect(() => {
        service.listFiles(".")
            .then(values => setFiles(values))
    }, []);
    
    return {
        files
    }
}