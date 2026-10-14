# Casos de teste: Pausar assinatura

**Origem:** HIST-430 · Pausar assinatura (D-pausar-assinatura.md) · **Gerado em:** 14/10/2026

**19 casos:** 7 positivos, 5 negativos, 7 de borda · **Prioridade:** 6 Alta, 13 Média, 0 Baixa

## Pontos a confirmar com o PO

**Dúvidas que bloqueiam a execução** (responder primeiro):

- **D1.** CA1 x CA2 se contradizem: CA1 oferece pausa de 90 dias e CA2 diz que a pausa máxima é de 2 meses. A opção de 90 dias existe? Se o máximo é 2 meses, 60 dias conta como 2 meses mesmo quando os 2 meses do calendário têm 59 dias (ex.: pausa iniciada em 01/02)? _(CA1, CA2 · bloqueia CT-03 · Sem a resposta não dá para julgar a pausa de 90 dias; CT-02 (60 dias) segue porque vale nos dois trechos)_
- **D2.** Os 12 meses do CA3 contam a partir do início ou do fim da pausa anterior? Exatamente 12 meses depois já pode pausar? Uma pausa retomada antes do fim (CA6) conta como a pausa do período? _(CA3 · bloqueia CT-06 · Muda a data do caso de limite. CT-05 e CT-07 seguem, porque são recusados em qualquer das contagens)_
- **D3.** Quando a pausa começa: no dia da confirmação ou no fim do ciclo já pago? O que acontece com os dias já pagos do ciclo atual? E como contam os 30 dias (dia da confirmação é o dia 0 ou o dia 1)? _(CA4, CA5 · bloqueia CT-14 · Define a data de fim da pausa e da cobrança. Os outros casos partem de 'pausa em vigor' e da data de fim registrada no banco para não depender disso)_

**Outras dúvidas** (o requisito não diz; nenhum caso inventa a resposta):

- **D4.** Como o assinante fica sabendo que não pode pausar (Pausar some, fica desabilitado ou mostra mensagem)? E qual mensagem aparece ao tentar assistir durante a pausa? _(CA3, CA4 · CT-05, CT-07 e CT-09 conferem só que a pausa não é criada e o vídeo não toca, não a tela nem a mensagem)_
- **D5.** Se o aparelho estiver offline quando a pausa começa, os downloads continuam assistíveis até ele reconectar? Quando são apagados? _(CA4 · CT-10 cobre só o aparelho online; o offline fica sem caso até a resposta)_
- **D6.** Depois da cobrança no fim da pausa ou na retomada, a data de renovação mensal passa a ser esse dia? E se o cartão for recusado nessa cobrança, a assinatura volta mesmo assim? _(CA5, CA6 · Sem caso para renovação seguinte e cartão recusado até a resposta)_
- **D7.** Quem pode pausar além do Mensal ativo em dia: assinatura em atraso, em teste grátis ou com cancelamento agendado? _(CA1 · Partições não cobertas; os casos usam só assinatura Mensal ativa e em dia)_

**Suposições** (usadas nos casos; se estiverem erradas, os casos indicados mudam):

- A cobrança no fim da pausa e na retomada é do valor cheio do plano Mensal (R$ 39,90), sem proporcional _(CT-13, CT-14, CT-15, CT-17, CT-18)_
- Pausa e retomada valem na hora em que o usuário confirma (sem etapa de aprovação) _(CT-01, CT-02, CT-10, CT-15, CT-16)_

## Critérios e cobertura

| Critério | Descrição | Casos | Dúvidas |
|---|---|---|---|
| CA1 | Assinante do plano Mensal pode pausar por 30, 60 ou 90 dias em Conta > Assinatura > Pausar | CT-01, CT-02, CT-03, CT-04 | D1, D7 |
| CA2 | A pausa máxima é de 2 meses | CT-02, CT-03 | D1 |
| CA3 | Só é possível pausar uma vez a cada 12 meses | CT-05, CT-06, CT-07 | D2, D4 |
| CA4 | Durante a pausa não há cobrança, o assinante não consegue assistir e os downloads offline são apagados do aparelho | CT-08, CT-09, CT-10 | D3, D4, D5 |
| CA5 | No fim da pausa a assinatura volta sozinha e a cobrança acontece no dia em que a pausa termina | CT-11, CT-12, CT-13, CT-14, CT-18 | D3, D6 |
| CA6 | O assinante pode retomar antes do fim em Conta > Assinatura > Retomar; a cobrança acontece no dia da retomada | CT-15, CT-16, CT-17, CT-18 | D6 |
| CA7 | Plano Anual não pode pausar: o botão Pausar não aparece | CT-19 | — |

## Casos

