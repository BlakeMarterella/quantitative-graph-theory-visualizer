module.exports = {
  mode: 'jit',
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],  // Updated from 'purge' to 'content'
  theme: {
    extend: {},
  },
  plugins: [],
}
