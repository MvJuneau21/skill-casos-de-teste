# Casos de teste: Cancelamento de assinatura pelo app

**Origem:** Mensagem do PO no Slack (regra do cancelamento para a próxima sprint), colada pelo usuário · **Gerado em:** 14/10/2026

**17 casos:** 9 positivos, 3 negativos, 5 de borda · **Prioridade:** 8 Alta, 9 Média, 0 Baixa

## Pontos a confirmar com o PO

**Dúvidas que bloqueiam a execução** (responder primeiro):

- **D1.** Plano anual cancelado depois de 7 dias: a mensagem diz que ele mantém o acesso até o fim do período pago e também que recebe reembolso dos meses não usados. Se os meses são reembolsados, o acesso acaba no cancelamento ou continua até o fim do ano contratado? _(CA4, CA6 · bloqueia CT-07 · As duas regras se contradizem para o anual; CT-07 não tem resultado esperado certo)_
- **D2.** Como contar os 7 dias: o dia da contratação é o dia 0 ou o dia 1? Conta em dias corridos (até 23:59 do 7º dia, em qual fuso) ou em 7 × 24 horas a partir do horário da contratação? _(CA3 · bloqueia CT-03, CT-04, CT-05 · Define se o cancelamento em 14/10 de quem contratou em 07/10 ou 06/10 tem reembolso integral)_
- **D3.** Como calcular os meses não usados do anual: o mês em andamento conta como usado, como não usado ou é proporcional por dia? O valor do mês é R$ 399,00 / 12 = R$ 33,25? Como arredonda os centavos se for por dia? _(CA6 · bloqueia CT-05, CT-06 · Muda o valor do reembolso: com 2 meses e 15 dias de uso pode ser R$ 299,25 (9 meses) ou R$ 332,50 (10 meses), por exemplo)_

**Outras dúvidas** (o requisito não diz; nenhum caso inventa a resposta):

- **D4.** Quem cancela em até 7 dias (com reembolso integral) perde o acesso na hora ou mantém até o fim do período? _(CA3, CA4 · Sem caso de acesso para cancelamento dentro dos 7 dias até a resposta)_
- **D5.** Os 7 dias contam só a partir da primeira contratação ou também de cada renovação (ex.: mensal renovado há 3 dias tem reembolso integral)? _(CA3 · Pode exigir um caso extra para renovação; os casos atuais usam a primeira contratação)_
- **D6.** O que Conta > Assinatura mostra depois do cancelamento (status, data de fim do acesso) e para uma assinatura já cancelada (o botão Cancelar some, fica desabilitado)? _(CA1 · CT-08 e CT-17 conferem só acesso e reembolso, não a tela)_
- **D7.** O que o e-mail de cancelamento precisa conter (plano, data de fim do acesso, valor e prazo do reembolso) e quais são os botões do diálogo "Tem certeza?"? _(CA2, CA7 · CT-14 e CT-15 conferem só a chegada do e-mail e o status, não o conteúdo)_
- **D8.** Como e em quanto tempo o reembolso chega ao assinante (estorno no cartão, crédito, prazo)? Assinaturas pagas com cupom recebem de volta o valor pago ou o preço cheio? _(CA3, CA6 · Os casos conferem o reembolso registrado no gateway, não o crédito na fatura)_

**Suposições** (usadas nos casos; se estiverem erradas, os casos indicados mudam):

- Plano mensal cancelado depois de 7 dias não tem reembolso (a mensagem só fala de reembolso dentro dos 7 dias e para o anual) _(CT-04)_
- Na contagem dos 7 dias, a data da contratação é o dia 0 e o 7º dia vale até 23:59 (contratou em 07/10, cancela até 14/10 com reembolso integral) _(CT-03, CT-04, CT-05)_
- No anual, o mês em andamento conta como usado e cada mês vale R$ 399,00 / 12 = R$ 33,25 _(CT-05, CT-06)_
- O reembolso pode ser conferido no histórico do gateway de pagamento de homologação e o relógio do ambiente pode ser avançado para simular renovação _(CT-01, CT-02, CT-03, CT-04, CT-05, CT-06, CT-09, CT-10, CT-11, CT-12, CT-16, CT-17)_

