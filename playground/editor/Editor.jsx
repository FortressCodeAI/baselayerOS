import React from "react"

export function Editor({ value, onChange }) {
  return (
    <textarea
      className="editor-textarea"
      value={value}
      onChange={e => onChange(e.target.value)}
      spellCheck={false}
    />
  )
}
