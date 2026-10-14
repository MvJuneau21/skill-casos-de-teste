---
name: casos-de-teste
description: Gera casos de teste no padrão de QA da Nexi a partir de uma história de usuário, critérios de aceite, regra de negócio, especificação ou texto solto do PO. Entrega casos positivos, negativos e de borda com passos, dados concretos e resultado esperado verificável, uma matriz de rastreabilidade critério → caso, as dúvidas para o PO e uma planilha .xlsx para executar os testes. Use sempre que o usuário pedir casos de teste, cenários de teste, roteiro de teste, plano de teste, test cases, "o que testar", "como testar essa feature", QA de uma história ou critério de aceite, ou colar uma história/requisito pedindo testes, mesmo sem usar a expressão "caso de teste".
---

# Casos de teste (padrão de QA Nexi)

Gera, a partir de um requisito:

1. **Documento em Markdown** para revisar com PO e dev: dúvidas, cobertura por critério e os casos.
2. **Planilha `.xlsx` de execução** com status por caso (casos bloqueados por dúvida já saem como "Bloqueado"), coluna "Depende de", evidência, bug, rastreabilidade e um resumo que se atualiza sozinho.

Um bom conjunto de casos **acha o bug antes do cliente** e **mostra o que o requisito não diz**. Não é uma lista longa: é a menor lista que cobre cada critério, os limites e os erros prováveis, com resultados que qualquer pessoa do time consegue conferir.

## Arquivos da skill

| Arquivo | Para que serve | Quando usar |
|---|---|---|
| `scripts/gerar_casos.py` | Valida o JSON (cobertura, IDs, resultados vagos) e gera o `.md` e o `.xlsx`. Com `--registrar`, grava o resultado da execução na planilha | Sempre, no final; `--registrar` quando os casos forem executados |
| `references/tecnicas-de-teste.md` | Técnicas (partição, valor limite, tabela de decisão, transição de estado), exemplos bons e ruins, checklist de erros prováveis | Leia quando o requisito tiver números, faixas, combinações de regras ou estados |
| `evals/`, `tests/` | Requisitos de teste com gabarito e testes do script | Só para quem for alterar a skill. Não use como exemplo de resposta |

O script precisa de Python 3.10+ e `openpyxl` (`pip install openpyxl`).

**Caminhos.** `<skill>` é a pasta deste arquivo. `<saida>` é a pasta onde o usuário quer os casos; se ele não disser, use a pasta do arquivo de requisito ou o diretório de trabalho atual. O `casos.json` vai em `<saida>`, nunca dentro de `<skill>`. Chame o script sempre com caminho absoluto.

## Fluxo

### 1. Conferir se dá para começar

Precisa existir **algum requisito**: história, critérios de aceite, regra, print de tela com descrição, ticket, texto do PO.

- Se o pedido for só o nome da funcionalidade ("casos de teste do login"), **não invente as regras**. Faça **uma pergunta só**, juntando o que falta. Exemplo: "Tem a história ou os critérios de aceite do login? Preciso saber principalmente: quantas tentativas antes de bloquear, se tem 'lembrar de mim' e quais mensagens de erro aparecem."
- Se o usuário pedir para seguir sem requisito, gere só o básico que vale para qualquer sistema e marque **cada** regra assumida em `suposicoes`.
- Se o requisito existe mas tem lacunas, **não pergunte antes**: gere os casos e registre as lacunas em `duvidas`. O documento serve justamente para levar essas dúvidas ao PO.
- Se o usuário mandar **o código junto** com o requisito, use o código só para caminhos de rota, nomes de campos, parâmetros e comandos. O **resultado esperado vem do requisito**, nunca do código: um caso escrito olhando a implementação só confirma o que ela já faz e não acha bug. Se o código diverge do requisito (ex.: o requisito diz 200 e o código devolve 409), o caso espera o que o requisito diz, e a divergência vai na resposta ao usuário como provável bug.
- Se dois trechos do requisito **se contradizem** ("pausa de 30, 60 ou 90 dias" e "pausa máxima de 2 meses"), não escolha um lado. Registre a contradição como dúvida que bloqueia os casos afetados e escreva esses casos com o que é certo nos dois trechos.

### 2. Listar os critérios

