# HIST-510 · Webhook de confirmação de pagamento Pix

O gateway de pagamento chama `POST /webhooks/pix` quando um Pix muda de status.

Corpo: `{"event_id": "evt_...", "cobranca_id": 123, "status": "pago", "valor": 39.90}`
Cabeçalho: `X-Assinatura: <HMAC-SHA256 do corpo com o segredo do gateway>`

## Critérios de aceite

- **CA1.** Assinatura ausente ou inválida: responder 401 e não alterar a cobrança.
- **CA2.** Evento com `status = pago`: a cobrança passa para `paga` e a resposta é 200.
- **CA3.** Evento repetido (mesmo `event_id` já processado): responder 200 sem processar de novo. O gateway reenvia o mesmo evento quando não recebe 200.
- **CA4.** Se o `valor` do evento for diferente do valor da cobrança, registrar no log de auditoria o alerta `VALOR_DIVERGENTE` com os dois valores. A cobrança é marcada como paga mesmo assim.
- **CA5.** Antes de marcar como paga, a API consulta o status no gateway (`GET /v1/pix/{id}` do gateway) para confirmar que o evento é verdadeiro.
- **CA6.** `cobranca_id` que não existe: responder 404.

Cobranças de homologação: #123 (R$ 39,90, pendente), #124 (R$ 399,00, pendente), #125 (R$ 39,90, já paga).
