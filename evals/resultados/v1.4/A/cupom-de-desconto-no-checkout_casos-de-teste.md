# Casos de teste: Cupom de desconto no checkout

**Origem:** HIST-412 (arquivo A-cupom-checkout.md) · **Gerado em:** 14/10/2026

**21 casos:** 5 positivos, 7 negativos, 9 de borda · **Prioridade:** 6 Alta, 14 Média, 1 Baixa

## Pontos a confirmar com o PO

**Dúvidas que bloqueiam a execução** (responder primeiro):

- **D1.** Com os planos atuais (R$ 39,90 e R$ 399,00) e desconto máximo de 50%, o menor total possível é R$ 19,95, então o piso de R$ 1,00 do CA5 não é alcançável. Ele vale para planos ou promoções futuras? Podemos cadastrar em homologação planos de teste de R$ 2,00 e R$ 1,98 para testar o piso? _(CA5 · bloqueia CT-17, CT-18 · Sem dado de teste não dá para executar os casos do piso)_
- **D2.** A validade "31/12/2026" inclui o dia 31 inteiro (até 23:59)? Em qual fuso horário (Brasília ou UTC)? _(CA3 · bloqueia CT-13 · Define se o cupom é aceito no último dia e em que horário vira expirado)_
- **D3.** Como arredondar descontos com fração de centavo? Ex.: 5% de R$ 39,90 = R$ 1,995 (total R$ 37,905). Arredonda para cima, para baixo ou trunca, e no desconto ou no total? _(CA1 · bloqueia CT-05 · Sem a regra não dá para julgar o total exibido nem o valor cobrado)_
- **D4.** Quando o segundo cupom é recusado (expirado, inexistente ou de primeira assinatura para quem já assinou), o primeiro cupom continua aplicado ou é removido? O CA3 diz que o valor não muda e o CA4 diz que o segundo substitui o primeiro. _(CA3, CA4 · bloqueia CT-16 · Define se o total fica R$ 359,10 (NEXI10 mantido) ou R$ 399,00 (NEXI10 removido))_
- **D5.** Para o CA6, quem conta como "já assinou"? Quem só fez teste grátis sem cobrança paga pode usar BEMVINDO50? A checagem é por conta/e-mail, CPF ou cartão, e acontece antes ou depois do login do visitante? _(CA6 · bloqueia CT-21 · Define o resultado do caso de teste grátis e se um ex-assinante pode burlar a regra com outro e-mail)_

**Outras dúvidas** (o requisito não diz; nenhum caso inventa a resposta):

- **D6.** Quais mensagens aparecem para código inexistente, para cupom de primeira assinatura recusado e para código vazio ou com espaços antes/depois (" NEXI10 ")? Os espaços são removidos? _(CA1, CA2, CA6 · CT-07 e CT-19 conferem só o total, não a mensagem; espaços não foram testados por falta de regra)_
- **D7.** O "para pagar menos na primeira cobrança" significa que o desconto vale só na primeira cobrança e a renovação volta ao preço cheio (R$ 39,90 / R$ 399,00)? O checkout deve informar isso? _(CA1 · Nenhum CA define o valor das cobranças seguintes; sem a regra a renovação não foi testada)_
- **D8.** Se o gateway de pagamento recusar o cartão ou estiver fora do ar ao finalizar com cupom, o cupom continua aplicado ao tentar de novo? Um cupom de primeira assinatura fica "gasto" numa cobrança que falhou? _(CA1, CA6 · Dependência externa sem comportamento definido; nenhum caso cobre a falha do gateway)_

**Suposições** (usadas nos casos; se estiverem erradas, os casos indicados mudam):

- O desconto aparece no resumo do checkout (linha de desconto e total atualizado) antes de finalizar o pagamento _(CT-01, CT-02, CT-03, CT-04, CT-08, CT-09, CT-13, CT-14, CT-15, CT-17, CT-20)_
- Um usuário cancelado (sem assinatura ativa) consegue abrir o checkout e assinar de novo _(CT-19, CT-20)_
- O relógio do ambiente de homologação pode ser ajustado para testar a validade dos cupons _(CT-12, CT-13)_

## Critérios e cobertura

