# Casos de teste: Cancelamento de assinatura pelo app

**Origem:** Mensagem do PO no Slack (colada pelo usuário em 14/10/2026) · **Gerado em:** 14/10/2026

**15 casos:** 7 positivos, 4 negativos, 4 de borda · **Prioridade:** 7 Alta, 8 Média, 0 Baixa

## Pontos a confirmar com o PO

**Dúvidas que bloqueiam a execução** (responder primeiro):

- **D1.** Como contam os 7 dias? O dia da contratação é o dia 0 ou o dia 1? São dias corridos ou 7 × 24 h a partir da hora da contratação? Qual fuso vale? _(CA3 · bloqueia CT-05 · Define se o cancelamento exatamente 7 dias depois tem reembolso integral)_
- **D2.** Como se calcula o reembolso proporcional do anual? O mês em andamento conta como usado? A base é R$ 399,00 ÷ 12 = R$ 33,25 por mês? Como arredondar centavos? Quem cancela no 12º mês recebe R$ 0,00? _(CA6 · bloqueia CT-10, CT-11 · Muda o valor esperado: com 3 meses e 15 dias pode ser R$ 266,00 (8 meses) ou R$ 299,25 (9 meses))_
- **D3.** O anual cancelado depois de 7 dias recebe reembolso dos meses não usados E continua com acesso até o fim do ano pago (regra dos 7 dias), ou o acesso termina no fim do mês em andamento? As duas regras do Slack se cruzam e não dizem qual vale _(CA4, CA6 · bloqueia CT-12 · Sem a resposta não dá para julgar o acesso do anual cancelado; risco de pagar reembolso e manter acesso)_

**Outras dúvidas** (o requisito não diz; nenhum caso inventa a resposta):

- **D4.** Quem cancela em até 7 dias e recebe reembolso integral perde o acesso na hora ou continua até o fim do período? _(CA3, CA4 · Nenhum caso confere o acesso depois do reembolso integral; faltaria um caso quando o PO responder)_
- **D5.** O que acontece se o gateway de pagamento (reembolso) ou o serviço de e-mail estiver fora do ar ou lento na hora do cancelamento? O cancelamento é concluído e o reembolso/e-mail fica pendente para nova tentativa? _(CA3, CA6, CA7 · Sem caso de dependência externa até a resposta)_
- **D6.** O que Conta > Assinatura mostra para uma assinatura já cancelada (a opção Cancelar some?) e para um usuário sem assinatura? _(CA1 · CT-15 confere só que não há reembolso nem e-mail duplicados, não o que a tela mostra)_
- **D7.** Quais são os textos exatos da confirmação (botões além de "Tem certeza?"), da tela depois de cancelar e do e-mail? O e-mail informa o valor do reembolso e a data de fim do acesso? Em quanto tempo deve chegar? _(CA2, CA7 · CT-02, CT-03 e CT-13 conferem só a pergunta e a chegada do e-mail, não o conteúdo)_
- **D8.** Em quanto tempo o reembolso deve aparecer no gateway e por qual meio é devolvido (mesmo meio de pagamento?) _(CA3, CA6 · Casos de reembolso conferem só o registro no gateway)_

**Suposições** (usadas nos casos; se estiverem erradas, os casos indicados mudam):

- Mensal cancelado depois de 7 dias não tem reembolso (o texto só cita reembolso até 7 dias e no anual) _(CT-06)_
- Dia da contratação é o dia 0 e o limite é 7 dias corridos no mesmo horário da contratação _(CT-05)_
- Reembolso proporcional do anual: R$ 33,25 por mês, mês em andamento conta como usado _(CT-10, CT-11)_
- Depois do fim do período pago, o assinante cancelado perde o acesso ao catálogo _(CT-09)_
- O reembolso é feito e conferido no gateway de pagamento da Nexi _(CT-01, CT-04, CT-05, CT-06, CT-10, CT-11, CT-14, CT-15)_

## Critérios e cobertura

