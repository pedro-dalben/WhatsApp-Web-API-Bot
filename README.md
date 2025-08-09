# 🚀 WhatsApp Web API Bot

Uma API REST simples e poderosa para enviar mensagens de texto e imagens via WhatsApp Web usando Python, Flask e Selenium.

## ✨ Funcionalidades

- 📱 Envio de mensagens de texto
- 🖼️ Envio de imagens com legendas opcionais
- 🔗 Download automático de imagens via URL
- 🔄 Sessão persistente (não precisa escanear QR code a cada reinício)
- 🌐 API REST para integração fácil
- ⚡ Interface simples via HTTP POST

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Flask** - Framework web
- **Selenium** - Automação do navegador
- **Chrome WebDriver** - Driver para Chrome
- **Requests** - Download de imagens

## 📋 Pré-requisitos

- Python 3.7+
- Google Chrome instalado
- ChromeDriver compatível com sua versão do Chrome

## 🚀 Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/[seu-usuario]/whatsapp-web-api-bot.git
cd whatsapp-web-api-bot
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Baixe o ChromeDriver:**
   - Acesse [ChromeDriver Downloads](https://chromedriver.chromium.org/)
   - Baixe a versão compatível com seu Chrome
   - Coloque o arquivo `chromedriver` na raiz do projeto

4. **Execute o bot:**
```bash
python bot.py
```

5. **Primeira execução:**
   - O Chrome abrirá automaticamente no WhatsApp Web
   - Escaneie o QR Code com seu celular
   - A sessão ficará salva para próximas execuções

## 📡 Como Usar a API

### Enviar Mensagem de Texto

```bash
curl -X POST http://localhost:5000/send_message \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "5511999999999",
    "message": "Olá! Esta é uma mensagem de teste."
  }'
```

### Enviar Imagem com Legenda

```bash
curl -X POST http://localhost:5000/send_message \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "5511999999999",
    "message": "Confira esta imagem!",
    "image_url": "https://exemplo.com/imagem.jpg"
  }'
```

### Parâmetros da API

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `phone` | string | ✅ | Número do telefone com código do país (ex: 5511999999999) |
| `message` | string | ✅* | Texto da mensagem ou legenda da imagem |
| `image_url` | string | ❌ | URL da imagem para download e envio |

*Obrigatório apenas para mensagens sem imagem

### Respostas da API

**Sucesso (200):**
```json
{
  "status": "Mensagem enviada com sucesso."
}
```

**Erro (400/500):**
```json
{
  "error": "Descrição do erro"
}
```

## ⚙️ Configurações

### Modo Headless
Para executar sem abrir a janela do Chrome, descomente a linha no código:
```python
chrome_options.add_argument("--headless")
```

### Porta do Servidor
Por padrão, a API roda na porta 5000. Para alterar:
```python
app.run(host='0.0.0.0', port=SUA_PORTA)
```

## 📁 Estrutura do Projeto

```
whatsapp-web-api-bot/
├── bot.py              # Código principal da API
├── chromedriver        # Driver do Chrome
├── requirements.txt    # Dependências Python
├── user_data/         # Dados da sessão do Chrome (criado automaticamente)
├── .gitignore         # Arquivos ignorados pelo Git
└── README.md          # Este arquivo
```

## 🔧 Solução de Problemas

### Chrome não abre ou erro de ChromeDriver
- Verifique se o ChromeDriver é compatível com sua versão do Chrome
- Certifique-se de que o arquivo `chromedriver` tem permissões de execução

### Erro de timeout
- Verifique sua conexão com a internet
- Aguarde o WhatsApp Web carregar completamente antes de enviar mensagens

### Sessão expirada
- Delete a pasta `user_data/` e execute novamente
- Escaneie o QR Code novamente

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## ⚠️ Aviso Legal

Este projeto é apenas para fins educacionais e de automação pessoal. Use com responsabilidade e respeite os Termos de Serviço do WhatsApp.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🙋‍♂️ Suporte

Se você encontrar algum problema ou tiver dúvidas, abra uma [issue](https://github.com/[seu-usuario]/whatsapp-web-api-bot/issues) no GitHub.

---

⭐ Se este projeto te ajudou, não esqueça de dar uma estrela!
# WhatsApp-Web-API-Bot
