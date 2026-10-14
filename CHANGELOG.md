# Changelog: casos-de-teste

Ciclo usado em cada versão: **usar → medir contra o gabarito → descobrir a causa → corrigir a instrução ou o script → testar de novo**.
Medição:
- `evals/gabarito.md`: armadilhas por cenário (A cupom, B cancelamento via Slack, C sem requisito, D pausar assinatura). Gabarito escrito **antes** de cada rodada.
- `tests/test_gerar_casos.py`: testes do script.

Cada teste prático roda numa sessão nova do Claude, que não vê o gabarito. As saídas reais de cada versão estão em `evals/resultados/`.

## Placar

| Versão | A | B | C | D | Total | Testes do script |
|---|---|---|---|---|---|---|
| v1.0, gabarito original | 12/12 | 11/11 | 3/3 | — | **26/26** | 17/17 |
| v1.0, gabarito da v1.1 | 12/14 | 11/14 | 3/3 | não rodou | 26/31 | — |
| v1.1 | 13/14 | **14/14** | 3/3* | 9/10 | **39/41** | 21/21 |
| v1.2 | **14/14** | 13/14 | 3/3* | **10/10** | **40/41** | 22/22 |
| v1.3 | **15/15** | **14/14** | 3/3* | **10/10** | **42/42** | 22/22 |
| v1.3 no cenário E (linha de base) | | | | | E: 9/9 | |
| v1.4 | **15/15** | **14/14** | 3/3* | **10/10** | **51/51** (com E: 9/9) | 28/28 |

\* As mudanças da v1.1, da v1.2 e da v1.3 não mexem no fluxo "sem requisito". O cenário C não foi rodado de novo.

## v1.4 (14/10/2026): melhorias encontradas em uso real

Fonte: aplicação da skill em 3 programas de verdade, com os casos executados.
- **Microagente RAG** (Java + Gemini): 15 casos passaram e 4 ficaram bloqueados pela cota do Gemini.
- **CineList API** (FastAPI): 22 de 23 passaram, com 1 bug real, depois corrigido.
- **gerar_ata.py** (CLI Python): 25 de 26 passaram, com 1 comportamento não documentado.

| # | Melhoria | Evidência | Prioridade |
|---|---|---|---|
| 1 | Para regras de validação ou aviso, o caso negativo natural é **"entrada limpa não gera aviso falso"** (falso positivo). A skill não sugere isso, e foi exatamente esse caso que achou o único defeito do gerar_ata.py | gerar_ata CT-24 | Alta |
| 2 | **Dependência externa indisponível** (LLM, provedor, gateway, banco) no checklist de erro provável e no passo 3 | Microagente: Gemini fora do ar → 500. CineList: TMDB falha → 500 (bug corrigido) | Alta |
| 3 | Instruir a escrever os casos **a partir do requisito, sem ler a implementação**; o código só serve para caminhos de rota, parâmetros e nomes de campos. Caso escrito olhando o código só confirma o que o código já faz | CineList: o bug só apareceu porque o caso seguiu a regra, não o código | Alta |
| 4 | `gerar_casos.py --registrar resultados.json`: preenche Status, Resultado obtido, Evidência e Bug na planilha, e a resposta das dúvidas resolvidas pela execução | Preenchi a planilha à mão com openpyxl nas 3 aplicações | Média |
| 5 | Em API e CLI, todo caso negativo confere **status/código de saída + ausência de efeito** (nada gravado, nenhum arquivo gerado). Orientar os passos por tipo de interface (tela, requisição, comando) | CineList e gerar_ata: o aviso de "resultado curto" em "Status 400" levou a isso manualmente | Média |
| 6 | O aviso de "ou" não deve disparar em caso listado em `bloqueia` (o resultado depende da dúvida) nem em lista negada ("não pede senha, código ou cartão") | Microagente CT-19; gerar_ata CT-04 e CT-23 | Baixa |