- Critérios escritos no requisito entram com `"fonte": "explícito"`, com o mesmo ID do requisito (CA1, CA2…), se ele tiver.
- Texto solto ("o usuário pode cancelar a qualquer momento; em até 7 dias tem reembolso") vira critérios que **você** numera, com `"fonte": "derivado"`, um por regra testável.
- Numa história de usuário, o "**para** …" ("para pagar menos na primeira cobrança") é o **objetivo** de quem pediu, não uma regra. Ele não vira critério. Se sugere uma regra que nenhum critério diz (o desconto vale só na primeira cobrança?), isso vira dúvida.
- Uma regra que o texto **implica sem dizer** (ex.: plano mensal cancelado depois de 7 dias não tem reembolso, porque o texto só fala de reembolso nos outros casos) não vira critério nem resultado esperado certo. Vai em `suposicoes`, citando os casos que dependem dela.

### 3. Desenhar os casos

Aplique as regras da próxima seção. Para cada critério, pense nesta ordem:
1. **Caminho feliz:** um caso que prova que a regra funciona.
2. **Partições:** grupos de entradas que o sistema trata igual. Um caso por grupo; dois casos do mesmo grupo são desperdício.
3. **Limites:** todo número, data, tamanho ou faixa do requisito gera casos **no limite e logo depois dele** (ver tabela abaixo).
4. **Negativos:** entrada inválida, usuário sem permissão, estado errado, ação cancelada no meio.
5. **Combinações:** se duas regras interagem (cupom + valor mínimo), um caso com as duas ao mesmo tempo.
6. **Falso positivo:** se uma regra manda o sistema **avisar, alertar ou recusar** algo (aviso de validação, alerta de auditoria, bloqueio), faça também um caso com a entrada válida que **não** deve disparar. Ex.: "valor diferente gera alerta" → "valor igual não gera alerta". Aviso que dispara sempre é tão ruim quanto aviso que nunca dispara.
7. **Dependência externa:** para cada serviço de fora que a funcionalidade usa (LLM, gateway de pagamento, API de terceiros, e-mail, banco), um caso ou uma dúvida para quando ele estiver **fora do ar ou lento**. O resultado esperado só sai do requisito; se ele não diz o que acontece, isso vira dúvida, e o caso afirma só o que é certo (ex.: "a cobrança continua pendente").
8. **Estados:** se a funcionalidade muda o estado de algo (ativa → pausada, ativa → cancelada), faça uma tabela estado × ação e cubra três coisas: a transição permitida, **repetir a ação no estado novo** (pausar o que já está pausado, cancelar o que já foi cancelado) e o que o usuário pode ou não fazer em cada estado. Se o requisito não diz o que acontece numa transição, ela vira dúvida.

### 4. Montar o JSON e gerar

Salve `<saida>/casos.json` no formato mais abaixo e rode:

```bash
python <skill>/scripts/gerar_casos.py <saida>/casos.json --saida <saida>
```

- **ERRO:** nada é gerado. Corrija e rode de novo. "Critério sem nenhum caso" é buraco de cobertura: crie o caso ou, se falta informação para testar, registre uma dúvida apontando para o critério.
- **AVISO:** os arquivos são gerados, mas leia cada aviso. Resultado vago, resultado com "ou", critério só com positivos e prioridade inflada quase sempre são problemas reais: corrija e rode de novo. Mantenha um aviso só se tiver motivo, e diga o motivo na resposta.

### 5. Responder ao usuário

De forma curta:
- quantos casos, quantos por tipo, e a tabela de cobertura (critério → casos);
- **as dúvidas para o PO**, primeiro as que bloqueiam casos (dizendo quais), depois as outras;
- as suposições usadas;
- os caminhos do `.md` e do `.xlsx`.

Não repita todos os casos no chat; eles estão no documento. Se o código veio junto e diverge do requisito, diga isso em destaque: é o achado mais valioso.

### 6. Registrar a execução (quando os casos forem rodados)

Se os casos forem executados (por você ou pelo usuário), não preencha a planilha à mão. Salve `<saida>/resultados.json` e rode:

```bash
python <skill>/scripts/gerar_casos.py <saida>/casos.json --saida <saida> --registrar <saida>/resultados.json
```

```json
{"executado_por": "Camila", "data": "14/10/2026",
 "casos": {"CT-01": {"status": "Passou", "obtido": "Status 401; cobrança continua pendente", "evidencia": "log-execucao.txt"},
           "CT-04": {"status": "Falhou", "obtido": "Status 409", "bug": "Requisito diz 200 (CA3)"}},
 "duvidas": {"D2": "Resposta encontrada na execução: o tipo inválido é ERRO"}}
```

`status` ∈ Não executado, Passou, Falhou, Bloqueado. A execução costuma responder dúvidas: registre a resposta em `duvidas`. Comportamento que aparece na execução e não está no requisito (um aviso não documentado, um status diferente) vai no `obtido` do caso e na resposta ao usuário.

