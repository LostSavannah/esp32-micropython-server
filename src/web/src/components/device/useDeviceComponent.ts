import { useState } from "react";
import { DeviceEsptoolService } from "../../services/DeviceEsptoolService";

export enum DeviceFlashState {
    None = 0,
    Pending = 1,
    Success = 2,
    Failure = 3
}

export function useDeviceComponent(){
    const [deviceFlashState, setDeviceFlashState] = useState<DeviceFlashState>(DeviceFlashState.None);
    
    const service = new DeviceEsptoolService("");

    function flashChip(){
        setDeviceFlashState(DeviceFlashState.Pending);
        service.flashChip()
            .then(() => setDeviceFlashState(DeviceFlashState.Success))
            .catch(() => setDeviceFlashState(DeviceFlashState.Failure));
    }

    return {
        deviceFlashState,
        flashChip
    }
}