| Critério | Descrição | Casos | Dúvidas |
|---|---|---|---|
| CA1 | Cupom válido aplica desconto percentual (entre 5% e 50%) sobre o valor do plano escolhido | CT-01, CT-02, CT-03, CT-04, CT-05, CT-06, CT-07 | D3, D6, D7, D8 |
| CA2 | O código do cupom não diferencia maiúsculas de minúsculas | CT-08, CT-09, CT-10 | D6 |
| CA3 | Cupom fora da validade mostra a mensagem "Este cupom expirou" e o valor não muda | CT-10, CT-11, CT-12, CT-13, CT-16 | D2, D4 |
| CA4 | Só um cupom por pedido; aplicar um segundo cupom substitui o primeiro | CT-14, CT-15, CT-16 | D4 |
| CA5 | O valor final nunca fica abaixo de R$ 1,00 | CT-17, CT-18 | D1 |
| CA6 | Cupons do tipo "primeira assinatura" só valem para quem nunca assinou o Nexi Play | CT-04, CT-19, CT-20, CT-21 | D5, D6, D8 |

## Casos

### CT-01 · NEXI10 no plano Mensal reduz o total para R$ 35,91

**Critérios:** CA1 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

> Depende de Suposição: O desconto aparece no resumo do checkout (linha de desconto e total atualizado) antes de finalizar o pagamento

**Pré-condições:**
- Visitante qa.cupom01@nexi.test, nunca assinou
- Checkout aberto com o plano Mensal (R$ 39,90)

**Dados:**
- `cupom`: NEXI10 (10%, validade 31/12/2026)
- `plano`: Mensal R$ 39,90
- `data do teste`: data atual (14/10/2026)

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Desconto de R$ 3,99 aparece no resumo e o total exibido muda de R$ 39,90 para R$ 35,91

### CT-02 · NEXI10 no plano Anual reduz o total para R$ 359,10

**Critérios:** CA1 · **Tipo:** positivo · **Técnica:** partição de equivalência · **Prioridade:** Média

> Depende de Suposição: O desconto aparece no resumo do checkout (linha de desconto e total atualizado) antes de finalizar o pagamento

**Pré-condições:**
- Visitante qa.cupom02@nexi.test, nunca assinou
- Checkout aberto com o plano Anual (R$ 399,00)

**Dados:**
- `cupom`: NEXI10 (10%, validade 31/12/2026)
- `plano`: Anual R$ 399,00

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Desconto de R$ 39,90 aparece no resumo e o total exibido muda de R$ 399,00 para R$ 359,10

### CT-03 · Cupom de 5% (limite mínimo) no Anual reduz o total para R$ 379,05

**Critérios:** CA1 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de Suposição: O desconto aparece no resumo do checkout (linha de desconto e total atualizado) antes de finalizar o pagamento

**Pré-condições:**
- Visitante qa.cupom03@nexi.test, nunca assinou
- Checkout aberto com o plano Anual (R$ 399,00)

**Dados:**
- `cupom`: MINIMO5 (5%, validade 31/12/2026)
- `plano`: Anual R$ 399,00

**Passos:**
1. Informar MINIMO5 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Desconto de R$ 19,95 aparece no resumo e o total exibido muda de R$ 399,00 para R$ 379,05

### CT-04 · Cupom de 50% (limite máximo) para quem nunca assinou reduz o Mensal para R$ 19,95

**Critérios:** CA1, CA6 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

> Depende de Suposição: O desconto aparece no resumo do checkout (linha de desconto e total atualizado) antes de finalizar o pagamento

**Pré-condições:**
- Visitante qa.cupom04@nexi.test, conta nova, nunca assinou nem fez teste grátis
- Checkout aberto com o plano Mensal (R$ 39,90)

**Dados:**
- `cupom`: BEMVINDO50 (50%, primeira assinatura, validade 31/12/2026)
- `plano`: Mensal R$ 39,90

**Passos:**
1. Informar BEMVINDO50 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Desconto de R$ 19,95 aparece no resumo e o total exibido muda de R$ 39,90 para R$ 19,95

### CT-05 · Desconto com meio centavo (5% do Mensal = R$ 1,995) expõe a regra de arredondamento (D3)

**Critérios:** CA1 · **Tipo:** borda · **Técnica:** suposição de erro · **Prioridade:** Média

> Depende de D3 (bloqueia)

**Pré-condições:**
- Visitante qa.cupom05@nexi.test, nunca assinou
- Checkout aberto com o plano Mensal (R$ 39,90)
- Bloqueado até a resposta da D3

**Dados:**
- `cupom`: MINIMO5 (5%, validade 31/12/2026)
- `plano`: Mensal R$ 39,90
- `conta sem arredondar`: 39,90 - 1,995 = 37,905

**Passos:**
1. Informar MINIMO5 no campo de cupom
2. Clicar em Aplicar
3. Finalizar a assinatura com o cartão de teste final 4242
4. Conferir o valor da primeira cobrança registrada no gateway

