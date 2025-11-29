/**
 * Extension Debugger Utility
 *
 * This utility helps identify which browser extension is causing injection errors.
 * Usage: Import and call `detectProblematicExtensions()` in your component or main.tsx
 */

interface ExtensionInfo {
  name: string
  pattern: string
  detected: boolean
}

/**
 * Detects which extensions have injected scripts into the page
 */
export function detectProblematicExtensions(): void {
  console.group('🔍 Browser Extension Detection')

  const knownExtensions: ExtensionInfo[] = [
    { name: '1Password', pattern: 'onepassword', detected: false },
    { name: 'LastPass', pattern: 'lastpass', detected: false },
    { name: 'Bitwarden', pattern: 'bitwarden', detected: false },
    { name: 'Dashlane', pattern: 'dashlane', detected: false },
    { name: 'NordPass', pattern: 'nordpass', detected: false },
    { name: 'Keeper', pattern: 'keeper', detected: false },
    { name: 'RoboForm', pattern: 'roboform', detected: false },
    { name: 'Google Password Manager', pattern: 'passkey', detected: false },
  ]

  // Check for injected scripts
  const scripts = document.querySelectorAll('script')
  scripts.forEach((script) => {
    const src = script.src || script.innerHTML
    knownExtensions.forEach((ext) => {
      if (src.toLowerCase().includes(ext.pattern)) {
        ext.detected = true
      }
    })
  })

  // Check for extension-specific DOM elements
  const bodyClasses = document.body.className
  const bodyDataset = Object.keys(document.body.dataset)

  knownExtensions.forEach((ext) => {
    if (bodyClasses.includes(ext.pattern) ||
        bodyDataset.some(key => key.toLowerCase().includes(ext.pattern))) {
      ext.detected = true
    }
  })

  // Report findings
  const detected = knownExtensions.filter(ext => ext.detected)

  if (detected.length > 0) {
    console.warn('⚠️ Detected password manager extensions:', detected.map(e => e.name))
    console.info('💡 If you see connection errors, try:')
    console.info('   1. Update the extension')
    console.info('   2. Disable it temporarily for development')
    console.info('   3. Use Incognito mode (extensions usually disabled)')
  } else {
    console.info('✅ No common password manager extensions detected')
  }

  // List all chrome-extension:// scripts
  const extensionScripts = Array.from(scripts)
    .filter(s => s.src.includes('chrome-extension://') || s.src.includes('moz-extension://'))
    .map(s => {
      const match = s.src.match(/(chrome-extension|moz-extension):\/\/([^\/]+)/)
      return match ? match[2] : 'unknown'
    })

  if (extensionScripts.length > 0) {
    console.info('🔌 Extension IDs injecting scripts:', [...new Set(extensionScripts)])
    console.info('   Check chrome://extensions to identify them')
  }

  console.groupEnd()
}

/**
 * Monitors for extension errors in real-time
 */
export function monitorExtensionErrors(): void {
  const originalConsoleError = console.error

  console.error = function(...args: any[]) {
    const message = args.join(' ')

    if (message.includes('Could not establish connection') ||
        message.includes('Receiving end does not exist') ||
        message.includes('Extension context invalidated')) {
      console.warn('🚨 Extension Error Detected:', message)
      console.info('💡 This is a browser extension issue, not your app')
      detectProblematicExtensions()
    } else {
      originalConsoleError.apply(console, args)
    }
  }
}

/**
 * Gets a list of all extension-injected resources
 */
export function listExtensionResources(): void {
  console.group('📦 Extension-Injected Resources')

  // Scripts
  const scripts = Array.from(document.querySelectorAll('script'))
    .filter(s => s.src.includes('extension://'))
    .map(s => s.src)

  if (scripts.length > 0) {
    console.log('Scripts:', scripts)
  }

  // Stylesheets
  const styles = Array.from(document.querySelectorAll('link[rel="stylesheet"]'))
    .filter((l: any) => l.href.includes('extension://'))
    .map((l: any) => l.href)

  if (styles.length > 0) {
    console.log('Stylesheets:', styles)
  }

  // Iframes
  const iframes = Array.from(document.querySelectorAll('iframe'))
    .filter(i => i.src.includes('extension://'))
    .map(i => i.src)

  if (iframes.length > 0) {
    console.log('Iframes:', iframes)
  }

  if (scripts.length === 0 && styles.length === 0 && iframes.length === 0) {
    console.info('✅ No extension resources detected')
  }

  console.groupEnd()
}

/**
 * Run all diagnostics
 */
export function runExtensionDiagnostics(): void {
  console.clear()
  console.log('%c🔧 Extension Diagnostics Report', 'font-size: 16px; font-weight: bold; color: #2563EB')
  console.log('=' .repeat(50))

  detectProblematicExtensions()
  listExtensionResources()

  console.log('=' .repeat(50))
  console.log('To run this again, call: runExtensionDiagnostics()')

  // Make function available globally for easy access
  ;(window as any).runExtensionDiagnostics = runExtensionDiagnostics
}
