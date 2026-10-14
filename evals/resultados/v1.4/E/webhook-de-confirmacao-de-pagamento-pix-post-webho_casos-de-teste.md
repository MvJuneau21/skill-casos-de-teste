# Casos de teste: Webhook de confirmação de pagamento Pix (POST /webhooks/pix)

**Origem:** HIST-510 (requisito.md) + trecho de webhook_controller.py usado só para rota, campos e cabeçalho · **Gerado em:** 14/10/2026

**18 casos:** 4 positivos, 8 negativos, 6 de borda · **Prioridade:** 6 Alta, 11 Média, 1 Baixa

## Pontos a confirmar com o PO

**Dúvidas que bloqueiam a execução** (responder primeiro):

- **D1.** Em GET /v1/pix/{id}, o {id} é o cobranca_id, o event_id ou um id do Pix no gateway? O código atual consulta com o event_id. _(CA5 · bloqueia CT-12 · Sem isso não dá para conferir se a consulta certa foi feita; consultar o id errado pode confirmar evento falso)_
- **D2.** Se o gateway está fora do ar ou lento na consulta, qual status a API responde e o evento fica marcado como processado? Como o gateway só reenvia quando não recebe 200, responder 200 ou marcar o evento como processado perde o pagamento. _(CA5, CA3 · bloqueia CT-15 · CT-14 confere só que a cobrança continua pendente; CT-15 depende da resposta. Há timeout definido para a consulta?)_

**Outras dúvidas** (o requisito não diz; nenhum caso inventa a resposta):