## Regras

Estas regras são o motivo de a skill existir. Casos de teste ruins quase sempre erram em um destes pontos.

**Dúvida que bloqueia x dúvida que não bloqueia.** Em `bloqueia`, liste os casos que **não dá para executar ou julgar** sem a resposta: o resultado esperado depende dela, falta dado de teste ou o requisito se contradiz. Esses casos saem na planilha com status "Bloqueado". Dúvida que só melhora o caso (texto exato da mensagem, fuso horário quando o teste não chega perto da meia-noite) não leva `bloqueia`. Escreva primeiro as que bloqueiam: o PO costuma responder as primeiras da lista. Junte dúvidas parecidas numa só (ex.: "Quais mensagens aparecem para código inexistente e para cupom recusado?" em vez de duas dúvidas). Mantenha **no máximo 8**: o script avisa acima disso, porque uma lista longa não é lida.

**Suposições sempre apontam para casos.** Toda suposição leva `casos` com os casos que mudam se ela estiver errada. A planilha mostra isso na coluna "Depende de", para o testador saber o que olhar quando o PO responder.

**Não invente comportamento.** O resultado esperado precisa vir do requisito. Se o requisito não diz o que acontece (qual mensagem aparece para cupom inexistente, se espaço no código é aceito, como arredondar centavos), **não escreva um caso com a resposta inventada**. Registre em `duvidas`, com o critério e o impacto. Se o caso ainda for útil para descobrir o comportamento, crie-o com resultado esperado que só afirma o que é certo (ex.: "o desconto não é aplicado e o valor continua R$ 39,90") e cite a dúvida no título ou nas pré-condições. Texto de mensagem de erro só vai entre aspas no resultado se estiver **escrito** no requisito.

**Resultado esperado verificável.** Diga o que se vê ou o que se confere: valor na tela, mensagem exata, status no banco, e-mail recebido, botão desabilitado.
- Ruim: "O sistema funciona corretamente", "Desconto aplicado com sucesso", "O vídeo reproduz normalmente", "Exibe erro ou bloqueia".
- Bom: "Total exibido muda de R$ 39,90 para R$ 35,91 e aparece a linha 'Cupom NEXI10 (-10%)'".
- Um "ou" no resultado esperado quase sempre é uma dúvida disfarçada.

**Valores calculados à mão.** Se o resultado tem conta (desconto, reembolso proporcional, juros), faça a conta e escreva o valor final. Escolha dados que **não dependam de uma regra que o requisito não define**: se o arredondamento não está definido, use valores com conta exata (R$ 40,00 × 15% = R$ 6,00) nos casos normais e deixe o arredondamento como dúvida, com **um** caso que o exponha.

**Valor limite.** Todo número do requisito vira casos no limite. Exemplos:

| Requisito | Casos |
|---|---|
| "desconto de 5% a 50%" | 5% e 50% (aceitos); 4% e 51% só se o usuário consegue informar o valor; se for configuração de outro sistema, vai em `fora_do_escopo` ou `duvidas` |
| "em até 7 dias da contratação" | dia 7 (dentro) e dia 8 (fora). Se não estiver claro se conta em dias corridos ou em horas, ou se o dia da contratação é o dia 0 ou o dia 1, vai em `duvidas` |
| "valor final nunca menor que R$ 1,00" | conta que daria exatamente R$ 1,00; conta que daria R$ 0,99 ou menos (vira R$ 1,00) |
| "senha de 8 a 64 caracteres" | 7, 8, 64 e 65 caracteres |
| "até 3 tentativas" | 3ª tentativa errada e 4ª tentativa |

**Um objetivo por caso.** Se o título precisa de "e" para descrever o que testa, provavelmente são dois casos. O script avisa acima de 10 passos.

**Dados concretos.** Nada de "um cupom válido" ou "um usuário qualquer". Escreva: `cupom: NEXI10 (10%, validade 31/12/2026)`, `plano: Mensal R$ 39,90`, `usuário: nunca assinou`. Datas relativas ao momento do teste ("contratado há 7 dias") podem ficar relativas, porque o teste roda em datas diferentes.

**Dado concreto não é comportamento concreto.** Dado de teste pode ser inventado, porque é escolha do testador: `cartão de teste final 4242`, `e-mail qa.cancel01@nexi.test`. O **resultado esperado** só afirma o que o requisito diz. Se o PO diz "tem reembolso" e não diz para onde, escreva "reembolso de R$ 39,90 registrado no gateway", e não "reembolso de R$ 39,90 no cartão final 4242". Antes de gerar, releia cada resultado esperado e pergunte: "o requisito diz isso, ou eu escolhi?". O que você escolheu sai do resultado, ou vira suposição ligada ao caso.

