import React from "react"
import { Panel } from "./components/Panel"
import { Field } from "./components/Field"
import { Metric } from "./components/Metric"
import { Action } from "./components/Action"

const COMPONENTS = {
  screen: ({ children }) => <div className="screen">{children}</div>,
  panel: Panel,
  field: Field,
  metric: Metric,
  action: Action,
}

export function renderAST(node) {
  const Component = COMPONENTS[node.type]
  if (!Component) {
    return <div className="unknown-node">Unknown primitive: {node.type}</div>
  }

  const children = (node.children || []).map((child, i) => (
    <React.Fragment key={i}>{renderAST(child)}</React.Fragment>
  ))

  return <Component {...node.attributes}>{children}</Component>
}
