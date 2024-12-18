import BaseHttpService from "./BaseHttpService";

export class DeviceAmpyService extends BaseHttpService{

    constructor(baseUrl:string){
        super(`${baseUrl}/device/ampy`);
    }

    public async listFiles(path:string){
        return this.get<string[]>(`files/${path}`)
    }

}