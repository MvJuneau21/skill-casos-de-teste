# Casos de teste: Cupom de desconto no checkout

**Origem:** HIST-412 (arquivo A-cupom-checkout.md) · **Gerado em:** 14/10/2026

**18 casos:** 5 positivos, 5 negativos, 8 de borda · **Prioridade:** 4 Alta, 13 Média, 1 Baixa

## Pontos a confirmar com o PO

**Dúvidas que bloqueiam a execução** (responder primeiro):

- **D1.** Como arredondar descontos com meio centavo? Ex.: MINIMO5 no Mensal = 5% de R$ 39,90 = R$ 1,995 (total R$ 37,90 ou R$ 37,91?) _(CA1 · bloqueia CT-05 · Sem a regra não dá para julgar o total do CT-05; os outros casos usam contas exatas)_
- **D2.** A validade "31/12/2026" inclui o dia 31 inteiro (até 23:59)? Em qual fuso horário? _(CA3 · bloqueia CT-11 · Define se NEXI10 deve ser aceito em 31/12/2026 23:59; o CT-10 (01/01/2027) não depende disso)_
- **D3.** Se já há um cupom aplicado e o segundo é recusado (expirado, inexistente ou de primeira assinatura para ex-assinante), o primeiro continua valendo ou é removido? _(CA4, CA3 · bloqueia CT-14 · O total esperado do CT-14 pode ser R$ 359,10 (mantém NEXI10) ou R$ 399,00 (remove); hoje o caso só confere que os 15% não foram aplicados)_
- **D4.** Com os planos (mínimo R$ 39,90) e cupons atuais (máximo 50%), o total nunca chega perto de R$ 1,00. Podemos cadastrar em homologação planos de teste de R$ 2,00 e R$ 1,10? Ou o CA5 vale para outro cenário (cupom de valor fixo, plano futuro)? _(CA5 · bloqueia CT-15, CT-16 · Sem dado de teste o CA5 não pode ser executado)_

**Outras dúvidas** (o requisito não diz; nenhum caso inventa a resposta):

- **D5.** Como o sistema sabe que a pessoa "nunca assinou": pela conta, CPF ou cartão? Quem só usou teste grátis (se existir) conta como já assinou? _(CA6 · Pode exigir novos casos (mesmo CPF/cartão em conta nova, conta só com teste grátis); CT-04 e CT-17 usam os casos claros)_
- **D6.** Quais mensagens aparecem para código inexistente e para cupom de primeira assinatura usado por ex-assinante? _(CA1, CA6 · CT-06 e CT-17 conferem só o valor, não o texto da mensagem)_
- **D7.** Espaços antes ou depois do código (" NEXI10 ") são aceitos? _(CA2 · Se forem, cabe um caso a mais de entrada)_
- **D8.** Ao trocar de plano no checkout com cupom aplicado, o cupom é mantido e o desconto recalculado sobre o novo plano? _(CA1 · Pode virar um caso de transição Mensal → Anual)_
- **D9.** O desconto vale só na primeira cobrança (como diz o "para" da história) e as renovações do Mensal cobram R$ 39,90 cheio? _(CA1 · Fora do checkout; afeta testes de renovação)_

**Suposições** (usadas nos casos; se estiverem erradas, os casos indicados mudam):

- Código não cadastrado não aplica desconto (o requisito só descreve cupom válido e expirado) _(CT-06)_
- A validade inclui o dia 31/12/2026 inteiro, até 23:59 no horário de Brasília _(CT-11)_
- O checkout exige conta logada, e é por ela que o sistema identifica se a pessoa já assinou _(CT-04, CT-15, CT-17, CT-18)_
- Ex-assinante com assinatura cancelada conta como "já assinou" _(CT-17)_

## Critérios e cobertura

