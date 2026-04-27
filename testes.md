#  Projeto: Controle Financeiro com IA

## Funcionalidades Principais

### funcionalidade 1. Cadastro e Login de Usuário
Permite que o usuário se registre e acesse o sistema com autenticação.
## 2. Regras de Negócio
### precondição:
 Cadastro e Login
 O login só é permitido com credenciais corretas.
### entrada:
 O usuário deve informar username e password.
### Ação: 
 cadastrar usuário e realizar login com dados corretos
### Resultado esperado: 
retorno `status: ok` e `user_id`
### Tipo: 
Integração

### Teste 1 Ação: 
tentar login com senha incorreta
### Resultado esperado:
 erro `401`
### Tipo: 
Integração

___

##  Funcionalidade 2: Controle Financeiro
### funcionalidade 2. Controle de Entradas e Saídas
Permite registrar movimentações financeiras e calcular o saldo automaticamente.

###  Controle Financeiro
Cada transação deve conter:
   descrição
   valor
   tipo (entrada ou saída)
O saldo é calculado por:
  
    saldo = entradas - saídas

### Ação: 
EX. adicionar entrada de R$100 e saída de R$40
### Resultado esperado: 
saldo = R$60
### Tipo: 
Integração

#### Caso teste
 Ação: tentar adicionar transação sem preencher campos
 Resultado esperado: sistema bloqueia ou exibe alerta
 Tipo: E2E

____



### funcionalidade 3. Integração com IA (Gemini)
Permite ao usuário fazer perguntas financeiras e receber respostas da IA.

###  Integração com IA
 O usuário pode enviar perguntas para a IA.
 O backend deve encaminhar para a API Gemini.
 A resposta deve ser retornada ao usuário.
 A chave da API deve estar protegida no `.env`.


###  Funcionalidade 3: IA

 enviar pergunta "Me dê uma dica financeira para economizar"
 Resultado esperado: resposta da IA (Status 200)
 Tipo: Integração

####  Caso teste
### Ação: 
executar sem chave válida da API
### Resultado esperado:
 erro de autenticação 
### Tipo:
 Integração