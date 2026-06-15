import React from "react"

export function ErrorPanel({ errors }) {
  if (!errors || errors.length === 0) {
    return <div className="errors-empty">No errors.</div>
  }

  return (
    <ul className="errors-list">
      {errors.map((err, i) => (
        <li key={i} className="error-item">
          {err}
        </li>
      ))}
    </ul>
  )
}
