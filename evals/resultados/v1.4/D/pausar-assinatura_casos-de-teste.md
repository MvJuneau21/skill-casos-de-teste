# Casos de teste: Pausar assinatura

**Origem:** HIST-430 (arquivo D-pausar-assinatura.md enviado pelo usuário) · **Gerado em:** 14/10/2026

**16 casos:** 5 positivos, 5 negativos, 6 de borda · **Prioridade:** 5 Alta, 11 Média, 0 Baixa

## Pontos a confirmar com o PO

**Dúvidas que bloqueiam a execução** (responder primeiro):

- **D1.** CA1 e CA2 se contradizem: CA1 oferece 30, 60 ou 90 dias e CA2 diz que a pausa máxima é de 2 meses. A opção de 90 dias existe? E '2 meses' equivale a 60 dias? _(CA1, CA2 · bloqueia CT-03 · Sem a resposta não dá para julgar se a opção 90 dias é bug ou regra)_
- **D2.** Quando a pausa começa: no dia em que o assinante confirma ou no fim do período já pago? Se começa na hora, o que acontece com os dias já pagos? Depois da volta, as próximas cobranças passam a ser mensais a partir da nova data? _(CA4, CA5 · bloqueia CT-12, CT-13, CT-15 · Define a data de fim da pausa, que é o dia da cobrança e do retorno automático)_
- **D3.** Os 12 meses do CA3 contam a partir do início da pausa anterior, do fim dela ou da retomada? _(CA3 · bloqueia CT-08 · Define em que dia a segunda pausa passa a ser permitida)_

**Outras dúvidas** (o requisito não diz; nenhum caso inventa a resposta):

- **D4.** O que o assinante vê quando não pode pausar (já pausou nos últimos 12 meses ou já está pausado): o botão Pausar some ou aparece com mensagem? Qual mensagem? E o botão Retomar aparece para assinatura que não está pausada? _(CA3, CA6 · CT-05, CT-06 e CT-07 conferem só que nenhuma pausa é criada, não a tela)_
- **D5.** Se o aparelho estiver sem internet quando a pausa começa, quando os downloads são apagados e eles continuam tocando offline até lá? _(CA4 · CT-11 cobre só aparelho com internet)_
- **D6.** Se a cobrança do fim da pausa ou da retomada for recusada ou o gateway estiver fora do ar, a assinatura volta mesmo assim, fica pausada ou é suspensa? _(CA5, CA6 · Sem caso para falha de pagamento até a resposta)_
- **D7.** O que o assinante vê durante a pausa ao tentar assistir (mensagem, tela de retomar)? _(CA4 · CT-10 confere só que o vídeo não toca)_

**Suposições** (usadas nos casos; se estiverem erradas, os casos indicados mudam):

- Uma pausa retomada antes do fim conta como a pausa do período de 12 meses _(CT-06)_

## Critérios e cobertura

| Critério | Descrição | Casos | Dúvidas |
|---|---|---|---|
| CA1 | Assinante do plano Mensal pode pausar por 30, 60 ou 90 dias em Conta > Assinatura > Pausar | CT-01, CT-02, CT-03, CT-04 | D1 |
| CA2 | A pausa máxima é de 2 meses | CT-02, CT-03 | D1 |
| CA3 | Só é possível pausar uma vez a cada 12 meses | CT-05, CT-06, CT-07, CT-08 | D3, D4 |
| CA4 | Durante a pausa não há cobrança, o assinante não consegue assistir e os downloads offline são apagados do aparelho | CT-09, CT-10, CT-11, CT-13 | D2, D5, D7 |
| CA5 | No fim da pausa a assinatura volta sozinha e a cobrança acontece no dia em que a pausa termina | CT-12, CT-13, CT-15 | D2, D6 |
| CA6 | O assinante pode retomar antes do fim em Conta > Assinatura > Retomar; a cobrança acontece no dia da retomada | CT-06, CT-14, CT-15 | D4, D6 |
| CA7 | Plano Anual não pode pausar: o botão Pausar não aparece | CT-16 | — |