| Critério | Descrição | Casos | Dúvidas |
|---|---|---|---|
| CA1 | Cupom válido aplica desconto percentual (entre 5% e 50%) sobre o valor do plano escolhido | CT-01, CT-02, CT-03, CT-04, CT-05, CT-06, CT-18 | D1, D6, D8, D9 |
| CA2 | O código do cupom não diferencia maiúsculas de minúsculas | CT-07, CT-08 | D7 |
| CA3 | Cupom fora da validade mostra "Este cupom expirou" e o valor não muda | CT-08, CT-09, CT-10, CT-11, CT-14 | D2, D3 |
| CA4 | Só um cupom por pedido; aplicar um segundo cupom substitui o primeiro | CT-12, CT-13, CT-14 | D3 |
| CA5 | O valor final nunca fica abaixo de R$ 1,00 | CT-15, CT-16 | D4 |
| CA6 | Cupons do tipo "primeira assinatura" só valem para quem nunca assinou o Nexi Play | CT-04, CT-17, CT-18 | D5, D6 |

## Casos

### CT-01 · NEXI10 no plano Mensal reduz o total para R$ 35,91

**Critérios:** CA1 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

**Pré-condições:**
- Visitante logado com conta que nunca assinou
- Checkout aberto com o plano Mensal (R$ 39,90)

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom`: NEXI10 (10%, validade 31/12/2026)

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido muda de R$ 39,90 para R$ 35,91 (desconto de R$ 3,99) e o cupom NEXI10 aparece como aplicado no resumo do pedido

### CT-02 · NEXI10 no plano Anual reduz o total para R$ 359,10

**Critérios:** CA1 · **Tipo:** positivo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Visitante logado com conta que nunca assinou
- Checkout aberto com o plano Anual (R$ 399,00)

**Dados:**
- `plano`: Anual R$ 399,00
- `cupom`: NEXI10 (10%, validade 31/12/2026)

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido muda de R$ 399,00 para R$ 359,10 (desconto de R$ 39,90)

### CT-03 · Cupom de 5% (limite mínimo) no Anual reduz o total para R$ 379,05

**Critérios:** CA1 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

**Pré-condições:**
- Visitante logado com conta que nunca assinou
- Checkout aberto com o plano Anual (R$ 399,00)

**Dados:**
- `plano`: Anual R$ 399,00
- `cupom`: MINIMO5 (5%, validade 31/12/2026)

**Passos:**
1. Informar MINIMO5 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido muda de R$ 399,00 para R$ 379,05 (desconto de R$ 19,95)

### CT-04 · Cupom de 50% (limite máximo) de primeira assinatura é aceito para quem nunca assinou

**Critérios:** CA1, CA6 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

> Depende de Suposição: O checkout exige conta logada, e é por ela que o sistema identifica se a pessoa já assinou

**Pré-condições:**
- Visitante logado com conta criada hoje, sem nenhuma assinatura anterior
- Checkout aberto com o plano Anual (R$ 399,00)

**Dados:**
- `plano`: Anual R$ 399,00
- `cupom`: BEMVINDO50 (50%, primeira assinatura, validade 31/12/2026)

**Passos:**
1. Informar BEMVINDO50 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido muda de R$ 399,00 para R$ 199,50 (desconto de R$ 199,50)

### CT-05 · MINIMO5 no Mensal expõe o arredondamento de meio centavo (ver dúvida de arredondamento)

**Critérios:** CA1 · **Tipo:** borda · **Técnica:** suposição de erro · **Prioridade:** Baixa

> Depende de D1 (bloqueia)

**Pré-condições:**
- Visitante logado com conta que nunca assinou
- Checkout aberto com o plano Mensal (R$ 39,90)
- 5% de R$ 39,90 = R$ 1,995: depende da regra de arredondamento pedida ao PO

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom`: MINIMO5 (5%, validade 31/12/2026)

**Passos:**
1. Informar MINIMO5 no campo de cupom
2. Clicar em Aplicar
3. Anotar o desconto e o total exibidos no checkout
4. Concluir o pagamento com cartão de teste
5. Comparar o valor cobrado com o total exibido no checkout

**Resultado esperado:** Desconto e total seguem a regra de arredondamento definida pelo PO, e o valor cobrado é igual ao total exibido no checkout

### CT-06 · Código inexistente não altera o total do Mensal

**Critérios:** CA1 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Média

> Depende de Suposição: Código não cadastrado não aplica desconto (o requisito só descreve cupom válido e expirado)

