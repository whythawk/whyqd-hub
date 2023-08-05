import type { NuxtI18nOptions } from "@nuxtjs/i18n"
import type { DateTimeFormats, NumberFormats, PluralizationRule, PluralizationRules } from "@intlify/core-base"
import type { LocaleObject } from "#i18n"

interface LocaleObjectData extends LocaleObject {
  numberFormats?: NumberFormats
  dateTimeFormats?: DateTimeFormats
  pluralRule?: PluralizationRule
}

export const countryLocaleVariants: Record<string, (LocaleObjectData & { country?: boolean })[]> = {}

const locales: LocaleObjectData[] = [
  {
    code: "en",
    file: "en.json",
    name: "English",
  },
  {
    code: "fr-FR",
    file: "fr-FR.json",
    name: "Français",
  },
]

function buildLocales() {
  const useLocales = Object.values(locales).reduce((acc, data) => {
    const locales = countryLocaleVariants[data.code]
    if (locales) {
      locales.forEach((l) => {
        const entry: LocaleObjectData = {
          ...data,
          code: l.code,
          name: l.name,
          files: [data.file!, `${l.code}.json`],
        }
        delete entry.file
        acc.push(entry)
      })
    }
    else {
      acc.push(data)
    }
    return acc
  }, <LocaleObjectData[]>[])

  return useLocales.sort((a, b) => a.code.localeCompare(b.code))
}

export const currentLocales = buildLocales()

const datetimeFormats = Object.values(currentLocales).reduce((acc, data) => {
  const dateTimeFormats = data.dateTimeFormats
  if (dateTimeFormats) {
    acc[data.code] = { ...dateTimeFormats }
    delete data.dateTimeFormats
  }
  else {
    acc[data.code] = {
      shortDate: {
        dateStyle: "short",
      },
      short: {
        dateStyle: "short",
        timeStyle: "short",
      },
      long: {
        dateStyle: "long",
        timeStyle: "medium",
      },
    }
  }

  return acc
}, <DateTimeFormats>{})

const numberFormats = Object.values(currentLocales).reduce((acc, data) => {
  const numberFormats = data.numberFormats
  if (numberFormats) {
    acc[data.code] = { ...numberFormats }
    delete data.numberFormats
  }
  else {
    acc[data.code] = {
      percentage: {
        style: "percent",
        maximumFractionDigits: 1,
      },
      smallCounting: {
        style: "decimal",
        maximumFractionDigits: 0,
      },
      kiloCounting: {
        notation: "compact",
        compactDisplay: "short",
        maximumFractionDigits: 1,
      },
      millionCounting: {
        notation: "compact",
        compactDisplay: "short",
        maximumFractionDigits: 2,
      },
    }
  }

  return acc
}, <NumberFormats>{})

const pluralRules = Object.values(currentLocales).reduce((acc, data) => {
  const pluralRule = data.pluralRule
  if (pluralRule) {
    acc[data.code] = pluralRule
    delete data.pluralRule
  }

  return acc
}, <PluralizationRules>{})

export const i18n: NuxtI18nOptions = {
  locales: currentLocales,
  lazy: true,
  strategy: "no_prefix",
  detectBrowserLanguage: false,
  langDir: "locales",
  defaultLocale: "en",
  vueI18n: {
    availableLocales: currentLocales.map(l => l.code),
    fallbackLocale: "en",
    fallbackWarn: false,
    missingWarn: false,
    datetimeFormats,
    numberFormats,
    pluralRules,
  },
}