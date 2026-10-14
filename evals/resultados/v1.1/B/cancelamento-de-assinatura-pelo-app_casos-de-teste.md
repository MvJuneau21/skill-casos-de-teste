# Casos de teste: Cancelamento de assinatura pelo app

**Origem:** Mensagem do PO no Slack (B-cancelamento-slack.txt), colada pelo usuário em 14/10/2026 · **Gerado em:** 14/10/2026

**16 casos:** 8 positivos, 3 negativos, 5 de borda · **Prioridade:** 8 Alta, 8 Média, 0 Baixa

## Pontos a confirmar com o PO

**Dúvidas que bloqueiam a execução** (responder primeiro):

- **D1.** D1 - Contradição no plano anual depois de 7 dias: a regra geral diz que o assinante continua com acesso até o fim do período pago, mas o anual recebe reembolso proporcional dos meses não usados. Se os meses são reembolsados, o acesso acaba na hora do cancelamento, no fim do mês em curso ou continua até o fim do ano? _(CA4, CA5 · bloqueia CT-08, CT-09 · Sem a resposta não dá para dizer se o reembolso proporcional vem junto com o acesso, nem testar o acesso do anual cancelado)_
- **D2.** D2 - Como calcular o reembolso proporcional do anual: (a) base é R$ 399,00 / 12 = R$ 33,25 por mês ou os meses usados são cobrados pelo preço do Mensal (R$ 39,90)? (b) o mês em curso conta como usado? Ex.: 3 meses de uso devolve R$ 299,25 (base anual) ou R$ 279,30 (399,00 - 3 × 39,90) _(CA5 · bloqueia CT-08, CT-09 · Muda o valor esperado do reembolso)_
- **D3.** D3 - Como contar os 7 dias: o dia da contratação é o dia 0 ou o dia 1? Conta em dias corridos ou em 7 × 24 h a partir do horário da contratação? Qual fuso? _(CA3 · bloqueia CT-03, CT-04, CT-09 · Muda em qual dia está o limite entre reembolso integral e não integral)_

**Outras dúvidas** (o requisito não diz; nenhum caso inventa a resposta):

- **D4.** D4 - Os 7 dias valem só para a primeira contratação ou também para cada renovação do Mensal (ex.: Mensal renovado há 3 dias tem reembolso integral da renovação)? _(CA3 · Se valer para renovação, falta um caso de reembolso de R$ 39,90 na renovação)_
- **D5.** D5 - No cancelamento em até 7 dias com reembolso integral, o acesso termina na hora ou continua até o fim do período? _(CA3, CA4 · CT-01 a CT-03 conferem só o reembolso, não o acesso)_
- **D6.** D6 - Como e quando o reembolso chega ao assinante (estorno no mesmo cartão, prazo) e onde ele aparece no app? _(CA3, CA5 · Os casos conferem o reembolso no gateway de homologação, não na fatura do cartão)_
- **D7.** D7 - Textos: nomes dos botões do diálogo "Tem certeza?" e o que o e-mail de confirmação precisa trazer (data de fim do acesso, valor do reembolso) _(CA2, CA6 · CT-11 a CT-14 conferem só a presença do diálogo e do e-mail, não o conteúdo)_
- **D8.** D8 - Assinatura já cancelada, ainda no período pago: a opção Cancelar continua aparecendo? O que acontece se o usuário tentar de novo? _(CA1 · Sem caso para cancelamento repetido)_

**Suposições** (usadas nos casos; se estiverem erradas, os casos indicados mudam):

- Plano Mensal cancelado depois de 7 dias não tem reembolso (o texto só fala em reembolso no integral e no anual) _(CT-04, CT-05, CT-06, CT-16)_
- Na contagem dos 7 dias, o dia da contratação é o dia 0 e contam dias corridos _(CT-03, CT-04, CT-09)_
- No anual, o mês em curso conta como usado no cálculo proporcional _(CT-09)_
- O ambiente de homologação permite simular a data de contratação e avançar o relógio, e tem painel do gateway para consultar cobranças e reembolsos _(CT-01, CT-02, CT-03, CT-04, CT-05, CT-06, CT-07, CT-08, CT-09, CT-10, CT-15, CT-16)_

