# Relatório do Projeto — Xadrez Simplificado em Python

## Objetivo do projeto

Desenvolver um sistema de xadrez simplificado em Python puro (sem bibliotecas externas), como trabalho da disciplina Algoritmos e Lógica de Programação (BSI). O sistema roda no terminal (partida demo) e na web (interface interativa), implementando movimentação de todas as peças, validação de movimentos, captura de peças adversárias e controle de turnos.

## Participação de cada integrante

| Integrante | Módulo | Responsabilidade |
|------------|--------|-----------------|
| [PREENCHER: Nome 1] | `tabuleiro.py` | Estrutura do tabuleiro, funções de posição, movimentação básica e notação |
| [PREENCHER: Nome 2] | `pecas_linha.py` | Movimentos de torre, bispo e dama; verificação de obstrução |
| [PREENCHER: Nome 3] | `capturas.py` | Movimentos do rei e cavalo; lógica de captura |
| [PREENCHER: Nome 4] | `peao.py`, `testes.py`, `README.md`, `relatorio.md` | Movimento do peão, controle de turnos, testes unitários e documentação |

A integração (`main.py` e `servidor_web.py`) foi feita em conjunto por todos os integrantes.

## Estrutura do sistema

O projeto é organizado em módulos independentes com importações unidirecionais:

- **tabuleiro.py** — Base do sistema. Não importa nada do projeto. Define a representação do tabuleiro (matriz 8×8 de strings), funções utilitárias (posição válida, obter peça, cor, tipo) e a conversão de notação algébrica.
- **pecas_linha.py** — Importa apenas `tabuleiro`. Implementa os movimentos de torre, bispo e dama, além da verificação de caminho livre (obstrução).
- **capturas.py** — Importa apenas `tabuleiro`. Implementa os movimentos do rei e do cavalo, verificação de mesma cor e lógica de captura.
- **peao.py** — Importa apenas `tabuleiro`. Implementa o movimento do peão (1 casa, 2 casas da posição inicial, captura diagonal) e o controle/troca de turnos.
- **main.py** — Importa todos os módulos. Implementa `executar_jogada` (validação completa em 7 etapas) e a partida demo com 15 jogadas (12 válidas + 3 inválidas).
- **testes.py** — Testes unitários com `unittest` cobrindo todas as peças, capturas, obstruções, turnos, movimentos inválidos e a demo.
- **servidor_web.py** — Servidor HTTP com interface web interativa usando apenas `http.server` e `json`.

## Dificuldades encontradas

- **Referências repetidas na matriz:** O uso de `[["."] * 8] * 8` cria 8 referências para a mesma lista, causando bugs difíceis de detectar. A solução foi criar cada linha individualmente com `for`.
- **Obstrução do peão de 2 casas:** Foi necessário verificar não apenas o destino, mas também a casa intermediária, para impedir o peão de "pular" por cima de peças.
- **Ordem das verificações em `executar_jogada`:** A especificação exige uma ordem precisa de validações (posição → peça → turno → movimento → mesma cor → captura). Errar essa ordem gera mensagens incorretas.
- **Diferença entre geometria e obstrução:** Para torre, bispo e dama, o movimento é verificado em duas etapas: primeiro a geometria pura (sem tabuleiro), depois com o tabuleiro para checar obstruções. Isso permite distinguir entre "movimento inválido" e "caminho obstruído".
- [PREENCHER: dificuldades pessoais dos integrantes, se houver]

## Soluções adotadas

- Uso de convenções rígidas (peça = 2 letras, posição = tupla, turno = string) para evitar ambiguidades entre módulos.
- Funções de movimento retornam apenas `True`/`False`, sem efeitos colaterais — somente `mover_peca` e `capturar_peca` alteram o tabuleiro.
- Testes abrangentes com `unittest`, verificando inclusive que jogadas rejeitadas não alteram o tabuleiro (comparação de cópia antes/depois).
- Partida demo com sequência fixa de 15 jogadas que exercita todas as peças (torre, bispo, cavalo, rei, dama, peão), capturas e erros.

## Conclusão e aprendizados

O projeto permitiu aplicar na prática os conceitos fundamentais de algoritmos e lógica de programação: funções, estruturas condicionais, laços, listas/tuplas/dicionários, e modularização. A divisão em módulos independentes com contratos bem definidos simulou o trabalho em equipe real, onde cada integrante precisa seguir uma interface acordada.

[PREENCHER: aprendizados pessoais dos integrantes]

