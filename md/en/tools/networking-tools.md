---
title: "Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide"
description: "Practical guide to essential networking tools: mtr for path analysis, iperf for bandwidth testing, dig for DNS troubleshooting, nmap for port scanning, and Wire"
date: 2026-05-12
board: tools
url: https://dingjiu1989-hue.github.io/en/tools/networking-tools.html
---

# Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide

## Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide

## Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide

## Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide

## Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide

## Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide

## Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide

## Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide

## Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide

## Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide

## Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide

## Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide

## Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide

## Networking Tools: mtr, iperf, dig, nmap, Wireshark Practical Guide

### Introduction

Network troubleshooting is a fundamental skill for developers and operations engineers. Whether diagnosing slow connections, DNS resolution failures, or firewall issues, the right tools make the difference between hours of frustration and minutes of focused debugging. This practical guide covers five essential networking tools: mtr, iperf, dig, nmap, and Wireshark.

### mtr (My Traceroute)

Combines traceroute and ping in a single tool for continuous network path analysis:

## Basic usage

mtr google.com

mtr --report google.com # Run once and generate report

mtr --report-cycles=10 google.com # 10 cycles for report

## Useful flags

mtr --icmp google.com # Use ICMP instead of UDP

mtr --tcp --port 443 api.example.com # TCP on specific port

mtr --udp google.com # UDP probes

mtr --no-dns 10.0.0.1 # Skip DNS resolution (faster)

mtr --report-wide google.com # Wide output format

## For continuous monitoring

mtr --interval 5 google.com # Update every 5 seconds

**Interpreting output** : Look for hops with high loss% or latency spikes. The last hop before consistent loss is usually the problem. 100% loss at intermediate hops may be a firewall dropping probes, not an actual failure.

### iperf3

Network bandwidth measurement tool:

## Start server (on receiving end)

iperf3 -s

iperf3 -s -p 5201

## Start client (on sending end)

iperf3 -c server-address

iperf3 -c server-address -p 5201

## Advanced tests

iperf3 -c server-address -t 30 # 30-second test

iperf3 -c server-address -P 4 # 4 parallel streams

iperf3 -c server-address -R # Reverse mode (server to client)

iperf3 -c server-address -u -b 100M # UDP test at 100 Mbps

## Bidirectional test

iperf3 -c server-address --bidir

## JSON output for automation

iperf3 -c server-address -J > results.json

## Test specific TCP window size

iperf3 -c server-address -w 64K

**When to use** : Benchmark network throughput between instances, verify bandwidth limits, test VPN performance, identify congestion. Typical patterns: run iperf3 in server mode on one host, client mode on another.

### dig (DNS Lookup)

The most powerful DNS troubleshooting tool:

## Basic lookup

dig google.com

dig @8.8.8.8 google.com # Query specific DNS server

## Query specific record types

dig google.com A # IPv4 address

dig google.com AAAA # IPv6 address

dig google.com MX # Mail exchange

dig google.com NS # Name servers

dig google.com TXT # Text records (SPF, DKIM)

dig google.com CNAME # Canonical name

dig example.com SOA # Start of authority

## Advanced queries

dig +short google.com # Short output

dig +trace google.com # Trace delegation path

dig +tcp google.com # Use TCP instead of UDP

dig -x 8.8.8.8 # Reverse DNS lookup

dig google.com ANY +noall +answer # Show only answer section

dig +dnssec google.com # DNSSEC validation

## Batch queries from file

dig -f domains.txt +short

## Check propagation

dig @ns1.google.com google.com # Query authoritative server

dig @8.8.8.8 google.com +stats # Show query statistics

**Common debugging workflow** : Start with `dig +trace` to see the full resolution path, then query specific servers to isolate where resolution fails.

### nmap (Network Mapper)

Port scanning and service discovery:

## Basic scans

nmap scanme.nmap.org # Default scan (1000 ports)

nmap -sS scanme.nmap.org # SYN stealth scan (needs root)

nmap -sT scanme.nmap.org # TCP connect scan

nmap -sU scanme.nmap.org # UDP scan

## Port specification