## Critérios e cobertura

| Critério | Descrição | Casos | Dúvidas |
|---|---|---|---|
| CA1 _(derivado)_ | Assinante cancela pelo app a qualquer momento em Conta > Assinatura > Cancelar | CT-01, CT-12, CT-17 | D6 |
| CA2 _(derivado)_ | Antes de cancelar, o app pede confirmação ("Tem certeza?") | CT-13, CT-14 | D7 |
| CA3 _(derivado)_ | Cancelamento em até 7 dias da contratação gera reembolso integral (CDC), em qualquer plano | CT-01, CT-02, CT-03, CT-04, CT-05, CT-16, CT-17 | D2, D4, D5, D8 |
| CA4 _(derivado)_ | Cancelamento depois de 7 dias mantém o acesso até o fim do período já pago | CT-04, CT-07, CT-08, CT-09 | D1, D4 |
| CA5 _(derivado)_ | Cancelamento depois de 7 dias impede nova cobrança | CT-10, CT-11, CT-12 | — |
| CA6 _(derivado)_ | Plano anual cancelado depois de 7 dias tem reembolso proporcional aos meses não usados | CT-05, CT-06, CT-07 | D1, D3, D8 |
| CA7 _(derivado)_ | Um e-mail confirmando o cancelamento é enviado ao assinante | CT-14, CT-15 | D7 |

## Casos

### CT-01 · Mensal cancelado no 3º dia recebe reembolso integral de R$ 39,90

**Critérios:** CA1, CA3 · **Tipo:** positivo · **Técnica:** tabela de decisão · **Prioridade:** Alta

> Depende de Suposição: O reembolso pode ser conferido no histórico do gateway de pagamento de homologação e o relógio do ambiente pode ser avançado para simular renovação

**Pré-condições:**
- Usuário qa.mensal01@nexi.test logado no app
- Plano Mensal R$ 39,90 contratado há 3 dias, pago com cartão de teste final 4242

**Dados:**
- `plano`: Mensal R$ 39,90
- `dias desde a contratação`: 3

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Consultar o histórico de reembolsos da assinatura no gateway de pagamento de homologação

**Resultado esperado:** Existe um reembolso de R$ 39,90 para o cartão final 4242 e a assinatura aparece com status Cancelada

### CT-02 · Anual cancelado no 3º dia recebe reembolso integral de R$ 399,00

**Critérios:** CA3 · **Tipo:** positivo · **Técnica:** tabela de decisão · **Prioridade:** Alta

> Depende de Suposição: O reembolso pode ser conferido no histórico do gateway de pagamento de homologação e o relógio do ambiente pode ser avançado para simular renovação

**Pré-condições:**
- Usuário qa.anual01@nexi.test logado no app
- Plano Anual R$ 399,00 contratado há 3 dias, pago com cartão de teste final 4242

**Dados:**
- `plano`: Anual R$ 399,00
- `dias desde a contratação`: 3

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Consultar o histórico de reembolsos no gateway de pagamento de homologação

**Resultado esperado:** Existe um único reembolso de R$ 399,00 (integral, não proporcional) para o cartão final 4242

### CT-03 · Mensal cancelado no 7º dia ainda recebe reembolso integral (aguarda dúvida da contagem dos 7 dias)

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

> Depende de D2 (bloqueia)

> Depende de Suposição: Na contagem dos 7 dias, a data da contratação é o dia 0 e o 7º dia vale até 23:59 (contratou em 07/10, cancela até 14/10 com reembolso integral)

> Depende de Suposição: O reembolso pode ser conferido no histórico do gateway de pagamento de homologação e o relógio do ambiente pode ser avançado para simular renovação

**Pré-condições:**
- Usuário qa.mensal02@nexi.test logado no app
- Plano Mensal R$ 39,90 contratado em 07/10/2026 (data de contratação ajustada no banco ou relógio do ambiente em 14/10/2026, 7º dia)

