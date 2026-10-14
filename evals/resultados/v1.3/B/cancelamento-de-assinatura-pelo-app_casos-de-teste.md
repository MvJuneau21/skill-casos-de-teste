# Casos de teste: Cancelamento de assinatura pelo app

**Origem:** Mensagem do PO no Slack (texto colado pelo usuário em 14/10/2026) · **Gerado em:** 14/10/2026

**16 casos:** 7 positivos, 4 negativos, 5 de borda · **Prioridade:** 8 Alta, 8 Média, 0 Baixa

## Pontos a confirmar com o PO

**Dúvidas que bloqueiam a execução** (responder primeiro):

- **D1.** Como contam os 7 dias? O dia da contratação é o dia 0 ou o dia 1? Conta por data (dias corridos) ou por 7 × 24 h a partir da hora da contratação? Em qual fuso? _(CA3 · bloqueia CT-03, CT-04, CT-09 · Define qual é o último dia com reembolso integral; os casos de limite usam a suposição de dia 0 e dias corridos)_
- **D2.** Como se calcula o reembolso proporcional do anual? Base de R$ 399,00 / 12 = R$ 33,25 por mês ou outra (ex.: mês usado cobrado a R$ 39,90)? O mês em curso conta como usado? Como arredondar centavos? _(CA6 · bloqueia CT-08, CT-09, CT-10 · Muda o valor esperado do reembolso (ex.: no 4º mês, R$ 266,00 se o mês em curso conta como usado; R$ 299,25 se não conta))_

**Outras dúvidas** (o requisito não diz; nenhum caso inventa a resposta):

- **D3.** O texto diz que, passados 7 dias, o assinante mantém acesso até o fim do período pago, e também que o anual tem reembolso dos meses não usados. No anual cancelado depois de 7 dias, o acesso vai até o fim do mês em curso ou até o fim do ano contratado (mesmo com reembolso)? _(CA4, CA6 · Contradição: falta o caso de acesso do anual depois do mês em curso. CT-11 só confere o que vale nas duas leituras (acesso dentro do mês em curso))_
- **D4.** Mensal cancelado depois de 7 dias fica sem nenhum reembolso? O texto só fala de reembolso em até 7 dias e no anual. _(CA3, CA6 · CT-04 assume que não há reembolso (ver suposição))_
- **D5.** Quem cancela em até 7 dias (com reembolso integral) perde o acesso na hora ou mantém até o fim do período? _(CA3, CA4 · Sem caso de acesso para cancelamento em até 7 dias; será criado com a resposta)_
- **D6.** O que o app mostra ao abrir Conta > Assinatura de uma assinatura já cancelada (botão Cancelar some, fica desabilitado, aparece mensagem)? E qual o texto dos botões da confirmação? _(CA1, CA2 · CT-13 e CT-16 conferem só gateway, banco e e-mail, não a tela)_
- **D7.** O que o e-mail de confirmação precisa conter (valor do reembolso, data de fim do acesso) e em quanto tempo deve chegar? O reembolso volta para o meio de pagamento original e em que prazo? _(CA7, CA3, CA6 · CT-14 confere só que o e-mail chega; casos de reembolso conferem o registro no gateway, não o estorno no cartão)_
- **D8.** A regra vale para assinaturas feitas por App Store/Google Play, para teste grátis e para cancelamento pela web, ou só para quem assinou e cancela pelo app? _(CA1 · Pode exigir casos adicionais por canal de compra)_

**Suposições** (usadas nos casos; se estiverem erradas, os casos indicados mudam):

- O dia da contratação é o dia 0 e os 7 dias contam por data, em dias corridos (contratado em 01/10: dia 7 = 08/10, dia 8 = 09/10) _(CT-03, CT-04, CT-09)_
- Plano mensal cancelado depois de 7 dias não tem reembolso (o texto só cita reembolso em até 7 dias e no anual) _(CT-04)_
- Reembolso proporcional = meses não usados × R$ 33,25 (R$ 399,00 / 12), e o mês em curso conta como usado _(CT-08, CT-09, CT-10)_

## Critérios e cobertura