### CT-01 · Assinante Mensal pausa por 30 dias

**Critérios:** CA1 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

> Depende de Suposição: Pausa e retomada valem na hora em que o usuário confirma (sem etapa de aprovação)

**Pré-condições:**
- Usuário mensal.pausa01@teste.nexi logado, plano Mensal R$ 39,90 ativo há 3 meses, nunca pausou

**Dados:**
- `plano`: Mensal R$ 39,90
- `duração`: 30 dias

**Passos:**
1. Acessar Conta > Assinatura > Pausar
2. Selecionar 30 dias
3. Confirmar a pausa

**Resultado esperado:** No banco, a assinatura tem uma pausa de 30 dias registrada; nenhuma cobrança é feita no ato; Conta > Assinatura passa a mostrar a opção Retomar

### CT-02 · Pausa de 60 dias (limite de 2 meses) é aceita

**Critérios:** CA1, CA2 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de Suposição: Pausa e retomada valem na hora em que o usuário confirma (sem etapa de aprovação)

**Pré-condições:**
- Usuário mensal.pausa02@teste.nexi logado, plano Mensal R$ 39,90 ativo há 3 meses, nunca pausou

**Dados:**
- `plano`: Mensal R$ 39,90
- `duração`: 60 dias

**Passos:**
1. Acessar Conta > Assinatura > Pausar
2. Selecionar 60 dias
3. Confirmar a pausa

**Resultado esperado:** No banco, a assinatura tem uma pausa de 60 dias registrada; nenhuma cobrança é feita no ato

### CT-03 · Opção de 90 dias em Pausar (contradição CA1 x CA2, ver dúvida 1)

**Critérios:** CA1, CA2 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D1 (bloqueia)

**Pré-condições:**
- Usuário mensal.pausa03@teste.nexi logado, plano Mensal R$ 39,90 ativo há 3 meses, nunca pausou
- Bloqueado até o PO responder a dúvida 1

**Dados:**
- `plano`: Mensal R$ 39,90
- `duração`: 90 dias

**Passos:**
1. Acessar Conta > Assinatura > Pausar
2. Conferir as opções de duração oferecidas
3. Se a opção 90 dias existir, selecioná-la e confirmar

**Resultado esperado:** A tela Pausar oferece 30 e 60 dias; a opção de 90 dias e a pausa registrada no banco batem com a regra definida pelo PO na dúvida 1

### CT-04 · Desistir no meio da pausa não pausa a assinatura

**Critérios:** CA1 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Média

**Pré-condições:**
- Usuário mensal.pausa04@teste.nexi logado, plano Mensal R$ 39,90 ativo, próxima cobrança agendada para daqui a 10 dias, nunca pausou

**Dados:**
- `duração`: 30 dias

**Passos:**
1. Acessar Conta > Assinatura > Pausar
2. Selecionar 30 dias
3. Fechar a tela sem confirmar

**Resultado esperado:** No banco não há pausa registrada; a próxima cobrança continua agendada para a mesma data; a opção Pausar continua disponível em Conta > Assinatura

### CT-05 · Segunda pausa 6 meses depois da primeira é recusada

**Critérios:** CA3 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Usuário mensal.pausa05@teste.nexi, plano Mensal ativo
- Pausa de 30 dias iniciada há 6 meses e já encerrada (ajustar datas no banco)

**Dados:**
- `duração tentada`: 30 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Tentar pausar por 30 dias

**Resultado esperado:** Nenhuma nova pausa é registrada no banco; a assinatura continua ativa e a próxima cobrança mantém a mesma data

### CT-06 · Pausa exatamente 12 meses depois da anterior é aceita (ver dúvida 2)

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D2 (bloqueia)

**Pré-condições:**
- Usuário mensal.pausa06@teste.nexi, plano Mensal ativo
- Pausa anterior de 30 dias iniciada em 14/10/2025 e encerrada em 13/11/2025 (ajustar no banco); data do ambiente: 14/10/2026
- Bloqueado até o PO responder a dúvida 2

**Dados:**
- `pausa anterior`: 14/10/2025 a 13/11/2025
- `nova pausa`: 30 dias em 14/10/2026

**Passos:**
1. Acessar Conta > Assinatura > Pausar
2. Selecionar 30 dias
3. Confirmar a pausa

**Resultado esperado:** No banco, uma nova pausa de 30 dias é registrada com início em 14/10/2026

### CT-07 · Pausa 1 dia antes de completar 12 meses da anterior é recusada

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

**Pré-condições:**
- Usuário mensal.pausa07@teste.nexi, plano Mensal ativo
- Pausa anterior de 30 dias iniciada em 15/10/2025 e encerrada (ajustar no banco); data do ambiente: 14/10/2026