**Resultado esperado:** Total exibido tem 2 casas decimais, segue a regra de arredondamento respondida na D3, e o valor cobrado no gateway é igual ao total exibido no checkout

### CT-06 · Primeira cobrança registrada no gateway sai com o desconto do cupom (R$ 35,91)

**Critérios:** CA1 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

**Pré-condições:**
- Visitante qa.cupom06@nexi.test, nunca assinou
- Checkout aberto com o plano Mensal (R$ 39,90)

**Dados:**
- `cupom`: NEXI10 (10%, validade 31/12/2026)
- `plano`: Mensal R$ 39,90
- `cartão`: cartão de teste final 4242

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar
3. Informar o cartão de teste final 4242
4. Clicar em Finalizar assinatura
5. Consultar a cobrança no painel do gateway de homologação

**Resultado esperado:** A primeira cobrança de qa.cupom06@nexi.test registrada no gateway é de R$ 35,91

### CT-07 · Código inexistente não aplica desconto e o total continua R$ 39,90

**Critérios:** CA1 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Visitante qa.cupom07@nexi.test, nunca assinou
- Checkout aberto com o plano Mensal (R$ 39,90)
- Mensagem exibida depende da D6

**Dados:**
- `cupom`: NEXI99 (não cadastrado)
- `plano`: Mensal R$ 39,90

**Passos:**
1. Informar NEXI99 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Nenhuma linha de desconto aparece no resumo e o total continua R$ 39,90

### CT-08 · Código em minúsculas (nexi10) aplica o mesmo desconto de NEXI10

**Critérios:** CA2 · **Tipo:** positivo · **Técnica:** partição de equivalência · **Prioridade:** Média

> Depende de Suposição: O desconto aparece no resumo do checkout (linha de desconto e total atualizado) antes de finalizar o pagamento

**Pré-condições:**
- Visitante qa.cupom08@nexi.test, nunca assinou
- Checkout aberto com o plano Mensal (R$ 39,90)

**Dados:**
- `cupom digitado`: nexi10
- `plano`: Mensal R$ 39,90

**Passos:**
1. Informar nexi10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Desconto de R$ 3,99 aparece no resumo e o total exibido muda de R$ 39,90 para R$ 35,91

### CT-09 · Código misto (NeXi10) aplica o mesmo desconto de NEXI10

**Critérios:** CA2 · **Tipo:** borda · **Técnica:** suposição de erro · **Prioridade:** Baixa

> Depende de Suposição: O desconto aparece no resumo do checkout (linha de desconto e total atualizado) antes de finalizar o pagamento

**Pré-condições:**
- Visitante qa.cupom09@nexi.test, nunca assinou
- Checkout aberto com o plano Anual (R$ 399,00)

**Dados:**
- `cupom digitado`: NeXi10
- `plano`: Anual R$ 399,00

**Passos:**
1. Informar NeXi10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Desconto de R$ 39,90 aparece no resumo e o total exibido muda de R$ 399,00 para R$ 359,10

### CT-10 · Cupom expirado em minúsculas (verao15) também mostra "Este cupom expirou"

**Critérios:** CA2, CA3 · **Tipo:** negativo · **Técnica:** tabela de decisão · **Prioridade:** Média

**Pré-condições:**
- Visitante qa.cupom10@nexi.test, nunca assinou
- Checkout aberto com o plano Mensal (R$ 39,90)

**Dados:**
- `cupom digitado`: verao15 (VERAO15, 15%, validade 31/03/2026)
- `plano`: Mensal R$ 39,90

**Passos:**
1. Informar verao15 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Aparece a mensagem "Este cupom expirou" e o total continua R$ 39,90, sem linha de desconto

### CT-11 · Cupom expirado (VERAO15) mostra "Este cupom expirou" e o total não muda

**Critérios:** CA3 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Visitante qa.cupom11@nexi.test, nunca assinou
- Checkout aberto com o plano Mensal (R$ 39,90)

**Dados:**
- `cupom`: VERAO15 (15%, validade 31/03/2026)
- `plano`: Mensal R$ 39,90

**Passos:**
1. Informar VERAO15 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Aparece a mensagem "Este cupom expirou" e o total continua R$ 39,90, sem linha de desconto

### CT-12 · NEXI10 no dia seguinte ao fim da validade (01/01/2027) mostra "Este cupom expirou"

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de Suposição: O relógio do ambiente de homologação pode ser ajustado para testar a validade dos cupons

