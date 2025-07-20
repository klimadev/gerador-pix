<?php
// gerador_pix.php

/**
 * Classe para gerar códigos "Pix Copia e Cola" estáticos (BR Code)
 * conforme as especificações do Banco Central do Brasil.
 */
class GeradorPix
{
    // IDs dos campos do BR Code
    const ID_PAYLOAD_FORMAT_INDICATOR = '00';
    const ID_MERCHANT_ACCOUNT_INFORMATION = '26';
    const ID_MERCHANT_ACCOUNT_INFORMATION_GUI = '00';
    const ID_MERCHANT_ACCOUNT_INFORMATION_KEY = '01';
    const ID_MERCHANT_ACCOUNT_INFORMATION_DESCRIPTION = '02';
    const ID_MERCHANT_CATEGORY_CODE = '52';
    const ID_TRANSACTION_CURRENCY = '53';
    const ID_TRANSACTION_AMOUNT = '54';
    const ID_COUNTRY_CODE = '58';
    const ID_MERCHANT_NAME = '59';
    const ID_MERCHANT_CITY = '60';
    const ID_ADDITIONAL_DATA_FIELD_TEMPLATE = '62';
    const ID_ADDITIONAL_DATA_FIELD_TEMPLATE_TXID = '05';
    const ID_CRC16 = '63';

    private $chavePix;
    private $nomeRecebedor;
    private $cidadeRecebedor;
    private $valor;
    private $mensagem;
    private $txid;

    public function __construct($chavePix, $nomeRecebedor, $cidadeRecebedor, $valor = null, $mensagem = null, $txid = '***')
    {
        $this->chavePix = $chavePix;
        $this->nomeRecebedor = $this->validarNome($nomeRecebedor);
        $this->cidadeRecebedor = $this->validarCidade($cidadeRecebedor);
        $this->valor = $valor ? $this->formatarValor($valor) : null;
        $this->mensagem = $mensagem;
        $this->txid = $txid ?: '***';
    }

    private function validarNome($nome)
    {
        if (strlen($nome) > 25) {
            throw new Exception("O nome do recebedor não pode exceder 25 caracteres.");
        }
        return strtoupper($nome);
    }

    private function validarCidade($cidade)
    {
        if (strlen($cidade) > 15) {
            throw new Exception("O nome da cidade não pode exceder 15 caracteres.");
        }
        return strtoupper($cidade);
    }

    private function formatarValor($valor)
    {
        return number_format($valor, 2, '.', '');
    }

    private function formatarCampo($idCampo, $valor)
    {
        $tamanho = str_pad(strlen($valor), 2, '0', STR_PAD_LEFT);
        return $idCampo . $tamanho . $valor;
    }

    private function montarPayload()
    {
        $gui = $this->formatarCampo(self::ID_MERCHANT_ACCOUNT_INFORMATION_GUI, 'br.gov.bcb.pix');
        $chave = $this->formatarCampo(self::ID_MERCHANT_ACCOUNT_INFORMATION_KEY, $this->chavePix);
        $descricao = $this->mensagem ? $this->formatarCampo(self::ID_MERCHANT_ACCOUNT_INFORMATION_DESCRIPTION, $this->mensagem) : '';

        $campo26 = $this->formatarCampo(self::ID_MERCHANT_ACCOUNT_INFORMATION, $gui . $chave . $descricao);

        $txidFormatado = $this->formatarCampo(self::ID_ADDITIONAL_DATA_FIELD_TEMPLATE_TXID, $this->txid);
        $campo62 = $this->formatarCampo(self::ID_ADDITIONAL_DATA_FIELD_TEMPLATE, $txidFormatado);

        $payload = [
            $this->formatarCampo(self::ID_PAYLOAD_FORMAT_INDICATOR, '01'),
            $campo26,
            $this->formatarCampo(self::ID_MERCHANT_CATEGORY_CODE, '0000'),
            $this->formatarCampo(self::ID_TRANSACTION_CURRENCY, '986'),
        ];

        if ($this->valor) {
            $payload[] = $this->formatarCampo(self::ID_TRANSACTION_AMOUNT, $this->valor);
        }

        $payload[] = $this->formatarCampo(self::ID_COUNTRY_CODE, 'BR');
        $payload[] = $this->formatarCampo(self::ID_MERCHANT_NAME, $this->nomeRecebedor);
        $payload[] = $this->formatarCampo(self::ID_MERCHANT_CITY, $this->cidadeRecebedor);
        $payload[] = $campo62;

        return implode('', $payload);
    }

    private function calcularCRC16($payload)
    {
        $payloadComCrcId = $payload . self::ID_CRC16 . '04';
        
        $polinomio = 0x1021;
        $resultado = 0xFFFF;
        
        for ($i = 0; $i < strlen($payloadComCrcId); $i++) {
            $byte = ord($payloadComCrcId[$i]);
            $resultado ^= ($byte << 8);
            for ($j = 0; $j < 8; $j++) {
                $resultado = ($resultado & 0x8000) ? (($resultado << 1) ^ $polinomio) : ($resultado << 1);
            }
        }
        
        return strtoupper(str_pad(dechex($resultado & 0xFFFF), 4, '0', STR_PAD_LEFT));
    }

    public function gerarCodigo()
    {
        $payload = $this->montarPayload();
        $crc = $this->calcularCRC16($payload);
        return $payload . self::ID_CRC16 . '04' . $crc;
    }
}

// Exemplo de uso
if (php_sapi_name() === 'cli' && realpath($argv[0]) == realpath(__FILE__)) {
    $gerador = new GeradorPix(
        "123e4567-e89b-12d3-a456-426655440000",
        "JOAO SILVA",
        "RIO DE JANEIRO",
        25.00,
        "Referente ao mes de Julho"
    );

    $codigoPix = $gerador->gerarCodigo();

    echo "--- Gerador de PIX Copia e Cola (PHP) ---\n";
    echo "Código PIX 'Copia e Cola':\n";
    echo $codigoPix . "\n";
}
