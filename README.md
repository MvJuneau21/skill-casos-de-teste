# Skill `casos-de-teste` para o Claude

Skill para o Claude Code que transforma um requisito (história de usuário, critérios de aceite, regra de negócio ou uma mensagem solta do PO) em:

1. **Um documento `.md` para revisar com PO e dev**, com as dúvidas que o requisito deixa em aberto (primeiro as que travam a execução), as suposições, a cobertura por critério e os casos: positivos, negativos e de borda, com dados concretos e resultado esperado verificável.
2. **Uma planilha `.xlsx` de execução**, com status por caso (os que dependem de resposta do PO já saem como "Bloqueado"), colunas de resultado obtido, evidência e bug, matriz de rastreabilidade critério × caso e um resumo que se atualiza sozinho.

> Os cenários em `evals/` (cupom, cancelamento, pausa de assinatura, webhook Pix) são **fictícios**, criados para testar a skill.

## O problema

Casos de teste costumam falhar de três jeitos:
- **inventam comportamento:** o requisito não diz qual mensagem aparece, e o caso afirma uma;
- **deixam buracos:** um critério fica sem teste, ou só o caminho feliz é testado, sem os limites ("no 7º dia ainda tem reembolso? e no 8º?");
- **não podem ser conferidos:** "o sistema funciona corretamente" não diz o que olhar.

A skill ataca esses três pontos e transforma as lacunas do requisito em perguntas para o PO, em vez de chutes.

## Estrutura

```
casos-de-teste/
├── SKILL.md                     fluxo, regras e formato do JSON
├── CHANGELOG.md                 histórico de melhorias (v1.0 → v1.4), placar e próximos passos
├── scripts/gerar_casos.py       valida o JSON, gera o .md e o .xlsx e registra a execução (--registrar)
├── references/
│   └── tecnicas-de-teste.md     partição, valor limite, tabela de decisão, transição de estado, erros prováveis
├── evals/
│   ├── A-cupom-checkout.md      história com critérios de aceite
│   ├── B-cancelamento-slack.txt mensagem solta do PO
│   ├── C-sem-requisito.txt      pedido sem requisito (a skill deve perguntar)
│   ├── D-pausar-assinatura.md   critérios que se contradizem
│   ├── E-webhook/               requisito + código que diverge dele
│   ├── gabarito.md              armadilhas de cada cenário, escritas antes de cada rodada
│   └── resultados/              saídas reais de cada versão
└── tests/test_gerar_casos.py    28 testes automatizados do script
```

## Como instalar e usar

```bash
# 1. Coloque a pasta em ~/.claude/skills/
git clone https://github.com/MvJuneau21/skill-casos-de-teste ~/.claude/skills/casos-de-teste

# 2. Dependência do script (Python 3.10+)
pip install openpyxl
```

Depois é só pedir no Claude Code: *"gera os casos de teste dessa história"* (colando a história ou anexando o arquivo), ou chamar `/casos-de-teste`.

Quando os casos forem executados, grave os resultados na planilha sem editar à mão:

```bash
python scripts/gerar_casos.py casos.json --saida <pasta> --registrar resultados.json
```

## Como ela foi testada e refinada

- **Gabarito escrito antes de cada rodada.** Cada cenário tem "armadilhas": a mensagem de erro que não está no requisito, o limite que nenhum plano cadastrado alcança, a conta que depende de um arredondamento indefinido.
- **Teste às cegas:** a cada versão, sessões novas do Claude usam a skill sem ver o gabarito. As saídas reais ficam em `evals/resultados/`.
- **Uso em programas reais:** a skill foi aplicada a uma API REST, a um serviço RAG com LLM e a duas ferramentas de linha de comando, e os casos foram executados. Numa API, um caso escrito a partir da regra (e não do código) encontrou um bug real: uma falha do provedor externo virava erro 500. A correção foi retestada com os mesmos casos.

| Versão | Placar | O que mudou |
|---|---|---|
| v1.0 | 26/26 | Primeira versão; o placar perfeito mostrou que o gabarito era fácil |
| v1.1 | 39/41 | Dúvidas que bloqueiam × que não bloqueiam, coluna "Depende de", detector de resultado vago |
| v1.2 | 40/41 | Limite de dúvidas, regra de transição de estado no passo a passo |
| v1.3 | 42/42 | "Dado concreto não é comportamento concreto"; o "para…" da história é objetivo, não regra |
| v1.4 | 51/51 | Falso positivo, dependência externa fora do ar, resultado esperado vem do requisito e não do código, `--registrar` |

O detalhe de cada mudança (problema → causa → correção) e a leitura honesta de cada placar estão no [CHANGELOG](CHANGELOG.md).