## Casos

### CT-01 · Assinante Mensal pausa por 30 dias

**Critérios:** CA1 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

**Pré-condições:**
- Usuário qa.pausa01@nexi.test logado, plano Mensal R$ 39,90 ativo há 3 meses, nunca pausou

**Dados:**
- `usuário`: qa.pausa01@nexi.test
- `plano`: Mensal R$ 39,90
- `duração`: 30 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Pausar
3. Escolher 30 dias
4. Confirmar a pausa

**Resultado esperado:** Conta > Assinatura passa a exibir o botão Retomar; no banco a assinatura de qa.pausa01@nexi.test fica pausada com duração de 30 dias

### CT-02 · Pausa de 60 dias (limite de 2 meses) é aceita

**Critérios:** CA1, CA2 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.pausa02@nexi.test logado, plano Mensal R$ 39,90 ativo há 3 meses, nunca pausou

**Dados:**
- `usuário`: qa.pausa02@nexi.test
- `duração`: 60 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Pausar
3. Escolher 60 dias
4. Confirmar a pausa

**Resultado esperado:** Conta > Assinatura passa a exibir o botão Retomar; no banco a assinatura fica pausada com duração de 60 dias

### CT-03 · Opção de 90 dias acima da pausa máxima de 2 meses (contradição CA1 x CA2, ver D1)

**Critérios:** CA1, CA2 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D1 (bloqueia)

**Pré-condições:**
- Usuário qa.pausa03@nexi.test logado, plano Mensal R$ 39,90 ativo há 3 meses, nunca pausou
- Caso bloqueado até o PO responder a D1

**Dados:**
- `usuário`: qa.pausa03@nexi.test
- `duração`: 90 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Pausar
3. Conferir as opções de duração exibidas
4. Se a opção 90 dias existir, escolher 90 dias e confirmar

**Resultado esperado:** A tela Pausar exibe as opções 30 dias e 60 dias; a presença da opção 90 dias e a duração gravada no banco são comparadas com a resposta da D1

### CT-04 · Sair da tela Pausar sem confirmar não pausa a assinatura

**Critérios:** CA1 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.pausa04@nexi.test logado, plano Mensal R$ 39,90 ativo, nunca pausou

**Dados:**
- `usuário`: qa.pausa04@nexi.test
- `duração escolhida`: 30 dias
- `conteúdo`: Série QA T1E1

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Pausar
3. Escolher 30 dias
4. Voltar para Conta > Assinatura sem confirmar
5. Dar play em Série QA T1E1

**Resultado esperado:** Conta > Assinatura não exibe o botão Retomar, nenhuma pausa é gravada no banco e o episódio Série QA T1E1 começa a tocar

### CT-05 · Assinatura já pausada não aceita nova pausa

**Critérios:** CA3 · **Tipo:** negativo · **Técnica:** transição de estado · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.pausa05@nexi.test com plano Mensal pausado há 5 dias, pausa de 30 dias

**Dados:**
- `usuário`: qa.pausa05@nexi.test
- `duração tentada`: 60 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Tentar pausar de novo por 60 dias

**Resultado esperado:** No banco continua existindo só a pausa de 30 dias, com a mesma data de fim de antes da tentativa

### CT-06 · Depois de retomar antes do fim, nova pausa no mesmo período de 12 meses é recusada

**Critérios:** CA3, CA6 · **Tipo:** negativo · **Técnica:** transição de estado · **Prioridade:** Média

> Depende de Suposição: Uma pausa retomada antes do fim conta como a pausa do período de 12 meses

**Pré-condições:**
- Usuário qa.pausa06@nexi.test, plano Mensal, pausou por 60 dias há 10 dias e retomou ontem em Conta > Assinatura > Retomar

**Dados:**
- `usuário`: qa.pausa06@nexi.test
- `duração tentada`: 30 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Tentar pausar por 30 dias

