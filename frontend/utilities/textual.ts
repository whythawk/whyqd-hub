import { createAvatar } from "@dicebear/core"
import * as bottts from "@dicebear/bottts"
import { IMimeType } from "@/interfaces"

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
  readableDate, capitalizeFirst, nameSpace, splitWordify, getMimeType, getAvatar
}