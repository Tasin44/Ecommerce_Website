/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/templates/**/*.html', // Matches all 'templates' directories in the project structure
    './cartapp/templates/**/*.html'
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

