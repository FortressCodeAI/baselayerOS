export function parseRegulus(source) {
  // Tokenize
  const tokens = source
    .replace(/\{/g, " { ")
    .replace(/\}/g, " } ")
    .split(/\s+/)
    .filter(Boolean)

  // Very simple recursive descent parser
  let index = 0

  function parseNode() {
    const type = tokens[index++]
    const id = tokens[index++].replace(/"/g, "")

    const node = { type, id, attributes: {}, children: [] }

    if (tokens[index] === "{") {
      index++
      while (tokens[index] !== "}") {
        if (tokens[index].match(/^[a-zA-Z]+$/)) {
          node.children.push(parseNode())
        } else {
          const key = tokens[index++]
          const value = tokens[index++].replace(/"/g, "")
          node.attributes[key] = value
        }
      }
      index++
    }

    return node
  }

  return parseNode()
}
