# Casos de teste: Pausar assinatura

**Origem:** HIST-430 (arquivo D-pausar-assinatura.md) · **Gerado em:** 14/10/2026

**17 casos:** 6 positivos, 5 negativos, 6 de borda · **Prioridade:** 4 Alta, 13 Média, 0 Baixa

## Pontos a confirmar com o PO

**Dúvidas que bloqueiam a execução** (responder primeiro):

- **D1.** CA1 permite pausar por 90 dias, mas CA2 diz que a pausa máxima é de 2 meses. A opção de 90 dias existe? Se não, CA1 fica só com 30 e 60 dias? _(CA1, CA2 · bloqueia CT-03 · Contradição no requisito: não dá para julgar se a opção 90 dias deve aparecer nem testar o limite máximo)_
- **D2.** Quando a pausa começa e termina? Começa no dia do pedido ou no fim do período já pago? Uma pausa de 30 dias pedida em 01/11 termina em 30/11 ou 01/12? _(CA5, CA4 · bloqueia CT-08, CT-09 · Sem isso não se sabe em que dia a assinatura deve voltar e ser cobrada)_
- **D3.** Os 12 meses do CA3 contam a partir do início ou do fim da pausa anterior? E a partir de que dia exatamente (o 12º mês inclui o próprio dia)? _(CA3 · bloqueia CT-16, CT-17 · Muda a data dos testes de limite)_

**Outras dúvidas** (o requisito não diz; nenhum caso inventa a resposta):

- **D4.** Qual o valor da cobrança na volta (automática ou por Retomar): R$ 39,90 cheio ou proporcional? E os dias já pagos e não usados quando o assinante pausa no meio do ciclo? _(CA5, CA6 · CT-08, CT-10 e CT-12 conferem só a data da cobrança, não o valor)_
- **D5.** Depois da volta, a próxima renovação passa a ser todo mês a partir do dia da volta? _(CA5, CA6 · Sem caso para a cobrança seguinte à volta)_
- **D6.** O que o assinante vê ao tentar assistir pausado e ao tentar pausar de novo dentro de 12 meses: o botão Pausar some ou aparece uma mensagem? Qual o texto? _(CA3, CA4 · CT-06, CT-13, CT-14, CT-15 e CT-17 conferem só que nada muda, não a mensagem)_
- **D7.** Se o aparelho estiver sem internet durante a pausa, quando os downloads são apagados? Os downloads voltam depois da retomada? _(CA4 · Sem caso para aparelho offline; CT-07 usa aparelho com internet)_
- **D8.** Durante a pausa o assinante pode cancelar a assinatura ou trocar para o plano Anual? O que acontece com a pausa? _(CA1, CA7 · Transições não cobertas pelos casos)_

**Suposições** (usadas nos casos; se estiverem erradas, os casos indicados mudam):

- Uma pausa de 60 dias está dentro do limite de 2 meses do CA2 _(CT-02)_
- Uma pausa retomada antes do fim conta como a pausa dos 12 meses _(CT-15)_
- Com o aparelho conectado, os downloads são apagados ao abrir o app depois da pausa _(CT-07)_
- Uma pausa só pode começar com a assinatura ativa; durante a pausa não se pode pausar de novo (pelo CA3) _(CT-13)_

## Critérios e cobertura

| Critério | Descrição | Casos | Dúvidas |
|---|---|---|---|
| CA1 | Assinante do plano Mensal pode pausar por 30, 60 ou 90 dias em Conta > Assinatura > Pausar | CT-01, CT-02, CT-03, CT-04 | D1, D8 |
| CA2 | A pausa máxima é de 2 meses | CT-02, CT-03 | D1 |
| CA3 | Só é possível pausar uma vez a cada 12 meses | CT-13, CT-14, CT-15, CT-16, CT-17 | D3, D6 |
| CA4 | Durante a pausa não há cobrança, o assinante não consegue assistir e os downloads offline são apagados do aparelho | CT-05, CT-06, CT-07 | D2, D6, D7 |
| CA5 | No fim da pausa a assinatura volta sozinha e a cobrança acontece no dia em que a pausa termina | CT-08, CT-09 | D2, D4, D5 |
| CA6 | O assinante pode retomar antes do fim em Conta > Assinatura > Retomar; a cobrança acontece no dia da retomada | CT-10, CT-11, CT-12, CT-15 | D4, D5 |
| CA7 | Plano Anual não pode pausar: o botão Pausar não aparece | CT-04 | D8 |

