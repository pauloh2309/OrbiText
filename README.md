# OrbiText

<img width="351" height="351" alt="image" src="https://github.com/user-attachments/assets/f76b0fa8-c4aa-441b-8afb-db735cd3ce98" />

Este projeto tem o intuito de criar um programa que ajude na leitura em outros idiomas (inglês, espanhol e francês), tendo a função de leitura e tradução simultânea para o português. Nesse programa, haverá diversos textos (artigos científicos, trechos de livros, poemas, entre outros).
Além disso, ele incentiva os estudantes a criarem o hábito da leitura, pois todos os dias será mostrado um texto aleatório.

Para que os usuários sintam vontade de usar o programa ainda mais, um sistema de gamificação foi implementado. Assim, cada vez que o usuário usar uma função do programa, como por exemplo: avaliar um texto lido, marcar um trecho interessante ou logar todos os dias, ele ganhará experiência (XP). Os usuários com maior XP ficarão no topo do pódio, que ficará na página principal.

---

# REQUISITOS FUNCIONAIS

## RELEASE 1.0
* **RF001** - Cadastro
* **RF002** - Login
* **RF003** - Redirecionamento à página principal
* **RF004** - Escolha de idioma
* **RF005** - Ferramenta de pesquisa
* **RF006** - Leitura na língua nativa e traduzida para o português

## RELEASE 1.1
* Dados do arquivo "lista" (textos em outros idiomas) foram migrados para uma estrutura organizada no módulo "dados".

## RELEASE 2.0
* **RF007** - Marcar trechos interessantes (Curtidas/Saves)
* **RF008** - Escrever observações particulares ou publicas (Comentários)
* **RF009** - Compartilhar anotações (Visualização de comentários públicos)
* **RF010** - Sistema de XP
* **RF011** - Sistema de Ranking
* **RF012** - Capacidade de curtir comentarios
* **RF013** - Capacidade de curtir paragrafos
* **RF014** - Escrever textos que poderão ser lidos por outros usuarios
* **RF015** - Escrever paragrafos de autoria própria e poder escolher entre compatilha-lo ou deixar como privado
* **RF016** - Escolher se os trechos interessantes que foram marcados serão visto pelo público ou serão privados
* **RF017** - Ver o sistema de ranking tanto em geral quanto para cada idioma
* **RF018** - Capacidade de deletar a propria conta
* **RF019** - Possibilidade de recuperar senha
* **RF020** - Adaptação do código para outros sistemas operacionais, como linux.



---

# 💻 DOCUMENTAÇÃO TÉCNICA

## 📦 Bibliotecas e Dependências

Para garantir a segurança, a usabilidade e a persistência de dados, o projeto utiliza um conjunto de bibliotecas nativas do Python e bibliotecas externas que necessitam de instalação.

### 1. Bibliotecas Externas (Instalação Necessária)
Para executar o projeto, é **obrigatório** instalar a seguinte biblioteca:

* **`maskpass`**
    * **Comando de instalação:** `pip install maskpass`
    * **Justificativa Técnica:** Utilizada nos módulos de autenticação (`main .py` e `recuperação_senha.py`). Essa biblioteca permite a entrada de dados ocultos no terminal (substituindo a senha por asteriscos `*`), garantindo que credenciais sensíveis não fiquem visíveis na tela durante a digitação, aumentando a segurança do usuário.

### 2. Bibliotecas Nativas (Python Standard Library)
O projeto utiliza módulos padrão do Python para garantir robustez sem excesso de dependências externas:

* **`json`**: Atua como o banco de dados da aplicação. Permite a persistência leve e portátil de dados de usuários, textos e interações em arquivos locais (`.json`).
* **`smtplib` e `email.message`**: Implementam o protocolo SMTP para o envio automatizado de e-mails de recuperação de senha.
* **`secrets`**: Utilizada para gerar tokens hexadecimais criptograficamente seguros para os códigos de verificação de e-mail.
* **`re` (Regular Expressions)**: Empregada no módulo `verificação.py` para validação robusta de padrões de e-mail e sanitização de strings.
* **`unicodedata`**: Utilizada para normalização de texto (remoção de acentos), facilitando a busca e comparação de strings independentemente da formatação.
* **`os` e `pathlib`**: Gerenciamento de caminhos de arquivos compatíveis entre sistemas operacionais (Windows/Linux) e limpeza de tela.