## Critérios e cobertura

| Critério | Descrição | Casos | Dúvidas |
|---|---|---|---|
| CA1 _(derivado)_ | Assinante cancela pelo app a qualquer momento, em Conta > Assinatura > Cancelar | CT-01, CT-16 | D8 |
| CA2 _(derivado)_ | Antes de cancelar, o app pede confirmação ("Tem certeza?") | CT-11, CT-12 | D7 |
| CA3 _(derivado)_ | Cancelamento em até 7 dias da contratação tem reembolso integral (CDC) | CT-01, CT-02, CT-03, CT-04, CT-09, CT-15 | D3, D4, D5, D6 |
| CA4 _(derivado)_ | Cancelamento depois de 7 dias: acesso continua até o fim do período pago e não há nova cobrança | CT-05, CT-06, CT-07, CT-10, CT-16 | D1, D5 |
| CA5 _(derivado)_ | Plano anual cancelado depois de 7 dias: reembolso proporcional aos meses não usados | CT-08, CT-09 | D1, D2, D6 |
| CA6 _(derivado)_ | Um e-mail confirmando o cancelamento é enviado | CT-13, CT-14 | D7 |

## Casos

### CT-01 · Mensal cancelado no 3º dia recebe reembolso integral de R$ 39,90

**Critérios:** CA1, CA3 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

> Depende de Suposição: O ambiente de homologação permite simular a data de contratação e avançar o relógio, e tem painel do gateway para consultar cobranças e reembolsos

**Pré-condições:**
- Usuário qa.cancel01@nexi.test logado no app
- Plano Mensal R$ 39,90 contratado há 3 dias (simular data de contratação no ambiente)

**Dados:**
- `usuário`: qa.cancel01@nexi.test
- `plano`: Mensal R$ 39,90
- `dias desde a contratação`: 3

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Consultar o reembolso da assinatura no painel do gateway de pagamento (homologação)

**Resultado esperado:** Conta > Assinatura mostra a assinatura como cancelada; o gateway registra um reembolso de R$ 39,90 para a cobrança da contratação

### CT-02 · Anual cancelado no 3º dia recebe reembolso integral de R$ 399,00

**Critérios:** CA3 · **Tipo:** positivo · **Técnica:** tabela de decisão · **Prioridade:** Alta

> Depende de Suposição: O ambiente de homologação permite simular a data de contratação e avançar o relógio, e tem painel do gateway para consultar cobranças e reembolsos

**Pré-condições:**
- Usuário qa.cancel02@nexi.test logado no app
- Plano Anual R$ 399,00 contratado há 3 dias (simular data de contratação no ambiente)

**Dados:**
- `usuário`: qa.cancel02@nexi.test
- `plano`: Anual R$ 399,00
- `dias desde a contratação`: 3

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Consultar o reembolso no painel do gateway de pagamento (homologação)

**Resultado esperado:** O gateway registra um reembolso de R$ 399,00 (valor integral), e não um valor proporcional

### CT-03 · Mensal cancelado no 7º dia ainda recebe reembolso integral

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

> Depende de D3 (bloqueia)

> Depende de Suposição: Na contagem dos 7 dias, o dia da contratação é o dia 0 e contam dias corridos

> Depende de Suposição: O ambiente de homologação permite simular a data de contratação e avançar o relógio, e tem painel do gateway para consultar cobranças e reembolsos

**Pré-condições:**
- Usuário qa.cancel03@nexi.test logado no app
- Plano Mensal R$ 39,90 contratado há exatamente 7 dias corridos, contando o dia da contratação como dia 0 (simular data no ambiente; ver dúvida sobre a contagem)

**Dados:**
- `usuário`: qa.cancel03@nexi.test
- `plano`: Mensal R$ 39,90
- `dias desde a contratação`: 7

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Consultar o reembolso no painel do gateway de pagamento (homologação)

**Resultado esperado:** O gateway registra um reembolso de R$ 39,90

### CT-04 · Mensal cancelado no 8º dia não recebe reembolso integral

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

