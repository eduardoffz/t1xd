# Xadrez Simplificado em Python

Projeto da disciplina **Algoritmos e Lógica de Programação (BSI)** — sistema de xadrez simplificado rodando na web e no terminal.

## Objetivo

Construir um sistema de xadrez simplificado em Python puro (sem bibliotecas externas), com interface web e terminal, implementando movimentação, captura e controle de turnos para todas as peças.

## Como rodar

```bash
# Rodar os testes (todos devem passar)
python testes.py

# Rodar a partida demo no terminal
python main.py

# Iniciar o servidor web (acessar http://localhost:8000)
python servidor_web.py
```

## Estrutura de arquivos

```
xadrez/
├── main.py            # Integração: executar_jogada + partida demo (CLI)
├── tabuleiro.py       # Integrante 1 — Estrutura e tabuleiro
├── pecas_linha.py     # Integrante 2 — Torre, Bispo, Dama
├── capturas.py        # Integrante 3 — Rei, Cavalo, Capturas
├── peao.py            # Integrante 4 — Peão, Turnos
├── testes.py          # Integrante 4 — Testes unitários
├── README.md          # Integrante 4 — Este arquivo
├── relatorio.md       # Integrante 4 — Relatório do projeto
└── servidor_web.py    # Extra — Interface web
```

## Convenções

| Conceito | Representação |
|----------|---------------|
| Posição | Tupla `(linha, coluna)`, valores de 0 a 7 |
| Peça | String de 2 letras: tipo + cor (ex: `Tb` = torre branca) |
| Casa vazia | `"."` |
| Turno | `"brancas"` ou `"pretas"` |
| Tipos | T=torre, C=cavalo, B=bispo, D=dama, R=rei, P=peão |
| Cores | b=branca, p=preta |

**Layout:** Linha 0 = topo (pretas); Linha 7 = base (brancas).

## Tabela de funções por integrante

| Integrante | Arquivo | Funções |
|------------|---------|---------|
| 1 | `tabuleiro.py` | `criar_tabuleiro`, `mostrar_tabuleiro`, `tabuleiro_para_texto`, `posicao_valida`, `mover_peca`, `obter_peca`, `cor_da_peca`, `tipo_da_peca`, `notacao_para_posicao` |
| 2 | `pecas_linha.py` | `caminho_livre`, `movimento_torre`, `movimento_bispo`, `movimento_dama` |
| 3 | `capturas.py` | `movimento_rei`, `movimento_cavalo`, `mesma_cor`, `captura_permitida`, `capturar_peca` |
| 4 | `peao.py` | `movimento_peao`, `controlar_turno`, `trocar_turno` |
| Todos | `main.py` | `executar_jogada`, `partida_demo`, `rodar_demo_terminal` |

## Limitações

- Sem roque
- Sem en passant
- Sem promoção de peão
- Sem xeque ou xeque-mate

## Integrantes

1. [PREENCHER: Nome — Integrante 1]
2. [PREENCHER: Nome — Integrante 2]
3. [PREENCHER: Nome — Integrante 3]
4. [PREENCHER: Nome — Integrante 4]

