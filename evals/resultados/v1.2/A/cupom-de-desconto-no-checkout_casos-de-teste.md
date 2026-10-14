# Casos de teste: Cupom de desconto no checkout

**Origem:** HIST-412 (arquivo A-cupom-checkout.md) · **Gerado em:** 14/10/2026

**19 casos:** 4 positivos, 5 negativos, 10 de borda · **Prioridade:** 7 Alta, 12 Média, 0 Baixa

## Pontos a confirmar com o PO

**Dúvidas que bloqueiam a execução** (responder primeiro):

- **D1.** Nenhum plano ou cupom de homologação deixa o total abaixo de R$ 1,00 (o maior desconto é 50% de R$ 39,90 = R$ 19,95). Dá para cadastrar um plano ou cupom de teste para o CA5 (ex.: plano R$ 2,00 e R$ 1,98 com cupom de 50%)? E em qual situação real o piso entra em jogo? _(CA5 · bloqueia CT-14, CT-15 · Sem esses dados o CA5 não é testável)_
- **D2.** Como arredondar centavos do desconto (ex.: 5% de R$ 39,90 = R$ 1,995)? Arredonda para cima, para baixo ou meio-para-cima, e no desconto ou no total? _(CA1 · bloqueia CT-05 · Define o valor esperado de CT-05 (R$ 37,90 ou R$ 37,91); o mesmo vale para VERAO15 no Mensal)_
- **D3.** A validade "31/12/2026" inclui o dia 31 inteiro (até 23:59)? Em qual fuso horário? _(CA3 · bloqueia CT-09 · Define se CT-09 deve aceitar o cupom)_
- **D4.** Com um cupom já aplicado, o que acontece se o segundo cupom for recusado (expirado, inexistente ou de primeira assinatura para quem já assinou)? O primeiro continua valendo ou é removido? _(CA4, CA3 · bloqueia CT-13 · Define o total esperado de CT-13; CA3 diz que 'o valor não muda', o que sugere manter o primeiro)_
- **D5.** Quem conta como "já assinou" para o CA6: quem só fez teste grátis conta? A checagem é por e-mail, CPF ou cartão (a mesma pessoa com outro e-mail consegue usar o cupom)? _(CA6 · bloqueia CT-17 · Define o resultado de CT-17 e pode gerar casos novos de identificação)_

**Outras dúvidas** (o requisito não diz; nenhum caso inventa a resposta):

- **D6.** Quais mensagens aparecem para código inexistente e para cupom de primeira assinatura recusado? _(CA1, CA6 · CT-16 e CT-18 conferem só o total, não a mensagem)_
- **D7.** O código aceita espaços antes/depois (" NEXI10 ")? O que acontece ao clicar em Aplicar com o campo vazio? _(CA2 · Sem resposta, não há casos para espaços e campo vazio)_
- **D8.** Trocar de plano (Mensal ↔ Anual) com o cupom já aplicado recalcula o desconto sobre o novo plano ou remove o cupom? _(CA1 · Sem resposta, não há caso de troca de plano com cupom aplicado)_

**Suposições** (usadas nos casos; se estiverem erradas, os casos indicados mudam):

- O total exibido no checkout é o valor da primeira cobrança (o valor cobrado no cartão é o mesmo da tela) _(CT-01, CT-02, CT-03, CT-04, CT-06, CT-11, CT-15)_
- Aplicar o mesmo cupom de novo conta como um cupom só, pela regra 'só um cupom por pedido' _(CT-12)_
- O ambiente de homologação permite ajustar o relógio para testar validade e renovação _(CT-09, CT-10, CT-19)_

## Critérios e cobertura

| Critério | Descrição | Casos | Dúvidas |
|---|---|---|---|
| CA1 | Cupom válido aplica desconto percentual sobre o valor do plano escolhido; cupons têm desconto entre 5% e 50% | CT-01, CT-02, CT-03, CT-04, CT-05, CT-18 | D2, D6, D8 |
| CA2 | O código do cupom não diferencia maiúsculas de minúsculas | CT-06, CT-07 | D7 |
| CA3 | Cupom fora da validade mostra a mensagem "Este cupom expirou" e o valor não muda | CT-07, CT-08, CT-09, CT-10, CT-13 | D3, D4 |
| CA4 | Só um cupom por pedido; aplicar um segundo cupom substitui o primeiro | CT-11, CT-12, CT-13 | D4 |
| CA5 | O valor final nunca fica abaixo de R$ 1,00 | CT-14, CT-15 | D1 |
| CA6 | Cupons do tipo "primeira assinatura" só valem para quem nunca assinou o Nexi Play | CT-04, CT-16, CT-17 | D5, D6 |
| CA7 _(derivado)_ | O desconto vale só na primeira cobrança ("para pagar menos na primeira cobrança") | CT-19 | — |

