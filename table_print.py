
CELLS_PER_ROW = 10
CHARS_PER_CELL = 15
DASHES = "-" * CHARS_PER_CELL
SEPARATOR = "|"
SPACE = " "

def print_table(stuffs):

    def print_empty_cells(number):
        print(SEPARATOR, end="")
        for i in range(number):
            print(SPACE*CHARS_PER_CELL, end="")
            print(SEPARATOR, end="")
        print("\n", end="")
    
    def print_rows():
        for i in range(CELLS_PER_ROW):
            print(SEPARATOR, end="")
            print(DASHES, end="")
        print(SEPARATOR)

    print_rows()
    counter = 0
    for stuff in stuffs:
        print(SEPARATOR, end="")

        if len(stuff) < CHARS_PER_CELL:
            stuff = stuff + SPACE*(CHARS_PER_CELL - len(stuff))
        print(stuff[:CHARS_PER_CELL], end="")
        counter += 1

        if counter == CELLS_PER_ROW:
            print(SEPARATOR)
            counter = 0
            print_rows()
    
    cells_left = CELLS_PER_ROW - len(stuffs)%CELLS_PER_ROW

    print_empty_cells(cells_left)
    print_rows()