**Negativo confere a ausência de efeito.** Um caso negativo prova que o sistema recusou **e** que nada mudou: "Status 401 **e** a cobrança #123 continua pendente", "código de saída 1 **e** nenhum arquivo gerado". Só o status não basta: uma rota pode devolver 400 depois de ter gravado metade dos dados.

**Passos conforme a interface.**
- **Tela:** "Acessar…", "Clicar em…", "Informar…".
- **API:** "Enviar POST /webhooks/pix com o corpo {…} e o cabeçalho X-Assinatura: …". O resultado tem o status **e** o efeito (dado no banco, evento publicado, log).
- **Linha de comando:** "Rodar `script.py arquivo.json --saida <pasta vazia>`". O resultado tem o código de saída **e** o efeito (arquivos gerados, linhas da saída).

**Pré-condição x passo.** Pré-condição é o estado antes do teste (usuário logado, assinatura ativa há 3 meses). Passo é o que o testador faz. Se uma pré-condição exige manipular data ou banco (simular 8 dias depois), diga isso nela.

**Tipo:**
- `positivo`: entrada válida, a regra funciona.
- `negativo`: entrada inválida, ação proibida, desistência, ou entrada válida que **não** deve disparar um aviso (falso positivo). Prova que o sistema recusa, não faz ou não avisa.
- `borda`: valor exatamente no limite ou logo depois dele, ou combinação de regras no limite.

Todo critério deveria ter pelo menos um caso negativo ou de borda. O script avisa quando não tem.

**Prioridade:** Média é o padrão.
- **Alta:** se falhar, cobra errado, perde dado, expõe dado de outra pessoa ou trava o fluxo principal (não dá para assinar, pagar ou entrar).
- **Baixa:** cosmético, texto, caso raro sem impacto em dinheiro ou dado.

Se mais da metade dos casos ficar Alta, o script avisa: prioridade serve para decidir o que rodar primeiro quando falta tempo.

**Escopo:** teste o que o requisito descreve. Casos genéricos (SQL injection, acessibilidade, performance, navegador) só se o usuário pedir ou se o requisito citar. Coisas relacionadas que ficaram de fora (tela de administração do cupom, reativar assinatura) vão em `fora_do_escopo`, para o time saber que não foram esquecidas.

**Tom:** português, frases curtas, passos no infinitivo ("Acessar…", "Informar…", "Clicar em…"). Títulos dizem a condição e o resultado: "Cupom expirado não é aplicado", e não "Teste de cupom 3".

## Formato do `casos.json`

O exemplo abaixo é ilustrativo, de uma funcionalidade fictícia. Não copie dados dele.