**O que foi implementado:**
- **SKILL.md:**
  - novos itens no passo 3: "Falso positivo" e "Dependência externa";
  - regra "o resultado esperado vem do requisito, nunca do código" (o código só serve para rotas e nomes, e a divergência é destacada na resposta);
  - regras "Negativo confere a ausência de efeito" e "Passos conforme a interface" (tela, API, linha de comando);
  - passo 6, "Registrar a execução", e o tipo `negativo` passa a incluir o falso positivo.
- **gerar_casos.py:**
  - `--registrar resultados.json` grava status, resultado obtido, evidência, bug, executor, data e as respostas das dúvidas, e valida IDs e status;
  - o aviso de "ou" ignora casos bloqueados e listas negadas;
  - o aviso de "resultado curto" sugere dizer o efeito.
- **references:** "dependência externa" e "falso positivo" entram no checklist.
- **Testes:** 6 novos, total 28/28.

**Medição.** O cenário E (webhook Pix, com código que diverge do requisito) foi escrito antes da mudança e rodado **também com a v1.3**, como linha de base.

| | v1.3 | v1.4 |
|---|---|---|
| Gabarito (A + B + D + E) | 48/48 | 48/48 |
| Dependência externa fora do ar (dúvidas + casos, A+B+D+E) | 2, só no E | **9, nos 4 cenários** |
| Caso de falso positivo no E | sim | sim |
| Divergência código × requisito destacada | sim, no meio da resposta | sim, em seção própria no topo |

**Leitura honesta:** o gabarito não separou as versões. A v1.3 já seguia o requisito e testava o falso positivo no E, porque o E deixa isso evidente. O efeito mensurável da v1.4 está em **lembrar de dependência externa onde ela não é óbvia**: no cancelamento (B), por exemplo, apareceu "e se o gateway ou o e-mail estiver fora do ar?". Nenhuma versão anterior tinha levantado isso. O resto da v1.4 (`--registrar`, a correção dos falsos positivos do "ou") é ganho de uso, medido pelos testes do script, e não pelo gabarito. Cada cenário rodou uma vez por versão.

**Uso real depois da v1.4** (`preparar_transcricao.py`): 11 casos, 10 passaram e 1 ficou bloqueado por dúvida. Foi o primeiro uso do `--registrar`, que gravou os 11 resultados na planilha sem edição manual. Dois ajustes pequenos para a próxima versão: (1) o `--registrar` repete os avisos de validação do casos.json, o que só polui a saída e pode ser desligado nesse modo; (2) permitir marcar um aviso como aceito, com motivo, no próprio casos.json (ex.: critério descritivo cujo caso negativo depende de uma dúvida), para ele não reaparecer a cada execução.

**Próximo passo para o gabarito:** ele está saturado (51/51). Para medir a próxima versão, ele precisa de armadilhas que a v1.4 ainda erra, tiradas de usos reais.

A melhoria 1 e a 3 vieram do mesmo aprendizado: o valor da skill está em testar **o que a regra diz**, inclusive o que ela diz que **não** deve acontecer.

## v1.3 (14/10/2026)

Corrige a regressão da v1.2. O gabarito ganhou a armadilha A15, escrita antes da rodada.

| Problema observado no teste da v1.2 | Causa | Correção |
|---|---|---|
| B10: resultado esperado afirmava "reembolso no cartão final 4242", mas o PO não disse para onde vai o reembolso | "Dados concretos" foi lido como licença para deixar o comportamento concreto também | Regra "Dado concreto não é comportamento concreto": dado de teste pode ser escolhido; o resultado esperado só afirma o que o requisito diz. Antes de gerar, o agente relê cada resultado e pergunta "o requisito diz isso, ou eu escolhi?" |
| A (nova A15): o "para pagar menos na primeira cobrança" virou critério CA7, e um caso afirmou que a renovação vem com o valor cheio | A skill não diferenciava o objetivo da história das regras dela | Regra no passo 2: o "para…" é objetivo, não critério; o que ele sugere vira dúvida |