| Critério | Descrição | Casos | Dúvidas |
|---|---|---|---|
| CA1 _(derivado)_ | Assinante cancela pelo app a qualquer momento em Conta > Assinatura > Cancelar | CT-01, CT-13, CT-16 | D6, D8 |
| CA2 _(derivado)_ | Antes de cancelar, o app pede confirmação ("Tem certeza?") | CT-12, CT-13 | D6 |
| CA3 _(derivado)_ | Cancelamento em até 7 dias da contratação tem reembolso integral | CT-01, CT-02, CT-03, CT-04, CT-09, CT-15, CT-16 | D1, D4, D5, D7 |
| CA4 _(derivado)_ | Cancelamento depois de 7 dias mantém o acesso até o fim do período já pago | CT-05, CT-06, CT-11 | D3, D5 |
| CA5 _(derivado)_ | Cancelamento depois de 7 dias não gera nova cobrança | CT-07 | — |
| CA6 _(derivado)_ | Plano anual cancelado depois de 7 dias tem reembolso proporcional aos meses não usados | CT-08, CT-09, CT-10, CT-11 | D2, D3, D4, D7 |
| CA7 _(derivado)_ | Um e-mail confirma o cancelamento | CT-13, CT-14 | D7 |

## Casos

### CT-01 · Mensal cancelado no 3º dia recebe reembolso integral de R$ 39,90

**Critérios:** CA1, CA3 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

**Pré-condições:**
- Usuário qa.cancel01@nexi.test logado no app
- Plano Mensal R$ 39,90 contratado há 3 dias, pago com cartão de teste final 4242

**Dados:**
- `usuário`: qa.cancel01@nexi.test
- `plano`: Mensal R$ 39,90
- `dias desde a contratação`: 3

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Confirmar na pergunta "Tem certeza?"
4. Consultar a transação da assinatura no gateway de pagamento

**Resultado esperado:** Gateway mostra reembolso de R$ 39,90 para a assinatura de qa.cancel01@nexi.test

### CT-02 · Anual cancelado no 3º dia recebe reembolso integral de R$ 399,00

**Critérios:** CA3 · **Tipo:** positivo · **Técnica:** tabela de decisão · **Prioridade:** Alta

**Pré-condições:**
- Usuário qa.cancel02@nexi.test logado no app
- Plano Anual R$ 399,00 contratado há 3 dias

**Dados:**
- `usuário`: qa.cancel02@nexi.test
- `plano`: Anual R$ 399,00
- `dias desde a contratação`: 3

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Confirmar na pergunta "Tem certeza?"
4. Consultar a transação da assinatura no gateway de pagamento

**Resultado esperado:** Gateway mostra reembolso de R$ 399,00 para a assinatura de qa.cancel02@nexi.test

### CT-03 · Mensal cancelado no 7º dia ainda recebe reembolso integral de R$ 39,90

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

> Depende de D1 (bloqueia)

> Depende de Suposição: O dia da contratação é o dia 0 e os 7 dias contam por data, em dias corridos (contratado em 01/10: dia 7 = 08/10, dia 8 = 09/10)

**Pré-condições:**
- Usuário qa.cancel03@nexi.test logado no app
- Plano Mensal R$ 39,90 contratado; data do ambiente avançada para contratação + 7 dias (ex.: contratado em 01/10, testar em 08/10)

**Dados:**
- `usuário`: qa.cancel03@nexi.test
- `plano`: Mensal R$ 39,90
- `dia do cancelamento`: contratação + 7 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Confirmar na pergunta "Tem certeza?"
4. Consultar a transação no gateway

**Resultado esperado:** Gateway mostra reembolso de R$ 39,90

### CT-04 · Mensal cancelado no 8º dia não recebe reembolso

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

> Depende de D1 (bloqueia)

> Depende de Suposição: O dia da contratação é o dia 0 e os 7 dias contam por data, em dias corridos (contratado em 01/10: dia 7 = 08/10, dia 8 = 09/10)

> Depende de Suposição: Plano mensal cancelado depois de 7 dias não tem reembolso (o texto só cita reembolso em até 7 dias e no anual)

**Pré-condições:**
- Usuário qa.cancel04@nexi.test logado no app
- Plano Mensal R$ 39,90 contratado; data do ambiente avançada para contratação + 8 dias (ex.: contratado em 01/10, testar em 09/10)

**Dados:**
- `usuário`: qa.cancel04@nexi.test
- `plano`: Mensal R$ 39,90
- `dia do cancelamento`: contratação + 8 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Confirmar na pergunta "Tem certeza?"
4. Consultar a transação no gateway

**Resultado esperado:** Gateway não mostra nenhum reembolso para a assinatura; a cobrança de R$ 39,90 continua liquidada

### CT-05 · Mensal cancelado no 15º dia mantém acesso até o fim do período pago

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.cancel05@nexi.test com plano Mensal R$ 39,90 contratado há 15 dias
- Assinatura cancelada pelo app no 15º dia
- Data do ambiente avançada para contratação + 25 dias (ainda dentro do mês pago)

