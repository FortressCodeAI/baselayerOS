import React, { useState, useEffect } from "react"
import { Editor } from "./editor/Editor"
import { Preview } from "./preview/Preview"
import { ErrorPanel } from "./preview/ErrorPanel"
import { parseRegulus } from "../cli/parser"
import { validateAST } from "../cli/validator"
import { renderAST } from "../ui/renderer/renderAST"

const INITIAL_SOURCE = `
screen "dashboard" {
  title: "Control Room"
  style: fortress

  panel "SystemStatus" {
    frame: shield
    metric "Active Cases" { bind: stats.active_cases }
    metric "Awaiting Clarification" { bind: stats.awaiting }
    action "Open Grievances" {
      do: open.grievances()
      goto: grievances.list
      style: primary-core
    }
  }
}
`.trim()

export function Playground() {
  const [source, setSource] = useState(INITIAL_SOURCE)
  const [ast, setAst] = useState(null)
  const [errors, setErrors] = useState([])
  const [element, setElement] = useState(null)

  useEffect(() => {
    const handle = setTimeout(() => {
      try {
        const parsed = parseRegulus(source)
        validateAST(parsed)
        const rendered = renderAST(parsed)
        setAst(parsed)
        setElement(rendered)
        setErrors([])
      } catch (err) {
        setAst(null)
        setElement(null)
        setErrors([err.message || String(err)])
      }
    }, 80)

    return () => clearTimeout(handle)
  }, [source])

  return (
    <div className="playground-root">
      <div className="playground-header">
        <h1>Regulus Playground</h1>
        <span className="tag">Fortress UI Language</span>
      </div>

      <div className="playground-layout">
        <div className="playground-column editor-column">
          <div className="panel frame-battlement">
            <div className="panel-header">Editor</div>
            <Editor value={source} onChange={setSource} />
          </div>
        </div>

        <div className="playground-column preview-column">
          <div className="panel frame-shield">
            <div className="panel-header">Preview</div>
            <Preview element={element} />
          </div>

          <div className="panel frame-metal errors-panel">
            <div className="panel-header">Errors</div>
            <ErrorPanel errors={errors} />
          </div>
        </div>
      </div>
    </div>
  )
}
