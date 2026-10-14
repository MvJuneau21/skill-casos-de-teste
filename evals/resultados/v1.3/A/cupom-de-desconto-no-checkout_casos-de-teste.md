# Casos de teste: Cupom de desconto no checkout

**Origem:** HIST-412 (arquivo A-cupom-checkout.md) · **Gerado em:** 14/10/2026

**20 casos:** 6 positivos, 6 negativos, 8 de borda · **Prioridade:** 5 Alta, 15 Média, 0 Baixa

## Pontos a confirmar com o PO

**Dúvidas que bloqueiam a execução** (responder primeiro):

- **D1.** Com os planos atuais (R$ 39,90 e R$ 399,00) e cupons de no máximo 50%, o menor total possível é R$ 19,95, então o piso de R$ 1,00 nunca é atingido. Em que situação o CA5 vale (outro plano, preço promocional, cupom acima de 50%)? Podemos cadastrar em homologação planos de teste de R$ 2,00 e R$ 1,98? _(CA5 · bloqueia CT-19, CT-20 · Sem um preço que chegue perto de R$ 1,00 não há como testar o CA5)_
- **D2.** Como arredondar centavos do desconto? Ex.: 5% de R$ 39,90 = R$ 1,995; o total fica R$ 37,90 ou R$ 37,91? _(CA1 · bloqueia CT-06 · Define o valor exato cobrado em descontos que não dão conta exata)_
- **D3.** A validade 31/12/2026 inclui o dia 31 inteiro (até 23:59:59)? Em qual fuso horário? _(CA3 · bloqueia CT-10 · Define se o cupom é aceito no último minuto do dia de validade)_
- **D4.** Quando o segundo cupom é recusado (expirado, inexistente ou não elegível), o primeiro cupom continua aplicado ou é removido? O CA3 diz que o valor não muda e o CA4 diz que o segundo substitui o primeiro. _(CA3, CA4 · bloqueia CT-14 · Define se o total fica R$ 359,10 ou volta para R$ 399,00)_
- **D5.** Ao trocar de plano no checkout com cupom já aplicado, o cupom continua e o desconto é recalculado sobre o novo plano? _(CA1 · bloqueia CT-15 · Risco de cobrar o Anual com o desconto calculado sobre o Mensal)_
- **D6.** Como o sistema decide que alguém 'nunca assinou' (conta/e-mail, CPF ou cartão)? Quem só fez teste grátis, sem pagar, conta como assinante? _(CA6 · bloqueia CT-18 · Define a elegibilidade ao BEMVINDO50 e se um ex-assinante consegue o cupom criando outra conta)_

**Outras dúvidas** (o requisito não diz; nenhum caso inventa a resposta):

- **D7.** A história diz 'pagar menos na primeira cobrança'. O desconto vale só na primeira cobrança ou também nas renovações? No Anual, vale para o primeiro ano inteiro? _(CA1 · Os casos conferem só o total do checkout; a cobrança da renovação não está coberta)_
- **D8.** Quais mensagens aparecem para código inexistente e para cupom de primeira assinatura recusado? Espaços antes ou depois do código (' NEXI10 ') são ignorados? _(CA1, CA2, CA6 · CT-05 e CT-16 conferem só o total, não a mensagem; não há caso para espaços no código)_

**Suposições** (usadas nos casos; se estiverem erradas, os casos indicados mudam):

- A validade de um cupom inclui o dia final inteiro, até 23:59 no horário de Brasília _(CT-10, CT-11)_
- Ao trocar de plano com cupom aplicado, o cupom continua e o desconto é recalculado sobre o novo plano _(CT-15)_
- O visitante já está identificado (logado ou com e-mail informado) quando aplica o cupom, para o sistema checar o CA6 _(CT-04, CT-16, CT-17, CT-18)_
- Cupom que não existe não aplica desconto (o CA1 só fala de cupom válido) _(CT-05)_

## Critérios e cobertura

