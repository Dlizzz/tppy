# talos-puzzle

This python 3 script solves the Sigil puzzles in Talos Principle game from Croteam: <http://www.croteam.com/talosprinciple/>

Puzzle board is made of Rows x Columns cells.
Column is the horizontal dimension.
Row is the vertical dimension.
The puzzle can use the following pieces:

- Square shape
- L Right shape
- L Left shape
- Bar shape
- Tee shape
- Step Right shape
- Step Left shape

The pieces can be flipped horizontally and vertically.

Solutions (if they exist) are output on the console and can be saved as PNG images.

## Command line arguments

- --verbose: Print progress status on stdout (toggle)
- --first: Stop at first solution found (toggle)
- --stats: Save puzzle solving statistics in CSV format (toggle)
- --rows #: Number of board rows (mandatory)
- --columns #: Number of board columns (mandatory)
- --square #: Number of Square shape pieces (default: 0)
- --l-right #: Number of L right shape pieces (default: 0)
- --l-left #: Number of L left shape pieces (default: 0)
- --bar #: Number of Bar shape pieces (default: 0)
- --tee #: Number of T shape pieces (default: 0)
- --step-right #: Number of Step right shape pieces (default: 0)
- --step-left #: Number of Step left shape pieces (default: 0)
- --images: Output solutions as png images (toggle)
- --output-dir dir: Directory where to output png images (default: script dir)
- --cell-size #: Size in pixels of one cell of the board (default: 100)
- --shape-color colorname: Color name (HTML) of the shape color (default: "Yellow")
- --fill-color colorname: Color name (HTML) of the fill color (default: "DatkMagenta")

## Requirements

The script is using the `pillow (PIL fork)` library for images generation and the `numpy` library for matrix manipulation

## Algorithm

To go through the tree of combinations, we use a "go deep" approach as opposed to a "go by level" approach. It means that as soon as we have a valid combination we go to the next piece (one level deeper), trying to find a possible solution as soon as possible. The path is more complex to manage (need to keep track of the path and being able to go backward on it) and may be a little bit slower, but it has a very good side effect, you don't need to store all the combinations (as with the "go by level" approach), just the one for the current node. So, in terms of memory management, it's much, much more performant.

A "go by level" approach means that you combine each valid combinations of one level with all nodes of the next level, store the new valid combinations and move to next level. It's faster but it requires a lot of memory space.

## Performances

The script uses a brute force approach:

- Generate all possible positions of each given piece on the board, some pieces having different patterns due to possible rotations
- Combine all the generated positions together to find the solutions (tree of combinations)
- To improve performance dead branches are dropped immediately. A branch is "dead" when a tested position overlaps with an existing combination of positions.
- Even with the early drop of dead branches, it could take some time to solve large puzzles and find all their possible solutions. As an example, to solve the red puzzle with 8 columns and 7 rows with 4 square, 4 tee, 2 bars, 1 step left, 1 step right, 1 l left and 1 l right, the script has to go through 577 289 330 256 198 172 046 386 176 combinations of pieces. It's why there is the option "first to stop after finding the first solution (no need to find all solutions for the game).

## Todo

- A javascript interface to configure the puzzle and show the results.
- Move to multithread for going trough the tree, at least one thread for each tree root.
