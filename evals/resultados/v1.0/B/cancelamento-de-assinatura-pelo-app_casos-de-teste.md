# Casos de teste: Cancelamento de assinatura pelo app

**Origem:** Mensagem do PO no Slack (B-cancelamento-slack.txt), colada pelo usuário em 14/10/2026 · **Gerado em:** 14/10/2026

**15 casos:** 6 positivos, 2 negativos, 7 de borda · **Prioridade:** 7 Alta, 8 Média, 0 Baixa

## Pontos a confirmar com o PO

**Dúvidas** (o requisito não diz; nenhum caso inventa a resposta):

- **D1.** Como contar os 7 dias: o dia da contratação é o dia 0 ou o dia 1? Dias corridos ou 7 × 24 h a partir do horário da compra? Qual fuso? _(CA3, CA6 · Define a data limite de CT-04, CT-05, CT-06 e CT-07; hoje eles usam a suposição de dias corridos com contratação = dia 0)_
- **D2.** Plano mensal cancelado depois de 7 dias realmente não tem nenhum reembolso? O texto só fala de reembolso para o anual nesse caso _(CA3, CA6 · CT-05 assume que não há estorno)_
- **D3.** No proporcional do anual, o mês em andamento conta como usado? Ou o cálculo é por dia? Como arredondar centavos se for por dia? _(CA6 · CT-07, CT-08 e CT-09 assumem mês em andamento = usado. Se não contar, CT-08 seria 9 × R$ 33,25 = R$ 299,25 e CT-07 seria R$ 399,00)_
- **D4.** Quem cancela dentro dos 7 dias (com reembolso integral) perde o acesso na hora ou continua até o fim do período? _(CA3, CA4 · Nenhum caso confere o acesso depois do cancelamento com reembolso integral)_
- **D5.** Quem cancela o anual com reembolso proporcional continua com acesso até o fim do ano pago ou só até o fim do mês em andamento? Acesso até o fim do ano somado ao reembolso dos meses seria pagar duas vezes _(CA4, CA6 · Sem caso de acesso para o anual cancelado após 7 dias)_
- **D6.** Como o reembolso é feito (estorno no mesmo cartão, crédito, Pix) e em quanto tempo deve aparecer? _(CA3, CA6 · Os casos conferem o estorno no gateway de homologação, não o prazo nem a forma)_
- **D7.** Assinaturas compradas pela App Store ou Google Play: o cancelamento e o reembolso também passam por Conta > Assinatura > Cancelar no nosso app? _(CA1 · Todos os casos assumem pagamento direto com cartão no gateway da Nexi)_
- **D8.** Qual o texto completo do diálogo e o nome dos botões (confirmar / desistir)? Só "Tem certeza?" está definido _(CA2 · CT-02 e CT-03 conferem só o texto "Tem certeza?")_
- **D9.** O que o e-mail de confirmação deve conter (valor do reembolso, data fim do acesso, assunto, remetente)? Em quanto tempo deve chegar? _(CA7 · CT-14 confere só que 1 e-mail chegou)_
- **D10.** O que o app mostra depois de cancelar (mensagem de sucesso, data fim do acesso em Conta > Assinatura) e para uma assinatura já cancelada o botão Cancelar continua aparecendo? _(CA1, CA4 · Nenhum caso confere mensagens na tela; não há caso de cancelar duas vezes a mesma assinatura)_
- **D11.** O que o usuário vê ao tentar assistir depois do fim do período pago (tela de assinar de novo, mensagem)? _(CA4 · CT-11 confere só que o título não reproduz)_

**Suposições** (usadas nos casos; se estiverem erradas, os casos indicados mudam):

- Os 7 dias são corridos e o dia da contratação é o dia 0 (contratado em 01/10, o 7º dia é 08/10) _(CT-04, CT-05, CT-06, CT-07)_
- Plano mensal cancelado depois de 7 dias não tem reembolso (o texto só fala de reembolso proporcional para o anual) _(CT-05)_
- No proporcional do anual, o mês em andamento conta como usado; valor mensal = R$ 399,00 / 12 = R$ 33,25 _(CT-07, CT-08, CT-09)_
- Ao fim do período pago o acesso ao conteúdo termina _(CT-11)_
- Pagamento direto com cartão no gateway da Nexi, conferível no painel de homologação _(CT-01, CT-04, CT-05, CT-06, CT-07, CT-08, CT-09, CT-12, CT-13, CT-15)_

## Critérios e cobertura

