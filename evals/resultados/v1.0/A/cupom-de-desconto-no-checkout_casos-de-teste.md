# Casos de teste: Cupom de desconto no checkout

**Origem:** HIST-412 (arquivo A-cupom-checkout.md) · **Gerado em:** 14/10/2026

**16 casos:** 4 positivos, 5 negativos, 7 de borda · **Prioridade:** 5 Alta, 11 Média, 0 Baixa

## Pontos a confirmar com o PO

**Dúvidas** (o requisito não diz; nenhum caso inventa a resposta):

- **D1.** Qual mensagem aparece para código inexistente? _(CA1 · CT-04 confere só que o desconto não é aplicado, não a mensagem)_
- **D2.** Qual a regra de arredondamento quando o desconto tem fração de centavo? Ex.: MINIMO5 no Mensal dá R$ 1,995 de desconto (total R$ 37,90 ou R$ 37,91?) _(CA1 · CT-05 só registra o valor exibido; não dá para dizer se está certo)_
- **D3.** O desconto vale só na primeira cobrança (a história diz 'pagar menos na primeira cobrança')? A renovação volta ao preço cheio? _(CA1 · Nenhum caso cobre a segunda cobrança)_
- **D4.** Se o visitante aplica o cupom e depois troca de plano (Mensal → Anual), o cupom continua aplicado e o desconto é recalculado sobre o novo plano? _(CA1 · Sem caso de troca de plano com cupom aplicado)_
- **D5.** Espaços antes/depois do código (' NEXI10 ') são ignorados? E clicar em Aplicar com o campo vazio? _(CA1, CA2 · Sem caso para espaços e campo vazio)_
- **D6.** A validade 31/12/2026 inclui o dia 31 inteiro (até 23:59)? Em qual fuso horário? _(CA3 · CT-10 depende de uma suposição)_
- **D7.** Com NEXI10 aplicado, se o visitante tentar um cupom expirado ou inválido, o NEXI10 continua aplicado ou é removido? _(CA3, CA4 · Sem caso para essa combinação)_
- **D8.** Com os planos atuais (mínimo R$ 39,90) e desconto máximo de 50%, o menor total possível é R$ 19,95: em que situação real a trava de R$ 1,00 atua? Dá para criar um plano ou cupom de teste em homologação? _(CA5 · CT-13 e CT-14 dependem de um plano de teste que não existe hoje)_
- **D9.** Qual mensagem aparece quando o cupom de primeira assinatura é recusado? _(CA6 · CT-15 confere só que o desconto não é aplicado)_
- **D10.** Como o sistema sabe que o visitante 'nunca assinou'? Por e-mail, CPF ou cartão? Quem criar conta nova com o mesmo CPF ou cartão de uma assinatura antiga consegue usar o BEMVINDO50? _(CA6 · Sem caso de fraude com conta nova; partição a definir)_
- **D11.** Quem só usou teste grátis, ou tem assinatura ativa, conta como 'já assinou'? Assinante ativo consegue chegar ao checkout? _(CA6 · Partições 'só teste grátis' e 'assinatura ativa' sem caso)_

**Suposições** (usadas nos casos; se estiverem erradas, os casos indicados mudam):

- A validade do cupom inclui o último dia inteiro, até 23:59 no horário de Brasília _(CT-10)_
- A trava de R$ 1,00 vale para qualquer plano, inclusive um plano de teste criado só para validar o CA5 _(CT-13, CT-14)_

## Critérios e cobertura

| Critério | Descrição | Casos | Dúvidas |
|---|---|---|---|
| CA1 | Cupom válido aplica desconto percentual sobre o valor do plano escolhido; cupons têm desconto entre 5% e 50% | CT-01, CT-02, CT-03, CT-04, CT-05, CT-16 | D1, D2, D3, D4, D5 |
| CA2 | O código do cupom não diferencia maiúsculas de minúsculas | CT-06, CT-07 | D5 |
| CA3 | Cupom fora da validade mostra a mensagem "Este cupom expirou" e o valor não muda | CT-07, CT-08, CT-09, CT-10 | D6, D7 |
| CA4 | Só um cupom por pedido; aplicar um segundo cupom substitui o primeiro | CT-11, CT-12 | D7 |
| CA5 | O valor final nunca fica abaixo de R$ 1,00 | CT-13, CT-14 | D8 |
| CA6 | Cupons do tipo "primeira assinatura" só valem para quem nunca assinou o Nexi Play | CT-03, CT-15, CT-16 | D9, D10, D11 |