**Dados:**
- `pausa anterior`: início 15/10/2025
- `tentativa`: 30 dias em 14/10/2026

**Passos:**
1. Acessar Conta > Assinatura
2. Tentar pausar por 30 dias

**Resultado esperado:** Nenhuma nova pausa é registrada no banco; a assinatura continua ativa e a próxima cobrança mantém a mesma data

### CT-08 · Data de renovação durante a pausa não gera cobrança

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Alta

**Pré-condições:**
- Usuário mensal.pausa08@teste.nexi, plano Mensal R$ 39,90, cartão de teste cadastrado
- Pausa de 60 dias em vigor; a data de renovação mensal que existia antes da pausa cai dentro do período pausado

**Passos:**
1. Avançar o relógio do ambiente para a data de renovação antiga
2. Rodar o processamento de cobranças do dia
3. Consultar as cobranças do usuário no gateway de pagamento e no banco

**Resultado esperado:** Nenhuma cobrança de R$ 39,90 é criada na data de renovação antiga

### CT-09 · Assinante pausado não consegue assistir

**Critérios:** CA4 · **Tipo:** negativo · **Técnica:** transição de estado · **Prioridade:** Média

**Pré-condições:**
- Usuário mensal.pausa09@teste.nexi logado no app web, plano Mensal
- Pausa de 30 dias em vigor

**Dados:**
- `estado da assinatura`: pausa em vigor (dia 10 de 30)

**Passos:**
1. Abrir um título do catálogo
2. Clicar em Assistir

**Resultado esperado:** O vídeo não começa a tocar (o player não exibe nenhum frame do conteúdo)

### CT-10 · Downloads offline são apagados do aparelho ao entrar em pausa

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Média

> Depende de Suposição: Pausa e retomada valem na hora em que o usuário confirma (sem etapa de aprovação)

**Pré-condições:**
- Usuário mensal.pausa10@teste.nexi logado no app Android, conectado à internet, plano Mensal ativo, nunca pausou
- 2 títulos baixados em Downloads (1 filme e 1 episódio)

**Passos:**
1. Pausar a assinatura por 30 dias em Conta > Assinatura > Pausar
2. Aguardar a pausa entrar em vigor com o aparelho online
3. Abrir Downloads no app

**Resultado esperado:** Downloads não lista nenhum dos 2 títulos e os arquivos não estão mais no armazenamento do aparelho

### CT-11 · Na véspera do fim da pausa não há cobrança

**Critérios:** CA5 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

**Pré-condições:**
- Usuário mensal.pausa11@teste.nexi, plano Mensal R$ 39,90
- Pausa de 30 dias em vigor; relógio do ambiente ajustado para 1 dia antes da data de fim registrada no banco

**Dados:**
- `data do ambiente`: data de fim da pausa - 1 dia

**Passos:**
1. Rodar o processamento de cobranças do dia
2. Consultar as cobranças do usuário no gateway e no banco

**Resultado esperado:** Nenhuma cobrança de R$ 39,90 é criada nesse dia e o banco ainda mostra a pausa em vigor

### CT-12 · No dia do fim da pausa o assinante volta a assistir sem retomar

**Critérios:** CA5 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Média

**Pré-condições:**
- Usuário mensal.pausa12@teste.nexi logado no app web, plano Mensal, cartão de teste válido
- Pausa de 30 dias em vigor; relógio do ambiente avançado para a data de fim registrada no banco e processamento do dia executado

**Dados:**
- `estado da assinatura`: data de fim da pausa

**Passos:**
1. Abrir um título do catálogo
2. Clicar em Assistir

**Resultado esperado:** O vídeo começa a tocar sem o usuário ter clicado em Retomar e o banco não mostra mais a pausa em vigor

### CT-13 · Fim da pausa gera cobrança de R$ 39,90 no mesmo dia

**Critérios:** CA5 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

> Depende de Suposição: A cobrança no fim da pausa e na retomada é do valor cheio do plano Mensal (R$ 39,90), sem proporcional

**Pré-condições:**
- Usuário mensal.pausa13@teste.nexi, plano Mensal R$ 39,90, cartão de teste válido
- Pausa de 30 dias em vigor; relógio do ambiente avançado para a data de fim registrada no banco

**Dados:**
- `data do ambiente`: data de fim da pausa

**Passos:**
1. Rodar o processamento de cobranças do dia
2. Consultar as cobranças do usuário no gateway e no banco

**Resultado esperado:** Existe exatamente 1 cobrança de R$ 39,90 com data igual à data de fim da pausa

### CT-14 · Pausa de 30 dias iniciada em 14/10/2026 termina em 13/11/2026 (ver dúvida 3)

**Critérios:** CA5 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D3 (bloqueia)