**Resultado:** 42/42. Em B, o cartão de teste aparece só como dado, e o resultado esperado ficou "o gateway mostra reembolso de R$ 39,90". Em A, o objetivo da história virou a dúvida "o desconto vale só na primeira cobrança ou também nas renovações?". D não regrediu.

**Cuidado com o placar:** cada cenário rodou uma vez por versão. As saídas variam de uma execução para outra, então 42/42 quer dizer "nenhuma armadilha conhecida falhou nesta rodada", e não "a skill não erra". Pontos para a próxima versão:
- Em A, o CT-15 é ao mesmo tempo suposição e caso bloqueado por dúvida. Não está errado, mas é redundante: se o caso está bloqueado, a suposição sobra.
- Rodar cada cenário 3 vezes e testar com histórias reais da sprint.
- Encontrado ao aplicar a skill no microagente RAG: o aviso de "ou" no resultado esperado dá falso positivo em lista negada ("não pede senha, código ou cartão"). Proposta: ignorar o "ou" quando a frase tem "não"/"nenhum" antes dele.
- Encontrado ao **executar** os casos no microagente RAG: com o Gemini fora do ar (503 e depois 429), a API devolveu HTTP 500 sem corpo. Nenhum caso previa isso, porque a skill não lembra de testar **dependência externa indisponível** (LLM, gateway, banco). Proposta: acrescentar esse item ao checklist de suposição de erro e ao passo 3 do SKILL.md, com resultado esperado vindo do requisito ou, se ele não disser, uma dúvida.
- Aplicação na API do CineList (23 casos, 22 passaram e 1 falhou, com um bug real de 500 quando o TMDB falha). Aprendizados: (1) escrever os casos a partir das regras, sem ler a implementação, foi o que permitiu achar o bug; (2) o aviso "resultado curto demais" em "Status 400" foi útil, porque levou a conferir que nada foi gravado. Proposta: para API, o SKILL.md pode pedir "status + efeito no banco" em todo caso negativo.
- Para API, os passos saem bem como requisição e resposta ("Enviar POST /triagem…"), mas a skill não orienta isso. Vale uma linha no SKILL.md.

## v1.2 (14/10/2026)

Corrige os 2 erros que ficaram da v1.1. O gabarito é **o mesmo** da v1.1, para a comparação ser justa.

| Problema observado no teste da v1.1 | Causa | Correção |
|---|---|---|
| A14: 9 dúvidas em A (limite 8) | "Junte dúvidas parecidas" era só instrução, sem limite nem exemplo | O script avisa acima de 8 dúvidas. O SKILL.md traz o limite e um exemplo de como juntar duas dúvidas numa só |
| D4: faltou testar pausar uma assinatura já pausada | A regra de transição de estado estava só em `references/`, que o agente não leu | Passo 6 no fluxo do SKILL.md: tabela estado × ação, incluindo **repetir a ação no estado novo** |

**Resultado:** 40/41. As duas correções funcionaram: A teve 8 dúvidas com as que bloqueiam primeiro, e D ganhou o caso "com a assinatura já pausada, não é possível pausar de novo". Em D, o agente também escreveu casos de limite que valem em qualquer forma de contar os 12 meses e bloqueou só o caso ambíguo.

Erros que ficam para a v1.3:

| Problema | Causa provável | Correção proposta |
|---|---|---|
| B10 (regressão, era 14/14 na v1.1): os resultados afirmam que o reembolso vai "para o cartão final 4242", mas o PO não diz para onde o reembolso vai, e o próprio agente registrou isso como dúvida | A regra "dados concretos" foi lida como licença para tornar concreto também o **comportamento** | Regra: dado de teste concreto (cartão 4242) pode; resultado esperado só afirma o que o requisito diz ("reembolso de R$ 39,90 registrado no gateway") |
| Fora do gabarito, em A: o "**para** pagar menos na primeira cobrança" da história virou critério derivado (CA7), e o CT-19 deu como certo que a renovação vem com o valor cheio | A skill não diz que o "para…" da história de usuário é objetivo, não regra | Regra: o "para…" da história é objetivo; o que ele sugere vira dúvida ou suposição. Nova armadilha A15 no gabarito |

