/* Tailwind theme preset for dark + green slide style */
window.DECK_TAILWIND_THEME = {
  theme: {
    extend: {
      colors: {
        deck: {
          bg: '#0b0d10',
          panel: '#111318',
          text: '#f3f4f6',
          muted: '#a1a1aa',
          accent: '#3ecf8e',
          accentHover: '#2fb67b',
          border: '#22262e'
        }
      },
      fontFamily: {
        sans: ['Inter', 'SF Pro Display', 'Segoe UI', 'PingFang SC', 'sans-serif']
      },
      boxShadow: {
        deck: '0 24px 60px rgba(0, 0, 0, 0.35)'
      }
    }
  }
};
