"""Sistema de biblioteca no terminal: trabalho de orientacao a objetos."""

from abc import ABC, abstractmethod


class Emprestavel(ABC):
    """Interface para itens que podem ser emprestados e devolvidos."""

    @abstractmethod
    def emprestar(self):
        pass

    @abstractmethod
    def devolver(self):
        pass


class ItemAcervo(ABC):
    """Classe abstrata que representa um item do acervo."""

    def __init__(self, codigo, nome):
        self._codigo = codigo
        self._nome = ""
        self._emprestado = False
        self.nome = nome  # Utiliza o setter com validacao.

    @property
    def codigo(self):
        return self._codigo

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O nome nao pode ficar vazio.")
        self._nome = valor.strip()

    @property
    def emprestado(self):
        return self._emprestado

    @abstractmethod
    def prazo_emprestimo(self):
        """Retorna o prazo de emprestimo em dias."""
        pass

    def informacoes_emprestimo(self):
        """Metodo concreto que usa o metodo abstrato."""
        return f"Prazo de emprestimo: {self.prazo_emprestimo()} dias"


class Livro(ItemAcervo, Emprestavel):
    def __init__(self, codigo, nome, autor):
        super().__init__(codigo, nome)
        if not autor.strip():
            raise ValueError("O autor nao pode ficar vazio.")
        self._autor = autor.strip()

    @property
    def autor(self):
        return self._autor

    def prazo_emprestimo(self):
        return 14

    def emprestar(self):
        if self._emprestado:
            return "Este livro ja esta emprestado."
        self._emprestado = True
        return f"Livro emprestado com sucesso por {self.prazo_emprestimo()} dias."

    def devolver(self):
        if not self._emprestado:
            return "Este livro ja esta disponivel."
        self._emprestado = False
        return "Livro devolvido com sucesso."

    def __str__(self):
        estado = "Emprestado" if self.emprestado else "Disponivel"
        return (f"[Livro] Codigo: {self.codigo} | Nome: {self.nome} | "
                f"Autor: {self.autor} | {estado} | {self.informacoes_emprestimo()}")


class Revista(ItemAcervo, Emprestavel):
    def __init__(self, codigo, nome, edicao):
        super().__init__(codigo, nome)
        if not isinstance(edicao, int) or edicao <= 0:
            raise ValueError("A edicao deve ser um numero inteiro positivo.")
        self._edicao = edicao

    @property
    def edicao(self):
        return self._edicao

    def prazo_emprestimo(self):
        return 7

    def emprestar(self):
        if self._emprestado:
            return "Esta revista ja esta emprestada."
        self._emprestado = True
        return f"Revista emprestada com sucesso por {self.prazo_emprestimo()} dias."

    def devolver(self):
        if not self._emprestado:
            return "Esta revista ja esta disponivel."
        self._emprestado = False
        return "Revista devolvida com sucesso."

    def __str__(self):
        estado = "Emprestada" if self.emprestado else "Disponivel"
        return (f"[Revista] Codigo: {self.codigo} | Nome: {self.nome} | "
                f"Edicao: {self.edicao} | {estado} | {self.informacoes_emprestimo()}")


class Biblioteca:
    """Gerencia a lista de objetos do acervo."""

    def __init__(self):
        self._itens = [
            Livro(1, "Dom Casmurro", "Machado de Assis"),
            Revista(2, "Ciencia Hoje", 150),
            Livro(3, "O Cortico", "Aluisio Azevedo"),
        ]
        self._proximo_codigo = 4

    def cadastrar(self, item):
        if any(existente.codigo == item.codigo for existente in self._itens):
            raise ValueError("Ja existe um item com este codigo.")
        self._itens.append(item)

    def novo_codigo(self):
        codigo = self._proximo_codigo
        self._proximo_codigo += 1
        return codigo

    def listar(self):
        if not self._itens:
            print("O acervo esta vazio.")
            return
        print("\n--- ACERVO ---")
        # Polimorfismo: a mesma chamada usa o __str__ de cada tipo concreto.
        for item in self._itens:
            print(item)
            print("  Prazo (polimorfismo):", item.prazo_emprestimo(), "dias")

    def buscar(self, termo):
        termo = termo.strip().casefold()
        return [item for item in self._itens
                if str(item.codigo) == termo or termo in item.nome.casefold()]

    def buscar_codigo(self, codigo):
        for item in self._itens:
            if item.codigo == codigo:
                return item
        return None

    def remover(self, codigo):
        item = self.buscar_codigo(codigo)
        if item is None:
            return "Item nao encontrado."
        if item.emprestado:
            return "Nao e possivel remover um item emprestado. Devolva-o primeiro."
        self._itens.remove(item)
        return "Item removido com sucesso."


def ler_inteiro(mensagem, minimo=1):
    while True:
        try:
            numero = int(input(mensagem).strip())
            if numero < minimo:
                print(f"Digite um numero inteiro maior ou igual a {minimo}.")
                continue
            return numero
        except ValueError:
            print("Entrada invalida. Digite um numero inteiro.")


def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print("Este campo nao pode ficar vazio.")


def executar_menu():
    biblioteca = Biblioteca()
    while True:
        print("\n===== SISTEMA DE BIBLIOTECA =====")
        print("1 - Cadastrar")
        print("2 - Listar")
        print("3 - Buscar")
        print("4 - Remover")
        print("5 - Acao do sistema (emprestar/devolver)")
        print("0 - Sair")
        try:
            opcao = input("Escolha uma opcao: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nPrograma encerrado.")
            break

        if opcao == "0":
            print("Programa encerrado. Ate logo!")
            break
        elif opcao == "1":
            print("1 - Livro | 2 - Revista")
            tipo = input("Tipo de item: ").strip()
            if tipo not in ("1", "2"):
                print("Tipo invalido. Cadastro cancelado.")
                continue
            nome = ler_texto("Nome: ")
            if tipo == "1":
                autor = ler_texto("Autor: ")
                item = Livro(biblioteca.novo_codigo(), nome, autor)
            else:
                edicao = ler_inteiro("Numero da edicao: ")
                item = Revista(biblioteca.novo_codigo(), nome, edicao)
            biblioteca.cadastrar(item)
            print(f"Item cadastrado com sucesso! Codigo: {item.codigo}")
        elif opcao == "2":
            biblioteca.listar()
        elif opcao == "3":
            termo = ler_texto("Digite o nome ou codigo: ")
            encontrados = biblioteca.buscar(termo)
            if encontrados:
                for item in encontrados:
                    print(item)
            else:
                print("Nenhum item encontrado.")
        elif opcao == "4":
            codigo = ler_inteiro("Codigo do item a remover: ")
            print(biblioteca.remover(codigo))
        elif opcao == "5":
            codigo = ler_inteiro("Codigo do item: ")
            item = biblioteca.buscar_codigo(codigo)
            if item is None:
                print("Item nao encontrado.")
                continue
            print(item)
            print("1 - Emprestar | 2 - Devolver | 3 - Consultar prazo")
            acao = input("Escolha a acao: ").strip()
            if acao == "1":
                print(item.emprestar())
            elif acao == "2":
                print(item.devolver())
            elif acao == "3":
                print(item.informacoes_emprestimo())
            else:
                print("Acao invalida.")
        else:
            print("Opcao invalida. Escolha uma opcao do menu.")


if __name__ == "__main__":
    executar_menu()

