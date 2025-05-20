import json # Permite ler e escrever arquivos JSON, que são usados para salvar e carregar os dados dos usuários.
import os # Fornece funções para interagir com o sistema operacional, como verificar se arquivos existem.
import re # Fornece funções para gerar hashes criptográficos, que são como "impressões digitais" de dados. Ideal para armazenar senhas com segurança.
import hashlib # Permite trabalhar com expressões regulares, para fazer verificações avançadas em strings (como emails). Verifica se o email tem o formato "algo@algo.algo"


# Nome do arquivo onde os dados dos usuários serão armazenados
ARQUIVO_USUARIOS = "usuarios.json" 

# Variável para guardar temporariamente a senha do usuário logado
senha_usuario = ""

# Variável para guardar o nome do usuário logado
usuario_logado = None


# Carrega os usuários do arquivo JSON
def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS): # Verifica se o arquivo existe
        with open(ARQUIVO_USUARIOS, "r") as f: # Abre o arquivo para leitura
            usuarios = json.load(f) # Carrega os dados do arquivo
        usuarios = migrar_usuarios_antigos(usuarios) # Atualiza estrutura se necessário
        return usuarios
    return {}  # Retorna dicionário vazio se arquivo não existir


# Salva os dados dos usuários no arquivo JSON
def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w") as f: # Abre o arquivo para escrita
        json.dump(usuarios, f, indent=4) # Salva os dados formatados


# Atualiza dados de usuários antigos que usam estrutura diferente
def migrar_usuarios_antigos(usuarios):
    mudou = False
    for nome, dados in usuarios.items():
        if "cursos" in dados and "curso_atual" not in dados:  # Verifica se precisa migrar
            if len(dados["cursos"]) > 0:
                dados["curso_atual"] = dados["cursos"][0] # Usa o primeiro curso como atual
            else:
                dados["curso_atual"] = None
            del dados["cursos"] # Remove campo antigo
            mudou = True
    if mudou:
        salvar_usuarios(usuarios) # Salva novamente se houve mudança
    return usuarios


# Valida a força da senha com base em critérios: tamanho, letras maiúsculas, minúsculas, números e caracteres especiais
def validar_senha(senha):
    if (len(senha) >= 8 and re.search(r"[A-Z]", senha)
            and re.search(r"[a-z]", senha) and re.search(r"[0-9]", senha)
            and re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha)):
        return True
    return False


# Retorna o hash da senha fornecida
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


# Compara o hash da senha digitada com o hash armazenado
def verificar_senha(senha_digitada, senha_armazenada):
    return hash_senha(senha_digitada) == senha_armazenada


# Tela inicial do sistema, onde o usuário escolhe login ou cadastro
def tela_inicial():
    print("\n=========================================================")
    print("================ BEM VINDO AO NEXT LEVEL ================")
    print("=========================================================")
    print("1. Login")
    print("2. Cadastro")
    escolha = input("Escolha uma opção: ").strip()
    if escolha == "1":
        tela_login()
    elif escolha == "2":
        tela_cadastro()
    else:
        print("Opção inválida! Tente novamente.")
        tela_inicial()


# Tela para cadastro de novo usuário
def tela_cadastro():
    usuarios = carregar_usuarios()
    print("\n=== TELA DE CADASTRO ===")
    nome = input("Digite seu nome completo: ").strip().lower()
    if nome in usuarios:
        print("Usuário já cadastrado! Caso tenha esquecido sua senha, por favor, entre em contato com o suporte: suporte@example.com")
        tela_login()
        return
    idade = input("Digite sua idade (mínimo 14 anos): ").strip()
    if not idade.isdigit() or int(idade) < 14:
        print("Idade inválida. Você deve ter pelo menos 14 anos.")
        tela_cadastro()
        return
    email = input("Digite seu email: ").strip().lower()
    while True:
        senha = input("Digite sua senha: ")
        if not validar_senha(senha):
            print("Senha fraca. A senha deve conter ao menos 8 caracteres, incluindo letra maiúscula, minúscula, número e caractere especial.")
            continue
        senha_confirma = input("Confirme sua senha: ")
        if senha != senha_confirma:
            print("Senhas não conferem. Tente novamente.")
        else:
            break
    usuarios[nome] = {
        "idade": int(idade),
        "email": email,
        "senha": hash_senha(senha),
        "curso_atual": None
    }
    salvar_usuarios(usuarios)
    print("Cadastro realizado com sucesso! Faça login para continuar.")
    tela_login()