**Dados:**
- `plano`: Mensal R$ 39,90
- `contratação`: 07/10/2026
- `cancelamento`: 14/10/2026 às 10:00

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Consultar o histórico de reembolsos no gateway de pagamento de homologação

**Resultado esperado:** Existe um reembolso de R$ 39,90 para o cartão final 4242

### CT-04 · Mensal cancelado no 8º dia não recebe reembolso (aguarda dúvida da contagem dos 7 dias)

**Critérios:** CA3, CA4 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

> Depende de D2 (bloqueia)

> Depende de Suposição: Plano mensal cancelado depois de 7 dias não tem reembolso (a mensagem só fala de reembolso dentro dos 7 dias e para o anual)

> Depende de Suposição: Na contagem dos 7 dias, a data da contratação é o dia 0 e o 7º dia vale até 23:59 (contratou em 07/10, cancela até 14/10 com reembolso integral)

> Depende de Suposição: O reembolso pode ser conferido no histórico do gateway de pagamento de homologação e o relógio do ambiente pode ser avançado para simular renovação

**Pré-condições:**
- Usuário qa.mensal03@nexi.test logado no app
- Plano Mensal R$ 39,90 contratado em 06/10/2026 (data ajustada no banco ou relógio do ambiente em 14/10/2026, 8º dia)

**Dados:**
- `plano`: Mensal R$ 39,90
- `contratação`: 06/10/2026
- `cancelamento`: 14/10/2026 às 10:00

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Consultar o histórico de reembolsos no gateway de pagamento de homologação

**Resultado esperado:** Nenhum reembolso registrado para a assinatura; status Cancelada

### CT-05 · Anual cancelado no 8º dia recebe reembolso proporcional de R$ 365,75 e não integral

**Critérios:** CA3, CA6 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D2 (bloqueia)

> Depende de D3 (bloqueia)

> Depende de Suposição: Na contagem dos 7 dias, a data da contratação é o dia 0 e o 7º dia vale até 23:59 (contratou em 07/10, cancela até 14/10 com reembolso integral)

> Depende de Suposição: No anual, o mês em andamento conta como usado e cada mês vale R$ 399,00 / 12 = R$ 33,25

> Depende de Suposição: O reembolso pode ser conferido no histórico do gateway de pagamento de homologação e o relógio do ambiente pode ser avançado para simular renovação

**Pré-condições:**
- Usuário qa.anual02@nexi.test logado no app
- Plano Anual R$ 399,00 contratado em 06/10/2026 (data ajustada no banco ou relógio do ambiente em 14/10/2026, 8º dia)

**Dados:**
- `plano`: Anual R$ 399,00
- `contratação`: 06/10/2026
- `cancelamento`: 14/10/2026
- `conta (suposição: mês em andamento conta como usado)`: 12 - 1 = 11 meses não usados × R$ 33,25 = R$ 365,75

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Consultar o histórico de reembolsos no gateway de pagamento de homologação

**Resultado esperado:** Existe um único reembolso de R$ 365,75 para o cartão final 4242 (e não de R$ 399,00)

### CT-06 · Anual cancelado com 2 meses e 15 dias de uso recebe reembolso de R$ 299,25

**Critérios:** CA6 · **Tipo:** positivo · **Técnica:** tabela de decisão · **Prioridade:** Alta

> Depende de D3 (bloqueia)

> Depende de Suposição: No anual, o mês em andamento conta como usado e cada mês vale R$ 399,00 / 12 = R$ 33,25

> Depende de Suposição: O reembolso pode ser conferido no histórico do gateway de pagamento de homologação e o relógio do ambiente pode ser avançado para simular renovação

**Pré-condições:**
- Usuário qa.anual03@nexi.test logado no app
- Plano Anual R$ 399,00 contratado em 30/07/2026 (data ajustada no banco; cancelamento em 14/10/2026 = 2 meses e 15 dias de uso)

**Dados:**
- `plano`: Anual R$ 399,00
- `contratação`: 30/07/2026
- `cancelamento`: 14/10/2026
- `conta (suposição: mês em andamento conta como usado)`: 12 - 3 = 9 meses não usados × R$ 33,25 = R$ 299,25

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Consultar o histórico de reembolsos no gateway de pagamento de homologação

