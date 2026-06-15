export function generateReact(ast) {
  const renderNode = (node) => {
    const props = Object.entries(node.attributes)
      .map(([k, v]) => `${k}="${v}"`)
      .join(" ")

    const children = node.children.map(renderNode).join("\n")

    return `<${node.type} ${props}>${children}</${node.type}>`
  }

  return `
import React from "react"
import { Panel, Field, Action, List, Metric } from "../ui/renderer/components"

export default function Generated() {
  return (
    <>
      ${renderNode(ast)}
    </>
  )
}
`
}
