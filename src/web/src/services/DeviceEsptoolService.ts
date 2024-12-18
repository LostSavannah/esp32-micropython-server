import BaseHttpService, { Method, rawCallback } from "./BaseHttpService";

export class DeviceEsptoolService extends BaseHttpService{

    constructor(baseUrl:string){
        super(`${baseUrl}/device/esptools`);
    }

    public async flashChip(){
        return this.send({
            url: "flash",
            method: Method.Post,
            callback: rawCallback
        })
    }

    public async uploadFirmware(){
        return this.send({
            url: "upload_firmware",
            method: Method.Post,
            callback: rawCallback
        })
    }

}