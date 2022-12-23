# ACOMP Report! Cultura Inglesa

Automação de relatórios Cultura Inglesa. Para rodar você precisa ter:

- Python 3
- Pipenv

Após clonar o projeto, execute para instalar as dependências:
`pipenv install`

Para rodar, execute:
`streamlit run app.py`

## Usando a automação de relatórios

Faça os exports dos relatórios nas plataformas.
**Período:** O mês analisado (mesmo que o ACOMP tire um quadro da semana, usa o acúmulo do mês.

Para fazer o exports dos relatórios das plataformas detalho abaixo:

- **Google Analytics**: Personalização >> Relatório Personalizado >> ACOMP CISP / ACOMP CIISA
  - Escolha o período, faça exibir todas as linhas (abaixo escolha o número máximo)
  - Clique em Exportar e escolha a opção CSV
- **Google Ads**: Ferramentas e Configurações >> Relatórios >> Report Weekly ACOMP
  - Escolha o período
  - Clique em Download e escolha a opção CSV
- **Hubspot**: Acesse Contatos >> Escolha a aba de visualização ABLAB >> Ações >> Exportar Visualização
  - Selecione a opção CSV na opção "Formato de Arquivo"
  - Deixe marcada a opção "Apenas propriedade na visualização"
  - Deixe a linguagem em Inglês
  - Faça o Export
- **Meta Ads**: Gerenciador de Anúncios >> Menu >> Relatório de Anúncios >> [Ablab] (CISP ou CIISA) - Report
  - Selecione o período e clique no botão de download (canto superior direito)
  - Escolha a opção CSV e clique em Exportar
  - A opção "incluir linha de resumo" **NUNCA** deve estar marcada
- **Tiktok Ads**: Gerenciador de Anúncios >> Reporting >> Selecione o relatório report-weekly-acomp
  - Selecione o período e clique em 'Run & Export'
  - Escolha a opção 'CSV' e clique em 'Export'

Pronto! Essa foi a parte mais difícil. Agora é só pegar cada arquivo e enviar na aplicação (você pode só arrastar e soltar em cada um). A aplicação já processa tudo automaticamente. Ao final, gera as tabelas tratadas para você conferir e no final da página tem um link para você baixar a planilha toda pronta para você!

Muito legal, né?
@jaimeflneto
