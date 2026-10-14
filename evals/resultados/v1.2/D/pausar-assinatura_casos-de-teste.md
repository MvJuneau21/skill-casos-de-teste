# Casos de teste: Pausar assinatura

**Origem:** HIST-430 · Pausar assinatura (arquivo D-pausar-assinatura.md) · **Gerado em:** 14/10/2026

**21 casos:** 7 positivos, 6 negativos, 8 de borda · **Prioridade:** 4 Alta, 17 Média, 0 Baixa

## Pontos a confirmar com o PO

**Dúvidas que bloqueiam a execução** (responder primeiro):

- **D1.** CA1 oferece pausa de 30, 60 ou 90 dias, mas CA2 diz que a pausa máxima é de 2 meses. Qual vale: a opção de 90 dias sai da tela ou o máximo passa a ser 3 meses? E 60 dias conta como dentro de 2 meses mesmo quando os 2 meses têm 59 dias (ex.: início em 01/01)? _(CA1, CA2 · bloqueia CT-03 · Sem a resposta não dá para julgar a tela de opções nem a pausa de 90 dias)_
- **D2.** Quando a pausa começa: na confirmação ou no fim do ciclo já pago? Se começa na confirmação, o que acontece com os dias pagos e não usados? E em que dia termina uma pausa de 30 dias iniciada em D: D+30 ou D+31? _(CA1, CA4, CA5 · bloqueia CT-15 · Define o dia da volta automática e da cobrança; pode haver perda de dias pagos pelo assinante)_
- **D3.** Os 12 meses do CA3 contam do início ou do fim da pausa anterior? O dia do aniversário (exatamente 12 meses) já permite nova pausa? _(CA3 · bloqueia CT-09 · CT-09 foi escrito supondo contagem pelo início, com o dia incluído)_

**Outras dúvidas** (o requisito não diz; nenhum caso inventa a resposta):

- **D4.** Como a tela mostra que o assinante não pode pausar (botão some, fica desabilitado ou aparece mensagem) e qual mensagem aparece ao tentar assistir durante a pausa? _(CA3, CA4 · CT-05, CT-06, CT-08, CT-11 e CT-21 conferem só o estado da assinatura e o player, não a mensagem)_
- **D5.** Se o aparelho está offline quando a pausa começa, quando os downloads são apagados (ao reconectar, ao abrir o app)? E o assinante pode baixar de novo depois da volta? _(CA4 · CT-13 confere só que o download não toca)_
- **D6.** Quem mais pode ou não pode pausar: assinatura com pagamento em atraso, com cancelamento agendado ou em período de teste? E o que acontece se o assinante cancelar ou trocar para o Anual durante a pausa? _(CA1, CA7 · Transições não cobertas pelos casos; podem virar novos casos)_
- **D7.** Depois da cobrança da volta (fim da pausa ou retomada), o vencimento mensal passa a ser esse novo dia e o valor é sempre o cheio de R$ 39,90? _(CA5, CA6 · Confirma as suposições usadas em CT-16, CT-18 e CT-20)_

**Suposições** (usadas nos casos; se estiverem erradas, os casos indicados mudam):

- A cobrança da volta (CA5 e CA6) é o valor cheio do Mensal, R$ 39,90, sem proporcional _(CT-16, CT-18, CT-20)_
- Depois de retomar antes do fim, não há nova cobrança na data de fim original da pausa (a cobrança da retomada substitui a do fim) _(CT-20)_
- Uma pausa encerrada antes do fim com Retomar conta como a pausa do período de 12 meses _(CT-21)_
- O ambiente de QA permite avançar o relógio ou ajustar datas no banco e disparar as rotinas de início/fim de pausa e de cobrança _(CT-05, CT-07, CT-08, CT-09, CT-10, CT-14, CT-15, CT-16, CT-18, CT-20, CT-21)_

## Critérios e cobertura

