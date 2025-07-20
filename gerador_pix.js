// gerador_pix.js

/**
 * Classe para gerar códigos "Pix Copia e Cola" estáticos (BR Code)
 * conforme as especificações do Banco Central do Brasil.
 */
class GeradorPix {
    // IDs dos campos do BR Code
    static ID_PAYLOAD_FORMAT_INDICATOR = '00';
    static ID_MERCHANT_ACCOUNT_INFORMATION = '26';
    static ID_MERCHANT_ACCOUNT_INFORMATION_GUI = '00';
    static ID_MERCHANT_ACCOUNT_INFORMATION_KEY = '01';
    static ID_MERCHANT_ACCOUNT_INFORMATION_DESCRIPTION = '02';
    static ID_MERCHANT_CATEGORY_CODE = '52';
    static ID_TRANSACTION_CURRENCY = '53';
    static ID_TRANSACTION_AMOUNT = '54';
    static ID_COUNTRY_CODE = '58';
    static ID_MERCHANT_NAME = '59';
    static ID_MERCHANT_CITY = '60';
    static ID_ADDITIONAL_DATA_FIELD_TEMPLATE = '62';
    static ID_ADDITIONAL_DATA_FIELD_TEMPLATE_TXID = '05';
    static ID_CRC16 = '63';

    constructor(chavePix, nomeRecebedor, cidadeRecebedor, valor = null, mensagem = null, txid = "***") {
        this.chavePix = chavePix;
        this.nomeRecebedor = this._validarNome(nomeRecebedor);
        this.cidadeRecebedor = this._validarCidade(cidadeRecebedor);
        this.valor = valor ? this._formatarValor(valor) : null;
        this.mensagem = mensagem;
        this.txid = txid || "***";
    }

    _validarNome(nome) {
        if (nome.length > 25) {
            throw new Error("O nome do recebedor não pode exceder 25 caracteres.");
        }
        return nome.toUpperCase();
    }

    _validarCidade(cidade) {
        if (cidade.length > 15) {
            throw new Error("O nome da cidade não pode exceder 15 caracteres.");
        }
        return cidade.toUpperCase();
    }

    _formatarValor(valor) {
        return valor.toFixed(2);
    }

    _formatarCampo(idCampo, valor) {
        const tamanho = valor.length.toString().padStart(2, '0');
        return `${idCampo}${tamanho}${valor}`;
    }

    _montarPayload() {
        const gui = this._formatarCampo(GeradorPix.ID_MERCHANT_ACCOUNT_INFORMATION_GUI, 'br.gov.bcb.pix');
        const chave = this._formatarCampo(GeradorPix.ID_MERCHANT_ACCOUNT_INFORMATION_KEY, this.chavePix);
        const descricao = this.mensagem ? this._formatarCampo(GeradorPix.ID_MERCHANT_ACCOUNT_INFORMATION_DESCRIPTION, this.mensagem) : '';
        
        const campo26 = this._formatarCampo(GeradorPix.ID_MERCHANT_ACCOUNT_INFORMATION, `${gui}${chave}${descricao}`);

        const txidFormatado = this._formatarCampo(GeradorPix.ID_ADDITIONAL_DATA_FIELD_TEMPLATE_TXID, this.txid);
        const campo62 = this._formatarCampo(GeradorPix.ID_ADDITIONAL_DATA_FIELD_TEMPLATE, txidFormatado);

        let payload = [
            this._formatarCampo(GeradorPix.ID_PAYLOAD_FORMAT_INDICATOR, '01'),
            campo26,
            this._formatarCampo(GeradorPix.ID_MERCHANT_CATEGORY_CODE, '0000'),
            this._formatarCampo(GeradorPix.ID_TRANSACTION_CURRENCY, '986'),
        ];

        if (this.valor) {
            payload.push(this._formatarCampo(GeradorPix.ID_TRANSACTION_AMOUNT, this.valor));
        }

        payload.push(
            this._formatarCampo(GeradorPix.ID_COUNTRY_CODE, 'BR'),
            this._formatarCampo(GeradorPix.ID_MERCHANT_NAME, this.nomeRecebedor),
            this._formatarCampo(GeradorPix.ID_MERCHANT_CITY, this.cidadeRecebedor),
            campo62
        );

        return payload.join('');
    }

    _calcularCRC16(payload) {
        const payloadComCrcId = payload + GeradorPix.ID_CRC16 + '04';
        
        let polinomio = 0x1021;
        let resultado = 0xFFFF;
        const buffer = Buffer.from(payloadComCrcId, 'utf-8');

        for (const byte of buffer) {
            resultado ^= (byte << 8);
            for (let i = 0; i < 8; i++) {
                if ((resultado & 0x8000) !== 0) {
                    resultado = (resultado << 1) ^ polinomio;
                } else {
                    resultado = (resultado << 1);
                }
            }
        }
        
        return (resultado & 0xFFFF).toString(16).toUpperCase().padStart(4, '0');
    }

    gerarCodigo() {
        const payload = this._montarPayload();
        const crc = this._calcularCRC16(payload);
        return `${payload}${GeradorPix.ID_CRC16}04${crc}`;
    }
}

// Exemplo de uso
if (require.main === module) {
    const gerador = new GeradorPix(
        "123e4567-e89b-12d3-a456-426655440000",
        "JOAO SILVA",
        "RIO DE JANEIRO",
        25.00,
        "Referente ao mes de Julho",
        "***"
    );

    const codigoPix = gerador.gerarCodigo();

    console.log("--- Gerador de PIX Copia e Cola (Node.js) ---");
    console.log(`Recebedor: ${gerador.nomeRecebedor}`);
    console.log(`Cidade: ${gerador.cidadeRecebedor}`);
    console.log(`Valor: R$ ${gerador.valor}`);
    console.log(`Mensagem: ${gerador.mensagem}`);
    console.log("\nCódigo PIX 'Copia e Cola':");
    console.log(codigoPix);
}

module.exports = GeradorPix;