**Pré-condições:**
- Relógio do ambiente de homologação ajustado para 01/01/2027 00:01
- Visitante qa.cupom12@nexi.test, nunca assinou
- Checkout aberto com o plano Mensal (R$ 39,90)

**Dados:**
- `cupom`: NEXI10 (10%, validade 31/12/2026)
- `plano`: Mensal R$ 39,90
- `data do teste`: 01/01/2027 00:01

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Aparece a mensagem "Este cupom expirou" e o total continua R$ 39,90, sem linha de desconto

### CT-13 · NEXI10 no último dia da validade (31/12/2026 23:59) é aplicado sem mensagem de expirado

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D2 (bloqueia)

> Depende de Suposição: O desconto aparece no resumo do checkout (linha de desconto e total atualizado) antes de finalizar o pagamento

> Depende de Suposição: O relógio do ambiente de homologação pode ser ajustado para testar a validade dos cupons

**Pré-condições:**
- Bloqueado até a resposta da D2
- Relógio do ambiente de homologação ajustado para 31/12/2026 23:59
- Visitante qa.cupom13@nexi.test, nunca assinou
- Checkout aberto com o plano Mensal (R$ 39,90)

**Dados:**
- `cupom`: NEXI10 (10%, validade 31/12/2026)
- `plano`: Mensal R$ 39,90
- `data do teste`: 31/12/2026 23:59

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** A mensagem "Este cupom expirou" não aparece e o total exibido muda de R$ 39,90 para R$ 35,91

### CT-14 · Segundo cupom substitui o primeiro: NEXI10 depois MINIMO5 deixa o Anual em R$ 379,05

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Alta

> Depende de Suposição: O desconto aparece no resumo do checkout (linha de desconto e total atualizado) antes de finalizar o pagamento

**Pré-condições:**
- Visitante qa.cupom14@nexi.test, nunca assinou
- Checkout aberto com o plano Anual (R$ 399,00)

**Dados:**
- `primeiro cupom`: NEXI10 (10%)
- `segundo cupom`: MINIMO5 (5%)
- `plano`: Anual R$ 399,00

**Passos:**
1. Informar NEXI10 e clicar em Aplicar
2. Conferir que o total ficou R$ 359,10
3. Informar MINIMO5 e clicar em Aplicar

**Resultado esperado:** O resumo mostra só o cupom MINIMO5, com desconto de R$ 19,95, e o total exibido é R$ 379,05 (não há desconto acumulado com NEXI10)

### CT-15 · Aplicar o mesmo cupom duas vezes não dobra o desconto

**Critérios:** CA4 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Média

> Depende de Suposição: O desconto aparece no resumo do checkout (linha de desconto e total atualizado) antes de finalizar o pagamento

**Pré-condições:**
- Visitante qa.cupom15@nexi.test, nunca assinou
- Checkout aberto com o plano Anual (R$ 399,00)

**Dados:**
- `cupom`: NEXI10 (10%), aplicado duas vezes
- `plano`: Anual R$ 399,00

**Passos:**
1. Informar NEXI10 e clicar em Aplicar
2. Informar NEXI10 de novo e clicar em Aplicar

**Resultado esperado:** O resumo mostra uma única linha de cupom NEXI10, com desconto de R$ 39,90, e o total continua R$ 359,10 (não R$ 323,19)

### CT-16 · Cupom expirado aplicado como segundo cupom não dá o desconto dele

**Critérios:** CA3, CA4 · **Tipo:** negativo · **Técnica:** tabela de decisão · **Prioridade:** Média

> Depende de D4 (bloqueia)

**Pré-condições:**
- Bloqueado até a resposta da D4 (NEXI10 continua ou sai)
- Visitante qa.cupom16@nexi.test, nunca assinou
- Checkout aberto com o plano Anual (R$ 399,00)

**Dados:**
- `primeiro cupom`: NEXI10 (10%, válido)
- `segundo cupom`: VERAO15 (15%, validade 31/03/2026)
- `plano`: Anual R$ 399,00

**Passos:**
1. Informar NEXI10 e clicar em Aplicar
2. Informar VERAO15 e clicar em Aplicar

**Resultado esperado:** Aparece a mensagem "Este cupom expirou", o total não fica em R$ 339,15 (15% de VERAO15) e o total final corresponde à resposta da D4

### CT-17 · Desconto que leva o total a exatamente R$ 1,00 mantém R$ 1,00

**Critérios:** CA5 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D1 (bloqueia)

> Depende de Suposição: O desconto aparece no resumo do checkout (linha de desconto e total atualizado) antes de finalizar o pagamento