**Pré-condições:**
- Visitante logado com conta que nunca assinou
- Checkout aberto com o plano Mensal (R$ 39,90)

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom`: NEXI100 (não cadastrado)

**Passos:**
1. Informar NEXI100 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total continua R$ 39,90 e nenhum cupom aparece como aplicado no resumo do pedido

### CT-07 · Código com maiúsculas e minúsculas misturadas (nExI10) aplica o mesmo desconto

**Critérios:** CA2 · **Tipo:** positivo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Visitante logado com conta que nunca assinou
- Checkout aberto com o plano Mensal (R$ 39,90)

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom digitado`: nExI10

**Passos:**
1. Informar nExI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido muda de R$ 39,90 para R$ 35,91, igual ao CT-01

### CT-08 · Cupom expirado digitado em minúsculas continua recusado como expirado

**Critérios:** CA2, CA3 · **Tipo:** negativo · **Técnica:** tabela de decisão · **Prioridade:** Média

**Pré-condições:**
- Visitante logado com conta que nunca assinou
- Checkout aberto com o plano Mensal (R$ 39,90)

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom digitado`: verao15 (VERAO15, 15%, validade 31/03/2026)

**Passos:**
1. Informar verao15 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Aparece a mensagem "Este cupom expirou" e o total continua R$ 39,90

### CT-09 · Cupom expirado mostra "Este cupom expirou" e mantém o valor

**Critérios:** CA3 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Visitante logado com conta que nunca assinou
- Checkout aberto com o plano Anual (R$ 399,00)

**Dados:**
- `plano`: Anual R$ 399,00
- `cupom`: VERAO15 (15%, validade 31/03/2026)

**Passos:**
1. Informar VERAO15 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Aparece a mensagem "Este cupom expirou" e o total continua R$ 399,00

### CT-10 · Cupom no dia seguinte ao fim da validade (01/01/2027) é recusado como expirado

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

**Pré-condições:**
- Relógio do ambiente de homologação ajustado para 01/01/2027 00:01
- Visitante logado com conta que nunca assinou
- Checkout aberto com o plano Mensal (R$ 39,90)

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom`: NEXI10 (10%, validade 31/12/2026)
- `data/hora do teste`: 01/01/2027 00:01

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Aparece a mensagem "Este cupom expirou" e o total continua R$ 39,90

### CT-11 · Cupom no último minuto da validade (31/12/2026 23:59) é aceito

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D2 (bloqueia)

> Depende de Suposição: A validade inclui o dia 31/12/2026 inteiro, até 23:59 no horário de Brasília

