# -*- coding: utf-8 -*-

class GeradorPix:
    """
    Classe para gerar códigos "Pix Copia e Cola" estáticos (BR Code)
    conforme as especificações do Banco Central do Brasil.
    """

    # IDs dos campos do BR Code
    ID_PAYLOAD_FORMAT_INDICATOR = '00'
    ID_MERCHANT_ACCOUNT_INFORMATION = '26'
    ID_MERCHANT_ACCOUNT_INFORMATION_GUI = '00'
    ID_MERCHANT_ACCOUNT_INFORMATION_KEY = '01'
    ID_MERCHANT_ACCOUNT_INFORMATION_DESCRIPTION = '02'
    ID_MERCHANT_CATEGORY_CODE = '52'
    ID_TRANSACTION_CURRENCY = '53'
    ID_TRANSACTION_AMOUNT = '54'
    ID_COUNTRY_CODE = '58'
    ID_MERCHANT_NAME = '59'
    ID_MERCHANT_CITY = '60'
    ID_ADDITIONAL_DATA_FIELD_TEMPLATE = '62'
    ID_ADDITIONAL_DATA_FIELD_TEMPLATE_TXID = '05'
    ID_CRC16 = '63'

    def __init__(self, chave_pix, nome_recebedor, cidade_recebedor, valor=None, mensagem=None, txid="***"):
        self.chave_pix = chave_pix
        self.nome_recebedor = self._validar_nome(nome_recebedor)
        self.cidade_recebedor = self._validar_cidade(cidade_recebedor)
        self.valor = self._formatar_valor(valor) if valor else None
        self.mensagem = mensagem
        self.txid = txid if txid else "***"

    def _validar_nome(self, nome):
        if len(nome) > 25:
            raise ValueError("O nome do recebedor não pode exceder 25 caracteres.")
        return nome.upper() # Nomes são geralmente em maiúsculas no extrato

    def _validar_cidade(self, cidade):
        if len(cidade) > 15:
            raise ValueError("O nome da cidade não pode exceder 15 caracteres.")
        return cidade.upper() # Cidades são geralmente em maiúsculas

    def _formatar_valor(self, valor):
        return f"{valor:.2f}"

    def _formatar_campo(self, id_campo, valor):
        """Formata um campo no padrão TLV (Type, Length, Value)."""
        tamanho = str(len(valor)).zfill(2)
        return f"{id_campo}{tamanho}{valor}"

    def _montar_payload(self):
        """Monta o payload principal do BR Code."""
        # Campo 26 (Informações da Conta)
        gui = self._formatar_campo(self.ID_MERCHANT_ACCOUNT_INFORMATION_GUI, 'br.gov.bcb.pix')
        chave = self._formatar_campo(self.ID_MERCHANT_ACCOUNT_INFORMATION_KEY, self.chave_pix)
        descricao = self._formatar_campo(self.ID_MERCHANT_ACCOUNT_INFORMATION_DESCRIPTION, self.mensagem) if self.mensagem else ''
        
        campo26 = self._formatar_campo(self.ID_MERCHANT_ACCOUNT_INFORMATION, f"{gui}{chave}{descricao}")

        # Campo 62 (Dados Adicionais - TxID)
        txid_formatado = self._formatar_campo(self.ID_ADDITIONAL_DATA_FIELD_TEMPLATE_TXID, self.txid)
        campo62 = self._formatar_campo(self.ID_ADDITIONAL_DATA_FIELD_TEMPLATE, txid_formatado)
        
        payload = [
            self._formatar_campo(self.ID_PAYLOAD_FORMAT_INDICATOR, '01'),
            campo26,
            self._formatar_campo(self.ID_MERCHANT_CATEGORY_CODE, '0000'),
            self._formatar_campo(self.ID_TRANSACTION_CURRENCY, '986'),
        ]

        if self.valor:
            payload.append(self._formatar_campo(self.ID_TRANSACTION_AMOUNT, self.valor))
        
        payload.extend([
            self._formatar_campo(self.ID_COUNTRY_CODE, 'BR'),
            self._formatar_campo(self.ID_MERCHANT_NAME, self.nome_recebedor),
            self._formatar_campo(self.ID_MERCHANT_CITY, self.cidade_recebedor),
            campo62
        ])

        return "".join(payload)

    def _calcular_crc16(self, payload):
        """Calcula o CRC16-CCITT-FFFF para o payload."""
        payload_com_crc_id = payload + self.ID_CRC16 + '04'
        
        polinomio = 0x1021
        resultado = 0xFFFF
        
        for byte in payload_com_crc_id.encode('utf-8'):
            resultado ^= (byte << 8)
            for _ in range(8):
                if (resultado & 0x8000):
                    resultado = (resultado << 1) ^ polinomio
                else:
                    resultado = (resultado << 1)
        
        return hex(resultado & 0xFFFF)[2:].upper().zfill(4)

    def gerar_codigo(self):
        """Gera o código 'Pix Copia e Cola' final."""
        payload = self._montar_payload()
        crc = self._calcular_crc16(payload)
        return f"{payload}{self.ID_CRC16}04{crc}"

if __name__ == '__main__':
    # Exemplo de uso baseado no arquivo pesquisa_pix.txt
    # Os dados foram ajustados para passar nas validações de tamanho
    gerador = GeradorPix(
        chave_pix="123e4567-e89b-12d3-a456-426655440000",
        nome_recebedor="JOAO SILVA",
        cidade_recebedor="RIO DE JANEIRO",
        valor=25.00,
        mensagem="Referente ao mes de Julho",
        txid="***" 
    )

    codigo_pix = gerador.gerar_codigo()

    print("--- Gerador de PIX Copia e Cola ---")
    print(f"Recebedor: {gerador.nome_recebedor}")
    print(f"Cidade: {gerador.cidade_recebedor}")
    print(f"Valor: R$ {gerador.valor}")
    print(f"Mensagem: {gerador.mensagem}")
    print("\nCódigo PIX 'Copia e Cola':")
    print(codigo_pix)