| Critério | Descrição | Casos | Dúvidas |
|---|---|---|---|
| CA1 _(derivado)_ | Assinante cancela pelo app a qualquer momento em Conta > Assinatura > Cancelar | CT-01, CT-03, CT-08, CT-15 | D7, D10 |
| CA2 _(derivado)_ | Antes de cancelar, o app pede confirmação com "Tem certeza?" | CT-02, CT-03 | D8 |
| CA3 _(derivado)_ | Cancelamento em até 7 dias da contratação tem reembolso integral (CDC), em qualquer plano | CT-01, CT-04, CT-05, CT-06, CT-15 | D1, D2, D4, D6 |
| CA4 _(derivado)_ | Cancelado depois de 7 dias, o assinante mantém acesso até o fim do período já pago | CT-10, CT-11 | D4, D5, D10, D11 |
| CA5 _(derivado)_ | Cancelado depois de 7 dias, o assinante não é cobrado de novo | CT-12, CT-13 | — |
| CA6 _(derivado)_ | Plano anual cancelado depois de 7 dias tem reembolso proporcional aos meses não usados (R$ 399,00 / 12 = R$ 33,25 por mês) | CT-07, CT-08, CT-09 | D1, D2, D3, D5, D6 |
| CA7 _(derivado)_ | Um e-mail confirmando o cancelamento é enviado ao assinante | CT-03, CT-14 | D9 |

## Casos

### CT-01 · Mensal cancelado no 3º dia recebe reembolso integral de R$ 39,90

**Critérios:** CA1, CA3 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

**Pré-condições:**
- Usuário qa.mensal01@nexiteste.com logado no app
- Plano Mensal R$ 39,90 contratado há 3 dias com o cartão de teste final 1111

**Dados:**
- `usuário`: qa.mensal01@nexiteste.com
- `plano`: Mensal R$ 39,90
- `dias desde a contratação`: 3

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Consultar as transações do cartão final 1111 no painel do gateway de homologação

**Resultado esperado:** Conta > Assinatura mostra a assinatura como cancelada; o gateway registra um estorno de R$ 39,90 para a cobrança da contratação

### CT-02 · Tocar em Cancelar abre o diálogo "Tem certeza?" sem cancelar ainda

**Critérios:** CA2 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.mensal02@nexiteste.com logado com plano Mensal R$ 39,90 ativo há 15 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Observar a tela sem responder ao diálogo

**Resultado esperado:** Aparece o diálogo com o texto "Tem certeza?"; enquanto ele está aberto, nenhum estorno é registrado no gateway e o status no banco continua ativo

### CT-03 · Desistir no diálogo "Tem certeza?" mantém a assinatura ativa

**Critérios:** CA1, CA2, CA7 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Alta

**Pré-condições:**
- Usuário qa.mensal03@nexiteste.com logado com plano Mensal R$ 39,90 ativo há 3 dias
- Nome do botão de desistir não definido (ver dúvida sobre o diálogo)

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. No diálogo "Tem certeza?", escolher a opção de não cancelar
4. Consultar o gateway de homologação e a caixa de qa.mensal03@nexiteste.com

**Resultado esperado:** Conta > Assinatura continua mostrando o plano Mensal ativo; nenhum estorno no gateway; nenhum e-mail de cancelamento recebido

### CT-04 · Mensal cancelado no 7º dia ainda recebe reembolso integral de R$ 39,90

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

**Pré-condições:**
- Usuário qa.mensal04@nexiteste.com com plano Mensal R$ 39,90 contratado em 01/10/2026
- Relógio do ambiente ajustado para 08/10/2026 (7 dias corridos após a contratação; ver suposição de contagem)

**Dados:**
- `contratação`: 01/10/2026
- `data do cancelamento`: 08/10/2026

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Consultar o gateway de homologação

**Resultado esperado:** O gateway registra um estorno de R$ 39,90

### CT-05 · Mensal cancelado no 8º dia não recebe reembolso

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

**Pré-condições:**
- Usuário qa.mensal05@nexiteste.com com plano Mensal R$ 39,90 contratado em 01/10/2026
- Relógio do ambiente ajustado para 09/10/2026 (8 dias corridos após a contratação)
- Depende da suposição de que mensal após 7 dias não tem reembolso

**Dados:**
- `contratação`: 01/10/2026
- `data do cancelamento`: 09/10/2026

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Consultar o gateway de homologação

**Resultado esperado:** Nenhum estorno é registrado no gateway para a cobrança de R$ 39,90

### CT-06 · Anual cancelado no 7º dia recebe reembolso integral de R$ 399,00

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** tabela de decisão · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.anual01@nexiteste.com com plano Anual R$ 399,00 contratado em 01/10/2026
- Relógio do ambiente ajustado para 08/10/2026

**Dados:**
- `plano`: Anual R$ 399,00
- `contratação`: 01/10/2026
- `data do cancelamento`: 08/10/2026

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Consultar o gateway de homologação

**Resultado esperado:** O gateway registra um estorno de R$ 399,00 (integral, e não proporcional)

### CT-07 · Anual cancelado no 8º dia recebe reembolso proporcional de R$ 365,75

**Critérios:** CA6 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

**Pré-condições:**
- Usuário qa.anual02@nexiteste.com com plano Anual R$ 399,00 contratado em 01/10/2026
- Relógio do ambiente ajustado para 09/10/2026 (1º mês em andamento)
- Depende da suposição de que o mês em andamento conta como usado

