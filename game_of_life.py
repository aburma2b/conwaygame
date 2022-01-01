# Name: Ankush Burman   
# Section: Self
# Date: Started: Dec 29, 2021; Finished: 
# game_of_life.py

import graphics5ab as gr 
import random

## Written by Sarina Canelake & Kelly Casteel, August 2010
## Revised January 2011

############################################################
# GLOBAL VARIABLES
############################################################
    
#BLOCK_SIZE = 40
BLOCK_SIZE = 25
BLOCK_OUTLINE_WIDTH = 2
#BOARD_WIDTH = 12
BOARD_WIDTH = 30
#BOARD_HEIGHT = 12
BOARD_HEIGHT = 30

neighbor_test_blocklist = [(0,0), (1,1)]
toad_blocklist = [(4,4), (3,5), (3,6), (5,7), (6,5), (6,6)]
beacon_blocklist = [(2,3), (2,4), (3,3), (3,4), (4,5), (4,6), (5,5), (5,6)]
glider_blocklist = [(1,2), (2,3), (3,1), (3,2), (3,3)]
pulsar_blocklist = [(2,4), (2,5), (2,6), (4,2), (4,7), (5,2), (5,7),
                    (6,2), (6,7), (7,4), (7,5), (7,6), ]
# for diehard, make board at least 25x25, might need to change block size
diehard_blocklist = [(5,7), (6,7), (6,8), (10,8), (11,8), (12,8), (11,6)]

############################################################
# TEST CODE (don't worry about understanding this section)
############################################################

def test_neighbors(board):
    '''
    Code to test the board.get_block_neighbor function
    '''
    for block in board.block_list.values():
        neighbors = board.get_block_neighbors(block)
        ncoords = [neighbor.get_coords() for neighbor in neighbors]
        if block.get_coords() == (0,0):
            zeroneighs = [(0,1), (1,1), (1,0)]
            for n in ncoords:
                if n not in zeroneighs:
                    print "Testing block at (0,0)"
                    print "Got", ncoords
                    print "Expected", zeroneighs
                    return False

            for neighbor in neighbors:
                if neighbor.get_coords() == (1, 1):
                    if neighbor.is_live() == False:
                        print "Testing block at (0, 0)..."
                        print "My neighbor at (1, 1) should be live; it is not."
                        print "Did you return my actual neighbors, or create new copies of them?"
                        print "FAIL: get_block_neighbors() should NOT return new Blocks!"
                        return False

        elif block.get_coords() == (1,1):
            oneneighs = [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1),(2,2)]
            for n in ncoords:
                if n not in oneneighs:
                    print "Testing block at (1,1)"
                    print "Got", ncoords
                    print "Expected", oneneighs
                    return False
            for n in oneneighs:
                if n not in ncoords:
                    print "Testing block at (1,1)"
                    print "Got", ncoords
                    print "Expected", oneneighs
                    return False
    print "Passed neighbor test"
    return True


############################################################
# BLOCK CLASS (Read through and understand this part!)
############################################################

class Block(gr.Rectangle):
    ''' Block class:
        Implement a block for a tetris piece
        Attributes: x - type: int
                    y - type: int
        specify the position on the board
        in terms of the square grid
    '''

    def __init__(self, pos, color):
        '''
        pos: a Point object specifing the (x, y) square of the Block (NOT in pixels!)
        color: a string specifing the color of the block (eg 'blue' or 'purple')
        '''
        self.x = pos.x
        self.y = pos.y
        
        p1 = gr.Point(pos.x*BLOCK_SIZE,
                   pos.y*BLOCK_SIZE)
        p2 = gr.Point(p1.x + BLOCK_SIZE, p1.y + BLOCK_SIZE)

        gr.Rectangle.__init__(self, p1, p2)
        self.setWidth(BLOCK_OUTLINE_WIDTH)
        self.setFill(color)
        self.status = 'dead'
        self.new_status = 'None'
        
    def get_coords(self):
        return (self.x, self.y)

    def set_live(self, canvas):
        '''
        Sets the block status to 'live' and draws it on the grid.
        Be sure to do this on the canvas!
        '''
        if self.status=='dead':
          self.status = 'live'
          self.draw(canvas)

    def set_dead(self):
        '''
        Sets the block status to 'dead' and undraws it from the grid.
        '''
        if self.status=='live':
          self.status = 'dead'
          self.undraw()

    def is_live(self):
        '''
        Returns True if the block is currently 'live'. Returns False otherwise.
        '''
        if self.status == 'live':
            return True
        return False

    def reset_status(self, canvas):
        '''
        Sets the new_status to be the current status
        '''
        if self.new_status=='dead':
            self.set_dead()
        elif self.new_status=='live':
            self.set_live(canvas)
        

