# Técnicas de teste: guia de consulta

Leia a técnica que combina com o requisito. Todos os exemplos são fictícios.

## Partição de equivalência

Divida as entradas em grupos que o sistema trata **do mesmo jeito**. Um caso por grupo basta.

Requisito: "cupom de primeira assinatura só para quem nunca assinou".

| Grupo | Exemplo | Esperado |
|---|---|---|
| Nunca assinou | conta nova | cupom aceito |
| Assinatura ativa | assina o Mensal hoje | cupom recusado |
| Já assinou e cancelou | cancelou em março | cupom recusado ("nunca assinou") |
| Só teste grátis | fez trial e não pagou | **o requisito não diz** → dúvida |

O último grupo é o mais valioso: é onde o requisito é ambíguo e onde o bug costuma estar.

## Valor limite

Bugs se concentram nas bordas (`<` no lugar de `<=`). Para uma faixa `[mín, máx]` teste `mín`, `máx` e, se o usuário consegue informar, `mín - 1` e `máx + 1`, usando a menor unidade que faz sentido (1 caractere, 1 centavo, 1 dia, 1 minuto).

Atenção a limites de **tempo**:
- "em até 7 dias": o dia da contratação é o dia 0 ou o dia 1? Conta em dias corridos ou em 7 × 24 h? Se o requisito não diz, é dúvida, e o caso do limite usa uma suposição registrada.
- "válido até 31/12": inclui o dia 31 inteiro (até 23:59)? Se não está escrito, é dúvida.

## Tabela de decisão

Use quando o resultado depende da **combinação** de duas ou mais condições.

Requisito: "reembolso integral em até 7 dias; depois disso, plano anual tem reembolso proporcional".

| Plano | Dias desde a contratação | Reembolso |
|---|---|---|
| Mensal | ≤ 7 | integral |
| Mensal | > 7 | não diz → **suposição** "sem reembolso" |
| Anual | ≤ 7 | integral |
| Anual | > 7 | proporcional aos meses não usados |

Cada linha vira pelo menos um caso. Linha que o requisito não cobre vira dúvida ou suposição.

## Transição de estado

Use quando a funcionalidade muda o estado de algo (assinatura: ativa → cancelada → expirada). Teste:
- cada transição permitida;
- uma transição **proibida** (cancelar uma assinatura já cancelada);
- o que o usuário pode fazer **em cada estado** (com a assinatura cancelada mas no período pago, ele ainda assiste?).

## Suposição de erro (checklist)

Erros prováveis, para conferir se fazem sentido no requisito:
- Clicar duas vezes no botão de confirmar (cobra ou cancela duas vezes?)
- Desistir no meio (fechar o diálogo, voltar no navegador)
- Campo vazio, só espaços, maiúsculas e minúsculas, acentos
- Valor zero, negativo, centavos que pedem arredondamento
- Sessão expirada no meio do fluxo
- Dois dispositivos ao mesmo tempo
- **Dependência externa fora do ar ou lenta** (LLM, gateway, API de terceiros): o erro dela vira 500 cru ou a resposta prevista?
- **Falso positivo:** a entrada válida dispara o aviso ou o alerta que só deveria aparecer no caso ruim?

Só vire caso o item que se aplica ao requisito. Se o comportamento não está definido, vira dúvida.

## Exemplos: ruim → bom

| Ruim | Problema | Bom |
|---|---|---|
| "Testar cupom válido" | Sem dado, sem resultado | "Cupom NEXI10 em plano de R$ 40,00 → total R$ 36,00" |
| "Sistema exibe mensagem de erro adequada" | "Adequada" não se confere | "Exibe 'Cupom expirado' abaixo do campo" (se a mensagem está no requisito) ou "Total continua R$ 40,00" (se não está) |
| "Exibe erro ou ignora o cupom" | Comportamento indefinido disfarçado de caso | Dúvida para o PO + caso que só afirma o certo |
| "Validar cancelamento e reembolso e e-mail" | Três objetivos | Três casos |
| 8 casos de cupom válido com códigos diferentes | Mesma partição | 1 caso + 1 de maiúsculas/minúsculas (se for regra) |
