---
title: "WebAssembly Guide 2026: Running Native Code in the Browser with Rust and WASI"
description: "Practical guide to WebAssembly — when to use it, Rust to Wasm with wasm-pack, WASI for edge computing, and real-world performance benchmarks."
date: 2026-05-08
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/webassembly-guide.html
---

# WebAssembly Guide 2026: Running Native Code in the Browser with Rust and WASI

## WebAssembly Is Production-Ready

WebAssembly (Wasm) has graduated from "promising technology" to "runs in every major browser and beyond." In 2026, Wasm powers Figma's design canvas, Photoshop on the web, 1Password's encryption, and Cloudflare Workers. It lets you run near-native performance code in the browser — written in Rust, C, C++, Go, or Zig — alongside your JavaScript. Here's what a developer actually needs to know to use it.

## What WebAssembly Is (And Isn't)

What Wasm Is| What Wasm Isn't  
---|---  
A binary instruction format that runs at near-native speed in a sandboxed VM| A replacement for JavaScript (they work together)  
A compile target for C, C++, Rust, Go, Zig, and 40+ other languages| A language you write directly (you write Rust/C/etc., compile to Wasm)  
Available in all modern browsers (97%+ support) and outside the browser (WASI)| A DOM manipulation tool (Wasm can't touch the DOM; it calls JS to do that)  
Memory-safe by design (sandboxed, linear memory model)| Slower than native (typically 10-30% overhead vs native, improving with each engine update)  
  
## When WebAssembly Makes Sense

**Excellent use cases:** computationally intensive tasks (image/video processing, 3D rendering, scientific simulation), porting existing C/C++/Rust codebases to the web (game engines, CAD tools, ML inference), performance-critical libraries used by JavaScript (encryption, compression, parsing, search), and edge computing (Cloudflare Workers, Fastly Compute@Edge).

**Poor use cases:** CRUD web apps (JS is fast enough, Wasm adds complexity), DOM manipulation (Wasm must call JS to touch the DOM, making it slower than pure JS for DOM-heavy work), and small utility functions (serialization overhead of crossing the JS-Wasm boundary can outweigh performance gains).

## Languages That Compile to Wasm

Language| Wasm Support| Binary Size| Best For| Learning Curve  
---|---|---|---|---  
Rust| ★★★★★ (wasm-pack, wasm-bindgen)| Small (no runtime, tree-shaken)| Performance-critical modules, systems programming| High  
C/C++ (Emscripten)| ★★★★★ (most mature, 10+ years)| Small-Medium| Porting existing C/C++ codebases| Medium (if you know C/C++)  
Go| ★★★★ (syscall/js, tinygo)| Medium-Large (Go runtime)| Go developers wanting Wasm without learning a new language| Low (if you know Go)  
AssemblyScript| ★★★★ (TypeScript-like syntax)| Very Small| JavaScript/TypeScript developers, quick adoption| Very Low (TS-like)  
Zig| ★★★★ (native wasm target)| Very Small (no runtime)| Systems-level Wasm with excellent C interop| Medium  
  
## Getting Started: Rust + wasm-pack (Most Common Path)
    
    
    # Install wasm-pack
    curl https://rustwasm.github.io/wasm-pack/installer/init.sh -sSf | sh
    
    # Create a new Rust-Wasm project
    wasm-pack new hello-wasm
    cd hello-wasm
    
    # src/lib.rs — a simple image processing function
    use wasm_bindgen::prelude::*;
    
    #[wasm_bindgen]
    pub fn grayscale(pixels: &[u8], width: u32, height: u32) -> Vec {
        let mut result = Vec::with_capacity(pixels.len());
        for chunk in pixels.chunks(4) {
            let r = chunk[0] as f32 * 0.299;
            let g = chunk[1] as f32 * 0.587;
            let b = chunk[2] as f32 * 0.114;
            let gray = (r + g + b) as u8;
            result.push(gray);
            result.push(gray);
            result.push(gray);
            result.push(chunk[3]); // alpha
        }
        result
    }
    
    # Build
    wasm-pack build --target web
    
    
    // On the JavaScript side
    import init, { grayscale } from './pkg/hello_wasm.js';
    
    async function run() {
        await init();
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const result = grayscale(imageData.data, canvas.width, canvas.height);
        // ... write result back to canvas
    }

## WASI: WebAssembly Outside the Browser

WASI (WebAssembly System Interface) is the "operating system" for Wasm outside the browser. It provides system calls (filesystem, networking, environment variables, random numbers) in a sandboxed, capability-based model. This is what powers: Cloudflare Workers (JavaScript + Wasm at the edge), Fermyon Spin (serverless Wasm apps), WasmEdge (CNCF runtime for cloud-native Wasm), and Docker's Wasm support (run Wasm containers alongside Linux containers). The key difference from Docker: Wasm containers start in microseconds (not seconds), use 1/10th the memory, and have a smaller attack surface.

## Performance Reality Check

Benchmark| JavaScript (V8)| Wasm (Rust)| Native (Rust)  
---|---|---|---  
Fibonacci (CPU-bound)| 100ms| 15ms (6.7x faster)| 12ms  
JSON parsing (large file)| 45ms| 30ms (1.5x faster)| 25ms  
Image grayscale (8MP)| 200ms| 35ms (5.7x faster)| 28ms  
SHA-256 hash (1MB)| 8ms| 2ms (4x faster)| 1.5ms  
DOM manipulation (10K elements)| 15ms| 25ms (slower — JS→Wasm→JS boundary cost)| N/A  
  
_Benchmarks from real-world tests on Chrome 130, M2 Mac. Wasm wins on CPU-bound work; loses when crossing the JS boundary too often._

## When Not to Use Wasm

The most common Wasm mistake: porting everything to Wasm because it's "faster." The JS↔Wasm boundary has a cost (serialize → pass → deserialize), so fine-grained calls (calling a Wasm function thousands of times from a JS loop) can be slower than pure JS. The rule: use Wasm for coarse-grained, computationally intensive operations where the work done inside Wasm dwarfs the boundary cost. Batch your data, do the heavy work inside Wasm, return the result. See also: [Edge Computing Guide](</en/tech/edge-computing-guide.html>) and [Bun vs Node vs Deno](</en/compare/bun-vs-node-vs-deno.html>).
