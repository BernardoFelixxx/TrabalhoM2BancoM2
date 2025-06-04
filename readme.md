# Simulador de Transações Concorrentes com Detecção de Deadlock

Este programa simula a execução de transações concorrentes com controle de acesso a recursos e detecção/resolução de deadlocks utilizando a política **wait-die baseada em timestamps**.

## Funcionalidades

- Execução de múltiplas threads representando transações.
- Simulação de bloqueios binários em recursos compartilhados (X e Y).
- Detecção e resolução de deadlocks com base em timestamps.
- Saída no terminal explicando cada etapa da execução.

## Como executar

### Pré-requisitos

- Python 3.8+

### Execução

```bash
python main.py
