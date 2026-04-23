import subprocess
import ctypes
import sys
import time

def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

def verificar_servico(nome):
    resultado = subprocess.run(
        f"sc query {nome}",
        shell=True, capture_output=True, text=True
    )
    return "RUNNING" in resultado.stdout

def toggle_mysql():
    run_as_admin()
    
    print("Verificando serviço MySQL80...")
    
    if verificar_servico("MySQL80"):
        print("MySQL80 está LIGADO → Parando serviço...")
        subprocess.run("net stop MySQL80", shell=True)
        print("MySQL80 parado com sucesso!")
        
    else:
        print("MySQL80 está DESLIGADO → Iniciando serviço...")
        subprocess.run("net start MySQL80", shell=True)
        print("MySQL80 iniciado com sucesso!")

toggle_mysql()

for i in range(3, 0, -1):
    print(f"Encerrando programa em: {i}s                                                        ", end="\r", flush=True)
    time.sleep(1)

sys.exit()