# Tela de login do sistema
def tela_login():
    global senha_usuario, usuario_logado
    usuarios = carregar_usuarios()
    print("\n=== TELA DE LOGIN ===")
    email = input("Digite seu email: ").strip().lower()
    senha = input("Digite sua senha: ")
    for nome, dados in usuarios.items():
        if dados["email"] == email and verificar_senha(senha, dados["senha"]):
            senha_usuario = senha
            usuario_logado = nome
            print(f"\nLogin bem-sucedido! Bem-vindo, {usuario_logado}")
            tela_menu()
            return
    print("\nEmail ou senha incorretos.")
    print("1. Tentar novamente")
    print("2. Cadastrar-se")
    escolha = input("Escolha uma opção: ").strip()
    if escolha == "1":
        tela_login()
    elif escolha == "2":
        tela_cadastro()
    else:
        print("Opção inválida!")
        tela_login()


# Menu principal após login
def tela_menu():
    print("\n=== Menu Principal ===")
    print("1. Inscrever em Curso")
    print("2. Acessar Curso")
    print("3. Ajuda")
    print("4. Sair")
    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        tela_curso()
    elif opcao == "2":
        acessar_curso()
    elif opcao == "3":
        tela_ajuda1()
    elif opcao == "4":
        print("Saindo... Obrigado por usar nossa plataforma!")
        exit()
    else:
        print("Opção inválida! Tente novamente.")
        tela_menu()


# Tela para seleção de cursos
def tela_curso():
    print("\n=== Cursos Disponiveis ===")
    print("\nEscolha a matéria que deseja cursar:")
    print("\n1. Introdução à Informatica")
    print("2. Segurança de Dados e LGPD")
    print("3. Noções de Progamação em Python")
    print("4. Ajuda")
    print("5. Sair")
    curso = input("Escolha uma opção: ").strip()

    if curso == "1":
        confirmaINT()
    elif curso == "2":
        confirmaLGPD()
    elif curso == "3":
        confirmaPY()
    elif curso == "4":
        tela_ajuda2()
    elif curso == "5":
        tela_menu()
    else:
        print("Opção inválida!")
        tela_curso()


# Funções de confirmação de inscrição para cada curso (ex: Introdução à Informática)
# Seguem a mesma lógica: confirmar senha -> salvar curso -> mostrar conteúdo


def confirmaINT():
    global senha_usuario
    usuarios = carregar_usuarios()
    print(f"\n=== Deseja se inscrever no curso de Introdução à Informatica? ===")
    print("1. Sim")
    print("2. Não")
    escolha = input("Escolha uma opção: ").strip()

    if escolha == "1":
        senha_confirmacao = input("\nPara continuar confirme sua senha: ")
        if senha_confirmacao == senha_usuario:
            usuarios[usuario_logado]["curso_atual"] = "introdução à informática"
            salvar_usuarios(usuarios)
            print(f"\nParabéns! Você foi inscrito com sucesso no curso de Introdução à Informatica")
            print(f"\nÉ uma disciplina que ensina os conceitos básicos de informática, como o funcionamento do computador, os componentes de hardware e software, e o uso da internet.")
            print(f"\nO que se aprende em Introdução à Informática? \nConceitos de computador, como sistema operacional, software, hardware, memória RAM, disco rígido, processadores, entre outros;\nComo o computador armazena e organiza as informações;\nComo usar os periféricos de entrada e saída, como o mouse;\nComo navegar na internet;\nNoções de segurança da informação;\nNoções de programação.")
            print(f"\nImportância da disciplina\nCompreender os conceitos de informática é fundamental para aproveitar as possibilidades da tecnologia e navegar na internet com segurança.")      
            print(f"\nInformática como ciência\nA informática é uma ciência que estuda o tratamento automático e racional da informação. É um ramo das ciências da informação e da computação.")
            print(f"\nFique ligado no calendário para não perder os próximos conteudos.")
            tela_menu()
        else:
            print("\nSenha incorreta. Tente novamente ou volte para a tela anterior.")
            print("1. Tentar novamente")
            print("2. Voltar")
            acao = input("Escolha uma opção: ").strip()
            if acao == "1":
                confirmaINT()
            elif acao == "2":
                tela_curso()
            else:
                print("Opção inválida! Retornando à tela anterior.")
                tela_curso()
    elif escolha == "2":
        print("Voltando para a tela de cursos...")
        tela_curso()
    else:
        print("Opção inválida! Voltando para a tela de cursos.")
        tela_curso()


