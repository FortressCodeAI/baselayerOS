import React from "react"

export function Preview({ element }) {
  if (!element) {
    return <div className="preview-empty">No valid UI rendered yet.</div>
  }

  return <div className="preview-surface">{element}</div>
}
