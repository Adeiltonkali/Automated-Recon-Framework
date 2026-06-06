import subprocess
import socket
import os
from datetime import datetime

def subfinder(domain):
    try:
        print("\n" + "=" * 70)
        print("[INFO] Starting Subfinder enumeration")
        print(f"[TARGET] Domain: {domain}")
        print("=" * 70)

        execucao = subprocess.run(
            ["subfinder",
             "-d",
             domain,
             "-silent"],
            capture_output=True,
            text=True,
            check=True
        )

        resultados = set(execucao.stdout.splitlines())

        print(f"[SUCCESS] Subfinder completed")
        print(f"[RESULTS] {len(resultados)} subdomains discovered")
        print("=" * 70)

        return resultados

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Subfinder execution failed: {e}")
        if e.stderr:
            print(f"[DETAILS] {e.stderr}")
        return set()


def amass(domain):
    try:
        print("\n" + "=" * 70)
        print("[INFO] Starting Amass passive enumeration")
        print(f"[TARGET] Domain: {domain}")
        print("=" * 70)

        comando = [
            "amass",
            "enum",
            "-passive",
            "-d",
            domain,
        ]

        execucao = subprocess.run(
            comando,
            shell=False,
            capture_output=True,
            text=True,
            check=True
        )

        resultados = set(execucao.stdout.splitlines())

        print(f"[SUCCESS] Amass completed")
        print(f"[RESULTS] {len(resultados)} subdomains discovered")
        print("=" * 70)

        return resultados

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Amass execution failed: {e}")
        return set()


def validar_httpx(lista_subdominios):
    try:
        print("\n" + "=" * 70)
        print("[INFO] Validating discovered hosts with HTTPX")
        print(f"[HOSTS] Total received: {len(lista_subdominios)}")
        print("=" * 70)

        dados_entrada = '\n'.join(lista_subdominios)

        execucao = subprocess.run(
            ["~/go/bin/httpx", "-silent"],
            input=dados_entrada,
            capture_output=True,
            shell=True,
            text=True,
            check=True
        )

        resultados = execucao.stdout.splitlines()

        print(f"[SUCCESS] HTTPX validation completed")
        print(f"[LIVE HOSTS] {len(resultados)} active hosts found")
        print("=" * 70)

        return resultados

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] HTTPX validation failed: {e}")
        if e.stderr:
            print(f"[DETAILS] {e.stderr}")
        return None


def scanner(available_domains):
    try:
        print("\n" + "#" * 70)
        print("# NETWORK RECONNAISSANCE PHASE")
        print("# NMAP PORT DISCOVERY")
        print("#" * 70)

        nmap_results = {}

        for domains in available_domains:

            domain_clean = domains.replace("https://", "").replace("http://", "")
            domain_clean = domain_clean.split("/")[0]

            try:
                print("\n" + "-" * 70)
                print(f"[INFO] Resolving hostname: {domain_clean}")

                ip = socket.gethostbyname(domain_clean)

                print(f"[SUCCESS] IP Address Resolved: {ip}")
                print(f"[TARGET] {domains}")
                print(f"[IP] {ip}")

                print("-" * 70)
                print("[INFO] Launching TCP port discovery scan")
                print("[INFO] Scan Profile : Full TCP Range")
                print("[INFO] Scan Engine  : Nmap")
                print("[INFO] Min Rate     : 5000 packets/sec")
                print("-" * 70)

                seeall_tcports = subprocess.run(
                    ["nmap", "-Pn", "-p-", "--min-rate", "5000", ip],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                nmap_results[domains] = seeall_tcports.stdout

                print(f"[SUCCESS] Scan completed for {domains}")
                print("-" * 70)

            except socket.gaierror:
                print(f"[ERROR] Unable to resolve hostname: {domains}")
                continue

            except subprocess.CalledProcessError as e:
                print(f"[ERROR] Scan failed: {e}")
                continue

        print("\n" + "#" * 70)
        print("# RECONNAISSANCE FINISHED")
        print(f"# TOTAL TARGETS SCANNED: {len(nmap_results)}")
        print("#" * 70)

        return nmap_results

    except Exception as e:
        print(f"[FATAL] Unexpected error: {e}")
        return {}

def salvar_relatorios(domain, live_hosts, nmap_results):
    try:
        print("\n" + "=" * 70)
        print("[INFO] Starting Report Generation Phase")
        print("=" * 70)

        data_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        pasta_base = os.path.join("resultados", data_atual, domain)
        os.makedirs(pasta_base, exist_ok=True)
        print(f"[SUCCESS] Output directory ready: {pasta_base}")

        arquivo_httpx = os.path.join(pasta_base, "subdominios_vivos.txt")
        with open(arquivo_httpx, "w") as f:
            f.write("\n".join(live_hosts) + "\n")
        print(f"[SUCCESS] Saved HTTPX targets to: {arquivo_httpx}")

        arquivo_nmap = os.path.join(pasta_base, "nmap_completo.txt")
        with open(arquivo_nmap, "w") as f:
            for host, scan_data in nmap_results.items():
                f.write(f"\n{'=' * 50}\n")
                f.write(f"TARGET: {host}\n")
                f.write(f"{'=' * 50}\n")
                f.write(scan_data)
                f.write("\n" + "-" * 50 + "\n")
        print(f"[SUCCESS] Saved Nmap scan results to: {arquivo_nmap}")
        print("=" * 70)
    except Exception as e:
        print(f"[ERROR] Failed to generate reports: {e}")