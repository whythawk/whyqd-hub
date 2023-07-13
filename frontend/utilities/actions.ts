import {
  IActionModifierType,
  IActionModel,
} from "@/interfaces"

function convertSelectArrayToScript(term: [string, IActionModifierType, string][]): string {
  let scriptTerms: string[] = []
  for (const chunk of term) {
    scriptTerms.push(`'${chunk[0]}' ${chunk[1]} '${chunk[2]}'`)
  }
  return `${scriptTerms.map( x => x)}`
}

function convertCalculateArrayToScript(term: [IActionModifierType, string][]): string {
  let scriptTerms: string[] = []
  for (const chunk of term) {
    scriptTerms.push(`${chunk[0]} '${chunk[1]}'`)
  }
  return `${scriptTerms.map( x => x)}`
}

function convertActionModelToScript(m: IActionModel): string | null {
  switch (m.action) {
    case "CALCULATE":
      // "CALCULATE > 'destination_field' < [modifier 'source_field', modifier 'source_field', etc]"
      // @ts-ignore
      return `${m.action} > '${m.destinationField}' < [${convertCalculateArrayToScript(m.sourceField)}]`
    case "CATEGORISE":
      // "CATEGORISE > 'destination_field'::'destination_term' < 'source_field'::['source_term']"
      // @ts-ignore
      const dTerm = m.sourceTerm.map( x => `'${x}'`)
      // @ts-ignore
      return `${m.action} > '${m.destinationField}' < '${m.sourceField}'::[${dTerm}]`
    case "DEBLANK":
      // "DEBLANK"
      return `${m.action}`
    case "DEDUPE":
      // "DEDUPE"
      return `${m.action}`
    case "DELETE_ROWS":
      // "DELETE_ROWS < [int, int, int, etc.]"
      if (m.rows) return `${m.action} < [${m.rows}]`
    case "NEW":
      // "NEW > 'destination_field' < ['value']"
      if (m.destinationField && m.sourceTerm)
        return `${m.action} > '${m.destinationField}' < ['${m.sourceTerm}']`
    case "PIVOT_CATEGORIES":
      // "PIVOT_CATEGORIES > 'destination_field' < 'source_field'::[int, int, int, etc.]"
      if (m.destinationField && m.sourceField && m.rows)
        // @ts-ignore
        return `${m.action} > '${m.destinationField}' < '${m.sourceField}'::[${m.rows}]`
    case "PIVOT_LONGER":
      // "PIVOT_LONGER > ['name_field', 'value_field'] < ['source_field', 'source_field', etc.]"
      if (Array.isArray(m.destinationField) && Array.isArray(m.sourceField)) {
        const dTerm = m.destinationField.map( x => `'${x}'`)
        const sTerm = m.sourceField.map( x => `'${x}'`)
        return `${m.action} > [${dTerm}] < [${sTerm}]`
      }
    case "RENAME":
      // "RENAME > 'destination_field' < ['source_field']"
      if (m.destinationField && !Array.isArray(m.destinationField) && m.sourceField)
        // @ts-ignore
        return `${m.action} > '${m.destinationField}' < ['${m.sourceField}']`
    case "SELECT":
      // "SELECT > 'destination_field' < ['source_field', 'source_field', etc.]"
      if (m.destinationField && !Array.isArray(m.destinationField) && Array.isArray(m.sourceField)) {
        const sTerm = m.sourceField.map( x => `'${x}'`)
        return `${m.action} > '${m.destinationField}' < [${sTerm}]`
      }
    case "SELECT_NEWEST":
      // "SELECT_NEWEST > 'destination_field' < ['source_field' + 'source_field_date', 'source_field' + 'source_field_date', etc.]"
      if (m.destinationField && m.sourceField) 
        // @ts-ignore
        return `${m.action} > '${m.destinationField}' < [${convertSelectArrayToScript(m.sourceField)}]`
    case "SELECT_OLDEST":
      // "SELECT_OLDEST > 'destination_field' < ['source_field' + 'source_field_date', 'source_field' + 'source_field_date', etc.]"
      if (m.destinationField && m.sourceField) 
        // @ts-ignore
        return `${m.action} > '${m.destinationField}' < [${convertSelectArrayToScript(m.sourceField)}]`
    case "SEPARATE":
      // "SEPARATE > ['destination_field_1', 'destination_field_2', etc. ] < 'by'::['source_field']"
      if (Array.isArray(m.destinationField) && m.sourceField && m.sourceTerm) {
        const dTerm = m.destinationField.map( x => `'${x}'`) 
        // @ts-ignore
        return `${m.action} > [${dTerm}] < '${m.sourceTerm}'::['${m.sourceField}']`
      }
    case "UNITE":
      // "UNITE > 'destination_field' < 'by'::['source_field', 'source_field', etc.]"
      if (m.destinationField && !Array.isArray(m.destinationField) && Array.isArray(m.sourceField) && m.sourceTerm) {
        const sTerm = m.sourceField.map( x => `'${x}'`)
        return `${m.action} > '${m.destinationField}' < '${m.sourceTerm}'::[${sTerm}]`
      }
  }
  return null
}

function convertActionModelList(ms: IActionModel[]): string[] {
  let modelList = []
  for (const m of ms) {
    const script = convertActionModelToScript(m)
    if (script) modelList.push(script)
  }
  return modelList
}

export { convertActionModelToScript, convertActionModelList }