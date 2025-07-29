# Captive Portal Detector

A Python utility to perform high-security network-integrity checks. \
It reliably detects captive portals and can identify TLS Man-in-the-Middle (MITM) attacks using SPKI pinning against redundant, user-controlled endpoints.

## Features

- **High-Security MITM Detection:** Uses SPKI-pinning against redundant, user-controlled endpoints to detect sophisticated TLS interception.
- **Comprehensive Checks:** Runs a suite of probes in parallel, including standard HTTP 204 checks, random domain requests, and IPv6 reachability tests.
- **Resilient by Design:** The final verdict prioritizes security, trusting only a successful pinned connection to declare the internet "OK".
- **Fast and Lightweight:** Concurrent probes provide a result in seconds with minimal overhead.

## Usage

Install via pip:

```bash
pip install captive-portal-detector
```

### CLI Usage
Simply run it with:
```capdet```

#### Advanced CLI Usage (detailed probe suite)
````sudo capdet [--advanced | -a] [--json]````

### Python Usage
```python
from capdet.network_probe import NetworkProbe

status = NetworkProbe().network_health()
print(status)
```
or
```python
from capdet.advanced_network_analyzer import AdvancedNetworkAnalyzer
ana = AdvancedNetworkAnalyzer()

result = ana.analyze_network_interference()
print(result)
```

### Advanced Usage (with your own pinned servers)
The library's real power is using your own endpoints. You can override the PINNED dictionary by passing it to the constructor:
```python
from capdet.network_probe import NetworkProbe
custom_pinned = {
    "c1": "sha256/your_custom_spki_hash1",
    "c2": "sha256/your_custom_spki_hash2"
}
network_probe = NetworkProbe(pinned=custom_pinned)
status = network_probe.network_health()
print(status)
```

## Output
The network_health() method returns one of three clear verdicts:

OK: A trusted, pinned TLS connection was successful. Internet access is confirmed. \
CAPTIVE: A definitive captive portal (redirect) or TLS pin mismatch (MITM attack) was detected. \
NO_INTERNET: No definitive CAPTIVE state was found, but a trusted connection could not be established.

## How It Works
The library runs multiple probes in parallel and makes a verdict based on a security-first principle:

1. If any probe detects a captive portal (like an HTTP redirect or a TLS pin mismatch), the final verdict is immediately CAPTIVE.
2. If no CAPTIVE state is found, it then checks if any of the high-security pinned probes returned OK. An "OK" from a simple public probe is not sufficient.
3. If neither of the above conditions is met, the verdict is NO_INTERNET, as a trusted connection could not be established.

## Security Model
This tool is designed for "zero trust" environments. Unlike simple checks, it does not trust a successful connection to a public website as proof of real internet access. 
The default PINNED servers (c1/c2.probecheck.fyi) provide a baseline but it's recommended you add your own for maximum security. 
This allows the tool to reliably detect most corporate and nation-state MITM interception attacks.
