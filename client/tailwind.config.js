/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'roboto-mono': ['Roboto Mono', 'monospace'],
      },
      animation: {
        'fly-in-letter': 'flyInLetter 1.2s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards',
        'ninja-strike': 'ninjaStrike 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards',
        'fade-in-up': 'fadeInUp 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards',
        'marquee': 'marquee 40s linear infinite',
      },
      keyframes: {
        flyInLetter: {
          '0%': {
            opacity: '0',
            transform: 'translate(var(--fly-x, 0), var(--fly-y, 0)) rotate(var(--fly-rotate, 0deg)) scale(0.3)',
          },
          '60%': {
            opacity: '1',
            transform: 'translate(calc(var(--fly-x, 0) * 0.1), calc(var(--fly-y, 0) * 0.1)) rotate(calc(var(--fly-rotate, 0deg) * 0.1)) scale(1.1)',
          },
          '100%': {
            opacity: '1',
            transform: 'translate(0, 0) rotate(0deg) scale(1)',
          },
        },
        ninjaStrike: {
          '0%': {
            opacity: '0',
            transform: 'translateY(-100px) scale(0.8) rotateX(90deg)',
          },
          '50%': {
            opacity: '1',
            transform: 'translateY(0) scale(1.05) rotateX(0deg)',
          },
          '60%': {
            transform: 'translateY(0) scale(1.05) rotateX(0deg)',
          },
          '70%': {
            transform: 'translateY(0) scale(1.02) rotateX(0deg)',
          },
          '80%': {
            transform: 'translateY(0) scale(1.05) rotateX(0deg)',
          },
          '90%': {
            transform: 'translateY(0) scale(1.02) rotateX(0deg)',
          },
          '100%': {
            opacity: '1',
            transform: 'translateY(0) scale(1) rotateX(0deg)',
          },
        },
        fadeInUp: {
          '0%': {
            opacity: '0',
            transform: 'translateY(30px)',
          },
          '100%': {
            opacity: '1',
            transform: 'translateY(0)',
          },
        },
        marquee: {
          '0%': {
            transform: 'translateX(0)',
          },
          '100%': {
            transform: 'translateX(-50%)',
          },
        },
      },
    },
  },
  plugins: [],
}
  