- **D3.** Quando o gateway não confirma o evento (responde status diferente de pago), qual status a API responde e deve registrar algum alerta de auditoria? _(CA5 · CT-13 confere só a cobrança; o código atual responde 200 {"ok": true} sem marcar nada)_
- **D4.** O que fazer com eventos de status diferente de pago (expirado, cancelado, devolvido)? A cobrança muda de status? Qual resposta? _(CA2 · CT-18 confere só que a cobrança não fica paga; o código atual ignora o campo status do evento e usa só o status do gateway)_
- **D5.** Novo event_id de pagamento para uma cobrança já paga (#125): responder 200, registrar alerta de pagamento em duplicidade, gerar estorno? _(CA2 · CT-17 confere só que a cobrança continua paga; possível cobrança em duplicidade sem rastro)_
- **D6.** O 404 de cobranca_id inexistente faz o gateway reenviar o evento (ele reenvia quando não recebe 200). Isso é o desejado? Há limite de reenvios? _(CA6 · Não muda o CT-16, mas pode gerar reenvio sem fim)_
- **D7.** Em que formato os dois valores vão no registro VALOR_DIVERGENTE (campos, casas decimais) e o registro inclui cobranca_id e event_id? _(CA4 · CT-09 e CT-10 conferem só que os dois valores aparecem)_
- **D8.** Qual resposta para corpo malformado ou sem campos obrigatórios (sem event_id, valor como texto)? _(CA1, CA2 · Sem caso escrito; hoje o código provavelmente devolve 500)_

**Suposições** (usadas nos casos; se estiverem erradas, os casos indicados mudam):

- Evento com status diferente de pago não marca a cobrança como paga (o requisito só define o que fazer com status pago) _(CT-18)_
- O ambiente de homologação tem mock ou sandbox do gateway que registra as requisições recebidas e permite configurar o status devolvido e simular indisponibilidade (503) _(CT-06, CT-12, CT-13, CT-14, CT-15)_
- As cobranças #123 e #124 voltam para pendente, e o log de auditoria é limpo, antes de cada caso que as usa como pendentes _(CT-01, CT-02, CT-03, CT-04, CT-05, CT-09, CT-10, CT-11, CT-12, CT-13, CT-14, CT-18)_

## Critérios e cobertura

| Critério | Descrição | Casos | Dúvidas |
|---|---|---|---|
| CA1 | Assinatura ausente ou inválida: responder 401 e não alterar a cobrança | CT-02, CT-03, CT-04, CT-05 | D8 |
| CA2 | Evento com status = pago: a cobrança passa para paga e a resposta é 200 | CT-01, CT-05, CT-09, CT-17, CT-18 | D4, D5, D8 |
| CA3 | Evento repetido (mesmo event_id já processado): responder 200 sem processar de novo | CT-06, CT-07, CT-08, CT-15 | D2 |
| CA4 | Valor do evento diferente do valor da cobrança: registrar VALOR_DIVERGENTE com os dois valores no log de auditoria; a cobrança é marcada como paga mesmo assim | CT-08, CT-09, CT-10, CT-11 | D7 |
| CA5 | Antes de marcar como paga, a API consulta o status no gateway (GET /v1/pix/{id}) para confirmar que o evento é verdadeiro | CT-12, CT-13, CT-14, CT-15 | D1, D2, D3 |
| CA6 | cobranca_id inexistente: responder 404 | CT-16 | D6 |

## Casos

### CT-01 · Evento pago com assinatura válida marca a cobrança #123 como paga

**Critérios:** CA2 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Alta

> Depende de Suposição: As cobranças #123 e #124 voltam para pendente, e o log de auditoria é limpo, antes de cada caso que as usa como pendentes

**Pré-condições:**
- Cobrança #123 (R$ 39,90) com status pendente
- Mock/sandbox do gateway responde status pago para o Pix da cobrança #123
- event_id evt_hist510_01 nunca enviado

**Dados:**
- `corpo`: {"event_id": "evt_hist510_01", "cobranca_id": 123, "status": "pago", "valor": 39.90}
- `X-Assinatura`: HMAC-SHA256 do corpo exato com o segredo de homologação do gateway

**Passos:**
1. Calcular o HMAC-SHA256 do corpo com o segredo de homologação
2. Enviar POST /webhooks/pix com o corpo e o cabeçalho X-Assinatura calculado
3. Consultar o status da cobrança #123 no banco

**Resultado esperado:** Status HTTP 200 e a cobrança #123 fica com status paga

### CT-02 · Requisição sem cabeçalho X-Assinatura é recusada com 401

**Critérios:** CA1 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Alta

> Depende de Suposição: As cobranças #123 e #124 voltam para pendente, e o log de auditoria é limpo, antes de cada caso que as usa como pendentes

**Pré-condições:**
- Cobrança #123 (R$ 39,90) com status pendente
- Mock do gateway responde status pago para a cobrança #123

**Dados:**
- `corpo`: {"event_id": "evt_hist510_02", "cobranca_id": 123, "status": "pago", "valor": 39.90}
- `X-Assinatura`: (não enviar)

**Passos:**
1. Enviar POST /webhooks/pix com o corpo e sem o cabeçalho X-Assinatura
2. Consultar o status da cobrança #123 no banco

**Resultado esperado:** Status HTTP 401 e a cobrança #123 continua pendente

### CT-03 · Assinatura calculada com segredo errado é recusada com 401

**Critérios:** CA1 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Alta

> Depende de Suposição: As cobranças #123 e #124 voltam para pendente, e o log de auditoria é limpo, antes de cada caso que as usa como pendentes

**Pré-condições:**
- Cobrança #123 (R$ 39,90) com status pendente
- Mock do gateway responde status pago para a cobrança #123

**Dados:**
- `corpo`: {"event_id": "evt_hist510_03", "cobranca_id": 123, "status": "pago", "valor": 39.90}
- `segredo usado`: segredo-errado-qa
- `X-Assinatura`: HMAC-SHA256 do corpo com segredo-errado-qa

**Passos:**
1. Calcular o HMAC-SHA256 do corpo com o segredo segredo-errado-qa
2. Enviar POST /webhooks/pix com o corpo e o cabeçalho X-Assinatura calculado
3. Consultar o status da cobrança #123 no banco

**Resultado esperado:** Status HTTP 401 e a cobrança #123 continua pendente

### CT-04 · Corpo alterado depois de assinado é recusado com 401

**Critérios:** CA1 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Média

> Depende de Suposição: As cobranças #123 e #124 voltam para pendente, e o log de auditoria é limpo, antes de cada caso que as usa como pendentes

**Pré-condições:**
- Cobrança #124 (R$ 399,00) com status pendente
- Mock do gateway responde status pago para a cobrança #124

**Dados:**
- `corpo assinado`: {"event_id": "evt_hist510_04", "cobranca_id": 124, "status": "pago", "valor": 399.00}
- `corpo enviado`: {"event_id": "evt_hist510_04", "cobranca_id": 124, "status": "pago", "valor": 0.01}
- `X-Assinatura`: HMAC-SHA256 do corpo assinado com o segredo de homologação

**Passos:**
1. Calcular o HMAC-SHA256 do corpo assinado com o segredo de homologação
2. Enviar POST /webhooks/pix com o corpo enviado (valor 0.01) e o cabeçalho X-Assinatura calculado
3. Consultar o status da cobrança #124 no banco e o log de auditoria

**Resultado esperado:** Status HTTP 401, a cobrança #124 continua pendente e o log de auditoria não tem registro do evt_hist510_04

### CT-05 · Corpo com espaços e ordem de campos diferentes, assinado corretamente, é aceito

**Critérios:** CA1, CA2 · **Tipo:** borda · **Técnica:** suposição de erro · **Prioridade:** Média

> Depende de Suposição: As cobranças #123 e #124 voltam para pendente, e o log de auditoria é limpo, antes de cada caso que as usa como pendentes

**Pré-condições:**
- Cobrança #123 (R$ 39,90) com status pendente
- Mock do gateway responde status pago para a cobrança #123

**Dados:**
- `corpo (bytes exatos)`: { "valor": 39.90,  "status": "pago", "cobranca_id": 123, "event_id": "evt_hist510_05" }
- `X-Assinatura`: HMAC-SHA256 desses bytes exatos com o segredo de homologação

**Passos:**
1. Calcular o HMAC-SHA256 dos bytes exatos do corpo com o segredo de homologação
2. Enviar POST /webhooks/pix com esses mesmos bytes e o cabeçalho X-Assinatura calculado
3. Consultar o status da cobrança #123 no banco

**Resultado esperado:** Status HTTP 200 e a cobrança #123 fica com status paga

### CT-06 · Reenvio do mesmo event_id responde 200

**Critérios:** CA3 · **Tipo:** positivo · **Técnica:** transição de estado · **Prioridade:** Alta

> Depende de Suposição: O ambiente de homologação tem mock ou sandbox do gateway que registra as requisições recebidas e permite configurar o status devolvido e simular indisponibilidade (503)

**Pré-condições:**
- CT-01 executado: evt_hist510_01 processado e cobrança #123 paga
- Mock do gateway com o contador de chamadas zerado depois do CT-01

**Dados:**
- `corpo`: {"event_id": "evt_hist510_01", "cobranca_id": 123, "status": "pago", "valor": 39.90}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo de homologação

**Passos:**
1. Enviar POST /webhooks/pix com o mesmo corpo e assinatura do CT-01
2. Conferir o contador de chamadas GET /v1/pix no mock do gateway
3. Consultar o status da cobrança #123 no banco

**Resultado esperado:** Status HTTP 200, o mock do gateway registra 0 chamadas novas e a cobrança #123 continua paga

### CT-07 · event_id já processado com outra cobrança no corpo não altera a cobrança #124

**Critérios:** CA3 · **Tipo:** borda · **Técnica:** suposição de erro · **Prioridade:** Média

**Pré-condições:**
- evt_hist510_01 já processado (CT-01)
- Cobrança #124 (R$ 399,00) com status pendente
- Mock do gateway responde status pago para a cobrança #124

**Dados:**
- `corpo`: {"event_id": "evt_hist510_01", "cobranca_id": 124, "status": "pago", "valor": 399.00}
- `X-Assinatura`: HMAC-SHA256 deste corpo com o segredo de homologação

**Passos:**
1. Calcular o HMAC-SHA256 do corpo com o segredo de homologação
2. Enviar POST /webhooks/pix com o corpo e o cabeçalho X-Assinatura calculado
3. Consultar o status da cobrança #124 no banco

**Resultado esperado:** Status HTTP 200 e a cobrança #124 continua pendente

### CT-08 · Reenvio de evento com valor divergente não gera segundo alerta VALOR_DIVERGENTE

**Critérios:** CA3, CA4 · **Tipo:** borda · **Técnica:** tabela de decisão · **Prioridade:** Média

**Pré-condições:**
- CT-09 executado: evt_hist510_09 processado, cobrança #124 paga e 1 alerta VALOR_DIVERGENTE no log

**Dados:**
- `corpo`: {"event_id": "evt_hist510_09", "cobranca_id": 124, "status": "pago", "valor": 39.90}
- `X-Assinatura`: a mesma do CT-09

**Passos:**
1. Enviar POST /webhooks/pix com o mesmo corpo e assinatura do CT-09
2. Contar os registros VALOR_DIVERGENTE da cobrança #124 no log de auditoria

**Resultado esperado:** Status HTTP 200 e o log de auditoria continua com exatamente 1 registro VALOR_DIVERGENTE da cobrança #124

### CT-09 · Valor menor que o da cobrança registra VALOR_DIVERGENTE e marca a cobrança #124 como paga

**Critérios:** CA4, CA2 · **Tipo:** positivo · **Técnica:** partição de equivalência · **Prioridade:** Alta

> Depende de Suposição: As cobranças #123 e #124 voltam para pendente, e o log de auditoria é limpo, antes de cada caso que as usa como pendentes

**Pré-condições:**
- Cobrança #124 (R$ 399,00) com status pendente
- Mock do gateway responde status pago para a cobrança #124
- Log de auditoria sem registros da cobrança #124

**Dados:**
- `corpo`: {"event_id": "evt_hist510_09", "cobranca_id": 124, "status": "pago", "valor": 39.90}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo de homologação

**Passos:**
1. Calcular o HMAC-SHA256 do corpo com o segredo de homologação
2. Enviar POST /webhooks/pix com o corpo e o cabeçalho X-Assinatura calculado
3. Consultar o log de auditoria
4. Consultar o status da cobrança #124 no banco

**Resultado esperado:** Status HTTP 200; o log de auditoria tem 1 registro VALOR_DIVERGENTE com os valores 399,00 (cobrança) e 39,90 (evento); a cobrança #124 fica com status paga

### CT-10 · Diferença de 1 centavo registra VALOR_DIVERGENTE

**Critérios:** CA4 · **Tipo:** borda · **Técnica:** valor limite · **Prioridade:** Média

> Depende de Suposição: As cobranças #123 e #124 voltam para pendente, e o log de auditoria é limpo, antes de cada caso que as usa como pendentes

**Pré-condições:**
- Cobrança #123 (R$ 39,90) com status pendente
- Mock do gateway responde status pago para a cobrança #123
- Log de auditoria sem registros da cobrança #123

**Dados:**
- `corpo`: {"event_id": "evt_hist510_10", "cobranca_id": 123, "status": "pago", "valor": 39.89}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo de homologação

**Passos:**
1. Calcular o HMAC-SHA256 do corpo com o segredo de homologação
2. Enviar POST /webhooks/pix com o corpo e o cabeçalho X-Assinatura calculado
3. Consultar o log de auditoria e o status da cobrança #123

**Resultado esperado:** Status HTTP 200; o log de auditoria tem 1 registro VALOR_DIVERGENTE com os valores 39,90 e 39,89; a cobrança #123 fica com status paga

### CT-11 · Valor igual ao da cobrança não gera alerta VALOR_DIVERGENTE

**Critérios:** CA4 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Média

> Depende de Suposição: As cobranças #123 e #124 voltam para pendente, e o log de auditoria é limpo, antes de cada caso que as usa como pendentes

**Pré-condições:**
- Cobrança #123 (R$ 39,90) com status pendente
- Mock do gateway responde status pago para a cobrança #123
- Log de auditoria sem registros da cobrança #123

**Dados:**
- `corpo`: {"event_id": "evt_hist510_11", "cobranca_id": 123, "status": "pago", "valor": 39.90}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo de homologação

**Passos:**
1. Calcular o HMAC-SHA256 do corpo com o segredo de homologação
2. Enviar POST /webhooks/pix com o corpo e o cabeçalho X-Assinatura calculado
3. Consultar o log de auditoria da cobrança #123

**Resultado esperado:** Status HTTP 200 e o log de auditoria tem 0 registros VALOR_DIVERGENTE da cobrança #123

### CT-12 · API consulta GET /v1/pix/{id} no gateway antes de marcar a cobrança como paga

**Critérios:** CA5 · **Tipo:** positivo · **Técnica:** caminho feliz · **Prioridade:** Média

> Depende de D1 (bloqueia)

> Depende de Suposição: O ambiente de homologação tem mock ou sandbox do gateway que registra as requisições recebidas e permite configurar o status devolvido e simular indisponibilidade (503)

> Depende de Suposição: As cobranças #123 e #124 voltam para pendente, e o log de auditoria é limpo, antes de cada caso que as usa como pendentes

**Pré-condições:**
- Cobrança #123 (R$ 39,90) com status pendente
- Mock do gateway registra as requisições recebidas, com horário
- Bloqueado por D1: qual valor vai em {id}

**Dados:**
- `corpo`: {"event_id": "evt_hist510_12", "cobranca_id": 123, "status": "pago", "valor": 39.90}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo de homologação

**Passos:**
1. Calcular o HMAC-SHA256 do corpo com o segredo de homologação
2. Enviar POST /webhooks/pix com o corpo e o cabeçalho X-Assinatura calculado
3. Conferir as requisições registradas no mock do gateway
4. Comparar o horário da requisição ao gateway com o horário da atualização da cobrança #123

**Resultado esperado:** O mock do gateway registra 1 chamada GET /v1/pix/{id} com o id definido em D1, antes da atualização da cobrança #123 para paga

### CT-13 · Evento pago que o gateway não confirma não marca a cobrança como paga

**Critérios:** CA5 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Alta

> Depende de Suposição: O ambiente de homologação tem mock ou sandbox do gateway que registra as requisições recebidas e permite configurar o status devolvido e simular indisponibilidade (503)

> Depende de Suposição: As cobranças #123 e #124 voltam para pendente, e o log de auditoria é limpo, antes de cada caso que as usa como pendentes

**Pré-condições:**
- Cobrança #124 (R$ 399,00) com status pendente
- Mock do gateway configurado para responder status pendente para o Pix da cobrança #124

**Dados:**
- `corpo`: {"event_id": "evt_hist510_13", "cobranca_id": 124, "status": "pago", "valor": 399.00}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo de homologação

**Passos:**
1. Calcular o HMAC-SHA256 do corpo com o segredo de homologação
2. Enviar POST /webhooks/pix com o corpo e o cabeçalho X-Assinatura calculado
3. Anotar o status HTTP (ver D3)
4. Consultar o status da cobrança #124 no banco

**Resultado esperado:** A cobrança #124 continua pendente

### CT-14 · Gateway fora do ar na consulta não marca a cobrança como paga

**Critérios:** CA5 · **Tipo:** negativo · **Técnica:** suposição de erro · **Prioridade:** Média

> Depende de Suposição: O ambiente de homologação tem mock ou sandbox do gateway que registra as requisições recebidas e permite configurar o status devolvido e simular indisponibilidade (503)

> Depende de Suposição: As cobranças #123 e #124 voltam para pendente, e o log de auditoria é limpo, antes de cada caso que as usa como pendentes

**Pré-condições:**
- Cobrança #123 (R$ 39,90) com status pendente
- Mock do gateway configurado para responder 503 em GET /v1/pix/{id}

**Dados:**
- `corpo`: {"event_id": "evt_hist510_14", "cobranca_id": 123, "status": "pago", "valor": 39.90}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo de homologação

**Passos:**
1. Calcular o HMAC-SHA256 do corpo com o segredo de homologação
2. Enviar POST /webhooks/pix com o corpo e o cabeçalho X-Assinatura calculado
3. Anotar o status HTTP (ver D2)
4. Consultar o status da cobrança #123 no banco

**Resultado esperado:** A cobrança #123 continua pendente

### CT-15 · Reenvio do evento depois que o gateway volta marca a cobrança como paga

**Critérios:** CA5, CA3 · **Tipo:** borda · **Técnica:** transição de estado · **Prioridade:** Média

> Depende de D2 (bloqueia)

> Depende de Suposição: O ambiente de homologação tem mock ou sandbox do gateway que registra as requisições recebidas e permite configurar o status devolvido e simular indisponibilidade (503)

**Pré-condições:**
- CT-14 executado: evt_hist510_14 recebido com gateway fora do ar e cobrança #123 pendente
- Mock do gateway volta a responder status pago para a cobrança #123
- Bloqueado por D2: o evento recebido com gateway fora do ar conta como processado?

**Dados:**
- `corpo`: {"event_id": "evt_hist510_14", "cobranca_id": 123, "status": "pago", "valor": 39.90}
- `X-Assinatura`: a mesma do CT-14

**Passos:**
1. Enviar POST /webhooks/pix com o mesmo corpo e assinatura do CT-14
2. Consultar o status da cobrança #123 no banco

**Resultado esperado:** Status HTTP 200 e a cobrança #123 fica com status paga

### CT-16 · cobranca_id inexistente responde 404

**Critérios:** CA6 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Média

**Pré-condições:**
- Nenhuma cobrança com id 999999 no banco
- Cobranças #123 e #124 pendentes e #125 paga

**Dados:**
- `corpo`: {"event_id": "evt_hist510_16", "cobranca_id": 999999, "status": "pago", "valor": 39.90}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo de homologação

**Passos:**
1. Calcular o HMAC-SHA256 do corpo com o segredo de homologação
2. Enviar POST /webhooks/pix com o corpo e o cabeçalho X-Assinatura calculado
3. Consultar o status das cobranças #123, #124 e #125 e o log de auditoria

**Resultado esperado:** Status HTTP 404; #123 e #124 continuam pendentes, #125 continua paga e o log de auditoria não tem registro do evt_hist510_16

### CT-17 · Novo evento pago para a cobrança #125, já paga, mantém a cobrança paga

**Critérios:** CA2 · **Tipo:** borda · **Técnica:** transição de estado · **Prioridade:** Baixa

**Pré-condições:**
- Cobrança #125 (R$ 39,90) com status paga
- Mock do gateway responde status pago para a cobrança #125

**Dados:**
- `corpo`: {"event_id": "evt_hist510_17", "cobranca_id": 125, "status": "pago", "valor": 39.90}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo de homologação

**Passos:**
1. Calcular o HMAC-SHA256 do corpo com o segredo de homologação
2. Enviar POST /webhooks/pix com o corpo e o cabeçalho X-Assinatura calculado
3. Anotar o status HTTP (ver D5)
4. Consultar o status e a data de pagamento da cobrança #125

**Resultado esperado:** A cobrança #125 continua com status paga

### CT-18 · Evento com status diferente de pago não marca a cobrança como paga

**Critérios:** CA2 · **Tipo:** negativo · **Técnica:** partição de equivalência · **Prioridade:** Média

> Depende de Suposição: Evento com status diferente de pago não marca a cobrança como paga (o requisito só define o que fazer com status pago)

> Depende de Suposição: As cobranças #123 e #124 voltam para pendente, e o log de auditoria é limpo, antes de cada caso que as usa como pendentes

**Pré-condições:**
- Cobrança #123 (R$ 39,90) com status pendente
- Mock do gateway responde status expirado para a cobrança #123

**Dados:**
- `corpo`: {"event_id": "evt_hist510_18", "cobranca_id": 123, "status": "expirado", "valor": 39.90}
- `X-Assinatura`: HMAC-SHA256 do corpo com o segredo de homologação

**Passos:**
1. Calcular o HMAC-SHA256 do corpo com o segredo de homologação
2. Enviar POST /webhooks/pix com o corpo e o cabeçalho X-Assinatura calculado
3. Anotar o status HTTP (ver D4)
4. Consultar o status da cobrança #123 no banco

**Resultado esperado:** A cobrança #123 não fica com status paga

## Fora do escopo

- Geração e rotação do segredo do gateway
- Criação da cobrança Pix e geração do QR Code
- Notificação ao assinante após o pagamento
- Tela ou consulta do log de auditoria
- Política de reenvio do próprio gateway (intervalos e limite)
- Segurança genérica (rate limit, SQL injection) e performance