## Casos

### CT-01 · Cupom NEXI10 no plano Mensal reduz o total para R$ 35,91

**Critérios:** CA1 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

**Pré-condições:**
- Data do ambiente entre 14/10/2026 e 31/12/2026
- Visitante no checkout com o plano Mensal (R$ 39,90) selecionado

**Dados:**
- `cupom`: NEXI10 (10%, validade 31/12/2026)
- `plano`: Mensal R$ 39,90

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Desconto exibido de R$ 3,99 e total muda de R$ 39,90 para R$ 35,91

### CT-02 · Cupom de 5% (MINIMO5) no plano Anual reduz o total para R$ 379,05

**Critérios:** CA1 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

**Pré-condições:**
- Data do ambiente entre 14/10/2026 e 31/12/2026
- Visitante no checkout com o plano Anual (R$ 399,00) selecionado

**Dados:**
- `cupom`: MINIMO5 (5%, validade 31/12/2026)
- `plano`: Anual R$ 399,00

**Passos:**
1. Informar MINIMO5 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Desconto exibido de R$ 19,95 e total muda de R$ 399,00 para R$ 379,05

### CT-03 · Cupom de 50% (BEMVINDO50) para quem nunca assinou reduz o Mensal para R$ 19,95

**Critérios:** CA1, CA6 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

**Pré-condições:**
- Data do ambiente entre 14/10/2026 e 31/12/2026
- Visitante com cadastro novo, sem nenhuma assinatura anterior do Nexi Play
- Checkout com o plano Mensal (R$ 39,90) selecionado

**Dados:**
- `cupom`: BEMVINDO50 (50%, primeira assinatura, validade 31/12/2026)
- `plano`: Mensal R$ 39,90
- `usuário`: nunca assinou

**Passos:**
1. Informar BEMVINDO50 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Desconto exibido de R$ 19,95 e total muda de R$ 39,90 para R$ 19,95

### CT-04 · Código inexistente não aplica desconto (mensagem: ver dúvida)

**Critérios:** CA1 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Visitante no checkout com o plano Mensal (R$ 39,90) selecionado
- Nenhum cupom NEXI99 cadastrado em homologação

**Dados:**
- `cupom`: NEXI99 (não cadastrado)
- `plano`: Mensal R$ 39,90

**Passos:**
1. Informar NEXI99 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Nenhuma linha de desconto aparece e o total continua R$ 39,90; anotar na evidência a mensagem exibida

### CT-05 · Desconto com fração de centavo (MINIMO5 no Mensal) expõe a regra de arredondamento

**Critérios:** CA1 · **Tipo:** borda · **Técnica:** suposição de erro · **Prioridade:** Média

**Pré-condições:**
- Data do ambiente entre 14/10/2026 e 31/12/2026
- Visitante no checkout com o plano Mensal (R$ 39,90) selecionado
- Regra de arredondamento ainda não definida (ver dúvida)

**Dados:**
- `cupom`: MINIMO5 (5%, validade 31/12/2026)
- `plano`: Mensal R$ 39,90
- `conta`: 39,90 × 5% = R$ 1,995 de desconto; total sem arredondar R$ 37,905

**Passos:**
1. Informar MINIMO5 no campo de cupom
2. Clicar em Aplicar
3. Avançar até a tela de confirmação do pagamento

**Resultado esperado:** Desconto e total aparecem com exatamente 2 casas decimais, o total fica abaixo de R$ 39,90 e o mesmo total aparece no checkout e na confirmação; registrar o valor exibido para comparar com a regra que o PO definir