> Depende de Suposição: A cobrança no fim da pausa e na retomada é do valor cheio do plano Mensal (R$ 39,90), sem proporcional

**Pré-condições:**
- Usuário mensal.pausa14@teste.nexi logado, plano Mensal R$ 39,90 ativo, nunca pausou; data do ambiente: 14/10/2026
- Bloqueado até o PO responder a dúvida 3

**Dados:**
- `duração`: 30 dias
- `data da confirmação`: 14/10/2026

**Passos:**
1. Acessar Conta > Assinatura > Pausar
2. Selecionar 30 dias e confirmar
3. Consultar no banco as datas de início e fim da pausa e a data da próxima cobrança

**Resultado esperado:** Banco registra início em 14/10/2026, fim em 13/11/2026 e próxima cobrança de R$ 39,90 em 13/11/2026

### CT-15 · Retomar antes do fim gera cobrança de R$ 39,90 no dia da retomada

**Critérios:** CA6 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

> Depende de Suposição: A cobrança no fim da pausa e na retomada é do valor cheio do plano Mensal (R$ 39,90), sem proporcional

> Depende de Suposição: Pausa e retomada valem na hora em que o usuário confirma (sem etapa de aprovação)

**Pré-condições:**
- Usuário mensal.pausa15@teste.nexi logado, plano Mensal R$ 39,90, cartão de teste válido
- Pausa de 60 dias em vigor há 10 dias

**Passos:**
1. Acessar Conta > Assinatura > Retomar
2. Confirmar a retomada
3. Consultar as cobranças do usuário no gateway e no banco

**Resultado esperado:** Existe 1 cobrança de R$ 39,90 com a data de hoje e o banco não mostra mais a pausa em vigor

### CT-16 · Depois de retomar, o assinante volta a assistir na hora

**Critérios:** CA6 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Média

> Depende de Suposição: Pausa e retomada valem na hora em que o usuário confirma (sem etapa de aprovação)

**Pré-condições:**
- Usuário mensal.pausa16@teste.nexi logado no app web, plano Mensal, cartão de teste válido
- Pausa de 30 dias em vigor há 5 dias

**Passos:**
1. Acessar Conta > Assinatura > Retomar e confirmar
2. Abrir um título do catálogo
3. Clicar em Assistir

**Resultado esperado:** O vídeo começa a tocar

### CT-17 · Clique duplo em Retomar gera uma cobrança só

**Critérios:** CA6 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Alta

> Depende de Suposição: A cobrança no fim da pausa e na retomada é do valor cheio do plano Mensal (R$ 39,90), sem proporcional

**Pré-condições:**
- Usuário mensal.pausa17@teste.nexi logado, plano Mensal R$ 39,90, cartão de teste válido
- Pausa de 30 dias em vigor há 5 dias

**Passos:**
1. Acessar Conta > Assinatura > Retomar
2. Clicar duas vezes seguidas no botão de confirmar
3. Consultar as cobranças do usuário no gateway e no banco

**Resultado esperado:** Existe exatamente 1 cobrança de R$ 39,90 com a data de hoje

### CT-18 · Retomar na véspera do fim não gera segunda cobrança no dia do fim

**Critérios:** CA5, CA6 · **Tipo:** borda · **Técnica:** tabela de decisão · **Prioridade:** Alta

> Depende de Suposição: A cobrança no fim da pausa e na retomada é do valor cheio do plano Mensal (R$ 39,90), sem proporcional

**Pré-condições:**
- Usuário mensal.pausa18@teste.nexi logado, plano Mensal R$ 39,90, cartão de teste válido
- Pausa de 30 dias em vigor; relógio do ambiente ajustado para 1 dia antes da data de fim registrada no banco

**Passos:**
1. Acessar Conta > Assinatura > Retomar e confirmar
2. Avançar o relógio do ambiente 1 dia (data de fim original)
3. Rodar o processamento de cobranças do dia
4. Consultar as cobranças do usuário no gateway e no banco

**Resultado esperado:** Existe 1 cobrança de R$ 39,90 na data da retomada e nenhuma cobrança na data de fim original

### CT-19 · Assinante Anual não vê o botão Pausar

**Critérios:** CA7 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Usuário anual.pausa19@teste.nexi logado, plano Anual R$ 399,00 ativo há 2 meses, nunca pausou

**Passos:**
1. Acessar Conta > Assinatura

**Resultado esperado:** O botão Pausar não aparece na tela

## Fora do escopo

- Cancelar a assinatura ou trocar de plano durante a pausa
- E-mails e notificações de início e fim de pausa
- Baixar de novo os títulos depois da pausa
- Pausa feita pelo suporte ou por tela de administração