**Dados:**
- `usuário`: qa.cancel05@nexi.test
- `título de teste`: QA-001
- `data simulada`: contratação + 25 dias (dentro do período pago)

**Passos:**
1. Abrir o app logado como qa.cancel05@nexi.test
2. Buscar o título QA-001
3. Tocar em reproduzir

**Resultado esperado:** O player reproduz QA-001 e o contador de tempo avança

### CT-06 · Mensal cancelado perde o acesso no dia seguinte ao fim do período pago

**Critérios:** CA4 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.cancel05@nexi.test com plano Mensal cancelado no 15º dia (mesmo usuário de CT-05)
- Data do ambiente avançada para 1 dia depois do fim do período pago (contratação + 1 mês + 1 dia)

**Dados:**
- `usuário`: qa.cancel05@nexi.test
- `título de teste`: QA-001
- `data simulada`: contratação + 1 mês + 1 dia (fora do período pago)

**Passos:**
1. Abrir o app logado como qa.cancel05@nexi.test
2. Buscar o título QA-001
3. Tocar em reproduzir

**Resultado esperado:** O player não reproduz QA-001 (contador de tempo não avança)

### CT-07 · Mensal cancelado no 15º dia não é cobrado na data de renovação

**Critérios:** CA5 · **Tipo:** negativo · **Técnica:** transição de estado · **Prioridade:** Alta

**Pré-condições:**
- Usuário qa.cancel06@nexi.test com plano Mensal R$ 39,90 cancelado pelo app no 15º dia
- Data do ambiente avançada para a data de renovação (contratação + 1 mês) e rotina de cobrança recorrente executada

**Dados:**
- `usuário`: qa.cancel06@nexi.test
- `plano`: Mensal R$ 39,90

**Passos:**
1. Consultar as transações da assinatura no gateway após a rotina de cobrança

**Resultado esperado:** Gateway mostra só a cobrança inicial de R$ 39,90; nenhuma cobrança nova na data de renovação

### CT-08 · Anual cancelado no 4º mês recebe reembolso proporcional de R$ 266,00

**Critérios:** CA6 · **Tipo:** positivo · **Técnica:** tabela de decisão · **Prioridade:** Alta

> Depende de D2 (bloqueia)

> Depende de Suposição: Reembolso proporcional = meses não usados × R$ 33,25 (R$ 399,00 / 12), e o mês em curso conta como usado

**Pré-condições:**
- Usuário qa.cancel07@nexi.test com plano Anual R$ 399,00 contratado há 3 meses e 10 dias (4º mês em curso); data do ambiente ajustada se preciso

**Dados:**
- `usuário`: qa.cancel07@nexi.test
- `plano`: Anual R$ 399,00
- `conta`: 399,00 / 12 = 33,25 por mês; 4 meses usados (mês em curso conta); 8 × 33,25 = 266,00

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Confirmar na pergunta "Tem certeza?"
4. Consultar a transação no gateway

**Resultado esperado:** Gateway mostra reembolso de R$ 266,00

### CT-09 · Anual cancelado no 8º dia recebe reembolso proporcional de R$ 365,75, não integral

**Critérios:** CA3, CA6 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

> Depende de D1 (bloqueia)

> Depende de D2 (bloqueia)

> Depende de Suposição: O dia da contratação é o dia 0 e os 7 dias contam por data, em dias corridos (contratado em 01/10: dia 7 = 08/10, dia 8 = 09/10)

> Depende de Suposição: Reembolso proporcional = meses não usados × R$ 33,25 (R$ 399,00 / 12), e o mês em curso conta como usado

**Pré-condições:**
- Usuário qa.cancel08@nexi.test com plano Anual R$ 399,00 contratado; data do ambiente avançada para contratação + 8 dias

**Dados:**
- `usuário`: qa.cancel08@nexi.test
- `plano`: Anual R$ 399,00
- `conta`: 1 mês usado (em curso); 11 × 33,25 = 365,75

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Confirmar na pergunta "Tem certeza?"
4. Consultar a transação no gateway

**Resultado esperado:** Gateway mostra reembolso de R$ 365,75

### CT-10 · Anual cancelado no 12º mês não gera reembolso

**Critérios:** CA6 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D2 (bloqueia)

> Depende de Suposição: Reembolso proporcional = meses não usados × R$ 33,25 (R$ 399,00 / 12), e o mês em curso conta como usado