```json
{
  "funcionalidade": "Alterar e-mail da conta",
  "origem": "HIST-208 (texto colado pelo usuário)",
  "criterios": [
    {"id": "CA1", "descricao": "Usuário altera o e-mail informando a senha atual", "fonte": "explícito"},
    {"id": "CA2", "descricao": "Novo e-mail só passa a valer depois de confirmado pelo link", "fonte": "explícito"},
    {"id": "CA3", "descricao": "Link de confirmação vale por 24 horas", "fonte": "derivado"}
  ],
  "casos": [
    {
      "id": "CT-01",
      "titulo": "E-mail é trocado após confirmar pelo link",
      "criterios": ["CA1", "CA2"],
      "tipo": "positivo",
      "tecnica": "caminho feliz",
      "prioridade": "Alta",
      "pre_condicoes": ["Usuário logado com ana@exemplo.com e senha Teste@123"],
      "dados": {"novo e-mail": "ana.nova@exemplo.com", "senha": "Teste@123"},
      "passos": ["Acessar Minha conta > E-mail", "Informar o novo e-mail e a senha", "Clicar em Salvar", "Abrir o link recebido em ana.nova@exemplo.com"],
      "resultado_esperado": "Minha conta mostra ana.nova@exemplo.com; login com ana@exemplo.com deixa de funcionar"
    },
    {
      "id": "CT-02",
      "titulo": "Link aberto 24h01min depois não confirma a troca",
      "criterios": ["CA3"],
      "tipo": "borda",
      "tecnica": "valor limite",
      "prioridade": "Média",
      "pre_condicoes": ["Troca solicitada; relógio do ambiente avançado em 24h01min"],
      "passos": ["Abrir o link de confirmação"],
      "resultado_esperado": "O e-mail da conta continua ana@exemplo.com"
    },
    {
      "id": "CT-03",
      "titulo": "Senha atual errada não inicia a troca",
      "criterios": ["CA1"],
      "tipo": "negativo",
      "tecnica": "partição de equivalência",
      "prioridade": "Média",
      "pre_condicoes": ["Usuário logado com ana@exemplo.com e senha Teste@123"],
      "dados": {"novo e-mail": "ana.nova@exemplo.com", "senha": "Errada@999"},
      "passos": ["Acessar Minha conta > E-mail", "Informar o novo e-mail e a senha errada", "Clicar em Salvar"],
      "resultado_esperado": "Nenhum e-mail chega em ana.nova@exemplo.com e a conta continua com ana@exemplo.com"
    },
    {
      "id": "CT-04",
      "titulo": "Sem abrir o link, o e-mail antigo continua valendo",
      "criterios": ["CA2"],
      "tipo": "negativo",
      "tecnica": "transição de estado",
      "prioridade": "Média",
      "pre_condicoes": ["Troca para ana.nova@exemplo.com solicitada e link ainda não aberto"],
      "passos": ["Sair da conta", "Entrar com ana@exemplo.com e Teste@123"],
      "resultado_esperado": "Login funciona com ana@exemplo.com e Minha conta ainda mostra ana@exemplo.com"
    }
  ],
  "duvidas": [
    {"descricao": "As 24 horas contam a partir do envio do link ou da solicitação?", "criterio": "CA3", "bloqueia": ["CT-02"], "impacto": "Muda o horário do teste de limite"},
    {"descricao": "Qual mensagem aparece ao abrir um link vencido?", "criterio": "CA3", "impacto": "CT-02 confere só o e-mail, não a mensagem"}
  ],
  "suposicoes": [
    {"descricao": "O link antigo deixa de valer quando um novo é pedido", "casos": ["CT-01"]}
  ],
  "fora_do_escopo": ["Troca de e-mail feita pelo suporte"]
}
```

Obrigatórios: `funcionalidade`, `criterios`, `casos`; em cada caso, `id`, `titulo`, `criterios`, `tipo`, `prioridade`, `passos` e `resultado_esperado`. `tipo` ∈ positivo, negativo, borda. `prioridade` ∈ Alta, Média, Baixa. `fonte` ∈ explícito, derivado. `tecnica` ∈ caminho feliz, partição de equivalência, valor limite, tabela de decisão, transição de estado, suposição de erro. `dados` pode ser objeto ou lista. Em `duvidas`, `criterio` pode ser um ID ou uma lista, e `bloqueia` é a lista de casos que não rodam sem a resposta. Em `suposicoes`, `casos` é a lista de casos que dependem dela. IDs dos casos: `CT-01`, `CT-02`…

## Exemplos de uso

**Exemplo 1: história com critérios de aceite**
> Usuário: cola a HIST-321 com CA1 a CA4 e pede "casos de teste pra isso"

Critérios explícitos CA1–CA4 → casos por critério (feliz, partições, limites, negativos) → dúvidas sobre o que os CAs não dizem → `gerar_casos.py` → responder com contagem, cobertura, dúvidas e caminhos.

**Exemplo 2: texto solto do PO**
> Usuário: "o PO mandou isso no Slack, me ajuda a testar: 'o usuário pode pausar a assinatura por até 2 meses, uma vez por ano'"

Critérios derivados: pausar (CA1), limite de 2 meses (CA2), uma vez por ano (CA3). Limites: 2 meses (aceito) e acima de 2 (recusado, se o usuário consegue escolher); segunda pausa no mesmo ano. Dúvidas: "ano" é ano civil ou 12 meses desde a última pausa? O que acontece com a cobrança durante a pausa?

**Exemplo 3: sem requisito**
> Usuário: "gera os casos de teste da tela de login"

Uma única pergunta pedindo a história ou as regras que mudam os casos (bloqueio por tentativas, "lembrar de mim", SSO, mensagens). Só gerar depois da resposta, ou com `suposicoes` explícitas se o usuário pedir para seguir assim.

## Quando NÃO usar

- Escrever o código de testes automatizados (pytest, Cypress, Jest): ajude direto. Os casos desta skill podem servir de base.
- Revisar código ou PR procurando bugs: é outra tarefa.
- Escrever um bug report: responda direto, com passos para reproduzir, esperado e obtido.