| Critério | Descrição | Casos | Dúvidas |
|---|---|---|---|
| CA1 _(derivado)_ | Assinante cancela pelo app a qualquer momento em Conta > Assinatura > Cancelar | CT-01, CT-15 | D6 |
| CA2 _(derivado)_ | Antes de cancelar, o app pede confirmação ("Tem certeza?") | CT-02, CT-03, CT-14 | D7 |
| CA3 _(derivado)_ | Cancelamento em até 7 dias da contratação tem reembolso integral (CDC) | CT-01, CT-04, CT-05, CT-06, CT-11, CT-14, CT-15 | D1, D4, D5, D8 |
| CA4 _(derivado)_ | Cancelamento depois de 7 dias mantém o acesso até o fim do período já pago | CT-06, CT-07, CT-09, CT-12 | D3, D4 |
| CA5 _(derivado)_ | Cancelamento depois de 7 dias não gera nova cobrança | CT-08 | — |
| CA6 _(derivado)_ | Plano anual cancelado depois de 7 dias tem reembolso proporcional aos meses não usados | CT-10, CT-11, CT-12 | D2, D3, D5, D8 |
| CA7 _(derivado)_ | Um e-mail confirmando o cancelamento é enviado ao assinante | CT-03, CT-13, CT-15 | D5, D7 |

## Casos

### CT-01 · Mensal cancelado 3 dias após a contratação recebe reembolso integral de R$ 39,90

**Critérios:** CA1, CA3 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

> Depende de Suposição: O reembolso é feito e conferido no gateway de pagamento da Nexi

**Pré-condições:**
- Usuário qa.cancel01@nexi.test logado no app
- Plano Mensal R$ 39,90 contratado há 3 dias (ajustar data de contratação no banco do ambiente de teste)

**Dados:**
- `usuário`: qa.cancel01@nexi.test
- `plano`: Mensal R$ 39,90
- `contratado há`: 3 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar na pergunta "Tem certeza?"

**Resultado esperado:** Reembolso de R$ 39,90 registrado no gateway de pagamento para a cobrança da contratação e assinatura com status cancelada no banco

### CT-02 · Clicar em Cancelar mostra "Tem certeza?" antes de cancelar

**Critérios:** CA2 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.cancel02@nexi.test logado com plano Mensal R$ 39,90 ativo, contratado há 15 dias

**Dados:**
- `usuário`: qa.cancel02@nexi.test
- `plano`: Mensal R$ 39,90

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Sem responder à pergunta, consultar o status da assinatura no banco

**Resultado esperado:** Aparece a pergunta "Tem certeza?" e, enquanto não há resposta, a assinatura continua com status ativa no banco

### CT-03 · Desistir na pergunta "Tem certeza?" não cancela a assinatura

**Critérios:** CA2, CA7 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.cancel03@nexi.test logado com plano Mensal R$ 39,90 ativo, contratado há 3 dias

**Dados:**
- `usuário`: qa.cancel03@nexi.test
- `plano`: Mensal R$ 39,90
- `contratado há`: 3 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Recusar a pergunta "Tem certeza?" (opção de não confirmar)

**Resultado esperado:** Assinatura continua com status ativa no banco, nenhum reembolso registrado no gateway e nenhum e-mail de cancelamento chega em qa.cancel03@nexi.test

### CT-04 · Anual cancelado 3 dias após a contratação recebe reembolso integral de R$ 399,00

**Critérios:** CA3 · **Tipo:** positivo · **Técnica:** tabela de decisão · **Prioridade:** Média

> Depende de Suposição: O reembolso é feito e conferido no gateway de pagamento da Nexi

**Pré-condições:**
- Usuário qa.cancel04@nexi.test logado no app
- Plano Anual R$ 399,00 contratado há 3 dias (ajustar data de contratação no banco)

**Dados:**
- `usuário`: qa.cancel04@nexi.test
- `plano`: Anual R$ 399,00
- `contratado há`: 3 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar na pergunta "Tem certeza?"

**Resultado esperado:** Reembolso de R$ 399,00 registrado no gateway de pagamento e assinatura com status cancelada no banco

### CT-05 · Mensal cancelado exatamente 7 dias após a contratação recebe reembolso integral (ver D1)

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

> Depende de D1 (bloqueia)

> Depende de Suposição: Dia da contratação é o dia 0 e o limite é 7 dias corridos no mesmo horário da contratação

> Depende de Suposição: O reembolso é feito e conferido no gateway de pagamento da Nexi

**Pré-condições:**
- Usuário qa.cancel05@nexi.test logado no app
- Plano Mensal R$ 39,90 contratado exatamente 7 dias corridos antes do teste, mesmo horário (ajustar data no banco)

**Dados:**
- `usuário`: qa.cancel05@nexi.test
- `plano`: Mensal R$ 39,90
- `contratado há`: 7 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar na pergunta "Tem certeza?"

**Resultado esperado:** Reembolso de R$ 39,90 registrado no gateway de pagamento

### CT-06 · Mensal cancelado 8 dias após a contratação não recebe reembolso integral

**Critérios:** CA3, CA4 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

