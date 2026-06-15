import React from "react"

export function Action({ children, label, style = "primary-core" }) {
  const text = label || children
  return <button className={`action-btn action-${style}`}>{text}</button>
}