**Pré-condições:**
- Bloqueado até a resposta da D1 (dado de teste)
- Plano de teste de R$ 2,00 cadastrado em homologação
- Visitante qa.cupom17@nexi.test, nunca assinou

**Dados:**
- `plano`: plano de teste R$ 2,00
- `cupom`: BEMVINDO50 (50%) → 2,00 - 1,00 = R$ 1,00

**Passos:**
1. Abrir o checkout com o plano de teste de R$ 2,00
2. Informar BEMVINDO50 e clicar em Aplicar

**Resultado esperado:** Desconto de R$ 1,00 aparece no resumo e o total exibido é R$ 1,00

### CT-18 · Desconto que levaria o total a R$ 0,99 é limitado e o total fica R$ 1,00

**Critérios:** CA5 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

> Depende de D1 (bloqueia)

**Pré-condições:**
- Bloqueado até a resposta da D1 (dado de teste)
- Plano de teste de R$ 1,98 cadastrado em homologação
- Visitante qa.cupom18@nexi.test, nunca assinou

**Dados:**
- `plano`: plano de teste R$ 1,98
- `cupom`: BEMVINDO50 (50%) → 1,98 - 0,99 = R$ 0,99 sem o piso

**Passos:**
1. Abrir o checkout com o plano de teste de R$ 1,98
2. Informar BEMVINDO50 e clicar em Aplicar

**Resultado esperado:** Total exibido é R$ 1,00, e não R$ 0,99

### CT-19 · Cupom de primeira assinatura não vale para quem já assinou e cancelou

**Critérios:** CA6 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Alta

> Depende de Suposição: Um usuário cancelado (sem assinatura ativa) consegue abrir o checkout e assinar de novo

**Pré-condições:**
- Usuário qa.excliente01@nexi.test assinou o Mensal e cancelou em março de 2026, sem assinatura ativa
- Logado e com o checkout aberto no plano Mensal (R$ 39,90)
- Mensagem exibida depende da D6

**Dados:**
- `cupom`: BEMVINDO50 (50%, primeira assinatura)
- `plano`: Mensal R$ 39,90
- `usuário`: ex-assinante (Mensal cancelado em março de 2026)

**Passos:**
1. Informar BEMVINDO50 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Nenhuma linha de desconto aparece no resumo e o total continua R$ 39,90

### CT-20 · Cupom comum (NEXI10) continua valendo para quem já assinou

**Critérios:** CA6 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Média

> Depende de Suposição: O desconto aparece no resumo do checkout (linha de desconto e total atualizado) antes de finalizar o pagamento

> Depende de Suposição: Um usuário cancelado (sem assinatura ativa) consegue abrir o checkout e assinar de novo

**Pré-condições:**
- Usuário qa.excliente02@nexi.test assinou o Mensal e cancelou em março de 2026, sem assinatura ativa
- Logado e com o checkout aberto no plano Mensal (R$ 39,90)

**Dados:**
- `cupom`: NEXI10 (10%, não é de primeira assinatura)
- `plano`: Mensal R$ 39,90

**Passos:**
1. Informar NEXI10 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** A restrição de primeira assinatura não é aplicada: desconto de R$ 3,99 aparece e o total muda de R$ 39,90 para R$ 35,91

### CT-21 · Cupom de primeira assinatura para quem só fez teste grátis segue a resposta da D5

**Critérios:** CA6 · **Tipo:** borda · **Técnica:** partição de equivalência · **Prioridade:** Média

> Depende de D5 (bloqueia)

**Pré-condições:**
- Bloqueado até a resposta da D5
- Usuário qa.trial01@nexi.test fez só o teste grátis, nunca teve cobrança paga
- Logado e com o checkout aberto no plano Mensal (R$ 39,90)

**Dados:**
- `cupom`: BEMVINDO50 (50%, primeira assinatura)
- `plano`: Mensal R$ 39,90
- `usuário`: só fez teste grátis, sem cobrança paga

**Passos:**
1. Informar BEMVINDO50 no campo de cupom
2. Clicar em Aplicar

**Resultado esperado:** Total exibido corresponde à resposta da D5: R$ 19,95 se teste grátis conta como nunca assinou; R$ 39,90 sem linha de desconto se não conta

## Fora do escopo

- Cadastro e administração de cupons (inclusive impedir cupom com menos de 5% ou mais de 50%, que é configuração e não entrada do visitante)
- Valor das renovações e cobranças seguintes (ver D7)
- Remover o cupom manualmente sem aplicar outro
- Segurança, acessibilidade e desempenho do checkout
