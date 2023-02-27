/** @type {import("tailwindcss").Config} */
// https://uicolors.app/create
// https://www.canva.com/colors/

module.exports = {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./nuxt.config.{js,ts}",
  ],
  theme: {
    extend: {
      colors: {
        ochre: {
          50: "#fdf8ed",
          100: "#f7ebce",
          200: "#efd598",
          300: "#e7bb62",
          400: "#e1a43e",
          500: "#cc7d24",
          600: "#c0651f",
          700: "#9f491e",
          800: "#823a1e",
          900: "#6b301c",
        },
        sienna: {
          50: "#fdf3f3",
          100: "#fde3e3",
          200: "#fbcdcd",
          300: "#f8a9aa",
          400: "#ef6061",
          500: "#e74c4d",
          600: "#d32f30",
          700: "#b12425",
          800: "#932122",
          900: "#7a2223",
        },
        eucalyptus: {
            50: "#f1fcf4",
            100: "#dff9e8",
            200: "#c0f2d0",
            300: "#8ee7ac",
            400: "#56d281",
            500: "#2fb85f",
            600: "#24a451",
            700: "#1e773d",
            800: "#1c5f35",
            900: "#194e2d",
        },
        cerulean: {
            50: "#f0faff",
            100: "#e0f5fe",
            200: "#b9ecfe",
            300: "#7cdefd",
            400: "#36cffa",
            500: "#0cb9eb",
            600: "#00a6df",
            700: "#0177a3",
            800: "#066486",
            900: "#0b526f",
        },
      },
    },
  },
  corePlugins: {
    aspectRatio: false,
  },
  plugins: [
    require("@tailwindcss/typography"),
    require("@tailwindcss/forms"),
    require("@tailwindcss/aspect-ratio"),
    require("@tailwindcss/line-clamp"),
  ],
}