> Depende de D3 (bloqueia)

> Depende de Suposição: Plano Mensal cancelado depois de 7 dias não tem reembolso (o texto só fala em reembolso no integral e no anual)

> Depende de Suposição: Na contagem dos 7 dias, o dia da contratação é o dia 0 e contam dias corridos

> Depende de Suposição: O ambiente de homologação permite simular a data de contratação e avançar o relógio, e tem painel do gateway para consultar cobranças e reembolsos

**Pré-condições:**
- Usuário qa.cancel04@nexi.test logado no app
- Plano Mensal R$ 39,90 contratado há 8 dias corridos, contando o dia da contratação como dia 0 (simular data no ambiente; ver dúvida sobre a contagem)

**Dados:**
- `usuário`: qa.cancel04@nexi.test
- `plano`: Mensal R$ 39,90
- `dias desde a contratação`: 8

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Consultar o reembolso no painel do gateway de pagamento (homologação)

**Resultado esperado:** O gateway não registra reembolso de R$ 39,90 para a cobrança da contratação

### CT-05 · Mensal cancelado no 15º dia mantém acesso até o último dia do período pago

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Média

> Depende de Suposição: Plano Mensal cancelado depois de 7 dias não tem reembolso (o texto só fala em reembolso no integral e no anual)

> Depende de Suposição: O ambiente de homologação permite simular a data de contratação e avançar o relógio, e tem painel do gateway para consultar cobranças e reembolsos

**Pré-condições:**
- Usuário qa.cancel05@nexi.test logado no app
- Plano Mensal R$ 39,90 contratado há 15 dias, período pago termina daqui a 15 dias (simular data no ambiente)

**Dados:**
- `usuário`: qa.cancel05@nexi.test
- `plano`: Mensal R$ 39,90
- `dias desde a contratação`: 15

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar e confirmar em "Tem certeza?"
3. Avançar o relógio do ambiente até o último dia do período pago
4. Abrir um título do catálogo no app

**Resultado esperado:** No último dia do período pago o título abre e é reproduzido no app

### CT-06 · Mensal cancelado no 15º dia não é cobrado na data de renovação

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

> Depende de Suposição: Plano Mensal cancelado depois de 7 dias não tem reembolso (o texto só fala em reembolso no integral e no anual)

> Depende de Suposição: O ambiente de homologação permite simular a data de contratação e avançar o relógio, e tem painel do gateway para consultar cobranças e reembolsos

**Pré-condições:**
- Usuário qa.cancel06@nexi.test logado no app
- Plano Mensal R$ 39,90 contratado há 15 dias (simular data no ambiente)

**Dados:**
- `usuário`: qa.cancel06@nexi.test
- `plano`: Mensal R$ 39,90
- `dias desde a contratação`: 15

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar e confirmar em "Tem certeza?"
3. Avançar o relógio do ambiente até 1 dia depois da data de renovação
4. Consultar as cobranças do usuário no painel do gateway (homologação)

**Resultado esperado:** O gateway mostra só a cobrança de R$ 39,90 da contratação; não existe cobrança na data de renovação

### CT-07 · Mensal cancelado perde o acesso no dia seguinte ao fim do período pago

**Critérios:** CA4 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de Suposição: O ambiente de homologação permite simular a data de contratação e avançar o relógio, e tem painel do gateway para consultar cobranças e reembolsos

**Pré-condições:**
- Usuário qa.cancel07@nexi.test com Mensal R$ 39,90 contratado há 15 dias e cancelado hoje pelo app
- Relógio do ambiente avançado para o dia seguinte ao fim do período pago

**Dados:**
- `usuário`: qa.cancel07@nexi.test
- `plano`: Mensal R$ 39,90

**Passos:**
1. Abrir o app logado com qa.cancel07@nexi.test
2. Tentar abrir um título do catálogo

**Resultado esperado:** O título não é reproduzido e Conta > Assinatura não mostra assinatura ativa

### CT-08 · Anual cancelado com 3 meses de uso recebe reembolso proporcional dos 9 meses restantes

**Critérios:** CA5 · **Tipo:** positivo · **Técnica:** tabela de decisão · **Prioridade:** Alta

