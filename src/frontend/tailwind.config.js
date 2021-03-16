module.exports = {
  purge: [
      './src/views/*.{js,jsx,ts,tsx,vue,html,ejs}'
  ],
  darkMode: 'class', // or 'media' or 'class'
  theme: {
    extend: {
      backgroundColor: ['checked'],
      borderColor: ['checked'],
      colors: {
        turquoise: {
          '50':  '#edf8f9',
          '100': '#d3f7f5',
          '200': '#a3f0e9',
          '300': '#74eae8',
          '400': '#23d2ca',
          '500': '#0bb8b1',
          '600': '#0a9b94',
          '700': '#0f7d78',
          '800': '#12615d',
          '900': '#114f4b',
        }
      }
    },
  },
  variants: {
    extend: {
      width: ['group-hover'],
      height: ['hover'],
    },
  },
  plugins: [
    require('@tailwindcss/custom-forms'),
  ],
}
