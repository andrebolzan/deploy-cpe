Deploy de CPE em Lote – FIX FIBRA

Automação para configuração de ONUs Huawei e Stavix
Criado por Giovana Sato

-- Sobre o projeto

Este projeto automatiza o processo de aplicação de arquivos XML em CPEs (ONUs) e também permite realizar deploy em lote para o modelo Stavix MP-X.

-- A automação utiliza:

Python

Selenium WebDriver

Tkinter (interface gráfica)

O objetivo é acelerar processos de provisionamento, reduzir erros e facilitar o trabalho de técnicos e provedores.

-- Funcionalidades

- Deploy automático de arquivos XML
- Login automático nos modelos Huawei e Stavix
- Upload e backup automático
- Validação inteligente de templates
- Modo individual e modo lote
- Interface gráfica simples e intuitiva
- Geração de log de erros

-- Equipamentos compatíveis

Huawei HG

Huawei EG

Stavix MP-X

Stavix MP-G

Stavix MP-X em lote (via CSV)

-- Como rodar
1. Instalar dependências
pip install -r requirements.txt

2. Rodar o programa
python src/deploy_cpe.py


A interface gráfica será aberta automaticamente.

-- Estrutura da GUI

Seleção de modelo da ONU

Seleção de arquivo XML

Seleção de CSV para deploy em lote

Botão "Deploy"

-- CSV para modo Lote MP-X

Seu CSV deve conter, pelo menos:

Coluna	Descrição
E	IP da ONU

O script usa automaticamente o IP da coluna E.

-- Tecnologias usadas

Python

Selenium WebDriver

WebDriver Manager

Tkinter

-- Licença

MIT License — fique livre para usar, modificar e contribuir.