function convertCSVtoJSON(
  csv: string,
  headers: string,
  constants: { [x: string]: string } = {}
): { [x: string]: string }[] {
  const rows = csv.replace(/\r/g, "").split(/\n/)
  const keys = headers.split(",")
  let response: { [x: string]: string }[] = []
  for (const row of rows) {
    // https://stackoverflow.com/a/39128144/295606
    const values = row.split(",")
    let rowObj = keys.reduce((o, k, i) => ({ ...o, [k]: values[i].trim() }), {})
    rowObj = Object.assign({}, rowObj, constants)
    response.push(rowObj)
  }
  // Remove duplicates
  // https://stackoverflow.com/a/53543030/295606
  response = response.filter(
    (
      (s) => (o) =>
        ((k) => !s.has(k) && s.add(k))(keys.map((k) => o[k]).join("|"))
    )(new Set())
  )
  return response
}

function convertBlobToBase64(blob: File): Promise<string | ArrayBuffer | null> {
  // https://stackoverflow.com/a/18650249/295606
  // User like:
  //  let b64 = (await this.convertBlobToBase64(blob)) as string
  //  b64 = b64.substring(b64.indexOf(",") + 1) to get rid of ';base64,'
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.onloadend = () => resolve(reader.result)
    reader.readAsDataURL(blob)
  })
}

export {
  convertCSVtoJSON, convertBlobToBase64
}