# Domain Recon Automation

An automated reconnaissance tool that combines subdomain enumeration, live host validation, port scanning, and report generation into a single workflow.

## Features

* Subdomain enumeration using Subfinder
* Passive reconnaissance using Amass
* Live host validation with HTTPX
* TCP port discovery using Nmap
* Automatic report generation
* Organized output structure by date and target domain

---

## Workflow

1. The user provides a target domain.
2. Subfinder is executed.
3. Amass passive enumeration is executed.
4. Results are merged and deduplicated.
5. HTTPX validates which hosts are alive.
6. Nmap performs TCP port discovery on live hosts.
7. Reports are generated and saved automatically.

---

## Project Structure

```text
.
├── main.py
├── recon_tools.py
├── resultados/
└── README.md
```

---

## Requirements

### Python

* Python 3.10 or newer

Verify installation:

```bash
python3 --version
```

---

### External Dependencies

#### Subfinder

```bash
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

Verify installation:

```bash
subfinder -h
```

---

#### HTTPX

```bash
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
```

Verify installation:

```bash
httpx -h
```

---

#### Amass

```bash
go install github.com/owasp-amass/amass/v4/...@master
```

Verify installation:

```bash
amass -h
```

---

#### Nmap

Ubuntu/Debian:

```bash
sudo apt install nmap
```

Arch Linux:

```bash
sudo pacman -S nmap
```

Verify installation:

```bash
nmap --version
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Adeiltonkali/Automated-Recon-Framework.git
```

Enter the project directory:

```bash
cd domain-recon-automation
```

Verify all dependencies:

```bash
subfinder -h
amass -h
httpx -h
nmap --version
```

---

## Usage

Run the application:

```bash
python3 main.py
```

Example:

```text
Enter the domain: example.com
```

---

## Output Structure

Generated reports are organized by timestamp and target domain:

```text
results/
└── 2026-06-06_15-20-45/
    └── example.com/
        ├── subdominios_vivos.txt
        └── nmap_completo.txt
```

### Live Hosts Report

`subdominios_vivos.txt`

Contains all hosts successfully validated by HTTPX.

### Nmap Scan Report

`nmap_completo.txt`

Contains the complete Nmap output for every live host discovered.

---

## Example Execution

```text
Enter the domain: example.com

[INFO] Starting Subfinder enumeration
[SUCCESS] Subfinder completed

[INFO] Starting Amass passive enumeration
[SUCCESS] Amass completed

[INFO] Validating discovered hosts with HTTPX
[SUCCESS] HTTPX validation completed

[INFO] Launching TCP port discovery scan
[SUCCESS] Scan completed

[INFO] Starting Report Generation Phase
[SUCCESS] Reports generated
```

---

## Disclaimer

This tool is intended for educational purposes, authorized security assessments, and research environments only.

Users are solely responsible for ensuring they have proper authorization before scanning, enumerating, or assessing any target.

Unauthorized use against systems you do not own or have permission to test may violate local laws and regulations.

---

## License

This project is distributed under the MIT License.

---

## Author

Developed by **Tyler(AdeiltonKali)**.
