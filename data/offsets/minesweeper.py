import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """       
        # {A,B,C} = 3 --> return {A,B,C}
        # {A,B,C} = 1 --> return {} ?
        if len(self.cells) > 0 and len(self.cells) == self.count:
            print(f"New knownmines: {str(self)}")
            return self.cells

        return set()

        # raise NotImplementedError

    
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        #   {A,B} = 0 --> return {A,B}
        # {A,B,C} = 1 --> return {} ?
        if len(self.cells) > 0 and self.count == 0:
            print(f"New knownsafes: {str(self)}")
            return self.cells

        return set()

        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # {A,B,C} = 1 --> mark_mine(A)
        # {B,C} = 0
        # {A,B,C,D} = 2 --> mark_mine(B)
        # {A,C,D} = 1
        if cell in self.cells:
            self.count -= 1
            self.cells.remove(cell)

        # raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # {A,B,C} = 1 --> mark_safe(A)
        # {B,C} = 1
        # {A,B,C} = 2 --> mark_safe(B)
        # {A,C} = 2
        if cell in self.cells:
            self.cells.remove(cell)

        # raise NotImplementedError

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1
        self.moves_made.add(cell)
        # 2
        self.safes.add(cell)
        # Como esta es segura, recorremos todas las sentencias
        # Para descartarla como "sospechosa", posible mina
        for sentence in self.knowledge:
            # la funcion verifica si la celda está en la sentencia
            sentence.mark_safe(cell)

        # 3
        # Formamos los vecinos de cell (i,j)
        cell_neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # Verificar si está en las dimensiones
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i,j) not in self.moves_made:
                        cell_neighbors.add((i,j))

        # Formamos y agregamos una nueva sentencia con vecinos = minas alrededor
        self.knowledge.append(Sentence(cell_neighbors, count))

        # 4
        for sentence in self.knowledge:
            new_mines = sentence.known_mines()
            new_safes = sentence.known_safes()
            
            self.mines = self.mines.union(new_mines)
            self.safes = self.safes.union(new_safes)

            for mine in self.mines:
                sentence.mark_mine(mine)
            for safe in self.safes:
                sentence.mark_safe(safe)
            # Remove empty sentences
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)

        # 5
        for k in range(len(self.knowledge)):
            sentence1 = self.knowledge[k]
            set1 = sentence1.cells

            for m in range(k+1, len(self.knowledge)):
                sentence2 = self.knowledge[m]
                set2 = sentence2.cells

                # Siguiendo la formula de la página
                # {A,B} = 1 is subset {A,B,C} = 2 (si)
                # {A,B,C} - {A,B} = 2 - 1
                # {C} = 1
                if set1.issubset(set2) and set1 != set2:
                    result_set = set2 - set1
                    result_count = sentence2.count - sentence1.count

                    self.knowledge.append(Sentence(result_set, result_count))

                    print(f"New sentence from {set1} and {set2}: {result_set} = {result_count}")

        print(f"{len(cell_neighbors)} Neighbors of {cell}: {cell_neighbors} - Count: {count}")
        print(f"{len(self.safes)} Safes: {self.safes}")
        print(f"{len(self.mines)} Mines: {self.mines}")
        print("-"*100)
        # raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        for cell in self.safes:
            if cell not in self.moves_made:
                # self.moves_made.add(cell) SHOULD NOT MODIFY ^
                return cell

        return None

        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        # Hacemos un set de todas las casillas
        possible_cells = []
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    possible_cells.append( (i,j) )
            
        if possible_cells:
            return random.choice(possible_cells)
        
        return None
    

        raise NotImplementedError