nmap -p 80,443 example.com # Specific ports

nmap -p- example.com # All 65535 ports (slow)

nmap -p 1-1000 example.com # Port range

nmap --top-ports 100 example.com # Most common ports

## Service detection

nmap -sV example.com # Version detection

nmap -O example.com # OS detection

nmap -A example.com # Aggressive (OS, version, script, traceroute)

## Network discovery

nmap -sn 192.168.1.0/24 # Ping sweep (find live hosts)

nmap -sL 192.168.1.0/24 # List scan (DNS resolution only)

## Scripts

nmap --script=http-title example.com

nmap --script=ssl-enum-ciphers example.com

nmap --script=vuln example.com --script-args=unsafe=1

## Output formats

nmap -oN scan.txt example.com # Normal

nmap -oX scan.xml example.com # XML

nmap -oG scan.grep example.com # Grepable

### Wireshark / tshark

Deep packet inspection and analysis:

## tshark (CLI version of Wireshark)

## Capture on interface

tshark -i eth0

tshark -i eth0 -c 100 # Capture 100 packets

## Capture filters (BPF syntax)

tshark -i eth0 "port 443"

tshark -i eth0 "host 10.0.0.1"

tshark -i eth0 "tcp port 80 or tcp port 443"

## Display filters (more powerful)

tshark -Y "http.request.method == GET"

tshark -Y "dns.qry.name contains example.com"

tshark -Y "tcp.analysis.flags" # TCP issues

tshark -Y "http.response.code >= 500"

## Follow streams

tshark -r capture.pcap -Y "http" -z follow,tcp,ascii,0

## Statistics

tshark -r capture.pcap -z io,stat,1 # IO graph

tshark -r capture.pcap -z conv,tcp # TCP conversations

## Save filtered output

tshark -r capture.pcap -Y "dns" -w dns-only.pcap

**Wireshark filters** : `ip.src == 10.0.0.1 && tcp.port == 443`, `http.response.code >= 400`, `tls.handshake.type == 1`

### Quick Reference

| Tool | Best For | Example Problem |

|------|----------|----------------|

| mtr | Path analysis, packet loss | "Connection intermittent to API" |

| iperf3 | Bandwidth measurement | "Slow file transfers to S3" |

| dig | DNS troubleshooting | "Website not loading, DNS error" |

| nmap | Port scanning, discovery | "Cannot connect to service, firewall?" |

| Wireshark | Deep packet inspection | "API returns corrupted data" |

### Recommendations

  * **First, check connectivity** : `ping` and `mtr` to verify basic reachability.

  * **DNS issues** : `dig +trace` to find where resolution fails.

  * **Performance issues** : `iperf3` to measure raw throughput between hosts.

  * **Firewall issues** : `nmap -sS -p` to check port accessibility.

  * **Protocol issues** : `tshark -Y` display filters to inspect application-layer behavior.




Mastering these five tools covers 95% of network troubleshooting scenarios. Start with mtr for path issues, dig for DNS, nmap for connectivity, iperf for performance, and Wireshark for deep protocol analysis.

**See also:** [Terraform Tools: Terragrunt, terratest, tfsec, Infracost](</en/tools/terraform-tools.html>), [Performance Profiling: perf, Flamegraphs, py-spy, pprof](</en/tools/performance-profiling.html>), [Memory Analysis: Valgrind, heaptrack, memray, Heap Profiling](</en/tools/memory-analysis.html>).

**See also:** [Terraform Tools: Terragrunt, terratest, tfsec, Infracost](</en/tools/terraform-tools.html>), [Command-Line Productivity: fzf, ripgrep, jq, bat, tmux, zoxide, and lazygit](</en/tools/command-line-productivity.html>), [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>)

**See also:** [Terraform Tools: Terragrunt, terratest, tfsec, Infracost](</en/tools/terraform-tools.html>), [Command-Line Productivity: fzf, ripgrep, jq, bat, tmux, zoxide, and lazygit](</en/tools/command-line-productivity.html>), [Code Editor Plugins: Must-Have Extensions for Productivity](</en/tools/code-editor-plugins.html>)
