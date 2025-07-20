# 🪙 Gerador de PIX "Copia e Cola" (BR Code) - Multi-Linguagem

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](gerador_pix.py)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](gerador_pix.js)
[![PHP](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white)](gerador_pix.php)
[![Go](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white)](gerador_pix.go)
[![Lua](https://img.shields.io/badge/Lua-2C2D72?style=for-the-badge&logo=lua&logoColor=white)](gerador_pix.lua)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

Este repositório oferece uma coleção de scripts em diversas linguagens de programação (`Python`, `JavaScript/Node.js`, `PHP`, `Go`, `Lua`) para a **geração de códigos "Pix Copia e Cola" estáticos**, também conhecidos como **BR Code**. O objetivo é fornecer uma ferramenta de fácil implementação para desenvolvedores que precisam automatizar cobranças Pix com valor fixo.

## ✨ O que é o "Pix Copia e Cola"?

O "Pix Copia e Cola" é a representação textual de um QR Code do Pix. Ele permite que um usuário compartilhe todas as informações de um pagamento (chave, valor, identificador, mensagem) em um único bloco de texto. Ao colar esse código no aplicativo do banco, todos os campos são preenchidos automaticamente, tornando o processo de pagamento mais rápido e menos propenso a erros.

A estrutura de dados por trás do código segue o padrão **EMV® QRCPS** (QR Code Specification for Payment Systems), que organiza as informações em um formato padronizado chamado **TLV (Type, Length, Value)**.

### Curiosidade: A "Mágica" do CRC16

Um dos últimos componentes do código é o `ID 63`, um CRC16 (Cyclic Redundancy Check). Mas o que ele faz?

> O CRC16 é um código de verificação de redundância cíclica. Ele funciona como uma "soma de verificação" sofisticada de todos os dados do Pix. Antes de exibir os dados do pagamento, o aplicativo do seu banco calcula seu próprio CRC16 a partir do código recebido e o compara com o CRC16 fornecido no final do código. Se os valores não baterem, o aplicativo exibe um erro, garantindo que o código não foi corrompido ou alterado durante a transmissão. É um pequeno, mas poderoso, guardião da integridade dos seus pagamentos.

## 🚀 Como Usar

Cada implementação é autocontida e pode ser executada diretamente para ver um exemplo prático.

### 🐍 Python
```bash
# Necessário Python 3
python gerador_pix.py
```

### 📜 JavaScript (Node.js)
```bash
# Necessário Node.js
node gerador_pix.js
```

### 🐘 PHP
```bash
# Necessário PHP CLI
php gerador_pix.php
```

### 🐹 Go
```bash
# Necessário Go
go run gerador_pix.go
```

### 🌙 Lua
```bash
# Necessário interpretador Lua (ex: 5.1+) com o módulo bit32
lua gerador_pix.lua
```

---

## 🛠️ Integrando em seu Projeto

A lógica pode ser facilmente importada em seus projetos. Veja exemplos básicos abaixo.

#### Exemplo em Python:
```python
from gerador_pix import GeradorPix
# ...
```

#### Exemplo em JavaScript:
```javascript
const GeradorPix = require('./gerador_pix.js');
// ...
```

#### Exemplo em PHP:
```php
require_once 'gerador_pix.php';
$gerador = new GeradorPix(/*...*/);
// ...
```

#### Exemplo em Go:
```go
// main.go
package main

import "fmt"
// ... (importar o pacote local se estruturado)
func main() {
    gerador, err := NewGeradorPix(/*...*/)
    // ...
}
```

#### Exemplo em Lua:
```lua
local GeradorPix = require("gerador_pix")
-- ...
```

## 📚 Estrutura do BR Code (Referência Rápida)

| ID | Obrigatório? | Descrição                      | Exemplo                                |
|----|:------------:|--------------------------------|----------------------------------------|
| 00 |      Sim     | Payload Format Indicator       | `000201`                               |
| 26 |      Sim     | Merchant Account Information   | (Agrupa campos abaixo)                 |
| 52 |      Sim     | Merchant Category Code         | `52040000` (Default)                   |
| 53 |      Sim     | Transaction Currency (BRL)     | `5303986`                              |
| 54 |      Não     | Transaction Amount             | `540510.50` (R$ 10,50)                 |
| 58 |      Sim     | Country Code (BR)              | `5802BR`                               |
| 59 |      Sim     | Merchant Name                  | `5913NOME COMPLETO`                    |
| 60 |      Sim     | Merchant City                  | `6008SAO PAULO`                        |
| 62 |      Não     | Additional Data Field (TxID)   | `62070503***`                          |
| 63 |      Sim     | CRC16                          | `6304XXXX` (Calculado dinamicamente)   |

---

**Palavras-chave para busca (SEO):** Gerador Pix, Pix Copia e Cola, BR Code, EMV QRCPS, Gerador de QR Code Pix, Pix Estático, Python, JavaScript, Node.js, PHP, Go, Golang, Lua, Pagamento Instantâneo, Banco Central, CRC16, TLV.