| Critério | Descrição | Casos | Dúvidas |
|---|---|---|---|
| CA1 | Cupom válido aplica desconto percentual (entre 5% e 50%) sobre o valor do plano escolhido | CT-01, CT-02, CT-03, CT-04, CT-05, CT-06, CT-15 | D2, D5, D7, D8 |
| CA2 | O código do cupom não diferencia maiúsculas de minúsculas | CT-07, CT-08 | D8 |
| CA3 | Cupom fora da validade mostra "Este cupom expirou" e o valor não muda | CT-08, CT-09, CT-10, CT-11, CT-14 | D3, D4 |
| CA4 | Só um cupom por pedido; aplicar um segundo cupom substitui o primeiro | CT-12, CT-13, CT-14 | D4 |
| CA5 | O valor final nunca fica abaixo de R$ 1,00 | CT-19, CT-20 | D1 |
| CA6 | Cupons do tipo "primeira assinatura" só valem para quem nunca assinou o Nexi Play | CT-04, CT-16, CT-17, CT-18 | D6, D8 |

## Casos

### CT-01 · NEXI10 no plano Anual reduz o total para R$ 359,10

**Critérios:** CA1 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

**Pré-condições:**
- Visitante no checkout com o plano Anual (R$ 399,00) selecionado
- Usuário qa.novo01@nexi.test, nunca assinou

**Dados:**
- `cupom`: NEXI10 (10%, validade 31/12/2026)
- `plano`: Anual R$ 399,00

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido muda de R$ 399,00 para R$ 359,10 (desconto de R$ 39,90)

### CT-02 · NEXI10 no plano Mensal reduz o total para R$ 35,91

**Critérios:** CA1 · **Tipo:** positivo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Visitante no checkout com o plano Mensal (R$ 39,90) selecionado
- Usuário qa.novo02@nexi.test, nunca assinou

**Dados:**
- `cupom`: NEXI10 (10%, validade 31/12/2026)
- `plano`: Mensal R$ 39,90

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido muda de R$ 39,90 para R$ 35,91 (desconto de R$ 3,99)

### CT-03 · Cupom no limite mínimo de 5% (MINIMO5) aplica R$ 19,95 de desconto no Anual

**Critérios:** CA1 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

**Pré-condições:**
- Visitante no checkout com o plano Anual (R$ 399,00) selecionado
- Usuário qa.novo03@nexi.test, nunca assinou

**Dados:**
- `cupom`: MINIMO5 (5%, validade 31/12/2026)
- `plano`: Anual R$ 399,00

**Passos:**
1. Informar MINIMO5 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido muda de R$ 399,00 para R$ 379,05

### CT-04 · Cupom no limite máximo de 50% (BEMVINDO50) para quem nunca assinou deixa o Mensal em R$ 19,95

**Critérios:** CA1, CA6 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

> Depende de Suposição: O visitante já está identificado (logado ou com e-mail informado) quando aplica o cupom, para o sistema checar o CA6

**Pré-condições:**
- Visitante no checkout com o plano Mensal (R$ 39,90) selecionado
- Usuário qa.novo04@nexi.test, conta sem nenhuma assinatura anterior

**Dados:**
- `cupom`: BEMVINDO50 (50%, primeira assinatura, validade 31/12/2026)
- `plano`: Mensal R$ 39,90

**Passos:**
1. Informar BEMVINDO50 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido muda de R$ 39,90 para R$ 19,95

### CT-05 · Código de cupom inexistente não altera o total

**Critérios:** CA1 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Média

> Depende de Suposição: Cupom que não existe não aplica desconto (o CA1 só fala de cupom válido)

**Pré-condições:**
- Visitante no checkout com o plano Mensal (R$ 39,90) selecionado
- Cupom NEXI99 não cadastrado em homologação

**Dados:**
- `cupom`: NEXI99 (não cadastrado)
- `plano`: Mensal R$ 39,90

**Passos:**
1. Informar NEXI99 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido continua R$ 39,90 e nenhum desconto aparece no resumo do pedido

### CT-06 · MINIMO5 no Mensal expõe o arredondamento de centavos (R$ 1,995 de desconto)

