import os
import csv
from datetime import datetime
import argparse

# Pastas e arquivos
DADOS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dados")
LOG_FILE = "logs/torre.log"

arquivos_obrigatorios = {
    "planos_voo": "planos_voo.csv",
    "pistas": "pistas.txt",
    "metar": "metar.txt",
    "notam": "notam.txt",
    "frota": "frota.csv",
    "pilotos": "pilotos.csv"
}

# Estruturas de dados globais
voos = []
pistas = {}
metar = []
notams = []
frota = {}
pilotos = {}

def log(mensagem):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().isoformat()} - {mensagem}\n")

def importar_dados():
    # 1️⃣ Verifica se todos os arquivos existem
    for key, file in arquivos_obrigatorios.items():
        path = os.path.join(DADOS_DIR, file)
        if not os.path.exists(path):
            msg = f"Erro: arquivo obrigatório não encontrado: {path}"
            print(msg)
            log(msg)
            return False

    # 2️⃣ Ler planos_voo.csv
    global voos
    path_voos = os.path.join(DADOS_DIR, arquivos_obrigatorios["planos_voo"])
    with open(path_voos, newline="") as f:
        reader = csv.DictReader(f)
        voos = [row for row in reader]

    # 3️⃣ Ler pistas.txt
    global pistas
    path_pistas = os.path.join(DADOS_DIR, arquivos_obrigatorios["pistas"])
    pistas = {}
    with open(path_pistas) as f:
        for line in f:
            if line.strip():
                pista, status = line.strip().split(",")
                pistas[pista] = status

    # 4️⃣ Ler metar.txt
    global metar
    path_metar = os.path.join(DADOS_DIR, arquivos_obrigatorios["metar"])
    with open(path_metar) as f:
        metar = [line.strip() for line in f if line.strip()]

    # 5️⃣ Ler notam.txt
    global notams
    path_notam = os.path.join(DADOS_DIR, arquivos_obrigatorios["notam"])
    with open(path_notam) as f:
        notams = [line.strip() for line in f if line.strip()]

    # 6️⃣ Ler frota.csv
    global frota
    path_frota = os.path.join(DADOS_DIR, arquivos_obrigatorios["frota"])
    with open(path_frota, newline="") as f:
        reader = csv.DictReader(f)
        frota = {row["aeronave"]: row for row in reader}

    # 7️⃣ Ler pilotos.csv
    global pilotos
    path_pilotos = os.path.join(DADOS_DIR, arquivos_obrigatorios["pilotos"])
    with open(path_pilotos, newline="") as f:
        reader = csv.DictReader(f)
        pilotos = {row["matricula"]: row for row in reader}

    # 8️⃣ Criar filas iniciais (vazias)
    os.makedirs(DADOS_DIR, exist_ok=True)
    with open(os.path.join(DADOS_DIR, "fila_decolagem.txt"), "w") as f:
        pass
    with open(os.path.join(DADOS_DIR, "fila_pouso.txt"), "w") as f:
        pass

    print("Dados importados com sucesso!")
    log("Dados importados com sucesso")
    return True

def listar(ordenar_por="voo"):
    path_voos = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dados", "planos_voo.csv")
    if not os.path.exists(path_voos):
        print(f"Arquivo {path_voos} não encontrado. Execute importar-dados primeiro.")
        return

    # Ler voos do CSV
    with open(path_voos, newline="") as f:
        reader = csv.DictReader(f)
        voos = [row for row in reader]

    if not voos:
        print("Nenhum voo encontrado no CSV.")
        return

    # Ordenar
    if ordenar_por in ["voo", "etd", "tipo", "prioridade"]:
        if ordenar_por == "prioridade":
            lista_ordenada = sorted(voos, key=lambda x: int(x["prioridade"]), reverse=True)
        else:
            lista_ordenada = sorted(voos, key=lambda x: x[ordenar_por])
    else:
        lista_ordenada = voos

    # Imprimir tabela
    colunas = ["voo","origem","destino","etd","eta","aeronave","tipo","prioridade","pista_pref"]
    print("\t".join(colunas))
    print("-"*80)
    for voo in lista_ordenada:
        print("\t".join([voo[c] for c in colunas]))

