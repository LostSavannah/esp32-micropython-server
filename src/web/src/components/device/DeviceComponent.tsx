import ActionCard from "../../shared/components/ActionCard";

export default function DeviceComponent() {
  return <div className="card m-2 p-1 bg-dark text-white w-100">
  <div className="card-title">Device</div>
  <ActionCard 
    title="Reset"
    description="Resets the device"
    action={() => {}}
    kind="success"
  />
  <ActionCard 
    title="Flash device"
    description="Flash the device's ROM"
    action={() => {}}
    kind="danger"
  />
  <ActionCard 
    title="Upload micropython"
    description="Loads micropython into the ROM"
    action={() => {}}
    kind="danger"
  />
  </div>
}