**Critérios:** CA1 · **Tipo:** borda · **Técnica:** suposição de erro · **Prioridade:** Média

> Depende de D2 (bloqueia)

**Pré-condições:**
- Visitante no checkout com o plano Mensal (R$ 39,90) selecionado
- Usuário qa.novo05@nexi.test, nunca assinou
- Bloqueado pela dúvida de arredondamento

**Dados:**
- `cupom`: MINIMO5 (5%, validade 31/12/2026)
- `plano`: Mensal R$ 39,90
- `conta sem arredondar`: 39,90 - 1,995 = 37,905

**Passos:**
1. Informar MINIMO5 no campo de cupom
2. Clicar em Aplicar
3. Anotar o total exibido com 2 casas decimais

**Resultado esperado:** Total exibido fica entre R$ 37,90 e R$ 37,91, com 2 casas decimais; o valor exato correto será definido pela regra de arredondamento do PO

### CT-07 · Código digitado em minúsculas (nexi10) aplica o mesmo desconto do NEXI10

**Critérios:** CA2 · **Tipo:** positivo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Visitante no checkout com o plano Mensal (R$ 39,90) selecionado
- Usuário qa.novo06@nexi.test, nunca assinou

**Dados:**
- `cupom digitado`: nexi10
- `plano`: Mensal R$ 39,90

**Passos:**
1. Informar nexi10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido muda de R$ 39,90 para R$ 35,91

### CT-08 · Cupom expirado digitado em minúsculas (verao15) também é recusado com "Este cupom expirou"

**Critérios:** CA2, CA3 · **Tipo:** negativo · **Técnica:** tabela de decisão · **Prioridade:** Média

**Pré-condições:**
- Visitante no checkout com o plano Mensal (R$ 39,90) selecionado
- Data do ambiente posterior a 31/03/2026 (ex.: 14/10/2026)

**Dados:**
- `cupom digitado`: verao15
- `plano`: Mensal R$ 39,90

**Passos:**
1. Informar verao15 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Aparece a mensagem "Este cupom expirou" e o total continua R$ 39,90

### CT-09 · Cupom expirado VERAO15 mostra "Este cupom expirou" e não muda o total

**Critérios:** CA3 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Alta

**Pré-condições:**
- Visitante no checkout com o plano Anual (R$ 399,00) selecionado
- Data do ambiente posterior a 31/03/2026 (ex.: 14/10/2026)

**Dados:**
- `cupom`: VERAO15 (15%, validade 31/03/2026)
- `plano`: Anual R$ 399,00

**Passos:**
1. Informar VERAO15 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Aparece a mensagem "Este cupom expirou" e o total continua R$ 399,00

### CT-10 · NEXI10 aplicado no último minuto da validade (31/12/2026 23:59) ainda dá desconto

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D3 (bloqueia)

> Depende de Suposição: A validade de um cupom inclui o dia final inteiro, até 23:59 no horário de Brasília

**Pré-condições:**
- Relógio do ambiente de homologação ajustado para 31/12/2026 23:59 (horário de Brasília)
- Visitante no checkout com o plano Mensal (R$ 39,90) selecionado
- Bloqueado pela dúvida sobre o fim da validade

**Dados:**
- `cupom`: NEXI10 (10%, validade 31/12/2026)
- `plano`: Mensal R$ 39,90
- `data/hora do ambiente`: 31/12/2026 23:59 (Brasília)

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido muda de R$ 39,90 para R$ 35,91 e a mensagem "Este cupom expirou" não aparece

### CT-11 · NEXI10 aplicado em 01/01/2027 00:01 é recusado como expirado

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de Suposição: A validade de um cupom inclui o dia final inteiro, até 23:59 no horário de Brasília

**Pré-condições:**
- Relógio do ambiente de homologação ajustado para 01/01/2027 00:01 (horário de Brasília)
- Visitante no checkout com o plano Mensal (R$ 39,90) selecionado

**Dados:**
- `cupom`: NEXI10 (10%, validade 31/12/2026)
- `plano`: Mensal R$ 39,90
- `data/hora do ambiente`: 01/01/2027 00:01 (Brasília)

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Aparece a mensagem "Este cupom expirou" e o total continua R$ 39,90

