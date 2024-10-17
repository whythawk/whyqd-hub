import { createAvatar } from "@dicebear/core"
import * as bottts from "@dicebear/bottts"
import type { IMimeType } from "@/interfaces"

function readableDate(term: Date | string, showYear: boolean = true) {
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toLocaleDateString
  // https://stackoverflow.com/a/66590756/295606
  // https://stackoverflow.com/a/67196206/295606
  const readable = term instanceof Date ? term : new Date(term)
  const day = readable.toLocaleDateString("en-UK", { day: "numeric" })
  const month = readable.toLocaleDateString("en-UK", { month: "short" })
  if (showYear) {
    const year = readable.toLocaleDateString("en-UK", { year: "numeric" })
    return `${day} ${month} ${year}`
  }
  return `${day} ${month}`
}

function readableNumber(term: string | number, trunc: boolean = false): string {
  // https://stackoverflow.com/a/2901298/295606
  // https://stackoverflow.com/a/10601315/295606
  if (!term) return "n/a"
  if (typeof term === "string") term = parseInt(term)
  if (trunc && term >= 1000) {
    const suffixes: string[] = ["k", "m", "b", "t"]
    for (let suffixNum = suffixes.length - 1; suffixNum >= 0; suffixNum--) {
      const scale = Math.pow(10, (suffixNum + 1) * 3)
      if (scale <= term) {
        term = Math.floor((term * 10) / scale) / 10
        if (term === 1000 && suffixNum < suffixes.length - 1) {
          term = 1
          suffixNum++
        }
        return term + suffixes[suffixNum]
      }
    }
  }
  return term.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",")
}

function capitalizeFirst(term: string): string {
  return term.charAt(0).toUpperCase() + term.slice(1).toLowerCase();
}

function nameSpace(term: string): string {
  // https://stackoverflow.com/a/9364527/295606
  return term.toLowerCase().replaceAll(" ", "_").replace(/\W/g, "").replaceAll("_", "-")
}

function splitWordify(text: string): string {
  return text
    .split("_")
    .map((x) => capitalizeFirst(x))
    .join(" ")
}

function getMimeType(term: string) {
  const IMimeReference: { [key: string]: IMimeType } = {
    "text/csv": "CSV",
    "application/vnd.ms-excel": "XLS",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "XLSX",
    "application/vnd.apache.parquet": "PARQUET",
    "application/vnd.apache.feather": "FEATHER"
  }
  return IMimeReference[term]
}

async function getAvatar(term: string) {
  return await createAvatar(bottts, {
    seed: term,
    scale: 90,
    randomizeIds: true,
  }).toDataUri()
}

export {
  readableDate, readableNumber, capitalizeFirst, nameSpace, splitWordify, getMimeType, getAvatar
}