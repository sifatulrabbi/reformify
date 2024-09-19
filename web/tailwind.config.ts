import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    darkMode: "class",
    theme: {
        extend: {
            colors: {
                primary: "#3ABFF8",
                secondary: "#F87272",
                accent: "#37CDDC",
                neutral: "#2A2E37",
                "base-100": "#1F2937",
                "base-200": "#374151",
                "base-300": "#4B5563",
                info: "#3ABFF8",
                success: "#36D399",
                warning: "#FBBD23",
                error: "#F87272",
                textBold: "#b1b9c4",
                textBase: "#929dac",
                textMuted: "#929dac",
            },
            // @ts-ignore
            typography: ({ theme }) => ({
                DEFAULT: {
                    css: {
                        color: theme("colors.textBase"),
                        h1: {
                            color: theme("colors.textBold"),
                            fontWeight: theme("fontWeight.medium"),
                        },
                        h2: { color: theme("colors.textBold") },
                        h3: {
                            color: theme("colors.textBold"),
                            letterSpacing: theme("letterSpacing.wide"),
                        },
                        h4: {
                            color: theme("colors.textBold"),
                            fontSize: "1.1rem",
                            fontWeight: theme("fontWeight.bold"),
                            letterSpacing: theme("letterSpacing.wide"),
                        },
                        h5: {
                            color: theme("colors.textBold"),
                            fontWeight: theme("fontWeight.medium"),
                            fontSize: theme("fontSize.sm"),
                            textTransform: "uppercase",
                            letterSpacing: theme("letterSpacing.wide"),
                        },
                        h6: {
                            color: theme("colors.textBold"),
                            fontWeight: theme("fontWeight.bold"),
                            fontSize: theme("fontSize.sm"),
                            letterSpacing: theme("letterSpacing.wide"),
                        },
                        a: { color: theme("colors.primary") },
                        strong: { color: theme("colors.textBold") },
                        code: { color: theme("colors.accent") },
                        blockquote: {
                            borderLeftColor: theme("colors.base-200"),
                            color: theme("colors.textBase"),
                        },
                        "ol > li::before": { color: theme("colors.primary") },
                        "ul > li::before": {
                            backgroundColor: theme("colors.primary"),
                        },
                        hr: { borderColor: theme("colors.base-300") },
                    },
                },
            }),
        },
    },
    plugins: [require("@tailwindcss/typography"), require("daisyui")],
    daisyui: {
        themes: "dark",
        darkTheme: "dark",
        base: true,
        styled: true,
        utils: true,
        prefix: "dui-",
    },
};
export default config;