# Confirmação e explicação do curso LGPD
def confirmaLGPD():
    global senha_usuario
    usuarios = carregar_usuarios()
    print(f"\n=== Deseja se inscrever no curso de Segurança de Dados e LGPD? ===")
    print("1. Sim")
    print("2. Não")
    escolha = input("Escolha uma opção: ").strip()

    if escolha == "1":
        senha_confirmacao = input("\nPara continuar confirme sua senha: ")
        if senha_confirmacao == senha_usuario:
            usuarios[usuario_logado]["curso_atual"] = "segurança de dados e lgpd"
            salvar_usuarios(usuarios)
            print(f"\nParabéns! Você foi inscrito com sucesso no curso de Segurança de Dados e LGPD.")
            print(f"\n A Lei Geral de Proteção de Dados (LGPD) estabelece regras para a segurança de dados pessoais, que devem ser coletados, processados, \narmazenados e compartilhados de forma segura.")
            print(f"\nA LGPD foi sancionada em 2018 e entrou em vigor em 2020.")
            print(f"\nPrincípios da LGPD")
            print(f"\nFinalidade, Adequação, Necessidade, Livre acesso, Qualidade dos dados, Transparência, Segurança, Prevenção, Não discriminação, \nResponsabilização e prestação de contas.")
            print(f"\nMedidas de segurança:")
            print(f"\n-Utilizar funções de localização remota, como 'Encontrar Meu iPhone' ou 'Encontre Meu Dispositivo'\n-Evitar redes públicas de Wi-Fi\n-Remover aplicativos não utilizados\n-Não deixar o celular, notebook ou computador ser acessado por pessoas estranhas\n-Encerrar a sessão sempre que sair do e-mail, de redes sociais\n-Limpar o histórico de navegação\n-Proteger a máquina de ataques virtuais")
            print(f"\nFique ligado no calendário para não perder os próximos conteudos.")
            tela_menu()
        else:
            print("\nSenha incorreta. Tente novamente ou volte para a tela anterior.")
            print("1. Tentar novamente")
            print("2. Voltar")
            acao = input("Escolha uma opção: ").strip()
            if acao == "1":
                confirmaLGPD()
            elif acao == "2":
                tela_curso()
            else:
                print("Opção inválida! Retornando à tela anterior.")
                tela_curso()
    elif escolha == "2":
        print("Voltando para a tela de cursos...")
        tela_curso()
    else:
        print("Opção inválida! Voltando para a tela de cursos.")
        tela_curso()


# Confirmação e explicação do curso Python
def confirmaPY():
    global senha_usuario
    usuarios = carregar_usuarios()
    print(f"\n=== Deseja se inscrever no curso de Noções de Programação em Python? ===")
    print("1. Sim")
    print("2. Não")
    escolha = input("Escolha uma opção: ").strip()

    if escolha == "1":
        senha_confirmacao = input("\nPara continuar confirme sua senha: ")
        if senha_confirmacao == senha_usuario:
            usuarios[usuario_logado]["curso_atual"] = "noções de programação em python"
            salvar_usuarios(usuarios)
            print(f"\nParabéns! Você foi inscrito com sucesso no curso de Noções de Programação em Python.")
            print(f"\n A programação em python é uma linguagem de programação de alto nível e de fácil aprendizado, muito usada para desenvolvimento de sites, análise de dados, inteligência artificial e muito mais.")
            print(f"\nConteúdo básico:")
            print(f"\n- Variáveis, Tipos de dados, Estruturas de controle, Funções, Bibliotecas, Entrada e saída de dados.")
            print(f"\nFique ligado no calendário para não perder os próximos conteudos.")
            tela_menu()
        else:
            print("\nSenha incorreta. Tente novamente ou volte para a tela anterior.")
            print("1. Tentar novamente")
            print("2. Voltar")
            acao = input("Escolha uma opção: ").strip()
            if acao == "1":
                confirmaPY()
            elif acao == "2":
                tela_curso()
            else:
                print("Opção inválida! Retornando à tela anterior.")
                tela_curso()
    elif escolha == "2":
        print("Voltando para a tela de cursos...")
        tela_curso()
    else:
        print("Opção inválida! Voltando para a tela de cursos.")
        tela_curso()