## Casos

### CT-01 · Assinante Mensal pausa por 30 dias

**Critérios:** CA1 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

**Pré-condições:**
- Usuário qa.pausa01@nexi.test logado
- Plano Mensal R$ 39,90 ativo há 3 meses, nunca pausou

**Dados:**
- `usuário`: qa.pausa01@nexi.test
- `plano`: Mensal R$ 39,90
- `duração`: 30 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Pausar
3. Escolher 30 dias
4. Confirmar a pausa

**Resultado esperado:** Conta > Assinatura mostra a assinatura pausada e exibe o botão Retomar

### CT-02 · Pausa de 60 dias (limite de 2 meses) é aceita

**Critérios:** CA1, CA2 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de Suposição: Uma pausa de 60 dias está dentro do limite de 2 meses do CA2

**Pré-condições:**
- Usuário qa.pausa02@nexi.test logado
- Plano Mensal R$ 39,90 ativo há 3 meses, nunca pausou

**Dados:**
- `usuário`: qa.pausa02@nexi.test
- `plano`: Mensal R$ 39,90
- `duração`: 60 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Pausar
3. Escolher 60 dias
4. Confirmar a pausa

**Resultado esperado:** Conta > Assinatura mostra a assinatura pausada e exibe o botão Retomar

### CT-03 · Opções de duração em Pausar (90 dias depende da dúvida 1)

**Critérios:** CA1, CA2 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D1 (bloqueia)

**Pré-condições:**
- Usuário qa.pausa03@nexi.test logado
- Plano Mensal R$ 39,90 ativo, nunca pausou
- Bloqueado pela contradição CA1 (90 dias) x CA2 (máximo 2 meses)

**Dados:**
- `usuário`: qa.pausa03@nexi.test
- `plano`: Mensal R$ 39,90

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Pausar
3. Abrir a lista de durações

**Resultado esperado:** A lista oferece 30 dias e 60 dias e nenhuma duração acima de 90 dias; a presença da opção 90 dias é conferida com a resposta da dúvida 1

### CT-04 · Plano Anual não mostra o botão Pausar

**Critérios:** CA7, CA1 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.pausa04@nexi.test logado
- Plano Anual R$ 399,00 ativo

**Dados:**
- `usuário`: qa.pausa04@nexi.test
- `plano`: Anual R$ 399,00

**Passos:**
1. Acessar Conta > Assinatura

**Resultado esperado:** O botão Pausar não aparece em Conta > Assinatura

### CT-05 · Data de renovação dentro da pausa não gera cobrança

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

**Pré-condições:**
- Usuário qa.pausa05@nexi.test com plano Mensal R$ 39,90, próxima renovação daqui a 10 dias
- Pausa de 30 dias feita hoje
- Relógio do ambiente avançado em 11 dias

**Dados:**
- `usuário`: qa.pausa05@nexi.test
- `plano`: Mensal R$ 39,90
- `duração`: 30 dias

**Passos:**
1. Consultar no gateway as cobranças da assinatura desde o dia da pausa

**Resultado esperado:** Nenhuma cobrança registrada no gateway entre o dia da pausa e o 11º dia, inclusive na data de renovação prevista

### CT-06 · Assinante pausado não consegue assistir

**Critérios:** CA4 · **Tipo:** negativo · **Técnica:** transição de estado · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.pausa06@nexi.test com plano Mensal pausado por 30 dias desde hoje

**Dados:**
- `usuário`: qa.pausa06@nexi.test
- `conteúdo`: qualquer episódio do catálogo, ex.: 1º episódio da série em destaque

**Passos:**
1. Entrar no Nexi Play pela web
2. Abrir o episódio
3. Clicar em Assistir

