import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

// Suppress browser extension errors (passkey managers, password managers, etc.)
// These extensions inject scripts that sometimes fail to connect to their background pages
// This is harmless and doesn't affect our application
window.addEventListener('error', (event) => {
  // Filter out errors from browser extension injected scripts
  if (event.filename && (
    event.filename.includes('passkeys-inject') ||
    event.filename.includes('chrome-extension://') ||
    event.filename.includes('moz-extension://') ||
    event.filename.includes('safari-extension://')
  )) {
    // Prevent the error from appearing in console
    event.preventDefault()
    console.debug('[Extension Error Suppressed]', event.message)
    return true
  }
})

// Also suppress unhandled promise rejections from extensions
window.addEventListener('unhandledrejection', (event) => {
  const error = event.reason
  if (error && error.stack && (
    error.stack.includes('passkeys-inject') ||
    error.stack.includes('chrome-extension://') ||
    error.stack.includes('moz-extension://')
  )) {
    event.preventDefault()
    console.debug('[Extension Promise Rejection Suppressed]', error.message)
    return true
  }
})

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
