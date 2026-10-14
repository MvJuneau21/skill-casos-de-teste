# Gabarito dos evals: casos-de-teste

Escrito **antes** da primeira execução. Cada armadilha vale 1 ponto. Quem roda o teste é uma sessão nova do Claude que usa a skill e **não vê este arquivo**.

Data de referência dos testes: 14/10/2026 (VERAO15 já está vencido).

## Cenário A: HIST-412 cupom no checkout (`A-cupom-checkout.md`), 12 pontos (14 a partir da v1.1, 15 a partir da v1.3)

Contas de referência: Mensal 39,90 × 10% = 3,99 → **35,91** · × 50% = **19,95** · × 15% = 5,985 e × 5% = 1,995 (**dependem de arredondamento**). Anual 399,00 × 5% = 19,95 → **379,05** · × 10% → **359,10** · × 15% = 59,85 → **339,15** · × 50% → **199,50**.

| # | Armadilha | Passa se |
|---|---|---|
| A1 | Cobertura | CA1–CA6 têm caso (CA5 pode ter só dúvida, se justificada) |
| A2 | Mensagem de cupom inexistente | Nenhum resultado esperado traz entre aspas uma mensagem que não está na HIST (só "Este cupom expirou" existe). Comportamento de cupom inexistente vira dúvida |
| A3 | Arredondamento | Nenhum caso afirma como certo um valor que depende de arredondamento (Mensal com 15% ou 5%) sem dúvida ou suposição registrada |
| A4 | Contas | Todos os valores calculados conferem com a tabela acima |
| A5 | CA5 inalcançável | Reconhece que nenhum plano + cupom dado chega abaixo de R$ 1,00 (mínimo é 19,95) e pede dado especial (dúvida ou pré-condição). Não inventa conta falsa |
| A6 | Último dia da validade | Dúvida ou suposição sobre se o dia da validade conta (inclusive?) |
| A7 | Primeira assinatura | Caso negativo com quem **já assinou e cancelou** |
| A8 | Faixa 5%–50% | Limites 5% (MINIMO5) e 50% (BEMVINDO50) testados; nenhum caso de checkout com cupom de 4% ou 51% e resultado inventado |
| A9 | Maiúsculas/minúsculas | Caso com variação de caixa (ex.: "nexi10") |
| A10 | Segundo cupom | Caso de substituição, com o valor final do segundo cupom |
| A11 | Prioridade e negativos | ≤ 50% Alta, e nenhum aviso de "só positivos" ignorado sem motivo |
| A12 | Execução | Script rodou sem erro e gerou .md e .xlsx |

Armadilhas acrescentadas na v1.1 (vindas da leitura das saídas da v1.0):

| # | Armadilha | Passa se |
|---|---|---|
| A13 | Dúvida que bloqueia | A dúvida do CA5 (dado de teste que não existe) bloqueia os casos do CA5 (`bloqueia`), e o arredondamento bloqueia o caso que o expõe |
| A14 | Dúvidas enxutas | ≤ 8 dúvidas, com as que bloqueiam primeiro |

Armadilha acrescentada na v1.3 (vinda da leitura das saídas da v1.2):

| # | Armadilha | Passa se |
|---|---|---|
| A15 | Objetivo da história não é regra | O "para pagar menos na primeira cobrança" não vira critério nem resultado esperado certo (ex.: "renovação vem com o valor cheio"). Se aparecer, é como dúvida ou suposição |

Bônus (não pontua): dúvida sobre o desconto valer só na primeira cobrança ou nas renovações; dúvida sobre usuário que só fez teste grátis.

## Cenário B: cancelamento, texto do Slack (`B-cancelamento-slack.txt`), 11 pontos (14 a partir da v1.1)

Contas de referência: Anual 399,00 / 12 = **33,25 por mês**. Cancelou com 3 meses completos usados → 9 × 33,25 = **299,25**. Usar 39,90 (preço do Mensal) como base do Anual é suposição, não regra.

| # | Armadilha | Passa se |
|---|---|---|
| B1 | Critérios derivados | ≥ 6 critérios com `"fonte": "derivado"` |
| B2 | Limite de 7 dias | Casos no dia 7 (dentro) e dia 8 (fora) **e** dúvida sobre como contar (dia 0 ou 1, corridos ou horas) |
| B3 | Proporcional | Valor calculado num caso **e** dúvida sobre mês parcial ou base de cálculo |
| B4 | Mensal depois de 7 dias | "Sem reembolso" aparece como suposição, não como regra do PO |
| B5 | Desistir na confirmação | Caso negativo: assinatura continua ativa |
| B6 | Fim do período | Casos de acesso até o fim do período e de não cobrar na renovação, com pré-condição de simular data |
| B7 | E-mail | Caso verifica que o e-mail chega; conteúdo não inventado |
| B8 | Textos de tela | Nenhuma mensagem entre aspas além de "Tem certeza?" |
| B9 | Tabela de decisão | Mensal ≤7, Mensal >7, Anual ≤7 e Anual >7 cobertos |
| B10 | Forma e prazo do reembolso | Não inventa para onde vai o dinheiro nem em quantos dias; se citar, é dúvida |
| B11 | Execução | Script rodou sem erro e gerou .md e .xlsx |
| B12 | Dúvida que bloqueia | A contagem dos 7 dias bloqueia os casos de limite (dia 7/dia 8) |
| B13 | Resultado verificável | Nenhum resultado vago ("normalmente", "corretamente"): v1.0 tinha "reproduz normalmente" |
| B14 | Dúvidas enxutas | ≤ 8 dúvidas, com as que bloqueiam primeiro |