### CT-12 · Segundo cupom (MINIMO5) substitui o primeiro (NEXI10), mesmo com desconto menor

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Alta

**Pré-condições:**
- Visitante no checkout com o plano Anual (R$ 399,00) selecionado
- NEXI10 já aplicado, total exibido R$ 359,10

**Dados:**
- `primeiro cupom`: NEXI10 (10%)
- `segundo cupom`: MINIMO5 (5%)
- `plano`: Anual R$ 399,00

**Passos:**
1. Informar MINIMO5 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido passa de R$ 359,10 para R$ 379,05 e o resumo do pedido mostra só o cupom MINIMO5 (não R$ 339,15, que seria 10% + 5% somados)

### CT-13 · Aplicar o mesmo cupom NEXI10 duas vezes não dobra o desconto

**Critérios:** CA4 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Média

**Pré-condições:**
- Visitante no checkout com o plano Mensal (R$ 39,90) selecionado
- NEXI10 já aplicado, total exibido R$ 35,91

**Dados:**
- `cupom`: NEXI10 (10%)
- `plano`: Mensal R$ 39,90

**Passos:**
1. Informar NEXI10 de novo no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido continua R$ 35,91 e o resumo do pedido mostra um único desconto de R$ 3,99

### CT-14 · Cupom expirado aplicado por cima do NEXI10 não soma desconto (destino do NEXI10 em dúvida)

**Critérios:** CA3, CA4 · **Tipo:** negativo · **Técnica:** tabela de decisão · **Prioridade:** Média

> Depende de D4 (bloqueia)

**Pré-condições:**
- Visitante no checkout com o plano Anual (R$ 399,00) selecionado
- NEXI10 já aplicado, total exibido R$ 359,10
- Bloqueado pela dúvida sobre segundo cupom recusado

**Dados:**
- `primeiro cupom`: NEXI10 (10%)
- `segundo cupom`: VERAO15 (15%, validade 31/03/2026)
- `plano`: Anual R$ 399,00

**Passos:**
1. Informar VERAO15 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Aparece a mensagem "Este cupom expirou"; o total exibido não é R$ 339,15 (15% do VERAO15) nem R$ 299,25 (10% + 15%); se o NEXI10 continua aplicado será julgado após a resposta do PO

### CT-15 · Trocar de Mensal para Anual com NEXI10 aplicado recalcula o desconto sobre R$ 399,00

**Critérios:** CA1 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Média

> Depende de D5 (bloqueia)

> Depende de Suposição: Ao trocar de plano com cupom aplicado, o cupom continua e o desconto é recalculado sobre o novo plano

**Pré-condições:**
- Visitante no checkout com o plano Mensal (R$ 39,90) selecionado
- NEXI10 já aplicado, total exibido R$ 35,91
- Bloqueado pela dúvida sobre troca de plano com cupom aplicado

**Dados:**
- `cupom`: NEXI10 (10%)
- `plano inicial`: Mensal R$ 39,90
- `plano final`: Anual R$ 399,00

**Passos:**
1. Trocar o plano para Anual no checkout
2. Conferir o resumo do pedido

**Resultado esperado:** Total exibido passa a ser R$ 359,10 (10% sobre R$ 399,00), e não R$ 395,01 (desconto de R$ 3,99 do Mensal mantido)

### CT-16 · BEMVINDO50 não dá desconto para quem já assinou e cancelou

**Critérios:** CA6 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Alta

> Depende de Suposição: O visitante já está identificado (logado ou com e-mail informado) quando aplica o cupom, para o sistema checar o CA6

**Pré-condições:**
- Usuário qa.excancel01@nexi.test assinou o Mensal no passado e cancelou
- Visitante logado com esse usuário no checkout do Mensal (R$ 39,90)

**Dados:**
- `cupom`: BEMVINDO50 (50%, primeira assinatura)
- `plano`: Mensal R$ 39,90

