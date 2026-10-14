# Trecho da implementação atual (para referência de rotas e campos)
from fastapi import APIRouter, Header, HTTPException

router = APIRouter()

@router.post("/webhooks/pix")
def receber_pix(evento: dict, x_assinatura: str | None = Header(default=None)):
    if not assinatura_valida(evento, x_assinatura):
        raise HTTPException(status_code=401, detail="Assinatura inválida")
    if evento_ja_processado(evento["event_id"]):
        raise HTTPException(status_code=409, detail="Evento já processado")
    cobranca = buscar_cobranca(evento["cobranca_id"])
    if cobranca is None:
        raise HTTPException(status_code=404, detail="Cobrança não encontrada")
    status_gateway = gateway.consultar_status(evento["event_id"])
    if status_gateway == "pago":
        if evento["valor"] != cobranca.valor:
            auditoria.registrar("VALOR_DIVERGENTE", esperado=cobranca.valor, recebido=evento["valor"])
        marcar_como_paga(cobranca)
    return {"ok": True}