### CT-06 · Código em minúsculas (nexi10) aplica o mesmo desconto que NEXI10

**Critérios:** CA2 · **Tipo:** positivo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Data do ambiente entre 14/10/2026 e 31/12/2026
- Visitante no checkout com o plano Mensal (R$ 39,90) selecionado

**Dados:**
- `cupom digitado`: nexi10
- `cupom cadastrado`: NEXI10 (10%, validade 31/12/2026)
- `plano`: Mensal R$ 39,90

**Passos:**
1. Informar nexi10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Desconto exibido de R$ 3,99 e total muda de R$ 39,90 para R$ 35,91

### CT-07 · Cupom expirado digitado em minúsculas (verao15) também mostra "Este cupom expirou"

**Critérios:** CA2, CA3 · **Tipo:** negativo · **Técnica:** tabela de decisão · **Prioridade:** Média

**Pré-condições:**
- Data do ambiente 14/10/2026 (depois de 31/03/2026)
- Visitante no checkout com o plano Mensal (R$ 39,90) selecionado

**Dados:**
- `cupom digitado`: verao15
- `cupom cadastrado`: VERAO15 (15%, validade 31/03/2026)
- `plano`: Mensal R$ 39,90

**Passos:**
1. Informar verao15 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Aparece a mensagem "Este cupom expirou" e o total continua R$ 39,90

### CT-08 · Cupom expirado VERAO15 mostra "Este cupom expirou" e não altera o valor

**Critérios:** CA3 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Alta

**Pré-condições:**
- Data do ambiente 14/10/2026 (depois de 31/03/2026)
- Visitante no checkout com o plano Anual (R$ 399,00) selecionado

**Dados:**
- `cupom`: VERAO15 (15%, validade 31/03/2026)
- `plano`: Anual R$ 399,00

**Passos:**
1. Informar VERAO15 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Aparece a mensagem "Este cupom expirou", nenhuma linha de desconto aparece e o total continua R$ 399,00

### CT-09 · NEXI10 no dia seguinte ao fim da validade (01/01/2027) mostra "Este cupom expirou"

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

**Pré-condições:**
- Relógio do ambiente ajustado para 01/01/2027 00:00
- Visitante no checkout com o plano Mensal (R$ 39,90) selecionado

**Dados:**
- `cupom`: NEXI10 (10%, validade 31/12/2026)
- `plano`: Mensal R$ 39,90
- `data/hora do ambiente`: 01/01/2027 00:00

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Aparece a mensagem "Este cupom expirou" e o total continua R$ 39,90

### CT-10 · NEXI10 no último minuto da validade (31/12/2026 23:59) ainda é aplicado

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

**Pré-condições:**
- Relógio do ambiente ajustado para 31/12/2026 23:59 (horário de Brasília)
- Visitante no checkout com o plano Mensal (R$ 39,90) selecionado
- Depende da suposição de que a validade inclui o dia 31/12 inteiro (ver dúvida)

**Dados:**
- `cupom`: NEXI10 (10%, validade 31/12/2026)
- `plano`: Mensal R$ 39,90
- `data/hora do ambiente`: 31/12/2026 23:59

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Desconto exibido de R$ 3,99 e total muda de R$ 39,90 para R$ 35,91

### CT-11 · Segundo cupom (MINIMO5) substitui o primeiro (NEXI10) sem somar descontos

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Alta

**Pré-condições:**
- Data do ambiente entre 14/10/2026 e 31/12/2026
- Visitante no checkout com o plano Anual (R$ 399,00) selecionado

**Dados:**
- `cupom 1`: NEXI10 (10%)
- `cupom 2`: MINIMO5 (5%)
- `plano`: Anual R$ 399,00

**Passos:**
1. Informar NEXI10 e clicar em Aplicar
2. Conferir que o total mostra R$ 359,10
3. Informar MINIMO5 e clicar em Aplicar

**Resultado esperado:** Só o cupom MINIMO5 aparece no pedido, o desconto exibido é R$ 19,95 e o total é R$ 379,05

