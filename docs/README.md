# Aero70 - Sistema de Torre de Controle

Este é um sistema de controle de tráfego aéreo simulado, implementado em Python. Ele permite **importar dados**, **listar voos**, **enfileirar decolagens/pousos**, **autorizar operações**, verificar **status** e gerar **relatórios de turno**.  

O projeto foi desenvolvido para execução **somente pelo terminal (Ubuntu)**, sem bibliotecas externas além do Python padrão.

---

## Estrutura de Diretórios

aero70/
├── dados/ # Arquivos CSV/TXT de entrada e filas
│ ├── planos_voo.csv
│ ├── frota.csv
│ ├── pilotos.csv
│ ├── metar.txt
│ ├── notam.txt
│ ├── pistas.txt
│ ├── fila_decolagem.txt # Criado pelo sistema
│ └── fila_pouso.txt # Criado pelo sistema
├── logs/
│ └── torre.log # Todas ações registradas
├── relatorios/
│ └── operacao_YYYYMMDD.txt # Relatórios de turno
└── torre/
└── torre.py # Script principal do sistema


---

## Comandos do Sistema

### 1 - `importar-dados`
Importa todos os dados de `dados/`. Valida arquivos obrigatórios e pré-calcula filas iniciais.

```bash
python3 torre.py importar-dados

### `listar`
Lista todos os voos, ordenados por prioridade, voo, ou ETD.

```bash
python3 torre.py listar --por=prioridade
python3 torre.py listar --por=voo
python3 torre.py listar --por=etd

### **3 - `enfileirar`**
Adiciona um voo à fila de decolagem ou pouso, respeitando regras de negócio (piloto, aeronave, duplicidade, etc).

```bash
python3 torre.py enfileirar decolagem --voo ALT123
python3 torre.py enfileirar pouso --voo ALT901

### 4 - `autorizar`
Autoriza ou nega o primeiro voo da fila escolhida. Verifica pista, NOTAM, clima e regras de prioridade.

```bash
python3 torre.py autorizar decolagem --pista 10/28
python3 torre.py autorizar pouso --pista 01/19

**### 5 - `status`**
Mostra o status completo da torre

```bash
python3 torre.py status

**### 6 - `relatorio`
Gera resumo do turno com métricas

```bash
python3 torre.py relatorio