> Depende de Suposição: Mensal cancelado depois de 7 dias não tem reembolso (o texto só cita reembolso até 7 dias e no anual)

> Depende de Suposição: O reembolso é feito e conferido no gateway de pagamento da Nexi

**Pré-condições:**
- Usuário qa.cancel06@nexi.test logado no app
- Plano Mensal R$ 39,90 contratado há 8 dias (ajustar data no banco)

**Dados:**
- `usuário`: qa.cancel06@nexi.test
- `plano`: Mensal R$ 39,90
- `contratado há`: 8 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar na pergunta "Tem certeza?"

**Resultado esperado:** Nenhum reembolso registrado no gateway para a cobrança de R$ 39,90 e assinatura com status cancelada no banco

### CT-07 · Mensal cancelado no 15º dia continua com acesso até o fim do período pago

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Alta

**Pré-condições:**
- Usuário qa.cancel07@nexi.test logado no app
- Plano Mensal R$ 39,90 contratado há 15 dias; período pago termina em 15 dias

**Dados:**
- `usuário`: qa.cancel07@nexi.test
- `plano`: Mensal R$ 39,90
- `contratado há`: 15 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar na pergunta "Tem certeza?"
4. Voltar ao catálogo e abrir um título qualquer

**Resultado esperado:** O título começa a tocar, sem tela pedindo assinatura, mesmo com a assinatura com status cancelada no banco

### CT-08 · Mensal cancelado depois de 7 dias não é cobrado na data de renovação

**Critérios:** CA5 · **Tipo:** negativo · **Técnica:** transição de estado · **Prioridade:** Alta

**Pré-condições:**
- Assinatura Mensal R$ 39,90 de qa.cancel08@nexi.test cancelada no 15º dia após a contratação
- Relógio do ambiente avançado para 1 dia depois da data de renovação e rotina de cobrança recorrente executada

**Dados:**
- `usuário`: qa.cancel08@nexi.test
- `plano`: Mensal R$ 39,90

**Passos:**
1. Consultar as cobranças de qa.cancel08@nexi.test no gateway de pagamento
2. Consultar as cobranças da assinatura no banco

**Resultado esperado:** Nenhuma nova cobrança de R$ 39,90 no gateway nem no banco além da cobrança da contratação

### CT-09 · Depois do fim do período pago, o assinante cancelado não acessa o catálogo

**Critérios:** CA4 · **Tipo:** borda · **Técnica:** transição de estado · **Prioridade:** Média

> Depende de Suposição: Depois do fim do período pago, o assinante cancelado perde o acesso ao catálogo

**Pré-condições:**
- Assinatura Mensal R$ 39,90 de qa.cancel09@nexi.test cancelada no 15º dia após a contratação
- Relógio do ambiente avançado para 1 minuto depois do fim do período pago

**Dados:**
- `usuário`: qa.cancel09@nexi.test
- `plano`: Mensal R$ 39,90

**Passos:**
1. Entrar no app com qa.cancel09@nexi.test
2. Abrir um título do catálogo

**Resultado esperado:** O título não começa a tocar

### CT-10 · Anual cancelado com 3 meses e 15 dias recebe reembolso proporcional de R$ 266,00 (ver D2)

**Critérios:** CA6 · **Tipo:** positivo · **Técnica:** tabela de decisão · **Prioridade:** Alta

> Depende de D2 (bloqueia)

> Depende de Suposição: Reembolso proporcional do anual: R$ 33,25 por mês, mês em andamento conta como usado

> Depende de Suposição: O reembolso é feito e conferido no gateway de pagamento da Nexi

**Pré-condições:**
- Usuário qa.cancel10@nexi.test logado no app
- Plano Anual R$ 399,00 contratado há 3 meses e 15 dias (ajustar data no banco)

**Dados:**
- `usuário`: qa.cancel10@nexi.test
- `plano`: Anual R$ 399,00
- `contratado há`: 3 meses e 15 dias
- `conta`: R$ 399,00 / 12 = R$ 33,25 por mês; 4 meses usados (3 + o mês em andamento); 8 não usados × R$ 33,25 = R$ 266,00

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar na pergunta "Tem certeza?"

**Resultado esperado:** Reembolso de R$ 266,00 registrado no gateway de pagamento

### CT-11 · Anual cancelado 8 dias após a contratação recebe reembolso proporcional de R$ 365,75 (ver D2)

**Critérios:** CA3, CA6 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D2 (bloqueia)