### CT-12 · Aplicar o mesmo cupom NEXI10 duas vezes não dobra o desconto

**Critérios:** CA4 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Média

**Pré-condições:**
- Data do ambiente entre 14/10/2026 e 31/12/2026
- Visitante no checkout com o plano Mensal (R$ 39,90) selecionado

**Dados:**
- `cupom`: NEXI10 (10%)
- `plano`: Mensal R$ 39,90

**Passos:**
1. Informar NEXI10 e clicar em Aplicar
2. Informar NEXI10 de novo e clicar em Aplicar

**Resultado esperado:** Só um cupom NEXI10 aparece no pedido, o desconto exibido é R$ 3,99 e o total é R$ 35,91

### CT-13 · Desconto que leva o total a exatamente R$ 1,00 é aceito sem ajuste

**Critérios:** CA5 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

**Pré-condições:**
- Plano de teste de R$ 2,00 criado em homologação pelo dev (os planos reais não chegam a R$ 1,00; ver dúvida)
- Visitante com cadastro novo, sem nenhuma assinatura anterior
- Checkout com o plano de teste de R$ 2,00 selecionado

**Dados:**
- `cupom`: BEMVINDO50 (50%, primeira assinatura)
- `plano`: Plano de teste R$ 2,00
- `conta`: 2,00 × 50% = R$ 1,00 de desconto

**Passos:**
1. Informar BEMVINDO50 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido é R$ 1,00

### CT-14 · Desconto que levaria o total a R$ 0,99 fica travado em R$ 1,00

**Critérios:** CA5 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

**Pré-condições:**
- Plano de teste de R$ 1,98 criado em homologação pelo dev (ver dúvida)
- Visitante com cadastro novo, sem nenhuma assinatura anterior
- Checkout com o plano de teste de R$ 1,98 selecionado

**Dados:**
- `cupom`: BEMVINDO50 (50%, primeira assinatura)
- `plano`: Plano de teste R$ 1,98
- `conta`: 1,98 × 50% = R$ 0,99 de desconto; total sem trava R$ 0,99

**Passos:**
1. Informar BEMVINDO50 no campo de cupom
2. Clicar em Aplicar
3. Avançar até a tela de confirmação do pagamento

**Resultado esperado:** Total exibido é R$ 1,00 no checkout e na confirmação do pagamento

### CT-15 · Cupom de primeira assinatura (BEMVINDO50) não é aplicado para ex-assinante

**Critérios:** CA6 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Alta

**Pré-condições:**
- Data do ambiente entre 14/10/2026 e 31/12/2026
- Usuário logado que já assinou o Mensal e cancelou (assinatura encerrada)
- Checkout com o plano Mensal (R$ 39,90) selecionado

**Dados:**
- `cupom`: BEMVINDO50 (50%, primeira assinatura)
- `plano`: Mensal R$ 39,90
- `usuário`: ex-assinante, assinatura cancelada

**Passos:**
1. Informar BEMVINDO50 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Nenhuma linha de desconto aparece e o total continua R$ 39,90; anotar na evidência a mensagem exibida

### CT-16 · Cupom comum (NEXI10) continua valendo para ex-assinante

**Critérios:** CA6, CA1 · **Tipo:** positivo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Data do ambiente entre 14/10/2026 e 31/12/2026
- Usuário logado que já assinou o Mensal e cancelou (assinatura encerrada)
- Checkout com o plano Mensal (R$ 39,90) selecionado

**Dados:**
- `cupom`: NEXI10 (10%, sem restrição de primeira assinatura)
- `plano`: Mensal R$ 39,90
- `usuário`: ex-assinante, assinatura cancelada

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Desconto exibido de R$ 3,99 e total muda de R$ 39,90 para R$ 35,91

## Fora do escopo

- Cadastro e configuração de cupons no admin (inclusive tentar criar cupom com 4% ou 51%)
- Remover o cupom aplicado sem aplicar outro
- Cobrança de renovação depois da primeira mensalidade/anuidade
- Processamento do pagamento (cartão, Pix) depois do checkout
