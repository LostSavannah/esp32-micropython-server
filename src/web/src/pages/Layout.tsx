import { Link, Outlet } from "react-router";

export default function Layout() {
  let links = [
    {
      text: "Files",
      location: "/files"
    },
    {
      text: "Device",
      location: "/device"
    }
  ];
  return (
    <div className="vh-100 d-flex flex-column bg-dark text-white p-0">
      <div className="w-100 p-1 bg-black">
        esp32-micropython-server
      </div>
      <div className="w-100 p-1 bg-black">
          {links.map(l => <Link className="badge" id={l.location} to={l.location}>{l.text}</Link>)}
      </div>
      <div className="h-100 d-flex flex-row">
        <Outlet/>
      </div>
      <div className="w-100 bg-primary">
        ...
      </div>
    </div>
  )
}