**Pré-condições:**
- Relógio do ambiente de homologação ajustado para 31/12/2026 23:59 (horário de Brasília)
- Visitante logado com conta que nunca assinou
- Checkout aberto com o plano Mensal (R$ 39,90)

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom`: NEXI10 (10%, validade 31/12/2026)
- `data/hora do teste`: 31/12/2026 23:59

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido muda de R$ 39,90 para R$ 35,91 e a mensagem "Este cupom expirou" não aparece

### CT-12 · Segundo cupom substitui o primeiro, mesmo com desconto menor

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Alta

**Pré-condições:**
- Visitante logado com conta que nunca assinou
- Checkout aberto com o plano Anual (R$ 399,00)

**Dados:**
- `plano`: Anual R$ 399,00
- `1º cupom`: NEXI10 (10%)
- `2º cupom`: MINIMO5 (5%)

**Passos:**
1. Informar NEXI10 e clicar em Aplicar
2. Conferir total de R$ 359,10
3. Informar MINIMO5 e clicar em Aplicar

**Resultado esperado:** Total exibido passa a ser R$ 379,05 (só 5%), apenas MINIMO5 aparece como aplicado e o total não é R$ 339,15 (10% + 5% somados)

### CT-13 · Aplicar o mesmo cupom duas vezes não dobra o desconto

**Critérios:** CA4 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Média

**Pré-condições:**
- Visitante logado com conta que nunca assinou
- Checkout aberto com o plano Anual (R$ 399,00)

**Dados:**
- `plano`: Anual R$ 399,00
- `cupom`: NEXI10 (10%)

**Passos:**
1. Informar NEXI10 e clicar em Aplicar
2. Informar NEXI10 de novo e clicar em Aplicar

**Resultado esperado:** Total continua R$ 359,10 e NEXI10 aparece uma única vez no resumo do pedido

### CT-14 · Segundo cupom expirado não aplica os 15% (efeito sobre o 1º cupom depende de dúvida)

**Critérios:** CA4, CA3 · **Tipo:** borda · **Técnica:** tabela de decisão · **Prioridade:** Média

> Depende de D3 (bloqueia)

**Pré-condições:**
- Visitante logado com conta que nunca assinou
- Checkout aberto com o plano Anual (R$ 399,00)
- NEXI10 já aplicado (total R$ 359,10)

**Dados:**
- `plano`: Anual R$ 399,00
- `1º cupom`: NEXI10 (10%)
- `2º cupom`: VERAO15 (15%, validade 31/03/2026)

**Passos:**
1. Informar VERAO15 no campo de cupom
2. Clicar em Aplicar
3. Anotar o total e os cupons exibidos no resumo

**Resultado esperado:** Aparece a mensagem "Este cupom expirou", VERAO15 não aparece como aplicado e o total não é R$ 339,15 (15% de desconto)

### CT-15 · Desconto que resulta exatamente em R$ 1,00 mantém R$ 1,00

**Critérios:** CA5 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D4 (bloqueia)

> Depende de Suposição: O checkout exige conta logada, e é por ela que o sistema identifica se a pessoa já assinou

**Pré-condições:**
- Plano de teste de R$ 2,00 cadastrado em homologação (dado a criar, ver dúvida do CA5)
- Visitante logado com conta que nunca assinou
- Checkout aberto com o plano de teste de R$ 2,00

**Dados:**
- `plano`: Plano de teste R$ 2,00
- `cupom`: BEMVINDO50 (50%, primeira assinatura)

**Passos:**
1. Informar BEMVINDO50 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido muda de R$ 2,00 para R$ 1,00

### CT-16 · Desconto que daria R$ 0,99 é limitado e o total fica R$ 1,00

**Critérios:** CA5 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D4 (bloqueia)

**Pré-condições:**
- Plano de teste de R$ 1,10 cadastrado em homologação (dado a criar, ver dúvida do CA5)
- Visitante logado com conta que nunca assinou
- Checkout aberto com o plano de teste de R$ 1,10

**Dados:**
- `plano`: Plano de teste R$ 1,10
- `cupom`: NEXI10 (10%; R$ 1,10 - R$ 0,11 = R$ 0,99)

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido é R$ 1,00, e não R$ 0,99

### CT-17 · Ex-assinante não recebe desconto do cupom de primeira assinatura

**Critérios:** CA6 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Alta

> Depende de Suposição: O checkout exige conta logada, e é por ela que o sistema identifica se a pessoa já assinou

> Depende de Suposição: Ex-assinante com assinatura cancelada conta como "já assinou"

**Pré-condições:**
- Visitante logado com conta que já assinou o Mensal e cancelou (assinatura encerrada)
- Checkout aberto com o plano Mensal (R$ 39,90)

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom`: BEMVINDO50 (50%, primeira assinatura)

**Passos:**
1. Informar BEMVINDO50 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total continua R$ 39,90 (não muda para R$ 19,95) e BEMVINDO50 não aparece como aplicado

### CT-18 · Ex-assinante recebe desconto de cupom que não é de primeira assinatura

**Critérios:** CA6, CA1 · **Tipo:** positivo · **Técnica:** partição de equivalência · **Prioridade:** Média

> Depende de Suposição: O checkout exige conta logada, e é por ela que o sistema identifica se a pessoa já assinou

**Pré-condições:**
- Visitante logado com conta que já assinou o Mensal e cancelou (assinatura encerrada)
- Checkout aberto com o plano Mensal (R$ 39,90)

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom`: NEXI10 (10%, sem restrição de primeira assinatura)

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido muda de R$ 39,90 para R$ 35,91

## Fora do escopo

- Cadastro e administração de cupons (incluindo tentar cadastrar desconto fora da faixa de 5% a 50%)
- Valor das renovações após a primeira cobrança
- Processamento do pagamento (cartão recusado, estorno)
- Testes genéricos de segurança, acessibilidade e desempenho
