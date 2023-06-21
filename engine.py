# Authores

# Name:  Edgar Sousa                          NMEC:   98757
# Name:  João Castanheira                     NMEC:   97521


from copy import deepcopy
import random
import threading

class Engine:

    # cost of previous state is added to the cost of the new state
    CUMMULATIVE_cost = 1

    # min normalized cost of new states
    MIN_NORMALIZED_cost = .9

    # send an 's' at the end of each play
    PULL_DOWN_PIECE = False

    # weights from https://github.com/takado8/Tetris
    A = -0.798752914564018
    B = 0.522287506868767
    C = -0.24921408023878
    D = -0.164626498034284

    # A = -0.510066
    # B =  0.760666
    # C = -0.35663
    # D = -0.184483

    S = (
        0b1100110000000,
        0b100001100001000000
    )

    Z = (
        0b11000011000000,
        0b100011000100000000
    )

    I = (
        0b10000100001000010000000,
        0b11110000000000000000
    )

    O = (
        0b11000110000000,
    )

    J = (
        0b1000011100000000000,
        0b110001000010000000,
        0b11100001000000,
        0b100001000110000000
    )

    L = (
        0b10011100000000000,
        0b100001000011000000,
        0b11100100000000,
        0b1100001000010000000
    )

    T = (
        0b100011100000000000,
        0b100001100010000000,
        0b11100010000000,
        0b100011000010000000
    )

    COORDS_TO_BIN = {
        ((0,0),(1,0),(1,1),(2,1)):(S,0),
        ((0,1),(0,2),(1,0),(1,1)):(S,1),
        ((0,1),(1,0),(1,1),(2,0)):(Z,0),
        ((0,0),(0,1),(1,1),(1,2)):(Z,1),
        ((0,0),(0,1),(0,2),(0,3)):(I,0),
        ((0,0),(1,0),(2,0),(3,0)):(I,1),
        ((0,0),(0,1),(1,0),(1,1)):(O,0),
        ((0,0),(1,0),(2,0),(2,1)):(L,0),
        ((0,0),(0,1),(0,2),(1,0)):(L,1),
        ((0,0),(0,1),(1,1),(2,1)):(L,2),
        ((0,2),(1,0),(1,1),(1,2)):(L,3),
        ((0,0),(0,1),(1,0),(2,0)):(J,0),
        ((0,0),(0,1),(0,2),(1,2)):(J,1),
        ((0,1),(1,1),(2,0),(2,1)):(J,2),
        ((0,0),(1,0),(1,1),(1,2)):(J,3),
        ((0,0),(1,0),(1,1),(2,0)):(T,0),
        ((0,0),(0,1),(0,2),(1,1)):(T,1),
        ((0,1),(1,0),(1,1),(2,1)):(T,2),
        ((0,1),(1,0),(1,1),(1,2)):(T,3),
    }

    POSSIBLE_PLAYS = {
        S:[
            ['a','a','a'],
            ['a','a'],
            ['a'],
            [],
            ['d'],
            ['d','d'],
            ['d','d','d'],
            ['w','a','a'],
            ['w','a'],
            ['w'],
            ['w','d'],
            ['w','d','d'],
            ['w','d','d','d'],
        ],
        Z:[
            ['a','a'],
            ['a'],
            [],
            ['d'],
            ['d','d'],
            ['d','d','d'],
            ['d','d','d','d'],
            ['w','a','a'],
            ['w','a'],
            ['w'],
            ['w','d'],
            ['w','d','d'],
            ['w','d','d','d'],
        ],
        L:[
            ['a','a','a'],
            ['a','a'],
            ['a'],
            [],
            ['d'],
            ['d','d'],
            ['d','d','d'],
            ['w','a','a'],
            ['w','a'],
            ['w'],
            ['w','d'],
            ['w','d','d'],
            ['w','d','d','d'],
            ['w','w','a','a'],
            ['w','w','a'],
            ['w','w'],
            ['w','w','d'],
            ['w','w','d','d'],
            ['w','w','d','d','d'],
            ['w','w','d','d','d','d'],
            ['w','w','w','a','a'],
            ['w','w','w','a'],
            ['w','w','w'],
            ['w','w','w','d'],
            ['w','w','w','d','d'],
            ['w','w','w','d','d','d'],
        ],
        J:[
            ['a','a','a'],
            ['a','a'],
            ['a'],
            [],
            ['d'],
            ['d','d'],
            ['d','d','d'],
            ['w','a','a'],
            ['w','a'],
            ['w'],
            ['w','d'],
            ['w','d','d'],
            ['w','d','d','d'],
            ['w','w','a','a'],
            ['w','w','a'],
            ['w','w'],
            ['w','w','d'],
            ['w','w','d','d'],
            ['w','w','d','d','d'],
            ['w','w','d','d','d','d'],
            ['w','w','w','a','a'],
            ['w','w','w','a'],
            ['w','w','w'],
            ['w','w','w','d'],
            ['w','w','w','d','d'],
            ['w','w','w','d','d','d'],
        ],
        O:[
            ['a','a'],
            ['a'],
            [],
            ['d'],
            ['d','d'],
            ['d','d','d'],
            ['d','d','d','d'],
        ],
        I:[
            ['a'],
            [],
            ['d'],
            ['d','d'],
            ['d','d','d'],
            ['w','a','a','a'],
            ['w','a','a'],
            ['w','a'],
            ['w'],
            ['w','d'],
            ['w','d','d'],
            ['w','d','d','d'],
            ['w','d','d','d','d'],
        ],
        T:[
            ['a','a','a'],
            ['a','a'],
            ['a'],
            [],
            ['d'],
            ['d','d'],
            ['d','d','d'],
            ['w','a','a'],
            ['w','a'],
            ['w'],
            ['w','d'],
            ['w','d','d'],
            ['w','d','d','d'],
            ['w','w','a','a'],
            ['w','w','a'],
            ['w','w'],
            ['w','w','d'],
            ['w','w','d','d'],
            ['w','w','d','d','d'],
            ['w','w','d','d','d','d'],
            ['w','w','w','a','a'],
            ['w','w','w','a'],
            ['w','w','w'],
            ['w','w','w','d'],
            ['w','w','w','d','d'],
            ['w','w','w','d','d','d'],
        ]
    }

    def calc_states(self):
        children = []

        if not self.pieces:
            return children

        plays = Engine.POSSIBLE_PLAYS[self.pieces[0]]        

        for play in plays:
            child = Engine(
                matrix=self.matrix,
                pieces=self.pieces[:]
            )
            child.cost = self.cost
            # if Engine.PULL_DOWN_PIECE:
            #     play.append('s')
            child.plays.append(play)
            for key in play:
                child.input(key)
                child.loop()
            while len(self.pieces) == len(child.pieces):
                child.loop()
            children.append(child)

        # removing shitty plays
        # max_fit = max([s.cost for s in children])
        # min_fit = min([s.cost for s in children])
        # dif = max_fit - min_fit

        # if dif:
        #     normalized = [((s.cost-min_fit)/dif,s) for s in children]
        #     children = [s for n,s in normalized if n >= Engine.MIN_NORMALIZED_cost]
        
        return children

    def empty_matrix():
        matrix = 0
        for _ in range(30):
            matrix <<= 10
            matrix |= 0b1000000001
        matrix <<= 10
        matrix |= 0b1111111111
        return matrix

    BORDERS = empty_matrix()

    DEFAULT_ROT = 1
    DEFAULT_X = 5
    DEFAULT_Y = 27

    def from_json(json):
        matrix = 0
        for l in json['game']:
            x = l[0]
            y = l[1]
            square = 1 << ((30 - y) * 10) << (9 - x)
            matrix |= square

        matrix |= Engine.BORDERS
        pieces = [json['piece']]
        pieces.extend(json['next_pieces'])

        x = 0
        y = 0
        rot = 0      

        for i, piece in enumerate(pieces):
            min_x = min([
                piece[0][0],
                piece[1][0],
                piece[2][0],
                piece[3][0],
            ])
            max_y = max([
                piece[0][1],
                piece[1][1],
                piece[2][1],
                piece[3][1],
            ])
            piece = [
                (piece[0][0]-min_x,max_y-piece[0][1]),
                (piece[1][0]-min_x,max_y-piece[1][1]),
                (piece[2][0]-min_x,max_y-piece[2][1]),
                (piece[3][0]-min_x,max_y-piece[3][1]),
            ]

            piece.sort()
            piece = tuple(piece)
            piece, curr_rot = Engine.COORDS_TO_BIN[piece]
            pieces[i] = piece

            # if i == 0:
            #     x = min_x + 3
            #     y = 29 - max_y
            #     rot = curr_rot
        
        game = Engine(
            matrix=matrix,
            pieces=pieces,
            # x=x,
            # y=y,
            # rot=rot
        )

        return game

    def __init__(
        self,
        matrix=BORDERS,
        pieces=[],
        weight =(A,B,C,D),
        rot=DEFAULT_ROT,
        x=DEFAULT_X,
        y=DEFAULT_Y
    ):
        self.matrix = matrix
        self.pieces = pieces
        self.weight = weight
        self.x = x
        self.y = y
        self.rot = rot
        self.plays = []
        self.lines = 0
        self.score = 0
        self.cost = 0
        self.key = ''

    def __str__(self):
        piece = self.piece_matrix()
        board = piece | self.matrix | 1 << 300
        string = ''
        for _ in range(30):
            row = board & 0b1111111111 | 0b10000000000
            board >>= 10
            string = bin(row)[3:] + '\n' + string
        string += '\n'
        return string#.replace('0','   ').replace('1',' * ')

    def __lt__(self,other):
        return self.cost > other.cost
    
    def add_piece(self, piece):
        self.pieces.append(piece)

    def input(self,key):
        self.key = key

    def clear_rows(self):
        upper_half = self.matrix >> 10
        lower_half = self.matrix & 0b1111111111
        lines = 0        
        i = 1
        while(upper_half):
            row = upper_half & 0b1111111111
            if row == 0b1000000001:
                break
            elif row == 0b1111111111:
                lines += 1
            else:
                lower_half = lower_half | row << 10 * i
                i += 1                
            upper_half >>= 10
        self.lines += lines
        self.score += lines ** 2
        self.matrix = lower_half | Engine.BORDERS
    
    def piece_matrix(self):
        matrix = 0

        if not self.pieces:
            return matrix

        # place piece on empty matrix
        rotations = len(self.pieces[0])
        piece = self.pieces[0][self.rot % rotations]

        for i in range(5):
            row = piece & 0b11111

            if row:
                row <<= 8
                row >>= self.x
                row <<= (i + self.y) * 10
                row >>= 30
                matrix |= row
            
            piece >>= 5
        
        return matrix

    def calc_cost(self):
        matrix = self.matrix

        height = [0,0,0,0,0,0,0,0]
        holes = [0,0,0,0,0,0,0,0]
        gaps = [0,0,0,0,0,0,0,0]

        for i in range(29):
            # get next row
            matrix >>= 10
            row = matrix & 0b1111111111

            # if empty row
            if row == 0b1000000001:
                break

            # remove borders to the sides
            row >>= 1
            row &= 0b11111111            

            # for each column of row
            for j in range(8):
                # if not empty
                if row & 0b00000001:
                    height[j] = i + 1
                    holes[j] += gaps[j]
                    gaps[j] = 0
                else:
                    gaps[j] += 1
                # move to next column
                row >>= 1

        agg_height = sum(height)

        holes = sum(holes)

        lines = self.lines

        bumpiness = sum([abs(height[i] - height[i+1]) for i in range(len(height) - 1)])

        a,b,c,d = self.weight

        '''if highest_height > 20 :
            a = -4'''

        cost = a * agg_height + b * lines + c * holes + d * bumpiness

        return cost

    def loop(self):
        if not self.pieces:
            return False

        piece = self.piece_matrix()
        
        collision = piece & self.matrix

        # game is over
        if collision:
            return False

        # piece drops down 1 square
        self.y -= 1

        piece = self.piece_matrix()

        collision = piece & self.matrix

        if collision:
            # pull piece back up 1 square
            piece <<= 10

            # join piece and matrix
            self.matrix |= piece

            # clear rows
            self.clear_rows()

            if self.pieces:
                self.pieces.pop(0)

            self.x = Engine.DEFAULT_X
            self.y = Engine.DEFAULT_Y
            self.rot = Engine.DEFAULT_ROT
            self.key = ''

            self.cost = Engine.CUMMULATIVE_cost * self.cost + self.calc_cost()
            
            return True

        # rotate piece
        if self.key == 'w':
            self.rot += 1
            self.rot %= len(self.pieces[0])

        # pull piece to the left
        elif self.key == 'a':
            self.x -= 1
        
        # pull piece to the right
        elif self.key == 'd':
            self.x += 1

        # place piece on matrix
        piece = self.piece_matrix()

        collision = piece & self.matrix

        # check for collisions
        if collision:        
            if self.key == 'w':
                self.rot -= 1
                self.rot %= len(self.pieces[0])

            elif self.key == 'a':
                self.x += 1

            elif self.key == 'd':
                self.x -= 1
        
        self.key = ''        
        return True
    


def main():


    game = Engine()

    t = threading.Thread(target=game.start)

    t.start()

    t.join()
    
    print('Done!')

if __name__ == '__main__':
    main()
    