**Pré-condições:**
- Usuário qa.cancel09@nexi.test com plano Anual R$ 399,00 contratado há 11 meses e 10 dias (12º mês em curso); data do ambiente ajustada

**Dados:**
- `usuário`: qa.cancel09@nexi.test
- `plano`: Anual R$ 399,00
- `conta`: 12 meses usados; 0 × 33,25 = 0,00

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Confirmar na pergunta "Tem certeza?"
4. Consultar a transação no gateway

**Resultado esperado:** Gateway não mostra reembolso para a assinatura (nenhum lançamento de R$ 0,00 nem valor negativo)

### CT-11 · Anual cancelado no 4º mês mantém acesso até o fim do mês em curso

**Critérios:** CA4, CA6 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.cancel07@nexi.test com plano Anual cancelado no 4º mês (mesmo usuário de CT-08)
- Data do ambiente avançada em 5 dias, ainda dentro do 4º mês

**Dados:**
- `usuário`: qa.cancel07@nexi.test
- `título de teste`: QA-001

**Passos:**
1. Abrir o app logado como qa.cancel07@nexi.test
2. Buscar o título QA-001
3. Tocar em reproduzir

**Resultado esperado:** O player reproduz QA-001 e o contador de tempo avança

### CT-12 · Tocar em Cancelar mostra a pergunta "Tem certeza?" antes de cancelar

**Critérios:** CA2 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.cancel10@nexi.test com plano Mensal R$ 39,90 ativo há 3 dias

**Dados:**
- `usuário`: qa.cancel10@nexi.test

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Sem responder a pergunta, consultar o gateway e a caixa de qa.cancel10@nexi.test

**Resultado esperado:** Aparece a pergunta "Tem certeza?"; o gateway não mostra reembolso e nenhum e-mail de cancelamento chegou

### CT-13 · Desistir na pergunta "Tem certeza?" não cancela a assinatura

**Critérios:** CA1, CA2, CA7 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.cancel10@nexi.test com plano Mensal R$ 39,90 ativo há 3 dias

**Dados:**
- `usuário`: qa.cancel10@nexi.test

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Desistir na pergunta "Tem certeza?" (opção de não confirmar ou fechar o diálogo)
4. Consultar o gateway, a caixa de e-mail e o status da assinatura no banco

**Resultado esperado:** Status da assinatura no banco continua ativa; gateway sem reembolso; nenhum e-mail de cancelamento em qa.cancel10@nexi.test

### CT-14 · Cancelamento confirmado envia e-mail de confirmação

**Critérios:** CA7 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.cancel11@nexi.test com plano Mensal R$ 39,90 ativo há 15 dias; caixa de e-mail vazia

**Dados:**
- `usuário`: qa.cancel11@nexi.test

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Confirmar na pergunta "Tem certeza?"
4. Abrir a caixa de qa.cancel11@nexi.test

**Resultado esperado:** Chega em qa.cancel11@nexi.test um e-mail confirmando o cancelamento da assinatura

### CT-15 · Toque duplo em confirmar registra um só reembolso

**Critérios:** CA3 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Alta

**Pré-condições:**
- Usuário qa.cancel12@nexi.test com plano Mensal R$ 39,90 contratado há 2 dias

**Dados:**
- `usuário`: qa.cancel12@nexi.test
- `plano`: Mensal R$ 39,90

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Tocar duas vezes seguidas na confirmação da pergunta "Tem certeza?"
4. Consultar a transação no gateway

**Resultado esperado:** Gateway mostra exatamente um reembolso de R$ 39,90 (total reembolsado R$ 39,90)

### CT-16 · Assinatura já cancelada não recebe segundo reembolso

**Critérios:** CA1, CA3 · **Tipo:** negativo · **Técnica:** transição de estado · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.cancel01@nexi.test com plano Mensal já cancelado no 3º dia e reembolsado em R$ 39,90 (estado final de CT-01)

**Dados:**
- `usuário`: qa.cancel01@nexi.test

**Passos:**
1. Acessar Conta > Assinatura
2. Tentar tocar em Cancelar de novo e confirmar, se a opção existir
3. Consultar a transação no gateway

**Resultado esperado:** Gateway continua com um único reembolso de R$ 39,90 (total reembolsado R$ 39,90)

## Fora do escopo

- Reativar assinatura cancelada
- Troca de plano (mensal ↔ anual)
- Cancelamento feito pelo suporte ou backoffice
- Cancelamento automático por falta de pagamento
- Layout e texto completo do e-mail de cancelamento