**Resultado esperado:** Existe um único reembolso de R$ 299,25 para o cartão final 4242

### CT-07 · Anual cancelado depois de 7 dias mantém acesso até 29/07/2027 (aguarda dúvida reembolso proporcional x acesso)

**Critérios:** CA4, CA6 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Média

> Depende de D1 (bloqueia)

**Pré-condições:**
- Usuário qa.anual03@nexi.test com o Anual contratado em 30/07/2026 e cancelado em 14/10/2026 (CT-06 executado)

**Dados:**
- `título para reproduzir`: qualquer título do catálogo, ex.: o primeiro da home

**Passos:**
1. Fazer login no app com qa.anual03@nexi.test
2. Abrir o primeiro título da home
3. Clicar em Assistir

**Resultado esperado:** O título começa a reproduzir no dia seguinte ao cancelamento (15/10/2026)

### CT-08 · Mensal cancelado no 20º dia continua reproduzindo conteúdo depois do cancelamento

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.mensal04@nexi.test logado no app
- Plano Mensal R$ 39,90 contratado há 20 dias; próxima renovação em 10 dias

**Dados:**
- `plano`: Mensal R$ 39,90
- `dias desde a contratação`: 20

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Voltar à home e abrir o primeiro título
5. Clicar em Assistir

**Resultado esperado:** O título começa a reproduzir mesmo com a assinatura cancelada

### CT-09 · Mensal cancelado perde o acesso no dia seguinte ao fim do período pago

**Critérios:** CA4 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de Suposição: O reembolso pode ser conferido no histórico do gateway de pagamento de homologação e o relógio do ambiente pode ser avançado para simular renovação

**Pré-condições:**
- Usuário qa.mensal04@nexi.test com o Mensal cancelado no 20º dia (CT-08 executado)
- Relógio do ambiente avançado para 1 dia depois da data em que o período pago termina

**Passos:**
1. Fazer login no app com qa.mensal04@nexi.test
2. Abrir o primeiro título da home
3. Clicar em Assistir

**Resultado esperado:** O título não reproduz

### CT-10 · Mensal cancelado no 20º dia não é cobrado na data de renovação

**Critérios:** CA5 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Alta

> Depende de Suposição: O reembolso pode ser conferido no histórico do gateway de pagamento de homologação e o relógio do ambiente pode ser avançado para simular renovação

**Pré-condições:**
- Usuário qa.mensal05@nexi.test com Mensal R$ 39,90 contratado há 20 dias e cancelado hoje pelo app
- Relógio do ambiente avançado para a data de renovação e rotina de cobrança recorrente executada

**Dados:**
- `plano`: Mensal R$ 39,90
- `dias desde a contratação no cancelamento`: 20

**Passos:**
1. Consultar as cobranças do cartão final 4242 no gateway de pagamento de homologação

**Resultado esperado:** Só existe a cobrança original de R$ 39,90; nenhuma cobrança nova na data de renovação

### CT-11 · Anual cancelado depois de 7 dias não é renovado no fim do ano

**Critérios:** CA5 · **Tipo:** positivo · **Técnica:** partição de equivalência · **Prioridade:** Média

> Depende de Suposição: O reembolso pode ser conferido no histórico do gateway de pagamento de homologação e o relógio do ambiente pode ser avançado para simular renovação

**Pré-condições:**
- Usuário qa.anual03@nexi.test com Anual contratado em 30/07/2026 e cancelado em 14/10/2026 (CT-06 executado)
- Relógio do ambiente avançado para 30/07/2027 e rotina de cobrança recorrente executada

**Dados:**
- `plano`: Anual R$ 399,00
- `renovação simulada`: 30/07/2027

**Passos:**
1. Consultar as cobranças do cartão final 4242 no gateway de pagamento de homologação

**Resultado esperado:** Nenhuma cobrança de R$ 399,00 em 30/07/2027

### CT-12 · Cancelamento feito no último dia do período pago impede a renovação do dia seguinte

**Critérios:** CA1, CA5 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

