export interface ActionCardProps{
    title: string
    description: string
    action: () => void
    kind: "danger" | "success" | "warning" | "info" | "primary"
}

export default function ActionCard({title, description, action, kind}:ActionCardProps) {
  return <div className={`mb-1 text-white bg-dark border border-${kind} card d-flex flex-row align-items-center justify-content-between p-2`}>
    <div>
        <div><strong>{title}</strong></div>
        <div>{description}</div>
    </div>
    <button className={`btn btn-${kind}`} onClick={() => action()}>{title}</button>
  </div>
}
