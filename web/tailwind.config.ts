import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: "hsl(var(--ink) / <alpha-value>)",
        muted: "hsl(var(--muted) / <alpha-value>)",
        line: "hsl(var(--line) / <alpha-value>)",
        panel: "hsl(var(--panel) / <alpha-value>)",
        panelAlt: "hsl(var(--panel-alt) / <alpha-value>)",
        accent: "hsl(var(--accent) / <alpha-value>)",
        accentSoft: "hsl(var(--accent-soft) / <alpha-value>)",
        caution: "hsl(var(--caution) / <alpha-value>)",
        danger: "hsl(var(--danger) / <alpha-value>)",
      },
      fontFamily: {
        sans: ["var(--font-sans)"],
        display: ["var(--font-display)"],
      },
      boxShadow: {
        soft: "0 24px 70px -32px rgba(18, 54, 63, 0.32)",
      },
    },
  },
  plugins: [],
};

export default config;