| Critério | Descrição | Casos | Dúvidas |
|---|---|---|---|
| CA1 | Assinante do plano Mensal pode pausar por 30, 60 ou 90 dias em Conta > Assinatura > Pausar | CT-01, CT-02, CT-03 | D1, D2, D6 |
| CA2 | A pausa máxima é de 2 meses | CT-02, CT-03 | D1 |
| CA3 | Só é possível pausar uma vez a cada 12 meses | CT-05, CT-06, CT-07, CT-08, CT-09, CT-21 | D3, D4 |
| CA4 | Durante a pausa não há cobrança, o assinante não consegue assistir e os downloads offline são apagados do aparelho | CT-10, CT-11, CT-12, CT-13, CT-14 | D2, D4, D5 |
| CA5 | No fim da pausa a assinatura volta sozinha e a cobrança acontece no dia em que a pausa termina | CT-14, CT-15, CT-16, CT-17, CT-20 | D2, D7 |
| CA6 | O assinante pode retomar antes do fim em Conta > Assinatura > Retomar; a cobrança acontece no dia da retomada | CT-18, CT-19, CT-20, CT-21 | D7 |
| CA7 | Plano Anual não pode pausar: o botão Pausar não aparece | CT-04 | D6 |

## Casos

### CT-01 · Assinante Mensal pausa por 30 dias

**Critérios:** CA1 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Média

**Pré-condições:**
- Usuário ana.mensal@nexi.test logado
- Plano Mensal R$ 39,90 ativo há 3 meses, pagamentos em dia, vencimento todo dia 20
- Nenhuma pausa nos últimos 12 meses

**Dados:**
- `usuário`: ana.mensal@nexi.test
- `plano`: Mensal R$ 39,90
- `duração`: 30 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Pausar
3. Escolher 30 dias
4. Confirmar a pausa

**Resultado esperado:** Conta > Assinatura mostra a assinatura como pausada por 30 dias, e o registro da assinatura no banco tem status de pausada com duração de 30 dias

### CT-02 · Pausa de 60 dias (limite de 2 meses) é aceita

**Critérios:** CA1, CA2 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

**Pré-condições:**
- Usuário bruno.mensal@nexi.test logado
- Plano Mensal R$ 39,90 ativo, pagamentos em dia
- Nenhuma pausa nos últimos 12 meses

**Dados:**
- `usuário`: bruno.mensal@nexi.test
- `duração`: 60 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Pausar
3. Escolher 60 dias
4. Confirmar a pausa

**Resultado esperado:** Conta > Assinatura mostra a assinatura como pausada por 60 dias, e o banco registra pausa de 60 dias

### CT-03 · Opções de duração na tela Pausar (90 dias contradiz o máximo de 2 meses)

**Critérios:** CA1, CA2 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D1 (bloqueia)

**Pré-condições:**
- Bloqueado pela dúvida sobre 90 dias x pausa máxima de 2 meses
- Usuário carla.mensal@nexi.test logado, plano Mensal R$ 39,90 ativo, sem pausa nos últimos 12 meses

**Dados:**
- `usuário`: carla.mensal@nexi.test

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Pausar
3. Anotar todas as opções de duração oferecidas
4. Se a opção 90 dias existir, escolher 90 dias e confirmar

**Resultado esperado:** Nenhuma opção acima de 90 dias é oferecida; a presença da opção de 90 dias e o resultado da confirmação são julgados pela resposta do PO

### CT-04 · Botão Pausar não aparece para o plano Anual

**Critérios:** CA7 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Usuário diego.anual@nexi.test logado
- Plano Anual R$ 399,00 ativo há 2 meses

**Dados:**
- `usuário`: diego.anual@nexi.test
- `plano`: Anual R$ 399,00

**Passos:**
1. Acessar Conta > Assinatura

**Resultado esperado:** A tela Conta > Assinatura não mostra o botão Pausar

### CT-05 · Segunda pausa 6 meses depois do fim da primeira é recusada

**Critérios:** CA3 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Média

> Depende de Suposição: O ambiente de QA permite avançar o relógio ou ajustar datas no banco e disparar as rotinas de início/fim de pausa e de cobrança

**Pré-condições:**
- Usuário elisa.mensal@nexi.test, plano Mensal R$ 39,90 ativo
- Pausa de 30 dias já concluída; relógio do ambiente (ou datas no banco) ajustado para 6 meses depois do fim dela

**Dados:**
- `usuário`: elisa.mensal@nexi.test
- `duração tentada`: 30 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Tentar pausar por 30 dias

**Resultado esperado:** Nenhuma nova pausa é registrada no banco e Conta > Assinatura continua mostrando a assinatura ativa

### CT-06 · Com a assinatura já pausada, não é possível pausar de novo

**Critérios:** CA3 · **Tipo:** negativo · **Técnica:** transição de estado · **Prioridade:** Média

**Pré-condições:**
- Usuário fabio.mensal@nexi.test, plano Mensal R$ 39,90
- Pausa de 30 dias em andamento, iniciada há 5 dias

