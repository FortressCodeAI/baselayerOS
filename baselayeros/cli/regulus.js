#!/usr/bin/env node

import fs from "fs"
import path from "path"
import { parseRegulus } from "./parser.js"
import { validateAST } from "./validator.js"
import { generateReact } from "./react-generator.js"

const input = process.argv[2]

if (!input) {
  console.error("Usage: regulus <file.regulus>")
  process.exit(1)
}

const filePath = path.resolve(process.cwd(), input)
const source = fs.readFileSync(filePath, "utf8")

// 1. Parse
const ast = parseRegulus(source)

// 2. Validate
validateAST(ast)

// 3. Generate React
const output = generateReact(ast)

// 4. Write output
const outPath = filePath.replace(".regulus", ".jsx")
fs.writeFileSync(outPath, output)

console.log(`Generated: ${outPath}`)