# Função auxiliar para log
def escrever_log(mensagem):
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "torre.log")
    with open(log_path, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {mensagem}\n")

# Função para ler os voos
def ler_voos():
    path_voos = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dados", "planos_voo.csv")
    if not os.path.exists(path_voos):
        print(f"Arquivo {path_voos} não encontrado. Execute importar-dados primeiro.")
        return []
    with open(path_voos, newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

# Função para ler pilotos
def ler_pilotos():
    path_pilotos = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dados", "pilotos.csv")
    with open(path_pilotos, newline="") as f:
        reader = csv.DictReader(f)
        return {row["matricula"]: row for row in reader}

# Função para ler frota
def ler_frota():
    path_frota = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dados", "frota.csv")
    with open(path_frota, newline="") as f:
        reader = csv.DictReader(f)
        return {row["aeronave"]: row for row in reader}

# Função principal de enfileirar
def enfileirar(tipo, codigo_voo):
    voos = ler_voos()
    pilotos = ler_pilotos()
    frota = ler_frota()

    # Encontrar o voo
    voo = next((v for v in voos if v["voo"] == codigo_voo), None)
    if not voo:
        print(f"Voo {codigo_voo} não encontrado no CSV")
        escrever_log(f"Falha ao enfileirar: voo {codigo_voo} não encontrado")
        return

    # Validar piloto
    matricula_piloto = voo.get("piloto", "")  # Ajuste se você tiver a coluna piloto
    if matricula_piloto and matricula_piloto in pilotos:
        piloto = pilotos[matricula_piloto]
        # Aqui você poderia validar licença e habilitação
        # Exemplo: checar validade
        # if piloto["licenca_vencida"]:
        #     print("Piloto inválido")
    else:
        piloto = None

    # Validar aeronave
    aeronave = voo["aeronave"]
    if aeronave not in frota:
        print(f"Aeronave {aeronave} não cadastrada na frota")
        escrever_log(f"Falha ao enfileirar: aeronave {aeronave} não cadastrada")
        return

    # Escolher arquivo da fila
    fila_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dados", f"fila_{tipo}.txt")
    os.makedirs(os.path.dirname(fila_file), exist_ok=True)

    # Adicionar voo à fila
    with open(fila_file, "a") as f:
        linha = f"{voo['voo']};{voo['etd']};{voo['prioridade']};{voo['pista_pref']}\n"
        f.write(linha)

    print(f"Voo {codigo_voo} adicionado à fila de {tipo}")
    escrever_log(f"Voo {codigo_voo} enfileirado em {tipo}")

def ler_pistas():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dados", "pistas.txt")
    with open(path, newline="") as f:
        reader = csv.reader(f)
        return {row[0]: row[1] for row in reader}  # {'10/28': 'ABERTA', ...}

def ler_notam():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dados", "notam.txt")
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [line.strip() for line in f]

def ler_metar():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dados", "metar.txt")
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [line.strip() for line in f]

def autorizar(tipo, pista):
    fila_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dados", f"fila_{tipo}.txt")
    if not os.path.exists(fila_file):
        print(f"Fila {tipo} está vazia")
        return

    # Ler filas
    with open(fila_file) as f:
        voos_fila = [line.strip() for line in f if line.strip()]

    if not voos_fila:
        print(f"Fila {tipo} está vazia")
        return

    pistas_status = ler_pistas()
    notams = ler_notam()
    metars = ler_metar()

    # Pegando o primeiro voo elegível
    voo_info = voos_fila[0].split(";")  # voo;hora;prioridade;pista_atribuida
    codigo_voo, hora, prioridade, pista_atribuida = voo_info

    # Verifica pista aberta
    if pista not in pistas_status or pistas_status[pista] != "ABERTA":
        resultado = f"NEGADO: pista {pista} não está ABERTA"
        print(resultado)
        escrever_log(f"{tipo} {codigo_voo} - {resultado}")
        return

    # Verifica NOTAM
    for n in notams:
        if pista in n and "FECHADA" in n:
            resultado = f"NEGADO: NOTAM ativo - {n}"
            print(resultado)
            escrever_log(f"{tipo} {codigo_voo} - {resultado}")
            return

    # Verifica clima (simples: VIS < 6KM bloqueia mais de 1 operação)
    vis_restrita = False
    for m in metars:
        if "VIS" in m:
            vis = int(m.split("VIS")[1].split("KM")[0].strip())
            if vis < 6:
                vis_restrita = True
                break
    if vis_restrita and len(voos_fila) > 1:
        resultado = f"NEGADO: visibilidade restrita, apenas 1 operação permitida"
        print(resultado)
        escrever_log(f"{tipo} {codigo_voo} - {resultado}")
        return

    # Se passou todas as checagens → AUTORIZADO
    resultado = "AUTORIZADO"
    print(f"{tipo} {codigo_voo} - {resultado}")
    escrever_log(f"{tipo} {codigo_voo} - {resultado}")

    # Remove voo da fila
    voos_fila.pop(0)
    with open(fila_file, "w") as f:
        for v in voos_fila:
            f.write(v + "\n")


def status():
    # Pastas e arquivos
    dados_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dados")
    fila_decolagem = os.path.join(dados_dir, "fila_decolagem.txt")
    fila_pouso = os.path.join(dados_dir, "fila_pouso.txt")
    pistas_file = os.path.join(dados_dir, "pistas.txt")
    notam_file = os.path.join(dados_dir, "notam.txt")
    metar_file = os.path.join(dados_dir, "metar.txt")

    # Ler filas
    def ler_fila(path):
        if os.path.exists(path):
            with open(path) as f:
                return [line.strip() for line in f if line.strip()]
        return []

    fila_d = ler_fila(fila_decolagem)
    fila_p = ler_fila(fila_pouso)

    # Ler pistas
    pistas = {}
    if os.path.exists(pistas_file):
        with open(pistas_file) as f:
            for line in f:
                p, status = line.strip().split(",")
                pistas[p] = status

    # Ler NOTAM
    notams = []
    if os.path.exists(notam_file):
        with open(notam_file) as f:
            notams = [line.strip() for line in f]

    # Ler METAR
    metars = []
    if os.path.exists(metar_file):
        with open(metar_file) as f:
            metars = [line.strip() for line in f]

    # Imprimir status
    print("=== STATUS DA TORRE ===\n")

    print("Pistas:")
    for p, st in pistas.items():
        print(f"{p}: {st}")
    print()

    print(f"Tamanho da fila de decolagem: {len(fila_d)}")
    print(f"Próximos 3 voos de decolagem:")
    for v in fila_d[:3]:
        print(f"  {v}")
    print()

    print(f"Tamanho da fila de pouso: {len(fila_p)}")
    print(f"Próximos 3 voos de pouso:")
    for v in fila_p[:3]:
        print(f"  {v}")
    print()

    print("NOTAM ativos:")
    for n in notams:
        print(f"  {n}")
    print()

    print("METAR ativos:")
    for m in metars:
        print(f"  {m}")
    print()


def relatorio():
    import re
    from datetime import datetime

    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
    log_file = os.path.join(logs_dir, "torre.log")

    if not os.path.exists(log_file):
        print("Nenhum log encontrado para gerar relatório.")
        return

    # Contadores
    autorizados = 0
    negados = 0
    motivos_negado = {}
    emergencias = 0

    with open(log_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # AUTORIZADO
            if "AUTORIZADO" in line:
                autorizados += 1
                if "EMERGENCIA" in line.upper():
                    emergencias += 1
            # NEGADO
            elif "NEGADO" in line.upper():
                negados += 1
                # Captura motivo
                match = re.search(r"NEGADO: (.+)$", line)
                if match:
                    motivo = match.group(1)
                    motivos_negado[motivo] = motivos_negado.get(motivo, 0) + 1

    # Criar pasta relatorios se não existir
    rel_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "relatorios")
    os.makedirs(rel_dir, exist_ok=True)

    # Nome do arquivo: operacao_YYYYMMDD.txt
    hoje = datetime.now().strftime("%Y%m%d")
    rel_file = os.path.join(rel_dir, f"operacao_{hoje}.txt")

    with open(rel_file, "w") as f:
        f.write(f"RELATÓRIO DO TURNO - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total de voos autorizados: {autorizados}\n")
        f.write(f"Total de voos negados: {negados}\n")
        f.write(f"Emergências atendidas: {emergencias}\n\n")
        f.write("Motivos mais comuns de negação:\n")
        for motivo, count in motivos_negado.items():
            f.write(f"  {motivo}: {count}\n")
    
    print(f"Relatório gerado: {rel_file}")


# Exemplo de teste
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="torre")
    subparsers = parser.add_subparsers(dest="comando")

    # Comando importar-dados
    subparsers.add_parser("importar-dados")
    # Comando para listar

    listar_parser = subparsers.add_parser("listar")
    listar_parser.add_argument("--por", choices=["voo","etd","tipo","prioridade"], default="voo")

    # Comando enfileirar
    enf_parser = subparsers.add_parser("enfileirar")
    enf_parser.add_argument("tipo", choices=["decolagem", "pouso"])
    enf_parser.add_argument("--voo", required=True)

    # Comando autorizar
    auth_parser = subparsers.add_parser("autorizar")
    auth_parser.add_argument("tipo", choices=["decolagem", "pouso"])
    auth_parser.add_argument("--pista", required=True)

    # Comando status
    status_parser = subparsers.add_parser("status")

    # Comando relatorio
    rel_parser = subparsers.add_parser("relatorio")

    args = parser.parse_args()

    if args.comando == "importar-dados":
        importar_dados()

    elif args.comando == "listar":
        listar(args.por)

    elif args.comando == "enfileirar":
        enfileirar(args.tipo, args.voo)

    elif args.comando == "autorizar":
        autorizar(args.tipo, args.pista)

    elif args.comando == "status":
        status()

    elif args.comando == "relatorio":
        relatorio()