## Casos

### CT-01 · NEXI10 no plano Mensal reduz o total para R$ 35,91

**Critérios:** CA1 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

> Depende de Suposição: O total exibido no checkout é o valor da primeira cobrança (o valor cobrado no cartão é o mesmo da tela)

**Pré-condições:**
- Visitante no checkout, identificado com visitante.ct01@nexi.test (nunca assinou)
- Data do ambiente antes de 31/12/2026

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom`: NEXI10 (10%, validade 31/12/2026)
- `data do teste`: 14/10/2026

**Passos:**
1. Acessar o checkout do Nexi Play
2. Escolher o plano Mensal
3. Informar NEXI10 no campo de cupom
4. Clicar em Aplicar

**Resultado esperado:** Desconto de R$ 3,99 exibido e total muda de R$ 39,90 para R$ 35,91

### CT-02 · NEXI10 no plano Anual reduz o total para R$ 359,10

**Critérios:** CA1 · **Tipo:** positivo · **Técnica:** partição de equivalência · **Prioridade:** Média

> Depende de Suposição: O total exibido no checkout é o valor da primeira cobrança (o valor cobrado no cartão é o mesmo da tela)

**Pré-condições:**
- Visitante no checkout, identificado com visitante.ct02@nexi.test (nunca assinou)
- Data do ambiente antes de 31/12/2026

**Dados:**
- `plano`: Anual R$ 399,00
- `cupom`: NEXI10 (10%, validade 31/12/2026)

**Passos:**
1. Acessar o checkout do Nexi Play
2. Escolher o plano Anual
3. Informar NEXI10 no campo de cupom
4. Clicar em Aplicar

**Resultado esperado:** Desconto de R$ 39,90 exibido e total muda de R$ 399,00 para R$ 359,10

### CT-03 · Cupom de 5% (mínimo da faixa) no Anual reduz o total para R$ 379,05

**Critérios:** CA1 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de Suposição: O total exibido no checkout é o valor da primeira cobrança (o valor cobrado no cartão é o mesmo da tela)

**Pré-condições:**
- Visitante no checkout, identificado com visitante.ct03@nexi.test (nunca assinou)
- Data do ambiente antes de 31/12/2026

**Dados:**
- `plano`: Anual R$ 399,00
- `cupom`: MINIMO5 (5%, validade 31/12/2026)

**Passos:**
1. Acessar o checkout do Nexi Play
2. Escolher o plano Anual
3. Informar MINIMO5 no campo de cupom
4. Clicar em Aplicar

**Resultado esperado:** Desconto de R$ 19,95 exibido e total muda de R$ 399,00 para R$ 379,05

### CT-04 · Cupom de 50% (máximo da faixa) de primeira assinatura vale para quem nunca assinou

**Critérios:** CA1, CA6 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

> Depende de Suposição: O total exibido no checkout é o valor da primeira cobrança (o valor cobrado no cartão é o mesmo da tela)

**Pré-condições:**
- Visitante no checkout, identificado com nunca.assinou@nexi.test, e-mail sem nenhuma assinatura nem teste grátis no histórico
- Data do ambiente antes de 31/12/2026

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom`: BEMVINDO50 (50%, primeira assinatura, validade 31/12/2026)
- `conta`: nunca.assinou@nexi.test

**Passos:**
1. Acessar o checkout do Nexi Play
2. Escolher o plano Mensal
3. Informar BEMVINDO50 no campo de cupom
4. Clicar em Aplicar

**Resultado esperado:** Desconto de R$ 19,95 exibido e total muda de R$ 39,90 para R$ 19,95

### CT-05 · MINIMO5 no Mensal expõe o arredondamento de R$ 37,905 (ver dúvida de arredondamento)

**Critérios:** CA1 · **Tipo:** borda · **Técnica:** suposição de erro · **Prioridade:** Média

> Depende de D2 (bloqueia)