**Dados:**
- `usuário`: fabio.mensal@nexi.test
- `duração tentada`: 60 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Tentar pausar por 60 dias

**Resultado esperado:** Continua existindo uma única pausa no banco, com a mesma data de fim de antes da tentativa

### CT-07 · Pausa 12 meses e 1 dia depois do fim da pausa anterior é aceita

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de Suposição: O ambiente de QA permite avançar o relógio ou ajustar datas no banco e disparar as rotinas de início/fim de pausa e de cobrança

**Pré-condições:**
- Usuário gabi.mensal@nexi.test, plano Mensal R$ 39,90 ativo
- Pausa de 30 dias anterior concluída; relógio ajustado para 12 meses e 1 dia depois do fim dela

**Dados:**
- `usuário`: gabi.mensal@nexi.test
- `duração`: 30 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Pausar
3. Escolher 30 dias
4. Confirmar a pausa

**Resultado esperado:** Conta > Assinatura mostra a assinatura pausada por 30 dias e o banco registra a nova pausa

### CT-08 · Pausa 1 dia antes de completar 12 meses do início da pausa anterior é recusada

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de Suposição: O ambiente de QA permite avançar o relógio ou ajustar datas no banco e disparar as rotinas de início/fim de pausa e de cobrança

**Pré-condições:**
- Usuário hugo.mensal@nexi.test, plano Mensal R$ 39,90 ativo
- Pausa de 30 dias anterior iniciada em 15/10/2025; relógio ajustado para 14/10/2026

**Dados:**
- `usuário`: hugo.mensal@nexi.test
- `início da pausa anterior`: 15/10/2025
- `data do teste`: 14/10/2026

**Passos:**
1. Acessar Conta > Assinatura
2. Tentar pausar por 30 dias

**Resultado esperado:** Nenhuma nova pausa é registrada no banco e a assinatura continua ativa

### CT-09 · Pausa exatamente 12 meses depois do início da pausa anterior

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D3 (bloqueia)

> Depende de Suposição: O ambiente de QA permite avançar o relógio ou ajustar datas no banco e disparar as rotinas de início/fim de pausa e de cobrança

**Pré-condições:**
- Bloqueado pela dúvida sobre como contar os 12 meses
- Usuário iris.mensal@nexi.test, plano Mensal R$ 39,90 ativo
- Pausa de 30 dias anterior iniciada em 14/10/2025; relógio em 14/10/2026

**Dados:**
- `usuário`: iris.mensal@nexi.test
- `início da pausa anterior`: 14/10/2025
- `data do teste`: 14/10/2026

**Passos:**
1. Acessar Conta > Assinatura
2. Tentar pausar por 30 dias

**Resultado esperado:** Pausa de 30 dias é aceita e o banco registra a nova pausa (vale se os 12 meses contarem do início da pausa anterior, com o dia do aniversário incluído; ajustar conforme resposta do PO)

### CT-10 · Vencimento que cai durante a pausa não gera cobrança

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

> Depende de Suposição: O ambiente de QA permite avançar o relógio ou ajustar datas no banco e disparar as rotinas de início/fim de pausa e de cobrança

**Pré-condições:**
- Usuário ana.mensal@nexi.test, plano Mensal R$ 39,90, vencimento todo dia 20, cartão de teste final 4242
- Pausa de 30 dias em andamento que cobre o próximo dia 20; relógio avançado até o dia 20 e rotina de cobrança executada

**Dados:**
- `usuário`: ana.mensal@nexi.test
- `vencimento`: dia 20
- `cartão`: final 4242

**Passos:**
1. Acessar Conta > Assinatura > Histórico de pagamentos
2. Consultar as transações do cartão final 4242 no gateway de teste

**Resultado esperado:** Nenhuma cobrança de R$ 39,90 com data do dia 20 aparece no histórico nem no gateway

### CT-11 · Assinante pausado não consegue reproduzir título

**Critérios:** CA4 · **Tipo:** negativo · **Técnica:** transição de estado · **Prioridade:** Média

**Pré-condições:**
- Usuário fabio.mensal@nexi.test com pausa de 30 dias em andamento, iniciada há 5 dias
- Navegador web logado na conta

**Dados:**
- `título`: qualquer filme do catálogo, ex.: o primeiro da home

**Passos:**
1. Abrir o primeiro filme da home
2. Clicar em Assistir

