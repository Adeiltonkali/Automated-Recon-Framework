from recon_tools import *

while True:

    domain = input("Enter the domain: ")

    result_subfinder = subfinder(domain)
    result_amass = amass(domain)

    both_results = result_subfinder | result_amass

    if both_results:
        final_results = validar_httpx(both_results)
        print("\n=== FINAL RESULTS (LIVE TARGETS) ===")
        print("\n".join(final_results))
        print("="*50)
        scan = scanner(final_results)
        print("\n=== NMAP SCAN RESULTS ===")
        for host, result in scan.items():
            print(f"\n[+] Host: {host}")
            print(result)
            print("-" * 30)
        salvar_relatorios(domain, final_results, scan)
    else:
        print("[x] no domain to analyze")

    while True:
        print("You Want continue? ")
        option = input("ENTER [YES or NO]: ").lower()
        if option == "yes":
            print("[+] Continuing program...")
            break
        elif option == "no":
            print("[+] Stopping program...")
            exit()
        else:
            print("[x] Invalid option")