**Resultado esperado:** Nenhuma pausa nova é gravada no banco e a assinatura continua ativa: o botão Retomar não aparece

### CT-07 · Segunda pausa 11 meses depois do início da primeira é recusada

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.pausa07@nexi.test, plano Mensal ativo
- Datas manipuladas no banco: pausa de 30 dias iniciada há 11 meses e encerrada automaticamente há 10 meses

**Dados:**
- `usuário`: qa.pausa07@nexi.test
- `duração tentada`: 30 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Tentar pausar por 30 dias

**Resultado esperado:** Nenhuma pausa nova é gravada no banco e a assinatura continua ativa: o botão Retomar não aparece

### CT-08 · Segunda pausa exatamente 12 meses depois do início da primeira (ver D3)

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D3 (bloqueia)

**Pré-condições:**
- Usuário qa.pausa08@nexi.test, plano Mensal ativo
- Datas manipuladas no banco: pausa de 30 dias iniciada há exatamente 12 meses e encerrada automaticamente há 11 meses
- Resultado esperado vale se os 12 meses contam do início da pausa anterior; bloqueado até a D3

**Dados:**
- `usuário`: qa.pausa08@nexi.test
- `duração`: 30 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Pausar
3. Escolher 30 dias
4. Confirmar a pausa

**Resultado esperado:** Conta > Assinatura passa a exibir o botão Retomar; no banco aparece uma segunda pausa de 30 dias

### CT-09 · Data de cobrança que cai durante a pausa não gera cobrança

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

**Pré-condições:**
- Usuário qa.pausa09@nexi.test, plano Mensal R$ 39,90 com próxima cobrança amanhã
- Pausa de 60 dias confirmada hoje
- Relógio do ambiente avançado em 10 dias (passa da data de cobrança e fica dentro da pausa em qualquer resposta da D2)

**Dados:**
- `usuário`: qa.pausa09@nexi.test
- `duração`: 60 dias

**Passos:**
1. Consultar no gateway as cobranças de qa.pausa09@nexi.test entre hoje e o 10º dia

**Resultado esperado:** Nenhuma cobrança de R$ 39,90 de qa.pausa09@nexi.test aparece no gateway nesse intervalo

### CT-10 · Assinante com assinatura pausada não consegue assistir

**Critérios:** CA4 · **Tipo:** negativo · **Técnica:** transição de estado · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.pausa10@nexi.test logado no site, plano Mensal R$ 39,90 com próxima cobrança amanhã
- Pausa de 60 dias confirmada hoje; relógio do ambiente avançado em 10 dias

**Dados:**
- `usuário`: qa.pausa10@nexi.test
- `conteúdo`: Série QA T1E1

**Passos:**
1. Abrir a página de Série QA T1E1
2. Clicar em play

**Resultado esperado:** O episódio Série QA T1E1 não começa a tocar

### CT-11 · Downloads offline são apagados do aparelho durante a pausa

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.pausa11@nexi.test, plano Mensal com próxima cobrança amanhã, logado no app Android com internet
- Episódios Série QA T1E1 e T1E2 baixados no aparelho
- Pausa de 60 dias confirmada hoje pelo site; relógio do ambiente avançado em 10 dias

**Dados:**
- `usuário`: qa.pausa11@nexi.test
- `aparelho`: Android de teste com internet
- `downloads`: ['Série QA T1E1', 'Série QA T1E2']

**Passos:**
1. Abrir o app no aparelho
2. Acessar a aba Downloads
3. Conferir o armazenamento do app nas configurações do Android

**Resultado esperado:** A aba Downloads não lista Série QA T1E1 nem T1E2 e o armazenamento do app não tem mais os arquivos dos dois episódios

### CT-12 · No dia do fim da pausa a assinatura volta sozinha com cobrança de R$ 39,90

**Critérios:** CA5 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Alta

> Depende de D2 (bloqueia)

