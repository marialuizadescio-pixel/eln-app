# ELN - Electronic Lab Notebook

Um caderno de laboratório digital para organizar amostras, experimentos, anotações e arquivos de pesquisa.

## Funcionalidades

- 📔 Cadastro e organização de amostras
- 🔬 Registro de experimentos vinculados a amostras
- 📎 Upload de arquivos (imagens, espectros, dados)
- 🔍 Busca por amostra e experimento
- 💾 Armazenamento local com banco de dados SQLite

## Instalação e Uso Local

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/eln-app.git
cd eln-app
```

### 2. Criar ambiente virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Rodar a aplicação

```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

## Estrutura do Projeto

```
eln-app/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── .gitignore            # Arquivos a ignorar no Git
├── README.md             # Este arquivo
├── templates/            # Páginas HTML
│   ├── base.html         # Template base
│   ├── index.html        # Página inicial
│   ├── new_sample.html   # Criar amostra
│   ├── view_sample.html  # Visualizar amostra
│   ├── new_experiment.html # Criar experimento
│   └── search_results.html # Resultados de busca
├── uploads/              # Arquivos enviados (criado automaticamente)
└── eln.db               # Banco de dados SQLite (criado automaticamente)
```

## Próximos Passos

- [ ] Adicionar autenticação de usuário
- [ ] Integrar com Supabase para hospedagem
- [ ] Adicionar edição de experimentos
- [ ] Integrar com Google Calendar
- [ ] Adicionar link para Zotero
- [ ] Estequiometria automatizada

## Contribuições

Sinta-se livre para fazer pull requests com melhorias!

## Licença

MIT
