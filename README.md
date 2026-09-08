# 🏛️ Enterprise Architecture Case Study - Banco Digital S.A.

Este repositório contém a resolução técnica e estratégica para o case de arquitetura corporativa, utilizando as boas práticas do setor bancário, o framework **TOGAF ADM (Fase A - Architecture Vision)** e os padrões do **Domain-Driven Design (DDD)** implementados em **Python**.

---

## 1. Recomendação Estratégica e Justificativa (Executive Summary)

### **A Escolha: Conta de Pagamentos**
O time de Enterprise Architecture recomenda formalmente a priorização do produto **Conta de Pagamentos** em detrimento do programa de Cashback isolado.

### **Justificativa Estratégica e Financeira**
1. **Fundação da Cadeia de Valor:** A Conta de Pagamentos atua como o "Core Líquido" do banco. É inviável rodar um programa de cashback eficiente e de baixo custo transacional sem uma conta interna para liquidar e reter os valores.
2. **Engajamento Sustentável:** A conta digital centraliza o pagamento de contas (boletos, PIX, DDA) e atrai a folha de pagamento (portabilidade), retendo o saldo do cliente na instituição e aumentando o *LTV (Lifetime Value)*.
3. **Plataforma de Core Bancário:** A aquisição/construção de uma plataforma moderna de Core Bancário (provocada pelo CTO) faz total sentido acoplada à Conta de Pagamentos. Ela servirá para quebrar os silos dos produtos de empréstimo atuais (CDC, Cartões, Consignado), centralizando os saldos e o livro-razão (*ledger*) em uma malha única e escalável.

---

## 2. Mapa de Problemas de Negócios (Subdomínios DDD)

Mapeamento do espaço do problema dividindo o domínio bancário do caso em subdomínios estratégicos:

| Subdomínio | Classificação DDD | Problema Identificado no Legado | Impacto no Negócio |
| :--- | :--- | :--- | :--- |
| **Gestão de Empréstimos (CDC, Consignado)** | *Core Domain* | Construído em silos isolados, sem comunicação entre produtos. | Baixo reaproveitamento, alto *Time-to-Market* para novas linhas de crédito. |
| **Conta de Pagamentos & Ledger** | *Core Domain (Novo)* | Inexistente na arquitetura atual. | Dependência de parceiros ou falta de retenção de saldo. |
| **Cartão de Crédito** | *Core Domain* | Operação legada isolada em silo técnico. | Dificuldade de cruzamento de limites e ofertas integradas. |
| **Autenticação e Cadastro (KYC)** | *Supporting Domain* | Duplicado ou fragmentado entre os silos de produtos atuais. | Atrito na jornada do cliente e ineficiência operacional. |
| **Cashback e Parcerias** | *Generic Domain* | Não prioritário no momento; depende de integrações externas. | Complexidade de contratos que não resolve a fundação do banco. |

---

## 3. Mapa de Capacidades de Negócio (Business Capabilities)

Classificação das capacidades *Top-Level* necessárias para sustentar o estado futuro (**TO-BE**):

### **1. Capacidades Estratégicas (Directional)**
*   **Gestão de Portfólio de Produtos:** Habilidade de configurar e lançar produtos financeiros dinamicamente.
*   **Gestão de Parcerias e Ecossistema:** Capacidade de plugar novos parceiros de negócios (futuro motor de cashback).

### **2. Capacidades de Core (Core Business)**
*   **Gestão de Saldos e Posições (Ledger):** Centralização do livro-razão transacional em tempo real.
*   **Processamento de Pagamentos (PIX, TED, Boletos):** Liquidação de transações de entrada e saída.
*   **Concessão e Ciclo de Vida de Crédito:** Unificação dos motores de análise para CDC, Consignado e Garantias.

### **3. Capacidades de Suporte (Enabling)**
*   **Onboarding & KYC (Know Your Customer):** Cadastro único e verificação de identidade reutilizável por todos os produtos.
*   **Prevenção a Fraude e Riscos:** Motor analítico transversal para avaliar transações e propostas de crédito.

---

## 4. Cadeia de Valor e Fluxo de Interoperabilidade

### **Cadeia de Valor Fim-a-Fim**
```
+---------------------------------------------------------------------------------------+
|                                CAPACIDADES GERENCIAIS                                 |
|         Gestão de Riscos Operacionais   |   Compliance Regulatório (BACEN)            |
+---------------------------------------------------------------------------------------+
|                                 CADEIA DE VALOR FIM-A-FIM                             |
|                                                                                       |
|  [ Atração & Onboarding ] -> [ Transacional / Conta ] -> [ Crédito Integrado ]         |
|  - Cadastro Unificado       - Abertura de Conta          - Motor de Crédito Único     |
|  - KYC Digital              - Transferências (PIX/TED)   - Gestão de Garantias        |
|  - Antifraude               - Consulta de Saldo/Extrato  - Cobrança Transversal       |
+---------------------------------------------------------------------------------------+
|                                CAPACIDADES DE SUPORTE                                 |
|            Core Bancário Centralizado  |  Contabilidade e Ledger Unificado           |
+---------------------------------------------------------------------------------------+
```

