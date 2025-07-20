# Gerador de PIX "Copia e Cola" (BR Code)

Este projeto contém um script Python (`gerador_pix.py`) para criar códigos "Pix Copia e Cola" estáticos, seguindo a especificação BR Code do Banco Central do Brasil.

## O que é o BR Code?

O "Pix Copia e Cola" é a representação textual de um QR Code do Pix. Ele permite compartilhar informações de pagamento (chave, valor, mensagem) de forma simples e padronizada. A estrutura de dados segue o padrão EMV® QRCPS (QR Code Specification for Payment Systems) e é organizada no formato TLV (Type, Length, Value).

## Funcionalidades

- **Geração de Payload:** Monta a string de pagamento com todos os campos necessários.
- **Cálculo de CRC16:** Inclui a verificação de integridade (CRC-16-CCITT-FFFF) exigida pelo padrão.
- **Flexibilidade:** Permite definir chave Pix, nome do recebedor, cidade, valor, mensagem e TxID.
- **Validação:** Realiza validações simples nos campos para garantir a conformidade com o padrão (ex: tamanho máximo de nome e cidade).

## Como Usar

O script pode ser executado diretamente para ver um exemplo de uso, ou a classe `GeradorPix` pode ser importada em outros projetos.

### Executando o Exemplo

Para executar o exemplo contido no arquivo, basta rodar o script:

```bash
python gerador_pix.py
```

Isso irá imprimir no console um código "Copia e Cola" gerado com dados de exemplo.

### Importando em outro projeto

Você pode importar a classe `GeradorPix` e usá-la para gerar códigos dinamicamente.

```python
from gerador_pix import GeradorPix

# Crie uma instância do gerador com as informações do pagamento
gerador = GeradorPix(
    chave_pix="seu-email@dominio.com",
    nome_recebedor="NOME DO RECEBEDOR",
    cidade_recebedor="SAO PAULO",
    valor=99.90,
    mensagem="Pagamento do pedido #123"
)

# Gere o código
codigo_pix = gerador.gerar_codigo()

# Imprima ou use o código como desejar
print(codigo_pix)

```

## Estrutura do BR Code

O script implementa a seguinte estrutura de campos:

- **ID 00:** Payload Format Indicator
- **ID 26:** Merchant Account Information (contendo GUI, Chave Pix e Mensagem)
- **ID 52:** Merchant Category Code
- **ID 53:** Transaction Currency (BRL - 986)
- **ID 54:** Transaction Amount
- **ID 58:** Country Code (BR)
- **ID 59:** Merchant Name
- **ID 60:** Merchant City
- **ID 62:** Additional Data Field (com TxID)
- **ID 63:** CRC16

Para mais detalhes sobre a especificação, consulte o arquivo `pesquisa_pix.txt` neste repositório.
