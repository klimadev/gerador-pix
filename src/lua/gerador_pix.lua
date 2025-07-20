--- gerador_pix.lua
-- Classe para gerar códigos "Pix Copia e Cola" estáticos (BR Code)

local GeradorPix = {}
GeradorPix.__index = GeradorPix

-- IDs dos campos do BR Code
local ID_PAYLOAD_FORMAT_INDICATOR = '00'
local ID_MERCHANT_ACCOUNT_INFORMATION = '26'
local ID_MERCHANT_ACCOUNT_INFORMATION_GUI = '00'
local ID_MERCHANT_ACCOUNT_INFORMATION_KEY = '01'
local ID_MERCHANT_ACCOUNT_INFORMATION_DESCRIPTION = '02'
local ID_MERCHANT_CATEGORY_CODE = '52'
local ID_TRANSACTION_CURRENCY = '53'
local ID_TRANSACTION_AMOUNT = '54'
local ID_COUNTRY_CODE = '58'
local ID_MERCHANT_NAME = '59'
local ID_MERCHANT_CITY = '60'
local ID_ADDITIONAL_DATA_FIELD_TEMPLATE = '62'
local ID_ADDITIONAL_DATA_FIELD_TEMPLATE_TXID = '05'
local ID_CRC16 = '63'

function GeradorPix.new(chave_pix, nome_recebedor, cidade_recebedor, valor, mensagem, txid)
    local self = setmetatable({}, GeradorPix)
    
    self.chave_pix = chave_pix
    self.nome_recebedor = self:_validar_nome(nome_recebedor)
    self.cidade_recebedor = self:_validar_cidade(cidade_recebedor)
    self.valor = valor and self:_formatar_valor(valor) or nil
    self.mensagem = mensagem
    self.txid = txid or "***"
    
    return self
end

function GeradorPix:_validar_nome(nome)
    if #nome > 25 then
        error("O nome do recebedor não pode exceder 25 caracteres.")
    end
    return string.upper(nome)
end

function GeradorPix:_validar_cidade(cidade)
    if #cidade > 15 then
        error("O nome da cidade não pode exceder 15 caracteres.")
    end
    return string.upper(cidade)
end

function GeradorPix:_formatar_valor(valor)
    return string.format("%.2f", valor)
end

function GeradorPix:_formatar_campo(id_campo, valor)
    local tamanho = string.format("%02d", #valor)
    return id_campo .. tamanho .. valor
end

function GeradorPix:_montar_payload()
    local gui = self:_formatar_campo(ID_MERCHANT_ACCOUNT_INFORMATION_GUI, 'br.gov.bcb.pix')
    local chave = self:_formatar_campo(ID_MERCHANT_ACCOUNT_INFORMATION_KEY, self.chave_pix)
    local descricao = self.mensagem and self:_formatar_campo(ID_MERCHANT_ACCOUNT_INFORMATION_DESCRIPTION, self.mensagem) or ''
    
    local campo26 = self:_formatar_campo(ID_MERCHANT_ACCOUNT_INFORMATION, gui .. chave .. descricao)

    local txid_formatado = self:_formatar_campo(ID_ADDITIONAL_DATA_FIELD_TEMPLATE_TXID, self.txid)
    local campo62 = self:_formatar_campo(ID_ADDITIONAL_DATA_FIELD_TEMPLATE, txid_formatado)

    local payload_parts = {
        self:_formatar_campo(ID_PAYLOAD_FORMAT_INDICATOR, '01'),
        campo26,
        self:_formatar_campo(ID_MERCHANT_CATEGORY_CODE, '0000'),
        self:_formatar_campo(ID_TRANSACTION_CURRENCY, '986'),
    }

    if self.valor then
        table.insert(payload_parts, self:_formatar_campo(ID_TRANSACTION_AMOUNT, self.valor))
    end
    
    table.insert(payload_parts, self:_formatar_campo(ID_COUNTRY_CODE, 'BR'))
    table.insert(payload_parts, self:_formatar_campo(ID_MERCHANT_NAME, self.nome_recebedor))
    table.insert(payload_parts, self:_formatar_campo(ID_MERCHANT_CITY, self.cidade_recebedor))
    table.insert(payload_parts, campo62)

    return table.concat(payload_parts)
end

function GeradorPix:_calcular_crc16(payload)
    local payload_com_crc_id = payload .. ID_CRC16 .. '04'
    
    local polinomio = 0x1021
    local resultado = 0xFFFF
    
    for i = 1, #payload_com_crc_id do
        local byte = string.byte(payload_com_crc_id, i)
        resultado = bit32.bxor(resultado, bit32.lshift(byte, 8))
        
        for _ = 1, 8 do
            if bit32.band(resultado, 0x8000) ~= 0 then
                resultado = bit32.bxor(bit32.lshift(resultado, 1), polinomio)
            else
                resultado = bit32.lshift(resultado, 1)
            end
        end
    end
    
    return string.format("%04X", bit32.band(resultado, 0xFFFF))
end

function GeradorPix:gerar_codigo()
    local payload = self:_montar_payload()
    local crc = self:_calcular_crc16(payload)
    return payload .. ID_CRC16 .. '04' .. crc
end

-- Exemplo de uso
if not pcall(debug.getlocal, 2, 1) then
    local gerador = GeradorPix.new(
        "123e4567-e89b-12d3-a456-426655440000",
        "JOAO SILVA",
        "RIO DE JANEIRO",
        25.00,
        "Referente ao mes de Julho",
        "***"
    )

    local codigo_pix = gerador:gerar_codigo()

    print("--- Gerador de PIX Copia e Cola (Lua) ---")
    print("Recebedor: " .. gerador.nome_recebedor)
    print("Cidade: " .. gerador.cidade_recebedor)
    print("Valor: R$ " .. gerador.valor)
    print("Mensagem: " .. gerador.mensagem)
    print("\nCódigo PIX 'Copia e Cola':")
    print(codigo_pix)
end

return GeradorPix
