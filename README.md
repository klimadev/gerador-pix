# 🪙 Gerador de PIX "Copia e Cola" (BR Code) - Multi-Linguagem

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](src/python/gerador_pix.py)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](src/javascript/gerador_pix.js)
[![PHP](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white)](src/php/gerador_pix.php)
[![Go](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white)](src/go/gerador_pix.go)
[![Lua](https://img.shields.io/badge/Lua-2C2D72?style=for-the-badge&logo=lua&logoColor=white)](src/lua/gerador_pix.lua)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

Este repositório oferece uma coleção de scripts em diversas linguagens de programação (`Python`, `JavaScript/Node.js`, `PHP`, `Go`, `Lua`) para a **geração de códigos "Pix Copia e Cola" estáticos**, também conhecidos como **BR Code**. O objetivo é fornecer uma ferramenta de fácil implementação para desenvolvedores que precisam automatizar cobranças Pix com valor fixo.

## ✨ O que é o "Pix Copia e Cola"?

O "Pix Copia e Cola" é a representação textual de um QR Code do Pix. Ele permite que um usuário compartilhe todas as informações de um pagamento (chave, valor, identificador, mensagem) em um único bloco de texto. Ao colar esse código no aplicativo do banco, todos os campos são preenchidos automaticamente, tornando o processo de pagamento mais rápido e menos propenso a erros.

A estrutura de dados por trás do código segue o padrão **EMV® QRCPS** (QR Code Specification for Payment Systems), que organiza as informações em um formato padronizado chamado **TLV (Type, Length, Value)**.

### Curiosidade: A "Mágica" do CRC16

Um dos últimos componentes do código é o `ID 63`, um CRC16 (Cyclic Redundancy Check). Mas o que ele faz?

> O CRC16 é um código de verificação de redundância cíclica. Ele funciona como uma "soma de verificação" sofisticada de todos os dados do Pix. Antes de exibir os dados do pagamento, o aplicativo do seu banco calcula seu próprio CRC16 a partir do código recebido e o compara com o CRC16 fornecido no final do código. Se os valores não baterem, o aplicativo exibe um erro, garantindo que o código não foi corrompido ou alterado durante a transmissão. É um pequeno, mas poderoso, guardião da integridade dos seus pagamentos.

## 📁 Estrutura do Projeto

Todos os códigos-fonte estão organizados por linguagem dentro do diretório `src/`:

```
.
├── src
│   ├── python
│   │   └── gerador_pix.py
│   ├── javascript
│   │   └── gerador_pix.js
│   ├── php
│   │   └── gerador_pix.php
│   ├── go
│   │   └── gerador_pix.go
│   └── lua
│       └── gerador_pix.lua
├── .gitignore
└── README.md
```

## 🚀 Como Usar

Cada implementação é autocontida e pode ser executada diretamente para ver um exemplo prático.

### 🐍 Python
```bash
# Necessário Python 3
python src/python/gerador_pix.py
```

### 📜 JavaScript (Node.js)
```bash
# Necessário Node.js
node src/javascript/gerador_pix.js
```

### 🐘 PHP
```bash
# Necessário PHP CLI
php src/php/gerador_pix.php
```

### 🐹 Go
```bash
# Necessário Go
go run src/go/gerador_pix.go
```

### 🌙 Lua
```bash
# Necessário interpretador Lua (ex: 5.1+) com o módulo bit32
lua src/lua/gerador_pix.lua
```

---

## 🛠️ Integrando em seu Projeto

A lógica pode ser facilmente importada em seus projetos. Veja exemplos práticos abaixo.

#### Exemplo em Python:
```python
# Crie um arquivo, por exemplo, 'meu_app.py' na raiz do projeto.
import sys
# Adiciona o diretório do script ao path do Python
sys.path.append('./src/python')

from gerador_pix import GeradorPix

# 1. Crie uma instância do gerador
gerador = GeradorPix(
    chave_pix="seuemail@exemplo.com.br",
    nome_recebedor="NOME DO RECEBEDOR",
    cidade_recebedor="SAO PAULO",
    valor=1.99,
    mensagem="Pagamento do pedido 123",
    txid="PEDIDO123"
)

# 2. Gere o código
codigo = gerador.gerar_codigo()

# 3. Exiba o código
print("Pix Copia e Cola:", codigo)

# Você pode então usar esse 'codigo' para gerar um QR Code
# com bibliotecas como 'qrcode' (pip install qrcode)
# import qrcode
# img = qrcode.make(codigo)
# img.save("pix_qr_code.png")
# print("QR Code salvo como pix_qr_code.png")

```

#### Exemplo em JavaScript:
```javascript
// Crie um arquivo, por exemplo, 'meuApp.js' na raiz do projeto.
const GeradorPix = require('./src/javascript/gerador_pix.js');

// 1. Crie uma instância do gerador
const gerador = new GeradorPix(
    '123.456.789-00',          // Chave PIX (CPF, CNPJ, Celular, Email ou Chave Aleatória)
    'NOME COMPLETO DO LOJISTA',// Nome do recebedor
    'CIDADE',                  // Cidade do recebedor
    99.90,                     // Valor (opcional)
    'Fatura #456',             // Mensagem (opcional)
    'FATURA456'                // TxID (identificador da transação)
);

// 2. Gere o código
const codigoPix = gerador.gerarCodigo();

// 3. Exiba o código
console.log('Código "Copia e Cola":', codigoPix);
```

#### Exemplo em PHP:
```php
<?php
// Crie um arquivo, por exemplo, 'index.php' na raiz do projeto.
require_once 'src/php/gerador_pix.php';

// 1. Crie uma instância do gerador
$gerador = new GeradorPix(
    'a1b2c3d4-e5f6-7890-1234-567890abcdef', // Chave Aleatória
    'EMPRESA XYZ LTDA',
    'BELO HORIZONTE',
    150.00,
    'Servico de Consultoria',
    'CONSULTORIA2024'
);

// 2. Gere o código
$codigoPix = $gerador->gerarCodigo();

// 3. Exiba o código (em um ambiente web, use htmlspecialchars)
echo '<h1>Pague com Pix</h1>';
echo '<p>Código Copia e Cola:</p>';
echo '<pre>' . htmlspecialchars($codigoPix) . '</pre>';
?>
```

#### Exemplo em Go:
```go
// Para usar o código de 'src/go', você precisaria estruturá-lo como um módulo Go.
// 1. Vá para a raiz do seu projeto e inicie um módulo:
//    go mod init meurepositorio.com/pix
// 2. Crie um arquivo 'main.go' na raiz:

// main.go
package main

import (
	"fmt"
	"log"
	pix "meurepositorio.com/pix/src/go" // Importando o pacote local
)

func main() {
	// 1. Crie uma instância do gerador
	gerador, err := pix.NewGeradorPix(
		"+5511987654321",         // Chave PIX (Celular)
		"ANA SOUZA",              // Nome do recebedor
		"SALVADOR",               // Cidade
		"Servico de Manutencao",  // Mensagem (opcional)
		"MANUT01",                // TxID
		250.75,                   // Valor (opcional)
	)
	if err != nil {
		log.Fatal("Erro ao criar gerador PIX:", err)
	}

	// 2. Gere o código
	codigo, err := gerador.GerarCodigo()
	if err != nil {
		log.Fatal("Erro ao gerar código PIX:", err)
	}

	// 3. Exiba o código
	fmt.Println("Código PIX:", codigo)
}
```

#### Exemplo em Lua:
```lua
-- Crie um arquivo, por exemplo, 'main.lua' na raiz do projeto.

-- Adicione o diretório do script ao package.path do Lua
package.path = package.path .. ';./src/lua/?.lua'

-- Importe a classe
local GeradorPix = require("gerador_pix")

-- 1. Crie uma instância
-- (chave_pix, nome_recebedor, cidade_recebedor, valor, mensagem, txid)
local gerador = GeradorPix:new(
    "chavealeatoria-1234-abcd-efgh-9876543210",
    "MARIA OLIVEIRA",
    "CURITIBA",
    "50.00",
    "Pagamento de produto X",
    "PRODX_PGTO_1"
)

-- 2. Gere o código
local codigo_pix = gerador:gerar_codigo()

-- 3. Exiba o resultado
print("--- Pagamento via PIX ---")
print("Código Copia e Cola: " .. codigo_pix)
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