## Cenário C: sem requisito (`C-sem-requisito.txt`), 3 pontos

| # | Armadilha | Passa se |
|---|---|---|
| C1 | Para e pergunta | Não gera arquivos; faz **uma** pergunta (uma mensagem) |
| C2 | Pergunta útil | Cita ≥ 2 regras que mudam os casos (bloqueio por tentativas, mensagens, "lembrar de mim", SSO, recuperar senha…) |
| C3 | Sem regra inventada | Não afirma regras como fato (ex.: "bloqueia após 5 tentativas") |

## Cenário D: HIST-430 pausar assinatura (`D-pausar-assinatura.md`), 10 pontos. Criado na v1.1

| # | Armadilha | Passa se |
|---|---|---|
| D1 | Contradição CA1 x CA2 | "90 dias" x "máximo de 2 meses" vira dúvida que **bloqueia** o caso de 90 dias. Não escolhe um lado como certo |
| D2 | 60 dias = 2 meses? | A pausa de 60 dias é testada; a diferença entre 60 dias e 2 meses aparece na dúvida (bônus se citada) ou o caso de 60 dias não depende dela |
| D3 | Limite de 12 meses | Caso de segunda pausa recusada dentro de 12 meses **e** dúvida sobre de quando contar (início ou fim da pausa) |
| D4 | Transição proibida | Caso ou dúvida para pausar de novo uma assinatura já pausada |
| D5 | Ciclo pago em andamento | Dúvida sobre os dias já pagos do ciclo atual quando a pausa começa (perde, adia ou só começa no fim do ciclo?) |
| D6 | Retomada antecipada | Caso com cobrança no dia da retomada e dúvida sobre a data das próximas cobranças |
| D7 | CA4 completo | Casos para sem cobrança, sem reprodução e downloads apagados (pode ser 1 caso por efeito ou combinado, com resultado verificável) |
| D8 | Anual | Caso negativo: botão Pausar não aparece |
| D9 | Sem mensagem inventada | Nenhum texto de tela entre aspas (a HIST não tem nenhum) |
| D10 | Execução e prioridade | Script sem erro, ≤ 50% Alta |

## Cenário E: HIST-510 webhook Pix (`E-webhook/`), 9 pontos. Criado na v1.4

Entrada: `requisito.md` **e** `webhook_controller.py`. O código diverge do requisito de propósito: evento repetido responde **409** no código e **200** no requisito (CA3). O pedido ao agente é "monta os casos de teste dessa história; o código atual está junto".

| # | Armadilha | Passa se |
|---|---|---|
| E1 | Segue o requisito, não o código | O caso de evento repetido espera **200** (CA3). Bônus se apontar a divergência com o 409 do código |
| E2 | Ausência de efeito no negativo | O caso de assinatura inválida confere 401 **e** que a cobrança continua pendente |
| E3 | Evento repetido não reprocessa | Confere que não há segundo processamento (ex.: nenhum segundo alerta, nenhuma nova consulta ou alteração) |
| E4 | Falso positivo | Caso: valor **igual** ao da cobrança **não** gera alerta `VALOR_DIVERGENTE` |
| E5 | Limite do alerta | Caso com diferença pequena (ex.: R$ 39,89 ou 39,91) gera o alerta e marca como paga |
| E6 | Gateway fora do ar | Caso ou dúvida para a consulta do CA5 indisponível (erro, timeout) |
| E7 | Sem resposta inventada para o gateway fora do ar | Não afirma como certo um status (503, 500, 200) que o requisito não define; se aparece, é dúvida ou suposição |
| E8 | Passos de API | Passos com método, rota, corpo e cabeçalho (ex.: "Enviar POST /webhooks/pix com…") |
| E9 | Execução | Script sem erro, ≤ 50% Alta |

**Total: 26 pontos na v1.0 · 41 pontos na v1.1 e na v1.2 · 42 pontos na v1.3 · 51 pontos a partir da v1.4** (E só existe a partir da v1.4; para comparar com a v1.3, E também é rodado com a v1.3). (A 14, B 14, C 3, D 10). Armadilhas novas só valem a partir da versão em que foram criadas.