###########################################################
# BOARD CLASS (Read through and understand this part!)
# Print out and turn in this section.
# Name: Ankush Burman
# Recitation: Self-Study 
###########################################################

class Board(object):
    ''' Board class: it represents the Game of Life board

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:CanvasFrame - where the blocks will be drawn
                    block_list - type:Dictionary - stores the blocks for a given position
    '''
    
    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.win = win
        # self.delay is the number of ms between each simulation. Change to be
        # shorter or longer if you wish!
        self.delay = 1000

        # create a canvas to draw the blocks on
        self.canvas = gr.GraphWin(win, self.width * BLOCK_SIZE,
                                       self.height * BLOCK_SIZE)
        self.canvas.setBackground('white')

        # initialize grid lines
        for x in range(1,self.width):
            self.draw_gridline(gr.Point(x, 0), gr.Point(x, self.height))

        for y in range(1,self.height):
            self.draw_gridline(gr.Point(0, y), gr.Point(self.width, y))

        # For each square on the board, we need to initialize
        # a block and store that block in a data structure. A
        # dictionary (self.block_list) that has key:value pairs of
        # (x,y):Block will be useful here.
        self.block_list = {}

        #### Ankush Burman Code ####
        for x in range(self.width):
             for y in range(self.height):
                 pos = gr.Point(x, y)
                 color = "plum"
                 self.block_list[(x,y)] = Block(pos, color)
        #### Ankush Burman Code ####

    def draw_gridline(self, startp, endp):
        ''' Parameters: startp - a Point of where to start the gridline
                        endp - a Point of where to end the gridline
            Draws two straight 1 pixel lines next to each other, to create
            a nice looking grid on the canvas.
        '''
        line = gr.Line(gr.Point(startp.x*BLOCK_SIZE, startp.y*BLOCK_SIZE), \
                    gr.Point(endp.x*BLOCK_SIZE, endp.y*BLOCK_SIZE))
        line.draw(self.canvas)
        
        line = gr.Line(gr.Point(startp.x*BLOCK_SIZE-1, startp.y*BLOCK_SIZE-1), \
                    gr.Point(endp.x*BLOCK_SIZE-1, endp.y*BLOCK_SIZE-1))
        line.draw(self.canvas)
        return None 

    def random_seed(self, percentage):
        ''' Parameters: percentage - a number between 0 and 1 representing the
                                     percentage of the board to be filled with
                                     blocks
            This method activates the specified percentage of blocks randomly.
        '''
        for block in self.block_list.values():
            if random.random() < percentage:
                block.set_live(self.canvas)

        return None

    def seed(self, block_coords):
        '''
        Seeds the board with a certain configuration.
        Takes in a list of (x, y) tuples representing block coordinates,
        and activates the blocks corresponding to those coordinates.
        '''
        #### Ankush Burman Code #####
        for pos in block_coords:
            block = self.block_list[pos]
            block.set_live(self.canvas)
    
        return None
        #### Ankush Burman Code ####

    def get_block_neighbors(self, block):
        '''
        Given a Block object, returns a list of neighboring blocks.
        Should not return itself in the list.
        '''
        #### Ankush Burman Code #####
        neighbor_list = []
        pos_x, pos_y = block.get_coords()
        pos_x, pos_y = int(pos_x), int(pos_y)
        start_x = pos_x-1
        start_y = pos_y-1
        for x in range(start_x, start_x+3):
            for y in range(start_y, start_y+3):
                if x == pos_x and y == pos_y:
                    continue 
                elif 0 <= x < self.width and 0 <= y < self.height:
                    block = self.block_list[(x, y)]
                    neighbor_list.append(block)
                
        return neighbor_list 
        #### Ankush Burman Code ####

    #### Ankush Burman Code ####
    def get_live_neighbors(self, neighbor_list):
        '''
        Given a list of neighbors, returns the number of live
        neighbors.
        '''
        live_neighbors = 0
        for block in neighbor_list:
            if block.is_live():
                live_neighbors += 1

        return live_neighbors 
    #### Ankush Burman Code ####

    #### Ankush Burman Code ####
    def calculate_new_status(self):
        '''
        Goes through every block on the board and determins it's 
        next status by looking at the block's neighbors. 
        1. Any live cell with fewer than two live neighbours dies. 
        2. Any live cell with more than three live neighbours dies. 
        3. Any live cell with exactly two or three live neighbours lives on. 
        4. Any dead cell with exactly three live neighbours becomes a live cell.
        '''
        for block in self.block_list.values():
            neighbor_list = self.get_block_neighbors(block)
            live_neighbors = self.get_live_neighbors(neighbor_list)

            if live_neighbors < 2 or live_neighbors > 3:
                block.new_status = "dead"
            elif live_neighbors == 3 and not block.is_live():
                block.new_status = "live"
            else:
                continue 
        
        return None
    #### Ankush Burman Code ####

    def simulate(self):
        '''
        Executes one turn of Conways Game of Life using the rules
        listed in the handout. Best approached in a two-step strategy:
        
        1. Calculate the new_status of each block by looking at the
           status of its neighbors.

        2. Set blocks to 'live' if their new_status is 'live' and their
           status is 'dead'. Similarly, set blocks to 'dead' if their
           new_status is 'dead' and their status is 'live'. Then, remember
           to call reset_status(self.canvas) on each block.
        '''

        #### Ankush Burman Code #####
        #Calculates new status of the blocks.
        self.calculate_new_status()
        #Sets the new status of all blocks as current status
        for block in self.block_list.values():
            block.reset_status(self.canvas)

        return None 
        #### Ankush Burman Code ####

    def animate(self):
        '''
        Animates the Game of Life, calling "simulate"
        once every second
        '''
        self.simulate()
        self.canvas.after(self.delay, self.animate)
        return None 


################################################################
# RUNNING THE SIMULATION
################################################################

if __name__ == '__main__':    
    # Initalize board
    win = "Conway's Game of Life"
    board = Board(win, BOARD_WIDTH, BOARD_HEIGHT)

    ## PART 1: Make sure that the board __init__ method works    
    #board.random_seed(.15)

    ## PART 2: Make sure board.seed works. Comment random_seed above and uncomment
    ##  one of the seed methods below
    #board.seed(toad_blocklist)

    ## PART 3: Test that neighbors work by commenting the above and uncommenting
    ## the following two lines:
    #board.seed(neighbor_test_blocklist)
    #test_neighbors(board)


    ## PART 4: Test that simulate() works by uncommenting the next two lines:
    #board.seed(toad_blocklist)
    #board.canvas.after(2000, board.simulate)

    ## PART 5: Try animating! Comment out win.after(2000, board.simulate) above, and
    ## uncomment win.after below.
    #board.seed(diehard_blocklist)
    board.random_seed(0.25)
    board.canvas.after(500, board.animate) 

    ## Yay, you're done! Try seeding with different blocklists (a few are provided at the top of this file!)
    
    board.canvas.mainloop()
                