> Depende de Suposição: Reembolso proporcional do anual: R$ 33,25 por mês, mês em andamento conta como usado

> Depende de Suposição: O reembolso é feito e conferido no gateway de pagamento da Nexi

**Pré-condições:**
- Usuário qa.cancel11@nexi.test logado no app
- Plano Anual R$ 399,00 contratado há 8 dias (ajustar data no banco)

**Dados:**
- `usuário`: qa.cancel11@nexi.test
- `plano`: Anual R$ 399,00
- `contratado há`: 8 dias
- `conta`: 1 mês usado (o mês em andamento); 11 não usados × R$ 33,25 = R$ 365,75

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar na pergunta "Tem certeza?"

**Resultado esperado:** Reembolso de R$ 365,75 registrado no gateway de pagamento, e não de R$ 399,00

### CT-12 · Anual cancelado depois de 7 dias: acesso após o reembolso proporcional (ver D3)

**Critérios:** CA4, CA6 · **Tipo:** positivo · **Técnica:** tabela de decisão · **Prioridade:** Média

> Depende de D3 (bloqueia)

**Pré-condições:**
- Assinatura Anual R$ 399,00 de qa.cancel12@nexi.test cancelada com 3 meses e 15 dias e reembolso proporcional registrado
- Relógio do ambiente avançado para 1 dia depois do fim do 4º mês

**Dados:**
- `usuário`: qa.cancel12@nexi.test
- `plano`: Anual R$ 399,00

**Passos:**
1. Entrar no app com qa.cancel12@nexi.test
2. Abrir um título do catálogo

**Resultado esperado:** Resultado depende da resposta de D3. Já certo: nenhuma nova cobrança de R$ 399,00 registrada no gateway

### CT-13 · Cancelamento confirmado envia e-mail de confirmação ao assinante

**Critérios:** CA7 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.cancel13@nexi.test logado com plano Mensal R$ 39,90 ativo, contratado há 15 dias
- Caixa de qa.cancel13@nexi.test vazia

**Dados:**
- `usuário`: qa.cancel13@nexi.test
- `plano`: Mensal R$ 39,90

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Confirmar na pergunta "Tem certeza?"
4. Abrir a caixa de qa.cancel13@nexi.test

**Resultado esperado:** Chega exatamente 1 e-mail confirmando o cancelamento da assinatura em qa.cancel13@nexi.test

### CT-14 · Toque duplo em confirmar registra um único reembolso de R$ 39,90

**Critérios:** CA2, CA3 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Alta

> Depende de Suposição: O reembolso é feito e conferido no gateway de pagamento da Nexi

**Pré-condições:**
- Usuário qa.cancel14@nexi.test logado com plano Mensal R$ 39,90 contratado há 3 dias

**Dados:**
- `usuário`: qa.cancel14@nexi.test
- `plano`: Mensal R$ 39,90
- `contratado há`: 3 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Cancelar
3. Tocar duas vezes seguidas no botão que confirma a pergunta "Tem certeza?"
4. Consultar os reembolsos no gateway e os e-mails em qa.cancel14@nexi.test

**Resultado esperado:** Exatamente 1 reembolso de R$ 39,90 registrado no gateway (total reembolsado R$ 39,90) e exatamente 1 e-mail de cancelamento recebido

### CT-15 · Assinatura já cancelada não gera segundo reembolso nem segundo e-mail (ver D6)

**Critérios:** CA1, CA3, CA7 · **Tipo:** negativo · **Técnica:** transição de estado · **Prioridade:** Média

> Depende de Suposição: O reembolso é feito e conferido no gateway de pagamento da Nexi

**Pré-condições:**
- Assinatura Mensal R$ 39,90 de qa.cancel15@nexi.test cancelada há 1 dia, contratada há 4 dias, com reembolso de R$ 39,90 já registrado

**Dados:**
- `usuário`: qa.cancel15@nexi.test
- `plano`: Mensal R$ 39,90

**Passos:**
1. Acessar Conta > Assinatura
2. Se a opção Cancelar aparecer, clicar nela e confirmar "Tem certeza?"
3. Consultar os reembolsos no gateway e os e-mails em qa.cancel15@nexi.test

**Resultado esperado:** Continua existindo só 1 reembolso de R$ 39,90 no gateway e só 1 e-mail de cancelamento na caixa

## Fora do escopo

- Reativar assinatura cancelada
- Cancelamento pelo site, pelo suporte ou por inadimplência
- Troca de plano (mensal para anual e vice-versa)
- Período de teste grátis e cupons
- Layout do e-mail de confirmação