### **Interoperabilidade do Fluxo de Valor**
1. **Atração & Cadastro:** Cliente realiza o Onboarding pelo App ──> Aciona o serviço central de **Cadastro/KYC**.
2. **Criação da Conta:** Serviço de **Core Bancário** abre a Conta de Pagamentos e gera o *Ledger* do cliente.
3. **Oferta de Crédito:** O motor de crédito analisa o perfil unificado ──> Disponibiliza limite de CDC diretamente na conta.
4. **Desembolso:** O cliente aceita o empréstimo ──> O valor é liquidado instantaneamente na sua **Conta de Pagamentos**, gerando engajamento imediato e quebrando o isolamento dos silos legados.

---

## 5. Arquitetura Alvo (TO-BE) e Padrões de Microservices

Para evitar os silos e garantir o reaproveitamento sem alterar o estilo arquitetural focado em microserviços, adotamos os seguintes padrões:

*   **Decomposição por Subdomínio (DDD):** Cada microserviço é dono de seu próprio contexto delimitado (*Bounded Context*), isolando dados e regras de negócio.
*   **Database per Service:** Impede que os microserviços acessem o banco de dados uns dos outros, eliminando o acoplamento que gerou os silos legados.
*   **Arquitetura Orientada a Eventos (EDA):** Uso de mensageria (ex: Kafka/RabbitMQ) para comunicação assíncrona e desacoplada.

```
                     [ Canais Digitais (Mobile/Web) ]
                                    |
                            [ API Gateway ]
                                    |
       +----------------------------+----------------------------+
       |                            |                            |
[ Microservice Conta ]    [ Microservice Crédito ]    [ Microservice Cadastro ]
  - Saldo / Extrato         - CDC / Consignado          - KYC / Antifraude
  - PIX / Ledger            - Garantias                 - Dados Cadastrais
       |                            |                            |
[ DB Conta (Isolado) ]    [ DB Crédito (Isolado) ]    [ DB Cadastro (Isolado) ]
       +----------------------------+----------------------------+
                                    | (Eventos de Domínio)
                            [ Message Broker ]
```

---

## 6. Padrão Tático do DDD (Implementação em Python)

O microsserviço de **Conta de Pagamentos** foi modelado isolando as regras de negócio bancárias de preocupações com infraestrutura ou banco de dados.

### **Conceitos Aplicados:**
*   **Aggregate Root (`Account`):** Controla o ciclo de vida da conta e garante a consistência transacional do saldo. Modificações de saldo só ocorrem por métodos de negócio (`credit` e `debit`).
*   **Entity (`Transaction`):** Representa um lançamento com identidade única e imutável no tempo.
*   **Value Objects (`AccountId`, `Amount`):** Objetos imutáveis por definição, que encapsulam validações estritas de domínio (como impedir operações com valores negativos ou zerados).

### **Exemplo do Modelo de Domínio (`domain/account.py`)**

```python
from datetime import datetime
from typing import List, Literal

class AccountId:
    def __init__(self, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("AccountId inválido.")
        self._value = value

    @property
    def value(self) -> str:
        return self._value

class Amount:
    def __init__(self, value: float, currency: str = "BRL"):
        if value <= 0:
            raise ValueError("O valor da operação deve ser maior que zero.")
        self._value = value
        self._currency = currency

    @property
    def value(self) -> float:
        return self._value

class Transaction:
    def __init__(self, transaction_id: str, amount: Amount, transaction_type: Literal['CREDIT', 'DEBIT']):
        self.id = transaction_id
        self.amount = amount
        self.type = transaction_type
        self.created_at = datetime.now()

class Account:
    def __init__(self, account_id: AccountId, initial_balance: float = 0.0):
        self._id = account_id
        self._balance = initial_balance
        self._transactions: List[Transaction] = []
        self._status: Literal['ACTIVE', 'BLOCKED'] = 'ACTIVE'

    @property
    def balance(self) -> float:
        return self._balance

    def debit(self, transaction_id: str, amount: Amount) -> None:
        self._validate_account_state()
        if self._balance < amount.value:
            raise ValueError("Saldo insuficiente para realizar o débito.")

        transaction = Transaction(transaction_id, amount, 'DEBIT')
        self._transactions.append(transaction)
        self._balance -= amount.value

    def credit(self, transaction_id: str, amount: Amount) -> None:
        self._validate_account_state()
        transaction = Transaction(transaction_id, amount, 'CREDIT')
        self._transactions.append(transaction)
        self._balance += amount.value

    def _validate_account_state(self) -> None:
        if self._status != 'ACTIVE':
            raise PermissionError("Operação negada: A conta não está ativa.")
```

---

## 7. Plano de Migração (Estratégia de Transição)

Para extrair o banco do cenário atual de silos sem impactar a operação em produção, adota-se o **Strangler Fig Pattern (Padrão Estrangulador)**:

1. **Fase 1: Abstração com API Layer (Curto Prazo):** Criação de um API Gateway e uma camada BFF (*Backend-For-Frontend*) para unificar a experiência dos canais digitais enquanto os sistemas legados de empréstimo continuam rodando de forma isolada.
2. **Fase 2: Implantação da Conta & Core Moderno (Médio Prazo):** Lançamento do microsserviço de Conta de Pagamentos e o novo Ledger unificado, passando a receber o fluxo transacional primário do banco.
3. **Fase 3: Estrangulamento do Legado (Longo Prazo):** Migração gradual das regras de negócio de cada silo de empréstimo (CDC, Cartões, etc.) para utilizarem as novas capacidades do Core unificado e liquidarem diretamente na nova conta digital. Desativação final dos sistemas legados.