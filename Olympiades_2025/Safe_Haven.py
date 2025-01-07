class Haven:
    
    def __init__(self, n, r, g):
        self.long = n
        self.large = n
        self.arena_size = self.long * self.large
        self.r_mod = r
        self.g_mod = g
        self.squares = [{'status': 'empty', 'number': i + 1} for i in range(self.arena_size)]
        self.red_control = 0
        self.green_control = 0
    
    def print_arena(self):
        print('\n', end='')
        for square in range(self.arena_size):
            if self.squares[square]['status'] == 'red':
                print('R', end='')
            elif self.squares[square]['status'] == 'green':
                print('G', end='')
            else:
                print('.', end='')
            if self.squares[square]['number'] % self.long == 0:
                print('\n', end='')    
        
    def take_control(self, square_number, color):
        if color == 'red':
            self.squares[square_number - 1]['status'] = 'red'
            self.red_control += 1
        elif color == 'green':
            self.squares[square_number - 1]['status'] = 'green'
            self.green_control += 1
        self.print_arena()

    def get_square_number(self, row, col):
        return row * self.long + col + 1

    def setup(self):
        for square in range(self.arena_size):
            self.squares[square]['status'] = 'empty'
        red_pos = 0
        green_pos = 0
        red_visits = 0
        green_visits = 0
        self.take_control(red_pos + 1, 'red')
        while any(square['status'] == 'empty' for square in self.squares):#

            # Green player's turn
            while green_visits < self.g_mod:
                green_pos = (green_pos + 1) % self.arena_size
                if self.squares[green_pos]['status'] == 'empty':
                    green_visits += 1
            self.take_control(green_pos + 1, 'green')
            green_visits = 0

            if all(square['status'] != 'empty' for square in self.squares):
                break

            # Red player's turn
            while red_visits < self.r_mod:
                red_pos = (red_pos + 1) % self.arena_size
                if self.squares[red_pos]['status'] == 'empty':
                    red_visits += 1
            self.take_control(red_pos + 1, 'red')
            red_visits = 0
        print('Setup complete')

    

    
            
        
    def is_neighbour(self, square1, square2):
        row1, col1 = divmod(square1 - 1, self.long)
        row2, col2 = divmod(square2 - 1, self.long)
        result = abs(row1 - row2) + abs(col1 - col2) == 1
        return result

    def find_haven(self, start_square):
        haven = []
        to_visit = [start_square]
        while to_visit:
            current = to_visit.pop()
            if current not in haven:
                haven.append(current)
                neighbours = [i for i in range(self.arena_size) if self.is_neighbour(current, i)]
                for neighbour in neighbours:
                    if self.squares[neighbour]['status'] == self.squares[start_square]['status']:
                        to_visit.append(neighbour)
        return haven

    def is_safe_haven(self, haven):
        color = self.squares[haven[0]]['status']
        for square in haven:
            if self.squares[square]['status'] != color:
                return False
        return True
    
    def select_move(self, color):
        opponent_color = 'green' if color == 'red' else 'red'
        havens = []
        
        for i in range(self.arena_size):
            if self.squares[i]['status'] == opponent_color:
                haven = self.find_haven(i)
                if haven not in havens:
                    havens.append(haven)
        
        # Filter non-safe havens
        non_safe_havens = [haven for haven in havens if not self.is_safe_haven(haven)]
        
        if not non_safe_havens:
            return None
        
        # Sort havens by the number of opponent's squares, then by player's squares, then by highest value position
        non_safe_havens.sort(key=lambda h: (
            sum(1 for sq in h if self.squares[sq]['status'] == opponent_color),
            -sum(1 for sq in h if self.squares[sq]['status'] == color),
            -max(h)
        ))
        
        selected_haven = non_safe_havens[0]
        
        # Find the lowest value position in this haven that the player controls
        player_squares = [sq for sq in selected_haven if self.squares[sq]['status'] == color]
        if not player_squares:
            return None
        
        player_squares.sort()
        
        for sq in player_squares:
            neighbours = [n for n in range(self.arena_size) if self.is_neighbour(sq, n) and self.squares[n]['status'] == opponent_color]
            if neighbours:
                self.move(sq, min(neighbours))
                return sq, min(neighbours)
        print_arena()
        return None
    
    def move(self, square1, square2):
        if self.is_neighbour(square1, square2) and self.squares[square1]['status'] != self.squares[square2]['status']:
            current_color = self.squares[square1]['status']
            self.squares[square1]['status'] = 'empty'
            self.squares[square2]['status'] = current_color
            if self.squares[square2]['status'] == 'empty':
                if current_color == 'red':
                    self.red_control -= 1
                    self.green_control += 1
                elif current_color == 'green':
                    self.green_control -= 1
                    self.red_control += 1
        print_arena()


    def count_safe_havens(self):
        red_safe_havens = 0
        green_safe_havens = 0
        visited = set()
        
        for i in range(self.arena_size):
            if i not in visited:
                haven = self.find_haven(i)
                if self.is_safe_haven(haven):
                    if self.squares[i]['status'] == 'red':
                        red_safe_havens += 1
                    elif self.squares[i]['status'] == 'green':
                        green_safe_havens += 1
                visited.update(haven)
        
        return red_safe_havens, green_safe_havens

#TEST
haven = Haven(3, 5, 5)
haven.setup()
red_safe_havens, green_safe_havens = haven.count_safe_havens()
print(red_safe_havens, green_safe_havens)
    
#assert (red_safe_havens, green_safe_havens) == (2, 1)
    
#QUESTION2(B)

        


    
    