**Pré-condições:**
- Usuário qa.pausa12@nexi.test, plano Mensal R$ 39,90, pausa de 30 dias confirmada
- Relógio do ambiente avançado até o dia em que a pausa termina (data depende da D2)

**Dados:**
- `usuário`: qa.pausa12@nexi.test
- `conteúdo`: Série QA T1E1

**Passos:**
1. Consultar no gateway as cobranças de qa.pausa12@nexi.test do dia
2. Entrar no site com qa.pausa12@nexi.test
3. Dar play em Série QA T1E1

**Resultado esperado:** O gateway mostra uma cobrança de R$ 39,90 com a data do fim da pausa e o episódio Série QA T1E1 começa a tocar, sem o assinante clicar em Retomar

### CT-13 · Na véspera do fim da pausa não há cobrança

**Critérios:** CA4, CA5 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D2 (bloqueia)

**Pré-condições:**
- Usuário qa.pausa13@nexi.test, plano Mensal R$ 39,90, pausa de 30 dias confirmada
- Relógio do ambiente avançado até o dia anterior ao fim da pausa (data depende da D2)

**Dados:**
- `usuário`: qa.pausa13@nexi.test

**Passos:**
1. Consultar no gateway as cobranças de qa.pausa13@nexi.test desde o início da pausa

**Resultado esperado:** Nenhuma cobrança de R$ 39,90 de qa.pausa13@nexi.test aparece no gateway desde o início da pausa

### CT-14 · Retomar antes do fim cobra R$ 39,90 no dia da retomada

**Critérios:** CA6 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

**Pré-condições:**
- Usuário qa.pausa14@nexi.test logado, plano Mensal R$ 39,90 com próxima cobrança amanhã
- Pausa de 60 dias confirmada hoje; relógio do ambiente avançado em 10 dias

**Dados:**
- `usuário`: qa.pausa14@nexi.test
- `conteúdo`: Série QA T1E1

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Retomar
3. Consultar no gateway as cobranças de qa.pausa14@nexi.test do dia
4. Dar play em Série QA T1E1

**Resultado esperado:** O gateway mostra uma cobrança de R$ 39,90 com a data da retomada e o episódio Série QA T1E1 começa a tocar

### CT-15 · Retomar no último dia da pausa gera uma única cobrança

**Critérios:** CA5, CA6 · **Tipo:** borda · **Técnica:** tabela de decisão · **Prioridade:** Alta

> Depende de D2 (bloqueia)

**Pré-condições:**
- Usuário qa.pausa15@nexi.test logado, plano Mensal R$ 39,90, pausa de 30 dias confirmada
- Relógio do ambiente avançado até o dia em que a pausa termina, antes do processamento automático do fim da pausa (data depende da D2)

**Dados:**
- `usuário`: qa.pausa15@nexi.test

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Retomar
3. Deixar rodar o processamento do fim da pausa do dia
4. Consultar no gateway as cobranças de qa.pausa15@nexi.test do dia

**Resultado esperado:** O gateway mostra exatamente uma cobrança de R$ 39,90 de qa.pausa15@nexi.test nesse dia

### CT-16 · Plano Anual não exibe o botão Pausar

**Critérios:** CA7 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.pausa16@nexi.test logado, plano Anual R$ 399,00 ativo há 2 meses

**Dados:**
- `usuário`: qa.pausa16@nexi.test
- `plano`: Anual R$ 399,00

**Passos:**
1. Acessar Conta > Assinatura

**Resultado esperado:** A tela Conta > Assinatura não exibe o botão Pausar e no banco a assinatura Anual não tem pausa registrada

## Fora do escopo

- Cancelar a assinatura durante a pausa
- Trocar de plano (Mensal para Anual ou o contrário) durante a pausa
- Baixar de novo os conteúdos depois da retomada
- Avisos por e-mail ou push sobre o início e o fim da pausa
- Pausa feita pelo suporte ou pela administração