# Tela para acessar o curso atual e responder um quiz básico
def acessar_curso():
    usuarios = carregar_usuarios()
    global usuario_logado
    curso = usuarios[usuario_logado].get("curso_atual")
    if curso:
        print(f"\n=== Acesso ao curso: {curso} ===")
        # Apresenta conteúdo e um mini quiz dependendo do curso
        # (implementação individual de quiz omitida aqui por brevidade)
        # Retorna ao menu após o conteúdo
        if curso == "introdução à informática":
            print("\n=======Conteúdo: Introdução à Informática=======")
            print("\n A informática é a ciência que estuda o tratamento automático e racional da informação por meio de computadores.")
            print("Compreender os conceitos básicos de hardware, software e redes é fundamental para aproveitar as tecnologias do mundo moderno.")
            print("\nEste quiz foi criado para testar o quanto você sabe sobre o assunto. Antes do inicio do curso")
            print("\nQuiz: Qual dos seguintes é um componente de hardware?")
            print("1. Sistema Operacional")
            print("2. Memória RAM")
            print("3. Navegador de internet")
            resposta = input("Escolha a alternativa correta (1 a 3): ").strip()
            if resposta == "2":
                print("Correto! Memória RAM é um componente de hardware.")
            else:
                print("Errado. A resposta correta é 2: Memória RAM.")

        elif curso == "segurança de dados e lgpd":
            print("\nConteúdo: Segurança de Dados e LGPD")
            print("A Lei Geral de Proteção de Dados (LGPD) foi criada para garantir que informações pessoais sejam coletadas, armazenadas")
            print("e usadas de forma segura e transparente, protegendo os direitos dos cidadãos na era digital.")
            print("\nEste quiz foi criado para testar o quanto você sabe sobre o assunto.")
            print("\nQuiz: Qual princípio da LGPD exige que os dados sejam usados apenas para a finalidade específica?")
            print("1. Transparência")
            print("2. Finalidade")
            print("3. Segurança")
            resposta = input("Escolha a alternativa correta (1 a 3): ").strip()
            if resposta == "2":
                print("Correto! Finalidade é o princípio que limita o uso dos dados.")
            else:
                print("Errado. A resposta correta é 2: Finalidade.")

        elif curso == "noções de programação em python":
            print("\nConteúdo: Noções de Programação em Python")
            print("Python é uma linguagem de programação versátil e acessível, amplamente utilizada para desenvolver aplicações web,")
            print("automação, análise de dados e inteligência artificial, sendo ideal para iniciantes em programação.")
            print("Este quiz foi criado para testar o quanto você sabe sobre o assunto.")
            print("\nQuiz: Qual símbolo é usado para comentar uma linha em Python?")
            print("1. //")
            print("2. #")
            print("3. /* */")
            resposta = input("Escolha a alternativa correta (1 a 3): ").strip()
            if resposta == "2":
                print("Correto! O símbolo # é usado para comentários em Python.")
            else:
                print("Errado. A resposta correta é 2: #.")

        else:
            print("Conteúdo do curso ainda não disponível.")

        print("\nDigite '1' para voltar ao menu principal.")
        cmd = input("Comando: ").strip()
        if cmd == "1":
            tela_menu()
        else:
            print("Comando inválido, retornando ao menu.")
            tela_menu()
    else:
        print("\nVocê não está inscrito em nenhum curso ainda.")
        print("1. Inscrever-se em um curso")
        print("2. Voltar ao menu")
        escolha = input("Escolha: ").strip()
        if escolha == "1":
            tela_curso()
        elif escolha == "2":
            tela_menu()
        else:
            print("Opção inválida, retornando ao menu.")
            tela_menu()


# Tela de ajuda acessada pelo menu principal
def tela_ajuda1():
    print("\n=== Ajuda ===")
    print("Se você tiver dificuldades, entre em contato pelo e-mail suporte@example.com.")
    print("Digite '1' para retornar ao menu principal.")
    comando = input().strip()
    if comando == "1":
        tela_menu()
    else:
        print("Comando inválido! Retornando ao menu principal.")
        tela_menu()


# Tela de ajuda acessada a partir da escolha de curso
def tela_ajuda2():
    print("\n=== Ajuda ===")
    print("Se você tiver dificuldades, entre em contato pelo e-mail suporte@example.com.")
    print("Digite '1' para retornar à escolha do curso.")
    comando = input().strip()
    if comando == "1":
        tela_curso()
    else:
        print("Comando inválido! Retornando ao menu principal.")
        tela_menu()


# Função principal que inicia o sistema
def main():
    tela_inicial()


# Garante que o programa só rode se for executado diretamente
if __name__ == "__main__":
    main()