**Pré-condições:**
- Visitante no checkout, identificado com visitante.ct05@nexi.test (nunca assinou)
- Data do ambiente antes de 31/12/2026

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom`: MINIMO5 (5%)
- `conta`: 39,90 x 5% = 1,995

**Passos:**
1. Acessar o checkout do Nexi Play
2. Escolher o plano Mensal
3. Informar MINIMO5 no campo de cupom
4. Clicar em Aplicar
5. Anotar o desconto e o total exibidos

**Resultado esperado:** Total exibido segue a regra de arredondamento definida pelo PO (R$ 37,90 se o desconto for arredondado para R$ 2,00; R$ 37,91 se for truncado para R$ 1,99) e é igual ao valor cobrado

### CT-06 · Código em minúsculas (nexi10) aplica o mesmo desconto do NEXI10

**Critérios:** CA2 · **Tipo:** positivo · **Técnica:** partição de equivalência · **Prioridade:** Média

> Depende de Suposição: O total exibido no checkout é o valor da primeira cobrança (o valor cobrado no cartão é o mesmo da tela)

**Pré-condições:**
- Visitante no checkout, identificado com visitante.ct06@nexi.test (nunca assinou)
- Data do ambiente antes de 31/12/2026

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom digitado`: nexi10

**Passos:**
1. Acessar o checkout do Nexi Play
2. Escolher o plano Mensal
3. Informar nexi10 no campo de cupom
4. Clicar em Aplicar

**Resultado esperado:** Desconto de R$ 3,99 exibido e total muda de R$ 39,90 para R$ 35,91

### CT-07 · Código expirado em caixa mista (VeRaO15) continua recusado como expirado

**Critérios:** CA2, CA3 · **Tipo:** negativo · **Técnica:** tabela de decisão · **Prioridade:** Média

**Pré-condições:**
- Visitante no checkout, identificado com visitante.ct07@nexi.test (nunca assinou)
- Data do ambiente 14/10/2026 (depois de 31/03/2026)

**Dados:**
- `plano`: Anual R$ 399,00
- `cupom digitado`: VeRaO15 (VERAO15, 15%, validade 31/03/2026)

**Passos:**
1. Acessar o checkout do Nexi Play
2. Escolher o plano Anual
3. Informar VeRaO15 no campo de cupom
4. Clicar em Aplicar

**Resultado esperado:** Aparece a mensagem "Este cupom expirou" e o total continua R$ 399,00

### CT-08 · Cupom VERAO15 vencido mostra "Este cupom expirou" e não altera o total

**Critérios:** CA3 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Alta

**Pré-condições:**
- Visitante no checkout, identificado com visitante.ct08@nexi.test (nunca assinou)
- Data do ambiente 14/10/2026 (depois de 31/03/2026)

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom`: VERAO15 (15%, validade 31/03/2026)

**Passos:**
1. Acessar o checkout do Nexi Play
2. Escolher o plano Mensal
3. Informar VERAO15 no campo de cupom
4. Clicar em Aplicar

**Resultado esperado:** Aparece a mensagem "Este cupom expirou" e o total continua R$ 39,90, sem linha de desconto

### CT-09 · NEXI10 no último dia da validade (31/12/2026) ainda é aplicado

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D3 (bloqueia)

> Depende de Suposição: O ambiente de homologação permite ajustar o relógio para testar validade e renovação

**Pré-condições:**
- Relógio do ambiente ajustado para 31/12/2026 12:00 (horário de Brasília)
- Visitante no checkout, identificado com visitante.ct09@nexi.test (nunca assinou)

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom`: NEXI10 (10%, validade 31/12/2026)
- `data do teste`: 31/12/2026 12:00

**Passos:**
1. Acessar o checkout do Nexi Play
2. Escolher o plano Mensal
3. Informar NEXI10 no campo de cupom
4. Clicar em Aplicar

**Resultado esperado:** Desconto de R$ 3,99 exibido e total muda de R$ 39,90 para R$ 35,91

### CT-10 · NEXI10 no dia seguinte ao fim da validade (01/01/2027) é recusado como expirado

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de Suposição: O ambiente de homologação permite ajustar o relógio para testar validade e renovação