**Resultado esperado:** O vídeo não começa a tocar (o tempo do player não sai de 00:00)

### CT-12 · Downloads offline são apagados do aparelho ao entrar em pausa

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Média

**Pré-condições:**
- Usuário julia.mensal@nexi.test, plano Mensal R$ 39,90 ativo
- App Android com 2 episódios baixados, aparelho conectado à internet
- Pausa de 30 dias confirmada e já iniciada

**Dados:**
- `aparelho`: Android, conectado
- `downloads`: 2 episódios

**Passos:**
1. Abrir o app no aparelho
2. Acessar Downloads
3. Conferir o armazenamento do app em Configurações do Android

**Resultado esperado:** A tela Downloads não lista nenhum episódio e o armazenamento do app não tem mais o espaço dos 2 episódios

### CT-13 · Download não toca em aparelho que estava offline quando a pausa começou

**Critérios:** CA4 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Média

**Pré-condições:**
- Usuário julia.mensal@nexi.test com 1 episódio baixado no app Android
- Aparelho em modo avião desde antes do início da pausa
- Pausa de 30 dias iniciada (confirmada por outro aparelho)

**Dados:**
- `aparelho`: Android em modo avião
- `downloads`: 1 episódio

**Passos:**
1. Abrir o app no aparelho em modo avião
2. Acessar Downloads
3. Tentar reproduzir o episódio baixado

**Resultado esperado:** O episódio não começa a tocar (o tempo do player não sai de 00:00)

### CT-14 · No 29º dia de uma pausa de 30 dias a assinatura continua pausada

**Critérios:** CA4, CA5 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de Suposição: O ambiente de QA permite avançar o relógio ou ajustar datas no banco e disparar as rotinas de início/fim de pausa e de cobrança

**Pré-condições:**
- Usuário ana.mensal@nexi.test, pausa de 30 dias com início D registrado no banco
- Relógio avançado para D+29

**Dados:**
- `duração`: 30 dias
- `data do teste`: D+29

**Passos:**
1. Acessar Conta > Assinatura
2. Abrir Histórico de pagamentos

**Resultado esperado:** A assinatura aparece como pausada e não há cobrança com data D+29

### CT-15 · Pausa de 30 dias iniciada em D volta sozinha em D+30

**Critérios:** CA5 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D2 (bloqueia)

> Depende de Suposição: O ambiente de QA permite avançar o relógio ou ajustar datas no banco e disparar as rotinas de início/fim de pausa e de cobrança

**Pré-condições:**
- Bloqueado pela dúvida sobre quando a pausa começa e em que dia termina
- Usuário ana.mensal@nexi.test, pausa de 30 dias com início D registrado no banco
- Relógio avançado para D+30 e rotina de fim de pausa executada

**Dados:**
- `duração`: 30 dias
- `data do teste`: D+30

**Passos:**
1. Acessar Conta > Assinatura

**Resultado esperado:** Em D+30 a assinatura aparece como ativa, sem o assinante ter clicado em Retomar

### CT-16 · Cobrança de R$ 39,90 no dia em que a pausa termina

**Critérios:** CA5 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

> Depende de Suposição: A cobrança da volta (CA5 e CA6) é o valor cheio do Mensal, R$ 39,90, sem proporcional

> Depende de Suposição: O ambiente de QA permite avançar o relógio ou ajustar datas no banco e disparar as rotinas de início/fim de pausa e de cobrança

**Pré-condições:**
- Usuário kaio.mensal@nexi.test, plano Mensal R$ 39,90, cartão de teste final 4242
- Pausa de 30 dias em andamento; relógio avançado até a data de fim registrada no banco e rotinas de fim de pausa e cobrança executadas

**Dados:**
- `usuário`: kaio.mensal@nexi.test
- `cartão`: final 4242

**Passos:**
1. Acessar Conta > Assinatura > Histórico de pagamentos
2. Consultar as transações do cartão final 4242 no gateway de teste

**Resultado esperado:** Existe exatamente uma cobrança de R$ 39,90 com a data de fim da pausa, no histórico e no gateway

### CT-17 · Após a volta automática o assinante volta a assistir

**Critérios:** CA5 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Média

**Pré-condições:**
- Usuário kaio.mensal@nexi.test com a pausa terminada pela data de fim (sem clicar em Retomar) e cobrança da volta aprovada
- Navegador web logado na conta

**Dados:**
- `título`: primeiro filme da home

