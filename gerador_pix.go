package main

import (
	"fmt"
	"strconv"
	"strings"
)

// GeradorPix encapsula a lógica para criar um BR Code.
type GeradorPix struct {
	ChavePix        string
	NomeRecebedor   string
	CidadeRecebedor string
	Valor           *float64
	Mensagem        string
	TxID            string
}

// IDs dos campos do BR Code
const (
	IDPayloadFormatIndicator             = "00"
	IDMerchantAccountInformation         = "26"
	IDMerchantAccountInformationGUI      = "00"
	IDMerchantAccountInformationKey      = "01"
	IDMerchantAccountInformationDescription = "02"
	IDMerchantCategoryCode             = "52"
	IDTransactionCurrency              = "53"
	IDTransactionAmount                = "54"
	IDCountryCode                      = "58"
	IDMerchantName                     = "59"
	IDMerchantCity                     = "60"
	IDAdditionalDataFieldTemplate      = "62"
	IDAdditionalDataFieldTemplateTxID  = "05"
	IDCRC16                            = "63"
)

// NewGeradorPix cria uma nova instância de GeradorPix com validações.
func NewGeradorPix(chavePix, nomeRecebedor, cidadeRecebedor string, valor *float64, mensagem, txid string) (*GeradorPix, error) {
	if len(nomeRecebedor) > 25 {
		return nil, fmt.Errorf("o nome do recebedor não pode exceder 25 caracteres")
	}
	if len(cidadeRecebedor) > 15 {
		return nil, fmt.Errorf("o nome da cidade não pode exceder 15 caracteres")
	}
	if txid == "" {
		txid = "***"
	}

	return &GeradorPix{
		ChavePix:        chavePix,
		NomeRecebedor:   strings.ToUpper(nomeRecebedor),
		CidadeRecebedor: strings.ToUpper(cidadeRecebedor),
		Valor:           valor,
		Mensagem:        mensagem,
		TxID:            txid,
	}, nil
}

func formatarCampo(id, valor string) string {
	tamanho := fmt.Sprintf("%02d", len(valor))
	return id + tamanho + valor
}

func (g *GeradorPix) montarPayload() string {
	gui := formatarCampo(IDMerchantAccountInformationGUI, "br.gov.bcb.pix")
	chave := formatarCampo(IDMerchantAccountInformationKey, g.ChavePix)
	descricao := ""
	if g.Mensagem != "" {
		descricao = formatarCampo(IDMerchantAccountInformationDescription, g.Mensagem)
	}

	campo26 := formatarCampo(IDMerchantAccountInformation, gui+chave+descricao)
	txidFormatado := formatarCampo(IDAdditionalDataFieldTemplateTxID, g.TxID)
	campo62 := formatarCampo(IDAdditionalDataFieldTemplate, txidFormatado)

	payload := []string{
		formatarCampo(IDPayloadFormatIndicator, "01"),
		campo26,
		formatarCampo(IDMerchantCategoryCode, "0000"),
		formatarCampo(IDTransactionCurrency, "986"),
	}

	if g.Valor != nil {
		valorStr := fmt.Sprintf("%.2f", *g.Valor)
		payload = append(payload, formatarCampo(IDTransactionAmount, valorStr))
	}

	payload = append(payload,
		formatarCampo(IDCountryCode, "BR"),
		formatarCampo(IDMerchantName, g.NomeRecebedor),
		formatarCampo(IDMerchantCity, g.CidadeRecebedor),
		campo62,
	)

	return strings.Join(payload, "")
}

func calcularCRC16(payload string) string {
	payloadComCrcID := payload + IDCRC16 + "04"
	polinomio := uint16(0x1021)
	resultado := uint16(0xFFFF)

	for _, b := range []byte(payloadComCrcID) {
		resultado ^= uint16(b) << 8
		for i := 0; i < 8; i++ {
			if (resultado & 0x8000) != 0 {
				resultado = (resultado << 1) ^ polinomio
			} else {
				resultado <<= 1
			}
		}
	}

	return fmt.Sprintf("%04X", resultado)
}

// GerarCodigo gera a string final do "Copia e Cola".
func (g *GeradorPix) GerarCodigo() string {
	payload := g.montarPayload()
	crc := calcularCRC16(payload)
	return payload + IDCRC16 + "04" + crc
}

func main() {
	valor := 25.00
	gerador, err := NewGeradorPix(
		"123e4567-e89b-12d3-a456-426655440000",
		"JOAO SILVA",
		"RIO DE JANEIRO",
		&valor,
		"Referente ao mes de Julho",
		"***",
	)
	if err != nil {
		fmt.Println("Erro ao criar gerador:", err)
		return
	}

	codigoPix := gerador.GerarCodigo()
	fmt.Println("--- Gerador de PIX Copia e Cola (Go) ---")
	fmt.Println("Código PIX 'Copia e Cola':")
	fmt.Println(codigoPix)
}
