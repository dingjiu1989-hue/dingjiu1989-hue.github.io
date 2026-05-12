---
title: "Browser Extension Development 2026: From Idea to Chrome Web Store"
description: "Technical guide to building cross-browser extensions: Manifest V3, service workers, content scripts, messaging, storage APIs, and publishing to Chrome Web Store and Firefox Add-ons. Includes React/Vue integration."
date: 2026-05-09
board: sidehustle
url: https://dingjiu1989-hue.github.io/en/sidehustle/browser-extension-development.html
---

# Browser Extension Development 2026: From Idea to Chrome Web Store

Browser extension development in 2026 is both a valuable skill and a profitable side hustle. With Manifest V3 now mandatory, the extension landscape has matured — offering better security, stricter permissions, and a cleaner API surface. This guide covers the complete technical stack for building modern browser extensions that work across Chrome, Edge, Brave, and Firefox.

## Manifest V2 vs V3: What Changed

Feature| Manifest V2 (Deprecated)| Manifest V3 (Current)  
---|---|---  
Background Scripts| Persistent background pages (always running)| Service workers (ephemeral, terminated when idle)  
Network Request Modification| webRequest blocking (sync)| declarativeNetRequest (async, rule-based)  
Host Permissions| All at install time| Optional, can be granted at runtime  
Remotely Hosted Code| Allowed| Not allowed (all code must be in the extension package)  
Content Security Policy| Optional| Enforced (no inline scripts, no eval)  
Cross-Browser Compatibility| Chrome-specific| Better alignment with Firefox/Safari (but not perfect)  

## Extension Architecture Patterns

    // manifest.json — the heart of a Manifest V3 extension
    {
      "manifest_version": 3,
      "name": "My Extension",
      "version": "1.0.0",
      "permissions": ["storage", "activeTab"],
      "host_permissions": ["https://*.example.com/*"],
      "background": {
        "service_worker": "background.js"  // Replaces background.page
      },
      "content_scripts": [{
        "matches": ["https://*.github.com/*"],
        "js": ["content.js"],
        "css": ["styles.css"]
      }],
      "action": {
        "default_popup": "popup.html",
        "default_icon": "icon.png"
      },
      "options_page": "options.html"
    }

    // Cross-browser compatibility tips:
    // - Use chrome.* APIs (Edge/Brave/Opera are Chromium-based)
    // - For Firefox: browser.* APIs are nearly identical (use webextension-polyfill)
    // - For Safari: Xcode project + iOS-style extensions (smaller market, consider later)

## Key APIs Every Extension Developer Should Know

API| Use Case| Permissions Required  
---|---|---  
chrome.storage.local / sync| Store user preferences and data| storage  
chrome.tabs| Create, update, query browser tabs| tabs  
chrome.contextMenus| Add right-click menu items| contextMenus  
chrome.runtime.onMessage| Pass messages between content scripts and service worker| None (built-in)  
chrome.alarms| Schedule periodic tasks (replaces setInterval in service workers)| alarms  
chrome.sidePanel| Add a persistent side panel (Chrome 114+)| sidePanel  
chrome.offscreen| Play audio, access DOM APIs from service worker| offscreen  

## Choosing Your Tech Stack

Stack| Best For| Pros| Cons  
---|---|---|---  
Vanilla JS + HTML + CSS| Simple extensions, minimal bundle| Zero build step, fastest review| No type safety, no modern DX  
React + Vite + CRXJS| Complex popup UIs, SPAs| Component model, HMR in development| Larger bundle (150KB+), CSP considerations  
Svelte + Vite| Minimal bundle, reactive UIs| Tiny bundle (~3KB), no virtual DOM| Smaller ecosystem than React  
Plasmo (Framework)| Full-featured extensions, rapid development| Manifest generation, HMR, cross-browser, built-in messaging| Abstraction overhead, less control  
WXT (Framework)| Type-safe extensions, modern DX| TypeScript-first, cross-browser (Chrome + Firefox), auto-reload| Newer framework, smaller community  

## Chrome Web Store Submission Checklist

  1. **Manifest:** V3 only. V2 extensions are rejected.
  2. **Privacy policy:** Required if you collect ANY data (even analytics). Link to a hosted privacy page.
  3. **Permissions justification:** Explain why each permission is needed. "Required for core functionality" is not sufficient — be specific.
  4. **Single purpose:** Each extension must do one thing. Multi-purpose extensions are rejected.
  5. **Screenshots:** At least 1 (1280x800), best practice 5+. Show the UI and the benefit.
  6. **Promotional images:** Small tile (440x280), large tile (920x680), marquee (1400x560).
  7. **Review time:** 1-5 business days for initial review, 1-3 days for updates.

**Bottom line:** Browser extensions are a $2B+ market that most developers ignore. Manifest V3 has raised the technical bar (disqualifying amateurs) while improving security for users. Start with Plasmo or WXT for the best developer experience, target Chrome first (80%+ market share), and submit early — the CWS review process often finds issues you will miss. See also: [Chrome Extension Monetization](</en/sidehustle/chrome-extension-monetization.html>) and [Web Security Basics](</en/tech/web-security-basics.html>).
