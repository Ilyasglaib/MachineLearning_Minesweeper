import itertools
import random
from turtle import width
from typing import List


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
        if len(self.cells)==self.count:
            return self.cells
        else:
            return set()



    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count==0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count=self.count-1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

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
        self.moves_made.add(cell)
        self.mark_safe(cell)
        i,j=cell
        all_moves=set()
        for k in range(self.height):
            for l in range(self.width):
                all_moves.add((k,l))
        L={(i+1,j),(i+1,j+1),(i+1,j-1),(i,j-1),(i,j+1),(i-1,j-1),(i-1,j),(i-1,j+1)}
        neighbors=set()
        for cell in L:
            if cell in all_moves:
                neighbors.add(cell)

        #find the possible neighbors depending on the position in the board
        c=count
        eliminated_cells=set()
        for cell in neighbors:
            if cell in self.mines:
                eliminated_cells.add(cell)
                c=c-1
            if cell in self.safes:
                eliminated_cells.add(cell)
            if cell in self.moves_made:
                eliminated_cells.add(cell)
        if len(eliminated_cells)!=0:
            for cell in eliminated_cells:
             neighbors.remove(cell)
        # neighbors contains now only uncertain cells
        new_sentence=Sentence(neighbors,c)
        #update knowledge with new sentence
        self.knowledge.append(new_sentence)
        new_safe_tiles=new_sentence.known_safes()
        new_mine_tiles=new_sentence.known_mines()
        if len(new_mine_tiles)!=0:
            bin1=set()

            for mine in new_mine_tiles:
                bin1.add(mine)
            for mine in bin1:
                self.mark_mine(mine)
        if len(new_safe_tiles)!=0:  
            bin2=set()  
            for safe in new_safe_tiles:
                bin2.add(safe)
            for safe in bin2:
                self.mark_safe(safe)
        
        #mark new tiles in the new sentence as safe or mines
         
        for sentence in self.knowledge:
            s_tiles=sentence.known_safes()
            m_tiles=sentence.known_mines()
            if len(s_tiles)!=0:
                bin3=set()

                for s in s_tiles:
                    bin3.add(s)
                for s in bin3:
                    self.mark_safe(s)
            if len(m_tiles)!=0:
                bin4=set()

                for m in m_tiles:
                    bin4.add(m)
                for m in bin4:
                    self.mark_mine(m)
        #new tiles discovered to be safe or mines as a consequence of marking the new tiles
        for sentence in self.knowledge:
            if len(sentence.cells)==0:
                self.knowledge.remove(sentence)

        #new inference that we can make
        additional_knowledge=[]
        for sentence1 in self.knowledge:
            cells1=sentence1.cells
            for sentence2 in self.knowledge:
                if not sentence2.__eq__(sentence1):
                    cells2=sentence2.cells
                    if cells2.issubset(cells1):
                        cells3=cells1.difference(cells2)
                        count3=sentence1.count-sentence2.count
                        sentence3=Sentence(cells3,count3)
                        additional_knowledge.append(sentence3)
        #add only different new sentences                
        if len(additional_knowledge)!=0:
            for sentence in additional_knowledge:
                if sentence not in self.knowledge:
                  self.knowledge.append(sentence)
        #add only non empty sentences
        for sentence in self.knowledge:
            if len(sentence.cells)==0:
                self.knowledge.remove(sentence)

        #based one the additional inferences, maybe some tiles were discovered to be mines or safe
        for sentence in additional_knowledge:
              if len(sentence.cells)==0:
                additional_knowledge.remove(sentence)
        #Draw new conclusions from new statements added
        for sentence in additional_knowledge:
            s_tiles2=sentence.known_safes()
            m_tiles2=sentence.known_mines()
            if len(s_tiles2)!=0:
                bin5=set()
                for s in s_tiles2:
                    bin5.add(s)
                for s in bin5:
                    self.mark_safe(s)
            if len(m_tiles2)!=0:
                bin6=set()
                for m in m_tiles2:
                    bin6.add(m)
                for m in bin6:
                    self.mark_mine(m)


       
            
            
            





    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        if len(self.safes)!=0:
            for cell in self.safes:
                if cell not in self.moves_made:
                    return cell
            
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        all_moves=set()
        for i in range(self.height-1):
            for j in range(self.width-1):
                all_moves.add((i,j))
        impossible_moves=self.moves_made.union(self.mines)
        possible_move=all_moves.difference(impossible_moves)
        if len(possible_move)!=0:
            L=list(possible_move)
            i=random.randint(0,len(L)-1)
            return L[i]
        else:
            return None
        