**Pré-condições:**
- Relógio do ambiente ajustado para 01/01/2027 12:00 (horário de Brasília)
- Visitante no checkout, identificado com visitante.ct10@nexi.test (nunca assinou)

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom`: NEXI10 (10%, validade 31/12/2026)
- `data do teste`: 01/01/2027 12:00

**Passos:**
1. Acessar o checkout do Nexi Play
2. Escolher o plano Mensal
3. Informar NEXI10 no campo de cupom
4. Clicar em Aplicar

**Resultado esperado:** Aparece a mensagem "Este cupom expirou" e o total continua R$ 39,90

### CT-11 · Segundo cupom válido substitui o primeiro no total

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Alta

> Depende de Suposição: O total exibido no checkout é o valor da primeira cobrança (o valor cobrado no cartão é o mesmo da tela)

**Pré-condições:**
- Visitante no checkout, identificado com visitante.ct11@nexi.test (nunca assinou)
- Data do ambiente antes de 31/12/2026

**Dados:**
- `plano`: Anual R$ 399,00
- `1º cupom`: NEXI10 (10%)
- `2º cupom`: MINIMO5 (5%)

**Passos:**
1. Acessar o checkout do Nexi Play
2. Escolher o plano Anual
3. Aplicar NEXI10 e conferir total de R$ 359,10
4. Informar MINIMO5 no campo de cupom
5. Clicar em Aplicar

**Resultado esperado:** Só o cupom MINIMO5 aparece no pedido, desconto de R$ 19,95, e o total passa a R$ 379,05 (não R$ 339,15 dos dois somados nem R$ 341,15 dos dois em sequência)

### CT-12 · Aplicar NEXI10 duas vezes não acumula o desconto

**Critérios:** CA4 · **Tipo:** borda · **Técnica:** suposição de erro · **Prioridade:** Média

> Depende de Suposição: Aplicar o mesmo cupom de novo conta como um cupom só, pela regra 'só um cupom por pedido'

**Pré-condições:**
- Visitante no checkout, identificado com visitante.ct12@nexi.test (nunca assinou)
- Data do ambiente antes de 31/12/2026

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom`: NEXI10 (10%)

**Passos:**
1. Acessar o checkout do Nexi Play
2. Escolher o plano Mensal
3. Aplicar NEXI10
4. Informar NEXI10 de novo no campo de cupom
5. Clicar em Aplicar

**Resultado esperado:** Total continua R$ 35,91 (não R$ 32,32) e o cupom NEXI10 aparece uma única vez no pedido

### CT-13 · Cupom expirado aplicado sobre NEXI10 mostra "Este cupom expirou" (efeito no NEXI10 depende de dúvida)

**Critérios:** CA3, CA4 · **Tipo:** negativo · **Técnica:** tabela de decisão · **Prioridade:** Média

> Depende de D4 (bloqueia)

**Pré-condições:**
- Visitante no checkout, identificado com visitante.ct13@nexi.test (nunca assinou)
- Data do ambiente 14/10/2026

**Dados:**
- `plano`: Mensal R$ 39,90
- `1º cupom`: NEXI10 (10%)
- `2º cupom`: VERAO15 (expirado em 31/03/2026)

**Passos:**
1. Acessar o checkout do Nexi Play
2. Escolher o plano Mensal
3. Aplicar NEXI10 e conferir total de R$ 35,91
4. Informar VERAO15 no campo de cupom
5. Clicar em Aplicar

**Resultado esperado:** Aparece a mensagem "Este cupom expirou", o desconto de 15% não é aplicado e o total segue a regra definida pelo PO para o NEXI10 (R$ 35,91 se ele é mantido; R$ 39,90 se é removido)

### CT-14 · Desconto que leva o total a exatamente R$ 1,00 é aceito

**Critérios:** CA5 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D1 (bloqueia)

**Pré-condições:**
- Combinação de plano e cupom em homologação cuja conta dê exatamente R$ 1,00 (ex.: plano de teste R$ 2,00 com cupom de 50%); não existe com os dados atuais, ver dúvida

**Dados:**
- `plano`: a definir (ex.: R$ 2,00)
- `cupom`: a definir (ex.: 50%)

**Passos:**
1. Acessar o checkout do Nexi Play
2. Escolher o plano de teste
3. Informar o cupom de teste
4. Clicar em Aplicar

**Resultado esperado:** Total exibido é R$ 1,00

### CT-15 · Desconto que levaria o total abaixo de R$ 1,00 para em R$ 1,00

**Critérios:** CA5 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