> Depende de D1 (bloqueia)

> Depende de D2 (bloqueia)

> Depende de Suposição: O ambiente de homologação permite simular a data de contratação e avançar o relógio, e tem painel do gateway para consultar cobranças e reembolsos

**Pré-condições:**
- Usuário qa.cancel08@nexi.test logado no app
- Plano Anual R$ 399,00 contratado exatamente 3 meses antes (ex.: contratação simulada em 14/07/2026 e cancelamento em 14/10/2026)
- Bloqueado pelas dúvidas D1 (acesso x reembolso) e D2 (base do cálculo)

**Dados:**
- `usuário`: qa.cancel08@nexi.test
- `plano`: Anual R$ 399,00
- `meses usados`: 3
- `meses não usados`: 9
- `valor por mês`: R$ 399,00 / 12 = R$ 33,25

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar e confirmar em "Tem certeza?"
3. Consultar o reembolso no painel do gateway de pagamento (homologação)

**Resultado esperado:** O gateway registra um reembolso de R$ 299,25 (9 meses × R$ 33,25)

### CT-09 · Anual cancelado no 8º dia recebe reembolso proporcional e não integral

**Critérios:** CA3, CA5 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D1 (bloqueia)

> Depende de D2 (bloqueia)

> Depende de D3 (bloqueia)

> Depende de Suposição: Na contagem dos 7 dias, o dia da contratação é o dia 0 e contam dias corridos

> Depende de Suposição: No anual, o mês em curso conta como usado no cálculo proporcional

> Depende de Suposição: O ambiente de homologação permite simular a data de contratação e avançar o relógio, e tem painel do gateway para consultar cobranças e reembolsos

**Pré-condições:**
- Usuário qa.cancel09@nexi.test logado no app
- Plano Anual R$ 399,00 contratado há 8 dias corridos, contando o dia da contratação como dia 0 (simular data no ambiente)
- Bloqueado pelas dúvidas D2 (mês em curso conta como usado?) e D3 (contagem dos 7 dias)

**Dados:**
- `usuário`: qa.cancel09@nexi.test
- `plano`: Anual R$ 399,00
- `dias desde a contratação`: 8
- `meses não usados`: 11 (1º mês em curso contado como usado)

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar e confirmar em "Tem certeza?"
3. Consultar o reembolso no painel do gateway de pagamento (homologação)

**Resultado esperado:** O gateway registra um reembolso de R$ 365,75 (11 meses × R$ 33,25), e não de R$ 399,00

### CT-10 · Anual cancelado no 40º dia não é cobrado na renovação anual

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** tabela de decisão · **Prioridade:** Média

> Depende de Suposição: O ambiente de homologação permite simular a data de contratação e avançar o relógio, e tem painel do gateway para consultar cobranças e reembolsos

**Pré-condições:**
- Usuário qa.cancel10@nexi.test logado no app
- Plano Anual R$ 399,00 contratado há 40 dias (simular data no ambiente)

**Dados:**
- `usuário`: qa.cancel10@nexi.test
- `plano`: Anual R$ 399,00
- `dias desde a contratação`: 40

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar e confirmar em "Tem certeza?"
3. Avançar o relógio do ambiente até 1 dia depois do aniversário de 12 meses da contratação
4. Consultar as cobranças do usuário no painel do gateway (homologação)

**Resultado esperado:** O gateway mostra só a cobrança de R$ 399,00 da contratação; não existe nova cobrança de R$ 399,00 na renovação

### CT-11 · Clicar em Cancelar abre a confirmação "Tem certeza?" sem cancelar ainda

**Critérios:** CA2 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.cancel11@nexi.test logado com Mensal R$ 39,90 ativo há 20 dias

**Dados:**
- `usuário`: qa.cancel11@nexi.test
- `plano`: Mensal R$ 39,90

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Sem responder ao diálogo, conferir o status da assinatura no banco/backoffice

**Resultado esperado:** Aparece um diálogo com o texto "Tem certeza?"; o status da assinatura no banco continua ativo

### CT-12 · Desistir na confirmação mantém a assinatura ativa

