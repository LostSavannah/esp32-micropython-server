import BaseHttpService, { Method, rawCallback } from "./BaseHttpService";

export class DeviceEsptoolService extends BaseHttpService{

    public async flashChip(){
        return this.send({
            url: "device/esptools/flash",
            method: Method.Post,
            callback: rawCallback
        })
    }

    public async uploadFirmware(){
        return this.send({
            url: "device/esptools/upload_firmware",
            method: Method.Post,
            callback: rawCallback
        })
    }
}