import React from "react"
import { createRoot } from "react-dom/client"
import { Playground } from "./Playground"
import "./styles.css"

const root = createRoot(document.getElementById("root"))
root.render(<Playground />)
