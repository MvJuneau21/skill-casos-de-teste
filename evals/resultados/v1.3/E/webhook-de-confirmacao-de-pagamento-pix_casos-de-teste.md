# Casos de teste: Webhook de confirmação de pagamento Pix

**Origem:** HIST-510 (requisito.md) + trecho atual de webhook_controller.py, usado só para rotas e campos · **Gerado em:** 14/10/2026

**16 casos:** 5 positivos, 7 negativos, 4 de borda · **Prioridade:** 7 Alta, 9 Média, 0 Baixa

## Pontos a confirmar com o PO

**Dúvidas que bloqueiam a execução** (responder primeiro):

- **D1.** No GET /v1/pix/{id} do gateway, o {id} é o cobranca_id, o event_id ou um id do Pix no gateway (txid)? O código atual consulta com event_id. _(CA5 · bloqueia CT-13 · Sem isso não dá para conferir se a consulta é feita para o Pix certo)_
- **D2.** Um evento novo (event_id diferente) de pagamento para uma cobrança que já está paga (#125) deve responder 200? Deve registrar algo na auditoria? O código atual marca como paga de novo. _(CA2, CA3 · bloqueia CT-08 · O código HTTP e o registro esperados no CT-08 dependem disso)_

**Outras dúvidas** (o requisito não diz; nenhum caso inventa a resposta):

- **D3.** Quando o gateway não confirma o pagamento (status diferente de pago) ou está fora do ar, qual código a API responde? Esse event_id passa a contar como processado? Se a resposta for 200, o gateway não reenvia e um pagamento real pode se perder; o código atual responde 200 quando o gateway não diz pago. _(CA5, CA3 · CT-14 e CT-15 conferem só que a cobrança continua pendente)_
- **D4.** O que fazer com eventos de status diferente de pago (ex.: expirado, devolvido)? O requisito só define pago, e o código atual não lê o campo status do evento. _(CA2 · Nenhum caso cobre outros status; se houver regra, faltam casos)_
- **D5.** Qual o segredo de homologação do gateway e o formato do X-Assinatura (hex ou base64, com ou sem prefixo como sha256=)? _(CA1 · Dado de ambiente: sem ele o testador não gera assinatura válida para nenhum caso; pedir ao dev antes de executar)_
- **D6.** Como e onde o QA consulta o log de auditoria, e com quais nomes de campo aparecem os dois valores do VALOR_DIVERGENTE? _(CA4 · CT-09 a CT-12 conferem os valores, não o nome dos campos)_
- **D7.** Qual resposta para corpo malformado (sem event_id ou cobranca_id, valor como texto)? O requisito não cobre. _(CA1, CA6 · Nenhum caso cobre corpo malformado)_

**Suposições** (usadas nos casos; se estiverem erradas, os casos indicados mudam):

- Se a consulta ao gateway não confirma o pagamento, a cobrança não é marcada como paga (o CA5 diz que a consulta serve para confirmar, mas não diz o que acontece quando não confirma) _(CT-14, CT-15)_
- Processar de novo inclui consultar o gateway e registrar VALOR_DIVERGENTE outra vez; por isso a repetição é conferida pela contagem desses registros e das chamadas ao mock _(CT-06, CT-07)_
- O ambiente de homologação permite trocar o gateway por um mock que registra chamadas e escolhe a resposta _(CT-06, CT-13, CT-14, CT-15)_

## Critérios e cobertura

| Critério | Descrição | Casos | Dúvidas |
|---|---|---|---|
| CA1 | Assinatura ausente ou inválida: responder 401 e não alterar a cobrança | CT-02, CT-03, CT-04, CT-05 | D5, D7 |
| CA2 | Evento com status = pago: a cobrança passa para paga e a resposta é 200 | CT-01, CT-05, CT-08 | D2, D4 |
| CA3 | Evento repetido (mesmo event_id já processado): responder 200 sem processar de novo | CT-06, CT-07, CT-08 | D2, D3 |
| CA4 | Valor do evento diferente do valor da cobrança: registrar VALOR_DIVERGENTE com os dois valores no log de auditoria e marcar a cobrança como paga mesmo assim | CT-09, CT-10, CT-11, CT-12 | D6 |
| CA5 | Antes de marcar como paga, a API consulta GET /v1/pix/{id} no gateway para confirmar o evento | CT-13, CT-14, CT-15 | D1, D3 |
| CA6 | cobranca_id que não existe: responder 404 | CT-16 | D7 |

## Casos

### CT-01 · Evento pago com assinatura válida marca a cobrança #123 como paga

**Critérios:** CA2 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

**Pré-condições:**
- Cobrança #123 (R$ 39,90) com status pendente
- Gateway (ou mock) responde status pago na consulta do Pix da #123
- Segredo de homologação do gateway disponível para calcular o HMAC

**Dados:**
- `corpo`: {"event_id": "evt_qa_123_01", "cobranca_id": 123, "status": "pago", "valor": 39.90}
- `X-Assinatura`: HMAC-SHA256 do corpo acima com o segredo de homologação

**Passos:**
1. Calcular o HMAC-SHA256 do corpo exato que será enviado
2. Enviar POST /webhooks/pix com o corpo e o cabeçalho X-Assinatura
3. Consultar o status da cobrança #123

**Resultado esperado:** Resposta HTTP 200 e a cobrança #123 fica com status paga

### CT-02 · Requisição sem cabeçalho X-Assinatura recebe 401 e não altera a cobrança

**Critérios:** CA1 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Alta

**Pré-condições:**
- Cobrança #123 (R$ 39,90) com status pendente

**Dados:**
- `corpo`: {"event_id": "evt_qa_123_02", "cobranca_id": 123, "status": "pago", "valor": 39.90}
- `X-Assinatura`: (cabeçalho não enviado)

**Passos:**
1. Enviar POST /webhooks/pix com o corpo, sem o cabeçalho X-Assinatura
2. Consultar o status da cobrança #123

**Resultado esperado:** Resposta HTTP 401 e a cobrança #123 continua pendente

### CT-03 · Assinatura calculada com segredo errado recebe 401 e não altera a cobrança

**Critérios:** CA1 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Alta

**Pré-condições:**
- Cobrança #123 (R$ 39,90) com status pendente

**Dados:**
- `corpo`: {"event_id": "evt_qa_123_03", "cobranca_id": 123, "status": "pago", "valor": 39.90}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo errado segredo-qa-invalido

**Passos:**
1. Calcular o HMAC-SHA256 do corpo com o segredo segredo-qa-invalido
2. Enviar POST /webhooks/pix com o corpo e essa assinatura
3. Consultar o status da cobrança #123

**Resultado esperado:** Resposta HTTP 401 e a cobrança #123 continua pendente

### CT-04 · Corpo alterado depois de assinado recebe 401 e não altera a cobrança

**Critérios:** CA1 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Média

**Pré-condições:**
- Cobrança #124 (R$ 399,00) com status pendente

**Dados:**
- `corpo assinado`: {"event_id": "evt_qa_124_04", "cobranca_id": 124, "status": "pago", "valor": 399.00}
- `corpo enviado`: {"event_id": "evt_qa_124_04", "cobranca_id": 124, "status": "pago", "valor": 0.01}
- `X-Assinatura`: HMAC-SHA256 do corpo assinado, com o segredo correto

**Passos:**
1. Calcular o HMAC-SHA256 do corpo assinado com o segredo de homologação
2. Enviar POST /webhooks/pix com o corpo enviado (valor 0.01) e a assinatura do corpo assinado
3. Consultar o status da cobrança #124

**Resultado esperado:** Resposta HTTP 401 e a cobrança #124 continua pendente

### CT-05 · Assinatura válida de corpo com espaços e campos em outra ordem é aceita

**Critérios:** CA1, CA2 · **Tipo:** borda · **Técnica:** suposição de erro · **Prioridade:** Média

**Pré-condições:**
- Cobrança #123 (R$ 39,90) com status pendente
- Gateway (ou mock) responde status pago na consulta do Pix da #123

**Dados:**
- `corpo (byte a byte)`: { "valor": 39.90,  "status": "pago", "cobranca_id": 123, "event_id": "evt_qa_123_05" }
- `X-Assinatura`: HMAC-SHA256 desses bytes exatos, com o segredo correto

**Passos:**
1. Calcular o HMAC-SHA256 dos bytes exatos do corpo, sem reformatar o JSON
2. Enviar POST /webhooks/pix com esses mesmos bytes e a assinatura
3. Consultar o status da cobrança #123

**Resultado esperado:** Resposta HTTP 200 e a cobrança #123 fica com status paga

### CT-06 · Reenvio de evento já processado responde 200 sem processar de novo

**Critérios:** CA3 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Alta

> Depende de Suposição: Processar de novo inclui consultar o gateway e registrar VALOR_DIVERGENTE outra vez; por isso a repetição é conferida pela contagem desses registros e das chamadas ao mock

> Depende de Suposição: O ambiente de homologação permite trocar o gateway por um mock que registra chamadas e escolhe a resposta

**Pré-condições:**
- Cobrança #124 (R$ 399,00) já marcada como paga pelo evento evt_qa_124_06 (valor 39.90), que gerou 1 registro VALOR_DIVERGENTE no log de auditoria
- Log de chamadas do mock do gateway zerado depois do primeiro processamento

**Dados:**
- `corpo`: {"event_id": "evt_qa_124_06", "cobranca_id": 124, "status": "pago", "valor": 39.90}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo correto

**Passos:**
1. Reenviar POST /webhooks/pix com o mesmo corpo e a mesma assinatura do primeiro envio
2. Contar os registros VALOR_DIVERGENTE da cobrança #124 no log de auditoria
3. Conferir o log de chamadas do mock do gateway

**Resultado esperado:** Resposta HTTP 200; o log de auditoria continua com 1 registro VALOR_DIVERGENTE para a #124 e o mock do gateway não recebe nenhuma consulta nova

### CT-07 · Dois envios simultâneos do mesmo evento são processados uma única vez

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** suposição de erro · **Prioridade:** Média

> Depende de Suposição: Processar de novo inclui consultar o gateway e registrar VALOR_DIVERGENTE outra vez; por isso a repetição é conferida pela contagem desses registros e das chamadas ao mock

**Pré-condições:**
- Cobrança #124 (R$ 399,00) com status pendente e nenhum registro VALOR_DIVERGENTE
- Gateway (ou mock) responde status pago na consulta do Pix da #124

**Dados:**
- `corpo`: {"event_id": "evt_qa_124_07", "cobranca_id": 124, "status": "pago", "valor": 39.90}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo correto
- `ferramenta`: 2 requisições disparadas em paralelo (ex.: 2 curl em background ou JMeter com 2 threads)

**Passos:**
1. Disparar duas requisições POST /webhooks/pix idênticas ao mesmo tempo
2. Contar os registros VALOR_DIVERGENTE da cobrança #124 no log de auditoria

**Resultado esperado:** As duas respostas são HTTP 200 e o log de auditoria tem exatamente 1 registro VALOR_DIVERGENTE para a #124

### CT-08 · Evento novo de pagamento para a cobrança #125, que já está paga

**Critérios:** CA2, CA3 · **Tipo:** borda · **Técnica:** transição de estado · **Prioridade:** Média

> Depende de D2 (bloqueia)

**Pré-condições:**
- Cobrança #125 (R$ 39,90) já com status paga
- event_id evt_qa_125_08 nunca enviado antes

**Dados:**
- `corpo`: {"event_id": "evt_qa_125_08", "cobranca_id": 125, "status": "pago", "valor": 39.90}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo correto

**Passos:**
1. Enviar POST /webhooks/pix com o corpo e a assinatura
2. Anotar o código HTTP da resposta
3. Consultar o status da cobrança #125

**Resultado esperado:** A cobrança #125 continua com status paga (código HTTP a conferir com a resposta da D2)

### CT-09 · Pagamento menor que a cobrança registra VALOR_DIVERGENTE com os dois valores

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** partição de equivalência · **Prioridade:** Alta

**Pré-condições:**
- Cobrança #124 (R$ 399,00) com status pendente
- Gateway (ou mock) responde status pago na consulta do Pix da #124

**Dados:**
- `corpo`: {"event_id": "evt_qa_124_09", "cobranca_id": 124, "status": "pago", "valor": 39.90}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo correto

**Passos:**
1. Enviar POST /webhooks/pix com o corpo e a assinatura
2. Consultar o log de auditoria da cobrança #124
3. Consultar o status da cobrança #124

**Resultado esperado:** Resposta HTTP 200; o log de auditoria tem um registro VALOR_DIVERGENTE com os valores 399.00 (cobrança) e 39.90 (evento); a cobrança #124 fica com status paga

### CT-10 · Pagamento maior que a cobrança marca a #123 como paga mesmo com divergência

**Critérios:** CA4 · **Tipo:** positivo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Cobrança #123 (R$ 39,90) com status pendente
- Gateway (ou mock) responde status pago na consulta do Pix da #123

**Dados:**
- `corpo`: {"event_id": "evt_qa_123_10", "cobranca_id": 123, "status": "pago", "valor": 40.00}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo correto

**Passos:**
1. Enviar POST /webhooks/pix com o corpo e a assinatura
2. Consultar o status da cobrança #123
3. Consultar o log de auditoria da cobrança #123

**Resultado esperado:** Resposta HTTP 200; a cobrança #123 fica com status paga e o log de auditoria tem um registro VALOR_DIVERGENTE com 39.90 e 40.00

### CT-11 · Diferença de 1 centavo (R$ 39,89 na #123) já registra VALOR_DIVERGENTE

**Critérios:** CA4 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

**Pré-condições:**
- Cobrança #123 (R$ 39,90) com status pendente
- Gateway (ou mock) responde status pago na consulta do Pix da #123

**Dados:**
- `corpo`: {"event_id": "evt_qa_123_11", "cobranca_id": 123, "status": "pago", "valor": 39.89}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo correto

**Passos:**
1. Enviar POST /webhooks/pix com o corpo e a assinatura
2. Consultar o log de auditoria da cobrança #123

**Resultado esperado:** O log de auditoria tem um registro VALOR_DIVERGENTE com 39.90 e 39.89

### CT-12 · Valor igual ao da cobrança (39.90 na #123) não registra VALOR_DIVERGENTE

**Critérios:** CA4 · **Tipo:** negativo · **Técnica:** valor limite · **Prioridade:** Média

**Pré-condições:**
- Cobrança #123 (R$ 39,90) com status pendente e nenhum registro VALOR_DIVERGENTE
- Gateway (ou mock) responde status pago na consulta do Pix da #123

**Dados:**
- `corpo`: {"event_id": "evt_qa_123_12", "cobranca_id": 123, "status": "pago", "valor": 39.90}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo correto

**Passos:**
1. Enviar POST /webhooks/pix com o corpo e a assinatura
2. Consultar o log de auditoria da cobrança #123

**Resultado esperado:** Nenhum registro VALOR_DIVERGENTE para a cobrança #123 no log de auditoria

### CT-13 · API consulta GET /v1/pix/{id} no gateway antes de marcar a cobrança como paga

**Critérios:** CA5 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

> Depende de D1 (bloqueia)

> Depende de Suposição: O ambiente de homologação permite trocar o gateway por um mock que registra chamadas e escolhe a resposta

**Pré-condições:**
- Cobrança #123 (R$ 39,90) com status pendente
- Gateway substituído por mock que registra as chamadas recebidas e responde status pago

**Dados:**
- `corpo`: {"event_id": "evt_qa_123_13", "cobranca_id": 123, "status": "pago", "valor": 39.90}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo correto

**Passos:**
1. Enviar POST /webhooks/pix com o corpo e a assinatura
2. Conferir o log de chamadas do mock
3. Comparar o horário da chamada ao mock com o horário em que a #123 mudou para paga

**Resultado esperado:** O mock recebeu 1 chamada GET /v1/pix/{id} com o identificador definido na D1, antes da mudança da #123 para paga

### CT-14 · Evento assinado que o gateway não confirma não marca a cobrança como paga

**Critérios:** CA5 · **Tipo:** negativo · **Técnica:** tabela de decisão · **Prioridade:** Alta

> Depende de Suposição: Se a consulta ao gateway não confirma o pagamento, a cobrança não é marcada como paga (o CA5 diz que a consulta serve para confirmar, mas não diz o que acontece quando não confirma)

> Depende de Suposição: O ambiente de homologação permite trocar o gateway por um mock que registra chamadas e escolhe a resposta

**Pré-condições:**
- Cobrança #124 (R$ 399,00) com status pendente
- Mock do gateway responde status pendente na consulta do Pix da #124

**Dados:**
- `corpo`: {"event_id": "evt_qa_124_14", "cobranca_id": 124, "status": "pago", "valor": 399.00}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo correto

**Passos:**
1. Enviar POST /webhooks/pix com o corpo e a assinatura
2. Anotar o código HTTP da resposta
3. Consultar o status da cobrança #124

**Resultado esperado:** A cobrança #124 continua pendente (código HTTP a conferir com a resposta da D3)

### CT-15 · Gateway fora do ar na consulta não marca a cobrança como paga

**Critérios:** CA5 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Média

> Depende de Suposição: Se a consulta ao gateway não confirma o pagamento, a cobrança não é marcada como paga (o CA5 diz que a consulta serve para confirmar, mas não diz o que acontece quando não confirma)

> Depende de Suposição: O ambiente de homologação permite trocar o gateway por um mock que registra chamadas e escolhe a resposta

**Pré-condições:**
- Cobrança #123 (R$ 39,90) com status pendente
- Mock do gateway configurado para responder HTTP 503 em GET /v1/pix/{id}

**Dados:**
- `corpo`: {"event_id": "evt_qa_123_15", "cobranca_id": 123, "status": "pago", "valor": 39.90}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo correto

**Passos:**
1. Enviar POST /webhooks/pix com o corpo e a assinatura
2. Anotar o código HTTP da resposta
3. Consultar o status da cobrança #123

**Resultado esperado:** A cobrança #123 continua pendente (código HTTP a conferir com a resposta da D3)

### CT-16 · cobranca_id inexistente (99999) com assinatura válida recebe 404

**Critérios:** CA6 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Não existe cobrança com id 99999 em homologação

**Dados:**
- `corpo`: {"event_id": "evt_qa_99999_16", "cobranca_id": 99999, "status": "pago", "valor": 39.90}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo correto

**Passos:**
1. Enviar POST /webhooks/pix com o corpo e a assinatura

**Resultado esperado:** Resposta HTTP 404

## Fora do escopo

- Criação da cobrança e geração do QR Code Pix
- Política de reenvio do gateway (quantas vezes e com que intervalo ele reenvia)
- Notificação ao cliente depois do pagamento
- Proteção contra replay por timestamp, rotação do segredo e testes de carga do webhook