**Resultado esperado:** O vídeo não toca: nenhum segundo do episódio é reproduzido e o progresso do episódio continua 00:00

### CT-07 · Downloads offline são apagados do aparelho ao pausar

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Média

> Depende de Suposição: Com o aparelho conectado, os downloads são apagados ao abrir o app depois da pausa

**Pré-condições:**
- Usuário qa.pausa07@nexi.test com plano Mensal ativo
- 2 episódios baixados no app Android, aparelho com internet

**Dados:**
- `usuário`: qa.pausa07@nexi.test
- `aparelho`: Android com app Nexi Play
- `downloads`: 2 episódios

**Passos:**
1. Pausar a assinatura por 30 dias em Conta > Assinatura > Pausar
2. Fechar e abrir o app no aparelho
3. Abrir a tela Downloads

**Resultado esperado:** A tela Downloads não lista os 2 episódios e o armazenamento usado pelo app não inclui mais os arquivos baixados

### CT-08 · Assinatura volta sozinha e é cobrada no dia em que a pausa termina

**Critérios:** CA5 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Alta

> Depende de D2 (bloqueia)

**Pré-condições:**
- Usuário qa.pausa08@nexi.test com plano Mensal R$ 39,90 pausado por 30 dias
- Relógio do ambiente avançado até o dia de fim da pausa (data depende da dúvida 2)

**Dados:**
- `usuário`: qa.pausa08@nexi.test
- `plano`: Mensal R$ 39,90
- `duração`: 30 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Consultar no gateway as cobranças da assinatura

**Resultado esperado:** Conta > Assinatura não mostra mais a pausa nem o botão Retomar, e o gateway tem uma cobrança com a data do fim da pausa

### CT-09 · Na véspera do fim da pausa a assinatura continua pausada e sem cobrança

**Critérios:** CA5 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D2 (bloqueia)

**Pré-condições:**
- Usuário qa.pausa09@nexi.test com plano Mensal R$ 39,90 pausado por 30 dias
- Relógio do ambiente avançado até o dia anterior ao fim da pausa (data depende da dúvida 2)

**Dados:**
- `usuário`: qa.pausa09@nexi.test
- `plano`: Mensal R$ 39,90
- `duração`: 30 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Consultar no gateway as cobranças da assinatura

**Resultado esperado:** Conta > Assinatura ainda mostra a assinatura pausada com o botão Retomar, e o gateway não tem cobrança desde o dia da pausa

### CT-10 · Retomar antes do fim gera cobrança no dia da retomada

**Critérios:** CA6 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

**Pré-condições:**
- Usuário qa.pausa10@nexi.test com plano Mensal R$ 39,90 pausado por 60 dias
- Relógio do ambiente avançado em 10 dias desde o início da pausa

**Dados:**
- `usuário`: qa.pausa10@nexi.test
- `plano`: Mensal R$ 39,90
- `duração`: 60 dias
- `retomada`: 10º dia da pausa

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Retomar
3. Consultar no gateway as cobranças da assinatura

**Resultado esperado:** Conta > Assinatura não mostra mais a pausa e o gateway tem uma cobrança com a data do 10º dia (dia da retomada)

### CT-11 · Depois de retomar o assinante volta a assistir

**Critérios:** CA6 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.pausa11@nexi.test com plano Mensal pausado por 30 dias
- Retomada feita hoje em Conta > Assinatura > Retomar

**Dados:**
- `usuário`: qa.pausa11@nexi.test
- `conteúdo`: 1º episódio da série em destaque

**Passos:**
1. Abrir o episódio pela web
2. Clicar em Assistir

**Resultado esperado:** O vídeo começa a tocar e o contador de tempo do player passa de 00:00

### CT-12 · Retomar no mesmo dia em que pausou gera cobrança nesse dia

**Critérios:** CA6 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.pausa12@nexi.test com plano Mensal R$ 39,90 pausado por 30 dias hoje