**Passos:**
1. Abrir o primeiro filme da home
2. Clicar em Assistir
3. Aguardar 10 segundos

**Resultado esperado:** O vídeo toca e o tempo do player passa de 00:05

### CT-18 · Retomar no 10º dia da pausa cobra R$ 39,90 no mesmo dia

**Critérios:** CA6 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

> Depende de Suposição: A cobrança da volta (CA5 e CA6) é o valor cheio do Mensal, R$ 39,90, sem proporcional

> Depende de Suposição: O ambiente de QA permite avançar o relógio ou ajustar datas no banco e disparar as rotinas de início/fim de pausa e de cobrança

**Pré-condições:**
- Usuário lara.mensal@nexi.test, plano Mensal R$ 39,90, cartão de teste final 4242
- Pausa de 30 dias iniciada há 10 dias (relógio ou banco ajustado)

**Dados:**
- `usuário`: lara.mensal@nexi.test
- `cartão`: final 4242

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Retomar e confirmar
3. Abrir Histórico de pagamentos
4. Consultar as transações do cartão final 4242 no gateway de teste

**Resultado esperado:** Existe exatamente uma cobrança de R$ 39,90 com a data de hoje, no histórico e no gateway

### CT-19 · Após retomar antes do fim, o assinante volta a assistir

**Critérios:** CA6 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Média

**Pré-condições:**
- Usuário lara.mensal@nexi.test retomou a pausa no 10º dia e a cobrança foi aprovada
- Navegador web logado na conta

**Dados:**
- `título`: primeiro filme da home

**Passos:**
1. Acessar Conta > Assinatura
2. Abrir o primeiro filme da home
3. Clicar em Assistir e aguardar 10 segundos

**Resultado esperado:** Conta > Assinatura mostra a assinatura ativa e o vídeo toca, com o tempo do player passando de 00:05

### CT-20 · Retomar na véspera do fim não gera segunda cobrança na data de fim original

**Critérios:** CA5, CA6 · **Tipo:** borda · **Técnica:** suposição de erro · **Prioridade:** Alta

> Depende de Suposição: A cobrança da volta (CA5 e CA6) é o valor cheio do Mensal, R$ 39,90, sem proporcional

> Depende de Suposição: Depois de retomar antes do fim, não há nova cobrança na data de fim original da pausa (a cobrança da retomada substitui a do fim)

> Depende de Suposição: O ambiente de QA permite avançar o relógio ou ajustar datas no banco e disparar as rotinas de início/fim de pausa e de cobrança

**Pré-condições:**
- Usuário mateus.mensal@nexi.test, plano Mensal R$ 39,90, cartão de teste final 4242
- Pausa de 30 dias; relógio no dia anterior à data de fim registrada no banco

**Dados:**
- `usuário`: mateus.mensal@nexi.test
- `cartão`: final 4242

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Retomar e confirmar
3. Avançar o relógio 1 dia (data de fim original) e executar as rotinas de fim de pausa e cobrança
4. Consultar Histórico de pagamentos e o gateway

**Resultado esperado:** Há uma única cobrança de R$ 39,90, com a data da retomada; nenhuma cobrança com a data de fim original

### CT-21 · Depois de retomar antes do fim, nova pausa no mesmo período de 12 meses é recusada

**Critérios:** CA3, CA6 · **Tipo:** negativo · **Técnica:** tabela de decisão · **Prioridade:** Média

> Depende de Suposição: Uma pausa encerrada antes do fim com Retomar conta como a pausa do período de 12 meses

> Depende de Suposição: O ambiente de QA permite avançar o relógio ou ajustar datas no banco e disparar as rotinas de início/fim de pausa e de cobrança

**Pré-condições:**
- Usuário lara.mensal@nexi.test retomou uma pausa de 30 dias no 10º dia, há 2 meses (relógio ajustado)
- Plano Mensal R$ 39,90 ativo e em dia

**Dados:**
- `usuário`: lara.mensal@nexi.test
- `duração tentada`: 30 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Tentar pausar por 30 dias

**Resultado esperado:** Nenhuma nova pausa é registrada no banco e a assinatura continua ativa

## Fora do escopo

- E-mails e notificações de início e fim da pausa (a história não cita)
- Troca de plano Mensal para Anual e vice-versa
- Pausa feita pelo suporte ou pela tela de administração
- Baixar de novo os conteúdos depois da volta da assinatura