> Depende de Suposição: O reembolso pode ser conferido no histórico do gateway de pagamento de homologação e o relógio do ambiente pode ser avançado para simular renovação

**Pré-condições:**
- Usuário qa.mensal06@nexi.test logado no app
- Plano Mensal R$ 39,90 no último dia do período pago (renovação amanhã), ajustado no banco ou relógio do ambiente

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Avançar o relógio do ambiente 1 dia e executar a rotina de cobrança recorrente
5. Consultar as cobranças do cartão final 4242 no gateway

**Resultado esperado:** Nenhuma cobrança nova de R$ 39,90 depois do cancelamento

### CT-13 · Clicar em Cancelar abre o diálogo "Tem certeza?" sem cancelar ainda

**Critérios:** CA2 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.mensal07@nexi.test logado no app
- Plano Mensal R$ 39,90 ativo há 20 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Com o diálogo aberto, conferir o status da assinatura no banco ou no painel interno

**Resultado esperado:** Aparece o diálogo com o texto "Tem certeza?" e o status da assinatura continua Ativa

### CT-14 · Desistir no diálogo "Tem certeza?" mantém a assinatura ativa e não envia e-mail

**Critérios:** CA2, CA7 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.mensal07@nexi.test logado no app
- Plano Mensal R$ 39,90 ativo há 20 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. No diálogo "Tem certeza?", escolher a opção de não cancelar (ou fechar o diálogo)
4. Conferir a caixa de entrada de qa.mensal07@nexi.test após 10 minutos

**Resultado esperado:** Conta > Assinatura continua mostrando a assinatura Ativa e nenhum e-mail de cancelamento chega

### CT-15 · E-mail de confirmação do cancelamento chega ao assinante

**Critérios:** CA7 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.mensal08@nexi.test logado no app, com caixa de entrada acessível
- Plano Mensal R$ 39,90 ativo há 20 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Abrir a caixa de entrada de qa.mensal08@nexi.test após 10 minutos

**Resultado esperado:** Chega exatamente 1 e-mail da Nexi para qa.mensal08@nexi.test confirmando o cancelamento da assinatura Mensal

### CT-16 · Duplo clique na confirmação gera um único reembolso

**Critérios:** CA3 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Alta

> Depende de Suposição: O reembolso pode ser conferido no histórico do gateway de pagamento de homologação e o relógio do ambiente pode ser avançado para simular renovação

**Pré-condições:**
- Usuário qa.mensal09@nexi.test logado no app
- Plano Mensal R$ 39,90 contratado há 2 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Clicar duas vezes seguidas, rápido, no botão de confirmar do diálogo "Tem certeza?"
4. Consultar o histórico de reembolsos no gateway de pagamento de homologação

**Resultado esperado:** Existe um único reembolso de R$ 39,90 (total reembolsado R$ 39,90, não R$ 79,80)

### CT-17 · Assinatura já cancelada não gera segundo reembolso

**Critérios:** CA1, CA3 · **Tipo:** negativo · **Técnica:** transição de estado · **Prioridade:** Média

> Depende de Suposição: O reembolso pode ser conferido no histórico do gateway de pagamento de homologação e o relógio do ambiente pode ser avançado para simular renovação

**Pré-condições:**
- Usuário qa.mensal10@nexi.test logado no app
- Plano Mensal R$ 39,90 contratado há 3 dias e já cancelado, com reembolso de R$ 39,90 registrado

**Passos:**
1. Acessar Conta > Assinatura
2. Se a opção Cancelar estiver disponível, clicar nela e confirmar
3. Consultar o histórico de reembolsos no gateway de pagamento de homologação

**Resultado esperado:** O histórico continua com um único reembolso de R$ 39,90

## Fora do escopo

- Cancelamento pelo site, por telefone ou pelo suporte (a mensagem fala só do app)
- Reativar uma assinatura cancelada
- Troca de plano (mensal para anual e vice-versa) e cancelamento logo depois da troca
- Assinaturas pagas por loja de apps (App Store / Google Play), onde o reembolso é da loja
- Telas internas de suporte e financeiro para consultar ou aprovar reembolsos