**Dados:**
- `usuário`: qa.pausa12@nexi.test
- `plano`: Mensal R$ 39,90
- `retomada`: dia 0 da pausa

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Retomar
3. Consultar no gateway as cobranças da assinatura

**Resultado esperado:** Conta > Assinatura não mostra mais a pausa e o gateway tem uma cobrança com a data de hoje

### CT-13 · Assinatura já pausada não aceita uma segunda pausa

**Critérios:** CA3 · **Tipo:** negativo · **Técnica:** transição de estado · **Prioridade:** Média

> Depende de Suposição: Uma pausa só pode começar com a assinatura ativa; durante a pausa não se pode pausar de novo (pelo CA3)

**Pré-condições:**
- Usuário qa.pausa13@nexi.test com plano Mensal pausado por 30 dias há 5 dias

**Dados:**
- `usuário`: qa.pausa13@nexi.test
- `duração tentada`: 60 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Tentar pausar por 60 dias (se o botão Pausar aparecer)

**Resultado esperado:** A data de fim da pausa continua a mesma e o banco tem só uma pausa registrada para a assinatura

### CT-14 · Nova pausa 2 meses depois do fim da anterior é recusada

**Critérios:** CA3 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Usuário qa.pausa14@nexi.test com plano Mensal ativo
- Pausa de 30 dias iniciada há 3 meses e já terminada (datas ajustadas no banco)

**Dados:**
- `usuário`: qa.pausa14@nexi.test
- `duração tentada`: 30 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Tentar pausar por 30 dias (se o botão Pausar aparecer)

**Resultado esperado:** A assinatura continua ativa, sem botão Retomar, e o banco continua com uma só pausa registrada

### CT-15 · Pausa retomada antes do fim conta para o limite de 12 meses

**Critérios:** CA3, CA6 · **Tipo:** negativo · **Técnica:** tabela de decisão · **Prioridade:** Média

> Depende de Suposição: Uma pausa retomada antes do fim conta como a pausa dos 12 meses

**Pré-condições:**
- Usuário qa.pausa15@nexi.test com plano Mensal ativo
- Pausa de 60 dias feita há 20 dias e retomada no 5º dia (datas ajustadas no banco)

**Dados:**
- `usuário`: qa.pausa15@nexi.test
- `duração tentada`: 30 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Tentar pausar por 30 dias (se o botão Pausar aparecer)

**Resultado esperado:** A assinatura continua ativa, sem botão Retomar, e o banco continua com uma só pausa registrada

### CT-16 · Nova pausa exatamente 12 meses depois da anterior é aceita

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D3 (bloqueia)

**Pré-condições:**
- Usuário qa.pausa16@nexi.test com plano Mensal ativo
- Pausa anterior de 30 dias registrada há exatamente 12 meses (marco de contagem depende da dúvida 3; datas ajustadas no banco)

**Dados:**
- `usuário`: qa.pausa16@nexi.test
- `duração`: 30 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Clicar em Pausar
3. Escolher 30 dias
4. Confirmar a pausa

**Resultado esperado:** Conta > Assinatura mostra a assinatura pausada e exibe o botão Retomar

### CT-17 · Nova pausa 1 dia antes de completar 12 meses é recusada

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de D3 (bloqueia)

**Pré-condições:**
- Usuário qa.pausa17@nexi.test com plano Mensal ativo
- Pausa anterior de 30 dias registrada há 12 meses menos 1 dia (marco de contagem depende da dúvida 3; datas ajustadas no banco)

**Dados:**
- `usuário`: qa.pausa17@nexi.test
- `duração tentada`: 30 dias

**Passos:**
1. Acessar Conta > Assinatura
2. Tentar pausar por 30 dias (se o botão Pausar aparecer)

**Resultado esperado:** A assinatura continua ativa, sem botão Retomar, e o banco continua com uma só pausa registrada

## Fora do escopo

- Cancelamento e troca de plano durante a pausa (ver dúvida 8)
- Assinante Anual que muda para o Mensal para poder pausar
- E-mails ou notificações de início e fim da pausa (não citados na história)
- Assinatura inadimplente ou com pagamento pendente pedindo pausa