**Passos:**
1. Informar BEMVINDO50 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido continua R$ 39,90 e nenhum desconto aparece no resumo do pedido

### CT-17 · Cupom comum (NEXI10) continua valendo para quem já assinou e cancelou

**Critérios:** CA6 · **Tipo:** positivo · **Técnica:** partição de equivalência · **Prioridade:** Média

> Depende de Suposição: O visitante já está identificado (logado ou com e-mail informado) quando aplica o cupom, para o sistema checar o CA6

**Pré-condições:**
- Usuário qa.excancel02@nexi.test assinou o Mensal no passado e cancelou
- Visitante logado com esse usuário no checkout do Mensal (R$ 39,90)

**Dados:**
- `cupom`: NEXI10 (10%, sem restrição de primeira assinatura)
- `plano`: Mensal R$ 39,90

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido muda de R$ 39,90 para R$ 35,91

### CT-18 · BEMVINDO50 para quem só usou teste grátis (elegibilidade em dúvida)

**Critérios:** CA6 · **Tipo:** borda · **Técnica:** partição de equivalência · **Prioridade:** Média

> Depende de D6 (bloqueia)

> Depende de Suposição: O visitante já está identificado (logado ou com e-mail informado) quando aplica o cupom, para o sistema checar o CA6

**Pré-condições:**
- Usuário qa.trial01@nexi.test fez teste grátis e nunca pagou uma assinatura
- Visitante logado com esse usuário no checkout do Mensal (R$ 39,90)
- Bloqueado pela dúvida sobre quem conta como 'já assinou'

**Dados:**
- `cupom`: BEMVINDO50 (50%, primeira assinatura)
- `plano`: Mensal R$ 39,90

**Passos:**
1. Informar BEMVINDO50 no campo de cupom
2. Clicar em Aplicar
3. Anotar o total exibido

**Resultado esperado:** O total exibido não fica abaixo de R$ 19,95 nem acima de R$ 39,90; se o cupom deve ser aceito será julgado após a resposta do PO

### CT-19 · Desconto que deixaria o total exatamente em R$ 1,00 é aplicado inteiro

**Critérios:** CA5 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D1 (bloqueia)

**Pré-condições:**
- Plano de teste de R$ 2,00 cadastrado em homologação (não existe hoje)
- Usuário qa.novo07@nexi.test, nunca assinou
- Bloqueado pela dúvida sobre como atingir o piso de R$ 1,00

**Dados:**
- `cupom`: BEMVINDO50 (50%)
- `plano`: Plano de teste R$ 2,00
- `conta`: 2,00 - 1,00 = 1,00

**Passos:**
1. Selecionar o plano de teste de R$ 2,00 no checkout
2. Informar BEMVINDO50 no campo de cupom
3. Clicar em Aplicar

**Resultado esperado:** Total exibido muda de R$ 2,00 para R$ 1,00

### CT-20 · Desconto que deixaria o total em R$ 0,99 é limitado e o total fica em R$ 1,00

**Critérios:** CA5 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D1 (bloqueia)

**Pré-condições:**
- Plano de teste de R$ 1,98 cadastrado em homologação (não existe hoje)
- Usuário qa.novo08@nexi.test, nunca assinou
- Bloqueado pela dúvida sobre como atingir o piso de R$ 1,00

**Dados:**
- `cupom`: BEMVINDO50 (50%)
- `plano`: Plano de teste R$ 1,98
- `conta sem piso`: 1,98 - 0,99 = 0,99

**Passos:**
1. Selecionar o plano de teste de R$ 1,98 no checkout
2. Informar BEMVINDO50 no campo de cupom
3. Clicar em Aplicar

**Resultado esperado:** Total exibido fica em R$ 1,00, e não em R$ 0,99

## Fora do escopo

- Cadastro e administração de cupons, incluindo a regra de 5% a 50% (4% e 51% não são informados pelo visitante)
- Remover um cupom já aplicado
- Processamento do pagamento no gateway e cobranças de renovação
- Cupom aplicado por assinante ativo fora do checkout de nova assinatura (troca de plano)
