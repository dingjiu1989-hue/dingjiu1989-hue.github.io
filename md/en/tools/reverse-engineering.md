---
title: "Reverse Engineering Tools: Ghidra, IDA Free, radare2, Binary Ninja"
description: "Compare reverse engineering tools: Ghidra for free comprehensive analysis, IDA Free for industry standard disassembly, radare2 for command-line reverse engineer"
date: 2026-02-05
board: tools
url: https://aidev.fit/en/tools/reverse-engineering.html
---

# Reverse Engineering Tools: Ghidra, IDA Free, radare2, Binary Ninja

## Introduction

Reverse engineering is the art of understanding how software works without access to its source code. Modern reverse engineering tools provide disassembly, decompilation, debugging, and scripting capabilities. This article compares four major platforms: Ghidra, IDA Free, radare2, and Binary Ninja.

## Ghidra

NSA's open-source reverse engineering framework:

// Ghidra scripting API

import ghidra.app.script.GhidraScript;

import ghidra.program.model.listing.*;

import ghidra.program.model.symbol.*;

public class AnalyzeFunction extends GhidraScript {

@Override

public void run() throws Exception {

// Get the current program

Program program = getCurrentProgram();

Listing listing = program.getListing();

// Iterate over all functions

FunctionIterator functions = listing.getFunctions(true);

for (Function function : functions) {

println("Function: " + function.getName());

println(" Address: " + function.getEntryPoint());

println(" Body size: " + function.getBody().getNumAddresses());

// Check for imported functions

SymbolTable symTable = program.getSymbolTable();

ReferenceIterator refs = program.getReferenceManager()

.getReferencesTo(function.getEntryPoint());

while (refs.hasNext()) {

Reference ref = refs.next();

println(" Referenced by: " + ref.getFromAddress());

}

}

}

}

**Key features** :

  * Decompiler (produces C-like pseudocode from assembly)

  * Program tree and listing views

  * Cross-reference analysis (XREFs)

  * Version tracking (collaborative analysis)

  * Scripting in Java and Python (Jython)

  * Processor support: x86, x64, ARM, AARCH64, MIPS, PowerPC, RISC-V, 6502, 8051, and 50+ more

## Ghidra Python script

from ghidra.program.model.symbol import SourceType

def find_string_refs(target_string):

for address in currentProgram.getListing().getDefinedData(True):

data = getDataAt(address)

if data and data.isString():

string_value = str(data.getDefaultValueRepresentation())

if target_string in string_value:

print(f"Found '{string_value}' at {address}")

refs = getReferencesTo(address)

for ref in refs:

print(f" Referenced from: {ref.getFromAddress()}")

**Key strengths** : Free and open-source, excellent decompiler, collaborative features, extensive processor support, active development.

## IDA Free

Hex-Rays' industry-standard disassembler (free edition):

## IDAPython scripting

import idautils

import ida_funcs

import ida_xref

def analyze_critical_functions():

for func_addr in idautils.Functions():

func = ida_funcs.get_func(func_addr)

name = ida_funcs.get_func_name(func_addr)

## Identify functions with many cross-references

xref_count = len(list(idautils.CodeRefsTo(func_addr, 0)))

if xref_count > 20:

print(f"Hot function: {name} at {hex(func_addr)} ({xref_count} refs)")

## Check if function references suspicious strings

for ref in idautils.XrefsFrom(func_addr):

if is_string(ref.to):

string_val = get_strlit_contents(ref.to)

if string_val and b"password" in string_val.lower():

print(f"Password reference in {name} at {hex(func_addr)}")

## Rename subroutines based on string references

for addr, name in idautils.Names():

if name.startswith("sub_"):

refs = list(idautils.DataRefsTo(addr))

for ref in refs[:3]:

string_ref = get_strlit_contents(ref)

if string_ref:

idaapi.set_name(addr, f"sub_{string_ref[:16].decode('utf-8', errors='replace')}")

break

**Key features** : Industry-standard disassembly, cross-references (the best XREF system), IDAPython scripting, mature plugin ecosystem, compact database format.

**Limitations of Free edition** : No decompiler (Hex-Rays decompiler is paid), x86/x64 only, no collaborative features.

## radare2

The most powerful command-line reverse engineering framework:

## Open a binary

r2 ./binary

r2 -d ./binary # Debug mode

r2 -A ./binary # Analyze automatically

## Common commands

aaaa # Full analysis

afl # List functions

afl ~main # Find main function

s main # Seek to main

pdf # Print disassembly of function

V # Visual mode (arrow keys to navigate)

VV # Graph view (control flow graph)

## Searching

/ \x00\x00\x00 # Search for bytes

/v 42 # Search for value

/! popen # Search for string

wx 9090 # Write bytes (patch)

## Analysis

afvn new_name var_4 # Rename local variable

afn new_name 0x401000 # Rename function

axt 0x401000 # Find XREFs to address

axf 0x401000 # Find XREFs from address

## Output formats

pdf > output.asm # Save disassembly

pdr # Decompiled pseudocode (experimental)

## Scripting (r2pipe)

r2 -q -c 'aaa; afl~main' ./binary

## Binary Ninja

Modern reverse engineering platform with Python scripting:

import binaryninja as bn

## Open binary

bv = bn.BinaryViewType.get_view_of_file("./binary")

bv.update_analysis()

## Analyze functions

for func in bv.functions:

print(f"Function: {func.name} @ {hex(func.start)}")

print(f" Basic blocks: {len(func.basic_blocks)}")

print(f" Callers: {len(func.callers)}")

## High-level IL

for block in func.high_level_il:

for instr in block:

print(f" HLIL: {instr}")

## Medium-level IL (more detailed)

for block in func.medium_level_il:

for instr in block:

if "call" in str(instr).lower():

print(f" Call: {instr}")

## Find all calls to a specific function

target = bv.get_function_at(bv.symbols["strcpy"][0].address)

for ref in target.callers:

caller = ref.function

print(f"strcpy called from: {caller.name} @ {hex(ref.address)}")

## Data flow analysis

var = func.mlil.ssa_form[42].dest

uses = func.mlil.ssa_form.get_ssa_uses(var)

for use in uses:

print(f" Used at: {use.address}")

## Comparison

| Feature | Ghidra | IDA Free | radare2 | Binary Ninja |

|---------|--------|----------|---------|--------------|

| Price | Free | Free | Free | $299-$999 |

| Decompiler | Excellent | None (paid) | Basic | Good |

| UI | GUI + Headless | GUI | CLI + Web GUI | GUI + CLI |

| Scripting | Java, Python | Python | Python, JS, Lua | Python, C++ |

| Processor support | 50+ | x86/x64 | 50+ | 20+ |

| Learning curve | High | High | Very high | Medium |

## Recommendations

  * **Starting reverse engineering** : Ghidra provides the best free experience with its decompiler and user-friendly interface.

  * **Quick analysis** : IDA Free for rapid disassembly if you are already familiar with the IDA workflow.

  * **Automation/scripting** : Binary Ninja's clean Python API makes it ideal for automated analysis pipelines.

  * **Power users** : radare2 for the deepest control and command-line workflows.

  * **Malware analysis** : Ghidra with its decompiler and extensive processor support.

All four tools are capable of serious reverse engineering work. Ghidra offers the best free decompiler and the broadest platform support. Binary Ninja has the cleanest API for scripting. radare2 is unbeatable for command-line automation.
