import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#8B4513', light: '#A0522D', dark: '#654321' },
        accent: { DEFAULT: '#DAA520', light: '#FFD700' },
      },
    },
  },
  plugins: [],
};
export default config;