## v1.1 (14/10/2026)

A v1.0 acertou tudo no gabarito original, o que mostrou que **o gabarito estava fácil demais**. A leitura das saídas mostrou problemas que ele não media:

| Problema observado no teste da v1.0 | Causa | Correção |
|---|---|---|
| 11 dúvidas em A e em B, sem dizer quais impedem a execução. O PO não sabe por onde começar | A skill não diferenciava dúvida que trava de dúvida que só melhora o caso | Campo `bloqueia` nas dúvidas. O documento separa "Dúvidas que bloqueiam a execução" das outras, e a skill manda juntar dúvidas parecidas. O script avisa quando há mais de 6 dúvidas e nenhuma com `bloqueia` |
| O testador não via na planilha que o CT-10 (A) dependia de suposição nem que o CT-13 e o CT-14 só rodam depois da resposta do PO | A planilha não ligava casos a dúvidas e suposições | Coluna "Depende de" na planilha e "> Depende de…" no documento. Caso bloqueado já sai com status "Bloqueado". Suposições precisam apontar para casos, e o script dá erro se apontarem para um caso que não existe |
| Agentes escreveram "anotar na evidência", mas a planilha não tinha onde | Faltava a coluna | Coluna "Evidência (print/vídeo/log)" |
| "O título reproduz normalmente" (B, CT-10) passou pelo detector de resultado vago | A regex só pegava "funciona normalmente" | "normalmente", "corretamente" e "adequadamente" sozinhos também geram aviso. Exemplo novo no SKILL.md |
| O exemplo de JSON do SKILL.md gerava 2 avisos de "só positivos" | O exemplo não seguia a própria regra | 2 casos negativos no exemplo, que agora valida sem avisos |
| Requisito com critérios contraditórios não tinha regra | Faltava o caso | Regra: contradição vira dúvida que bloqueia, sem escolher um lado |

**Resultado:** 39/41. Os casos bloqueados saem como "Bloqueado" na planilha e as dúvidas que bloqueiam vêm primeiro nos 3 cenários. Em B, o agente achou uma contradição real no texto do PO: o anual mantém acesso até o fim do período **e** recebe os meses não usados de volta. Ela virou uma dúvida que bloqueia.

Erros que ficam para a v1.2:

| Problema | Causa provável | Correção proposta |
|---|---|---|
| A14: 9 dúvidas em A (limite 8). Duas são sobre mensagens que não estão escritas na história e podiam ser uma só | "Junte dúvidas parecidas" é só instrução; o script só avisa quando nenhuma dúvida bloqueia | Aviso no script acima de 8 dúvidas |
| D4: faltou o caso ou a dúvida de pausar uma assinatura que já está pausada | A regra de transição de estado está só em `references/`, e o agente não a leu | Trazer para o SKILL.md: "se a funcionalidade muda um estado, teste repetir a ação no estado novo" |

**Gabarito ampliado:** A13–A14, B12–B14 (dúvidas que bloqueiam, dúvidas enxutas, resultado vago) e o cenário **D** (pausar assinatura: critérios contraditórios, transição de estado, ciclo pago em andamento), com 10 armadilhas novas.

## v1.0 (14/10/2026)

Primeira versão: SKILL.md, `gerar_casos.py` (valida cobertura, IDs, resultados vagos e gera .md e .xlsx), `references/tecnicas-de-teste.md` e os cenários A, B e C com gabarito.
**Resultado:** 26/26. Pontos fortes: não inventou mensagens de erro, percebeu que o CA5 de A não pode ser alcançado com os planos que existem, tratou o arredondamento como dúvida e fez uma única pergunta no cenário sem requisito.