**Dados:**
- `meses não usados`: 11
- `conta`: 11 × R$ 33,25 = R$ 365,75

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Consultar o gateway de homologação

**Resultado esperado:** O gateway registra um estorno de R$ 365,75 (e não de R$ 399,00)

### CT-08 · Anual cancelado no 4º mês recebe reembolso proporcional de R$ 266,00

**Critérios:** CA1, CA6 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

**Pré-condições:**
- Usuário qa.anual03@nexiteste.com com plano Anual R$ 399,00 contratado em 01/07/2026
- Data do teste: 14/10/2026 (4º mês em andamento; 3 meses completos)
- Depende da suposição de que o mês em andamento conta como usado

**Dados:**
- `meses usados`: 4 (3 completos + o mês em andamento)
- `meses não usados`: 8
- `conta`: 8 × R$ 33,25 = R$ 266,00

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Consultar o gateway de homologação

**Resultado esperado:** O gateway registra um estorno de R$ 266,00

### CT-09 · Anual cancelado no 12º mês fica sem reembolso proporcional

**Critérios:** CA6 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.anual04@nexiteste.com com plano Anual R$ 399,00 contratado em 01/11/2025
- Data do teste: 14/10/2026 (12º mês em andamento)
- Depende da suposição de que o mês em andamento conta como usado

**Dados:**
- `meses não usados`: 0
- `conta`: 0 × R$ 33,25 = R$ 0,00

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Consultar o gateway de homologação

**Resultado esperado:** Nenhum estorno é registrado no gateway (nem estorno de R$ 0,00)

### CT-10 · Mensal cancelado no 15º dia continua assistindo até o fim do período pago

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.mensal06@nexiteste.com com plano Mensal R$ 39,90 contratado em 29/09/2026 (período pago até 29/10/2026)
- Data do teste: 14/10/2026

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Voltar ao catálogo e dar play em um título

**Resultado esperado:** O título reproduz normalmente depois do cancelamento

### CT-11 · Acesso termina depois da data fim do período pago

**Critérios:** CA4 · **Tipo:** borda · **Técnica:** transição de estado · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.mensal06@nexiteste.com de CT-10 (cancelado em 14/10/2026, período pago até 29/10/2026)
- Relógio do ambiente avançado para 30/10/2026
- Depende da suposição de que o acesso termina no fim do período pago; tela exibida não definida

**Passos:**
1. Abrir o app
2. Dar play no mesmo título de CT-10

**Resultado esperado:** O título não reproduz

### CT-12 · Mensal cancelado após 7 dias não é cobrado na data de renovação

**Critérios:** CA5 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Alta

**Pré-condições:**
- Usuário qa.mensal06@nexiteste.com de CT-10 (cancelado em 14/10/2026, renovação seria em 29/10/2026)
- Relógio do ambiente avançado para 29/10/2026 e job de renovação executado

**Passos:**
1. Consultar as transações do cartão final 1111 no gateway de homologação

**Resultado esperado:** Nenhuma cobrança de R$ 39,90 é registrada em 29/10/2026

### CT-13 · Anual cancelado após 7 dias não é cobrado na renovação anual

**Critérios:** CA5 · **Tipo:** positivo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.anual03@nexiteste.com de CT-08 (contratado em 01/07/2026, cancelado em 14/10/2026)
- Relógio do ambiente avançado para 01/07/2027 e job de renovação executado

**Passos:**
1. Consultar as transações do cartão do usuário no gateway de homologação

**Resultado esperado:** Nenhuma cobrança de R$ 399,00 é registrada em 01/07/2027

### CT-14 · E-mail de confirmação chega após cancelar

**Critérios:** CA7 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.mensal07@nexiteste.com logado com plano Mensal R$ 39,90 ativo há 15 dias
- Caixa de e-mail de teste acessível (ex.: Mailtrap do ambiente)

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. Confirmar no diálogo "Tem certeza?"
4. Abrir a caixa de qa.mensal07@nexiteste.com

**Resultado esperado:** Exatamente 1 e-mail de confirmação de cancelamento é recebido em qa.mensal07@nexiteste.com

### CT-15 · Toque duplo em Confirmar gera um único reembolso

**Critérios:** CA1, CA3 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.mensal08@nexiteste.com com plano Mensal R$ 39,90 contratado há 2 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Tocar em Cancelar
3. No diálogo "Tem certeza?", tocar duas vezes rapidamente em confirmar
4. Consultar o gateway de homologação

**Resultado esperado:** O gateway registra exatamente 1 estorno de R$ 39,90 (total estornado R$ 39,90)

## Fora do escopo

- Cancelamento pela web ou pelo suporte/administração
- Reativar uma assinatura cancelada
- Troca de plano (mensal para anual e vice-versa)
- Período de teste grátis e assinaturas com cupom de desconto
- Assinaturas compradas pela App Store / Google Play (até a resposta do PO)
