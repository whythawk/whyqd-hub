import { defineRule, configure } from "vee-validate";
import { required, email, min, max, url, numeric } from "@vee-validate/rules";
import { localize } from "@vee-validate/i18n";

export default defineNuxtPlugin((nuxtApp) => {
  defineRule("required", required);
  defineRule("email", email);
  defineRule("min", min);
  defineRule("max", max);
  defineRule("url", url);
  defineRule("numeric", numeric);
  // @ts-ignore
  defineRule("confirmed", (value, [target], ctx) => {
    // https://vee-validate.logaretm.com/v4/guide/global-validators#cross-field-validation
    if (value === ctx.form[target]) {
      return true;
    }
    return "Passwords must match.";
  });
  // @ts-ignore
  defineRule("range", (value: string, [target], ctx) => {
    // https://vee-validate.logaretm.com/v4/guide/global-validators#cross-field-validation
    if (value < (ctx.form[target] as string)) {
      return true;
    }
    return "To date must be earlier.";
  });
  // @ts-ignore
  defineRule("numericRange", (value: number, [target], ctx) => {
    // https://vee-validate.logaretm.com/v4/guide/global-validators#cross-field-validation
    // Value is the number in that input field, target is that of the other
    // Value must be bigger than the target
    // Appears to store input values as strings
    if (value > +(ctx.form[target] as number)) {
      return true;
    }
    return "Maximum must be larger.";
  });
});

configure({
  // Generates an English message locale generator
  generateMessage: localize("en", {
    messages: {
      required: "This field is required.",
      email: "This email address is invalid.",
      min: "Passwords must be 8 to 64 characters long.",
      max: "Passwords must be 8 to 64 characters long.",
      url: "This url is invalid.",
      numeric: "Numeric value required."
    },
  }),
});

/*
  References:

  https://vee-validate.logaretm.com/v4/guide/overview/
  https://github.com/razorcx-courses/nuxt3-veevalidate
  https://vee-validate.logaretm.com/v4/guide/global-validators/#available-rules
  https://vee-validate.logaretm.com/v4/guide/i18n
*/