**Critérios:** CA2 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.cancel12@nexi.test logado com Mensal R$ 39,90 ativo há 20 dias

**Dados:**
- `usuário`: qa.cancel12@nexi.test
- `plano`: Mensal R$ 39,90

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. No diálogo "Tem certeza?", escolher a opção de desistir (não confirmar)
4. Recarregar Conta > Assinatura

**Resultado esperado:** Conta > Assinatura mostra o Mensal ativo, com a mesma data de renovação de antes do teste

### CT-13 · Cancelamento confirmado envia e-mail de confirmação

**Critérios:** CA6 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.cancel13@nexi.test logado com Mensal R$ 39,90 ativo há 20 dias
- Caixa de entrada de qa.cancel13@nexi.test vazia

**Dados:**
- `usuário`: qa.cancel13@nexi.test
- `plano`: Mensal R$ 39,90

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar e confirmar em "Tem certeza?"
3. Abrir a caixa de entrada de qa.cancel13@nexi.test

**Resultado esperado:** Chega 1 e-mail para qa.cancel13@nexi.test informando que a assinatura Mensal foi cancelada

### CT-14 · Desistir na confirmação não envia e-mail de cancelamento

**Critérios:** CA6 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.cancel14@nexi.test logado com Mensal R$ 39,90 ativo há 20 dias
- Caixa de entrada de qa.cancel14@nexi.test vazia

**Dados:**
- `usuário`: qa.cancel14@nexi.test
- `plano`: Mensal R$ 39,90

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. No diálogo "Tem certeza?", escolher a opção de desistir
4. Aguardar 10 minutos e abrir a caixa de entrada de qa.cancel14@nexi.test

**Resultado esperado:** Nenhum e-mail de cancelamento chega em qa.cancel14@nexi.test

### CT-15 · Duplo clique em confirmar gera um único reembolso de R$ 39,90

**Critérios:** CA3 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Alta

> Depende de Suposição: O ambiente de homologação permite simular a data de contratação e avançar o relógio, e tem painel do gateway para consultar cobranças e reembolsos

**Pré-condições:**
- Usuário qa.cancel15@nexi.test logado com Mensal R$ 39,90 contratado há 2 dias (simular data no ambiente)

**Dados:**
- `usuário`: qa.cancel15@nexi.test
- `plano`: Mensal R$ 39,90
- `dias desde a contratação`: 2

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Clicar duas vezes seguidas, rápido, no botão de confirmar do diálogo "Tem certeza?"
4. Consultar os reembolsos no painel do gateway (homologação)

**Resultado esperado:** O gateway mostra exatamente 1 reembolso, de R$ 39,90; total reembolsado é R$ 39,90

### CT-16 · Mensal cancelado no último dia do período não é cobrado no dia seguinte

**Critérios:** CA1, CA4 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

> Depende de Suposição: Plano Mensal cancelado depois de 7 dias não tem reembolso (o texto só fala em reembolso no integral e no anual)

> Depende de Suposição: O ambiente de homologação permite simular a data de contratação e avançar o relógio, e tem painel do gateway para consultar cobranças e reembolsos

**Pré-condições:**
- Usuário qa.cancel16@nexi.test logado com Mensal R$ 39,90
- Relógio do ambiente no último dia do período pago, antes do horário da renovação automática

**Dados:**
- `usuário`: qa.cancel16@nexi.test
- `plano`: Mensal R$ 39,90

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar e confirmar em "Tem certeza?"
3. Avançar o relógio do ambiente para 1 dia depois da data de renovação
4. Consultar as cobranças do usuário no painel do gateway (homologação)

**Resultado esperado:** Não existe cobrança de R$ 39,90 na data de renovação; Conta > Assinatura não mostra assinatura ativa

## Fora do escopo

- Cancelamento pelo site, pelo suporte ou pela loja de apps (Apple/Google)
- Reativar assinatura cancelada
- Troca de plano (Mensal para Anual e vice-versa)
- Cancelamento de assinatura em período de teste grátis ou com cupom de desconto
- Conteúdo e layout completos do e-mail de cancelamento
