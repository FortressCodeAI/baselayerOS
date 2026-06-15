import * as Components from "./components"

export function renderAST(node) {
  const Component = Components[node.type]

  if (!Component) {
    return <div>Unknown primitive: {node.type}</div>
  }

  const children = node.children?.map(renderAST)

  return (
    <Component {...node.attributes}>
      {children}
    </Component>
  )
}
