#
#
# main() será executado quando você chamar essa ação
#
# @param As ações do Cloud Functions aceitam um único parâmetro, que deve ser um objeto JSON.
#
# @return A saída dessa ação, que deve ser um objeto JSON.
#
#
import sys
import requests
import json

def pacote_de_servicos_pessoa_fisica(nome, linhas=10000,param='Servico,ValorMaximo'):
    
    bancos = [{'nome':'Banco do Brasil', 'cnpj':'00000000'},
               {'nome':'Caixa', 'cnpj':'00360305'}, 
               {'nome':'Itau', 'cnpj':'60701190'},
               {'nome':'Bradesco', 'cnpj':'60746948'},
               {'nome':'Santander', 'cnpj':'90400888'}
              ]
    
    instituicao = list(filter(lambda x: x['nome']==nome['nome'],bancos))[0]
    
    def filtro_pacote_servicos(json):
        return filter(lambda x: 'PACOTE PADRONIZADO DE SERV' in x['Servico'],json)
    
    # configuração da url
    url = "https://olinda.bcb.gov.br/olinda/servico/Informes_ListaTarifasPorInstituicaoFinanceira/versao/v1/odata/ListaTarifasPorInstituicaoFinanceira"
    url2 = f"(PessoaFisicaOuJuridica=@PessoaFisicaOuJuridica,CNPJ=@CNPJ)?@PessoaFisicaOuJuridica='F'&@CNPJ='{instituicao['cnpj']}'&$top={linhas}&$format=json&$select={param}"
    
    # resposta da chamada do banco central
    response = json.loads(requests.get(url+url2).text)
    response = response['value']
    
    # para cada pacote encontrado, quebramos a resposta em 3 valores com a função zip
    bancos,pacotes,tarifas = zip(*[(instituicao['nome'],
                                    value['Servico'],
                                    value['ValorMaximo']) for value in filtro_pacote_servicos(response)])
    
    return {'tarifas':(bancos,pacotes,tarifas)}

def main(json):
    return pacote_de_servicos_pessoa_fisica(json)
