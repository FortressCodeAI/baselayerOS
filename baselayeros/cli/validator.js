import primitives from "../ui/primitives/index.js"
import grammar from "../ui/grammar/index.js"

export function validateAST(ast) {
  const primitive = primitives[ast.type]
  if (!primitive) throw new Error(`Unknown primitive: ${ast.type}`)

  const rules = grammar[ast.type]
  if (!rules) return

  // Validate children
  for (const child of ast.children) {
    if (!rules.children.allowed.includes(child.type)) {
      throw new Error(`${ast.type} cannot contain ${child.type}`)
    }
    validateAST(child)
  }
}