---

## 📂 Organização dos Módulos

A arquitetura do software segue o princípio de separação de responsabilidades (SoC), facilitando a manutenção e escalabilidade:

| Arquivo | Descrição |
| :--- | :--- |
| **`main .py`** | **Entry Point**. Controla o fluxo inicial (Login/Cadastro) e o loop principal da aplicação. |
| **`usuario.py`** | Define a classe `Usuario`. Gerencia a sessão atual, lógica de gamificação (cálculo de XP) e manipulação da lista de usuários. |
| **`dados.py`** | Camada de acesso a dados. Centraliza as operações de leitura e escrita nos arquivos JSON de textos e interações. |
| **`menu_principal.py`** | Hub de navegação pós-login. Direciona o usuário para leitura, perfil, rankings ou configurações. |
| **`menu_leitura.py`** | Interface de leitura. Gerencia a exibição paginada dos textos bilíngues e a interação (curtidas/comentários). |
| **`recuperação_senha.py`** | Lógica de segurança. Gerencia o envio de tokens por e-mail e redefinição de credenciais. |
| **`verificação.py`** | Utilitário de validação. Verifica força de senha e formatação de e-mail. |
| **`util.py`** | Funções auxiliares globais, como limpeza de tela e normalização de texto. |

---

## 💡 Diferenciais e Inovação

O **OrbiText** se destaca por transformar o ambiente de linha de comando (CLI), geralmente árido, em uma plataforma de aprendizado rica e engajadora. As principais inovações técnicas e pedagógicas incluem:

### 1. Algoritmo de Gamificação Anti-Spam
Diferente de sistemas que premiam apenas o "clique", o OrbiText implementa um algoritmo inteligente de cálculo de XP (Experiência) localizado no método `Usuario.adicionar_xp_leitura`.
* **Lógica:** O sistema calcula uma proporção entre o `tempo_real_de_leitura` e o `tamanho_do_texto`.
* **Benefício:** Isso desencoraja o usuário a pular textos apenas para farmar pontos, recompensando o tempo de estudo real e a dedicação.

### 2. Metodologia de Leitura Paralela (Side-by-Side)
A arquitetura do módulo de leitura foi projetada para suportar o **Método de Texto Paralelo**.
* O sistema renderiza simultaneamente o parágrafo no idioma alvo (Inglês, Francês ou Espanhol) e sua tradução em Português.
* Isso permite a comparação sintática imediata, acelerando a aquisição de vocabulário e compreensão gramatical sem a necessidade de ferramentas externas de tradução.

### 3. Progressão Visual Hierárquica no Console
Apesar das limitações gráficas de um terminal, o projeto inova na UX (Experiência do Usuário) através de um sistema de feedback visual mapeado:
* **Ranking Geral:** Evolui de seres míticos menores até forças da natureza (ex: Nível 10 = 🌊 'Oceano').
* **Ranking por Idioma:** Utiliza a fauna para representar o domínio específico (ex: Nível 10 = 🦏 'Rinoceronte').
* Isso cria um senso de identidade e progresso tangível para o usuário a cada login.

### 4. Foco em "Deep Work" (Trabalho Profundo)
A escolha por uma interface CLI (Command Line Interface) é intencional. Ao remover distrações visuais comuns em interfaces web modernas (pop-ups, banners, cores excessivas), o OrbiText oferece um ambiente minimalista que favorece a concentração total na leitura e interpretação de texto.

## ▶️ Como Rodar o Projeto

1.  Certifique-se de ter o **Python 3.x** instalado.
2.  Instale a dependência externa:
    ```bash
    pip install maskpass
    ```
3.  Execute o arquivo principal:
    ```bash
    python "main .py"
    ```