> Depende de D1 (bloqueia)

> Depende de Suposição: O total exibido no checkout é o valor da primeira cobrança (o valor cobrado no cartão é o mesmo da tela)

**Pré-condições:**
- Combinação de plano e cupom em homologação cuja conta dê R$ 0,99 ou menos (ex.: plano de teste R$ 1,98 com cupom de 50% = R$ 0,99); não existe com os dados atuais, ver dúvida

**Dados:**
- `plano`: a definir (ex.: R$ 1,98)
- `cupom`: a definir (ex.: 50%)

**Passos:**
1. Acessar o checkout do Nexi Play
2. Escolher o plano de teste
3. Informar o cupom de teste
4. Clicar em Aplicar
5. Concluir o pagamento

**Resultado esperado:** Total exibido é R$ 1,00 (não R$ 0,99) e a cobrança registrada é de R$ 1,00

### CT-16 · BEMVINDO50 é recusado para quem já assinou e cancelou

**Critérios:** CA6 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Alta

**Pré-condições:**
- Conta ex.assinante@nexi.test com assinatura Mensal paga e cancelada em 03/2026
- Visitante no checkout identificado com ex.assinante@nexi.test
- Data do ambiente antes de 31/12/2026

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom`: BEMVINDO50 (50%, primeira assinatura)
- `conta`: ex.assinante@nexi.test (assinou e cancelou)

**Passos:**
1. Acessar o checkout do Nexi Play
2. Escolher o plano Mensal
3. Informar BEMVINDO50 no campo de cupom
4. Clicar em Aplicar

**Resultado esperado:** O desconto não é aplicado e o total continua R$ 39,90

### CT-17 · BEMVINDO50 para quem só fez teste grátis (regra depende de dúvida)

**Critérios:** CA6 · **Tipo:** borda · **Técnica:** partição de equivalência · **Prioridade:** Média

> Depende de D5 (bloqueia)

**Pré-condições:**
- Conta so.trial@nexi.test que fez teste grátis e nunca pagou nenhuma cobrança
- Visitante no checkout identificado com so.trial@nexi.test
- Data do ambiente antes de 31/12/2026

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom`: BEMVINDO50 (50%, primeira assinatura)
- `conta`: so.trial@nexi.test (só teste grátis)

**Passos:**
1. Acessar o checkout do Nexi Play
2. Escolher o plano Mensal
3. Informar BEMVINDO50 no campo de cupom
4. Clicar em Aplicar

**Resultado esperado:** Total segue a definição do PO: R$ 19,95 se teste grátis não conta como assinatura; R$ 39,90 se conta

### CT-18 · Código inexistente (NEXI99) não altera o total

**Critérios:** CA1 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Visitante no checkout, identificado com visitante.ct18@nexi.test (nunca assinou)
- Cupom NEXI99 não cadastrado em homologação

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom`: NEXI99

**Passos:**
1. Acessar o checkout do Nexi Play
2. Escolher o plano Mensal
3. Informar NEXI99 no campo de cupom
4. Clicar em Aplicar

**Resultado esperado:** O desconto não é aplicado, o total continua R$ 39,90 e não aparece a mensagem "Este cupom expirou"

### CT-19 · Segunda cobrança do Mensal com NEXI10 vem pelo valor cheio

**Critérios:** CA7 · **Tipo:** borda · **Técnica:** transição de estado · **Prioridade:** Alta

> Depende de Suposição: O ambiente de homologação permite ajustar o relógio para testar validade e renovação

**Pré-condições:**
- Assinatura Mensal contratada por visitante.ct19@nexi.test com NEXI10, primeira cobrança de R$ 35,91 paga
- Relógio do ambiente avançado até a data da segunda cobrança (1 mês depois)

**Dados:**
- `plano`: Mensal R$ 39,90
- `cupom`: NEXI10 (10%)

**Passos:**
1. Disparar o processamento de renovação da assinatura
2. Consultar as cobranças da assinatura

**Resultado esperado:** A segunda cobrança registrada é de R$ 39,90 e a primeira continua R$ 35,91

## Fora do escopo

- Cadastro e administração de cupons (inclusive impedir cupons com 4% ou 51%)
- Cupons de valor fixo (a história só fala de percentual)
- Meios de pagamento e falhas no pagamento
- Cupons aplicados em renovações ou upgrade de plano
