import sys # allows access to argv 
import re # allows access to regular expressions
import pprint # allows pretty printing of objects and lists
import copy # allows be to pass immutable objects by value by copying them into a new memory location
import pdb
from math import sqrt
from operator import itemgetter

# generalized function that removes comments(denoted by sep) from a string-line
def removeComments(line, sep):
    for s in sep:
        i = line.find(s)
        if i >= 0:
            line = line[:i]
    return line.strip()

def print_state(state, puzzle_size):
    data = []
    y = puzzle_size - 1
    while y >= 0:
        x = 0
        row = []
        while x < puzzle_size:
            for node in state:
                if node['currX'] == x and node['currY'] == y:
                    row.append(node['num'])
            x = x + 1
        data.append(row)
        y = y - 1  
    col_width = max(len(str(word)) for r in data for word in r) + 1  # padding
    for r in data:
        print "".join(str(word).ljust(col_width) for word in r) 

def generate_solution(puzzle_size):
    puz = []
    counter = 1
    max_s = puzzle_size - 1
    min_s = -1
    y = max_s
    x = 0
    while max_s >= 1 :
        while x < max_s:
            puz.append({'num': counter, 'x': x, 'y': y})
            counter += 1
            x += 1    
        min_s = min_s + 1 
        while y > min_s:
            puz.append({'num': counter, 'x': x, 'y': y})
            counter += 1
            y -= 1   
        while x > min_s:
            puz.append({'num': counter, 'x': x, 'y': y})
            counter += 1
            x -= 1   
        max_s = max_s - 1
        while y < max_s:
            puz.append({'num': counter, 'x': x, 'y': y})
            counter += 1
            y += 1
        if counter == puzzle_size * puzzle_size :
            puz.append({'num': 0, 'x': x, 'y': y})
            return puz

def isEven(num):
    if int(num) % 2 == 0:
        return True # Even 
    else:
        return False

def checkInversions(state, puzzle_size):
    # TODO make function for these lines of code
    inv = 0
    snail3 = [0,1,2,5,8,7,6,3,4]
    snail4 = [0,1,2,3,7,11,15,14,13,12,8,4,5,6,10,9]
    snail5 = [0,1,2,3,4,9,14,19,24,23,22,21,20,15,10,5,6,7,8,13,18,17,16,11,12]
    snail = []
    if puzzle_size > 4 :
        print '5 puzzle is not supported'
        quit()
    elif puzzle_size == 3:
        for i in snail3:
            if state[i]['num'] != 0:
                snail.append(state[i]['num'])
    elif puzzle_size == 4:
        for i in snail4:
            if state[i]['num'] != 0:
                snail.append(state[i]['num'])
    
    for i in range(len(snail)):
        for j in range(i, len(snail)):
            if snail[i] > snail[j] and snail[i] != 0 and snail[j] != 0:
                print snail[i],
                print ' > ',
                print snail[j]
                inv += 1
    if isEven(inv):
        print inv
        print "EVEN"
    else: 
        print inv
        print "ODD"
    return inv

def isSolvable(state, puzzle_size):
    blank = (item for item in state if item['num'] == 0).next()
    print blank
    print_state(state, puzzle_size)
    if not isEven(puzzle_size) and isEven(checkInversions(state, puzzle_size)):
        return True
    elif isEven(puzzle_size):
        if isEven(blank['currX'] +  1) and not isEven(checkInversions(state, puzzle_size)):
            return True
        elif not isEven(blank['currX'] + 1) and isEven(checkInversions(state, puzzle_size)):
            return True
        else:
            return False    
    else:        
        return False


def addGoals(state,puzzle):
    for node in state:
        node['goalX'] = puzzle[node['num'] - 1]['x']
        node['goalY'] = puzzle[node['num'] - 1]['y']
    return state

def check_tile(node):
    if not (node['currX'] == node['goalX'] and node['currY'] == node['goalY']):
        return 1
    return 0
def euclidean_distance(node):
    return sqrt((node['currX'] - node['goalX']) **2 + (node['currY'] - node['goalY'])**2)
def manhattan_distance(node):
    return abs(node['currX'] - node['goalX']) + abs(node['currY'] - node['goalY'])

def tiles_out_row_column(node, hCounter):
    if node['currX'] != node['goalX']: 
        hCounter += 1
    if node['currY'] != node['goalY']: 
        hCounter += 1
    return hCounter
def linear_conflict(state):
    comp1 = [i for i in state]
    comp2 = [x for x in state]
    h = 0
    for a in comp1:
        if a['num'] != 0:
            h = h + manhattan_distance(a)
            for b in comp2:
                if b['num'] != 0:
                    if a['num'] != b['num']:
                        if a['currX'] == b['currX'] == a['goalX'] == b['goalX'] :
                            if a['currY'] > b['currY'] and a['goalY'] < b['goalY']:
                                h = h + 2 
                        elif a['currY'] == b['currY'] == a['goalY'] == b['goalY']:
                            if a['currX'] > b['currX'] and a['goalX'] < b['goalX']:
                                h = h + 2
    return h                     
def get_heuristic(state, puzzle):
    hCounter = 0
    hFinal = 0
    
    for node in state:
        if node['num'] != 0:
            if node['heuristic'] == 'man':
                hFinal = hFinal + manhattan_distance(node)
            elif node['heuristic'] == 'mis' :
                hFinal = hFinal + check_tile(node)
            elif node['heuristic'] == 'lin' :
                return linear_conflict(state)  
            elif node['heuristic'] == 'euc' :
                hFinal = hFinal + euclidean_distance(node)    
            elif node['heuristic'] == 'row':
                hFinal = hFinal + tiles_out_row_column(node, hCounter)
            else:
                print('ERROR: unknown heuristic: ' + node['heuristic'])
                quit()
    return int(hFinal)

def getDirection(st, direction, puzzle_size):  
    count = 0
    if direction == 'up': up_down = 1
    elif direction == 'down': up_down = -1
    else: up_down = 0
    if direction == 'right': right_left = 1
    elif direction == 'left': right_left = -1
    else : right_left = 0
    tempX = 'NA'
    tempY = 'NA'
    for node in st:
        if node['num'] == 0:
            blank = node
    for node in st:
        if node['currX'] == blank['currX'] + right_left and node['currY'] == blank['currY'] + up_down:
            tempX = node['currX']
            tempY = node['currY']
            node['currX'] = blank['currX']
            node['currY'] = blank['currY']    
        else:
            count += 1 
    for node in st:
        if node['num'] == 0 and tempX != 'NA' and tempY != 'NA':
            node['currX'] = tempX
            node['currY'] = tempY               
    if count == puzzle_size * puzzle_size:
        return False
    return st
def itemInSet(curr, setOfStates):
    for item in setOfStates:
        if item['state'] == curr['state']:
            return True
    return False        
        
def reconstruct_path(current, puzzle_size, total_path = []):
    if  current == 'start' :
        return total_path
    else: 
        temp = copy.deepcopy(current)
        total_path.append(temp)
        temp = temp['parent']
        return reconstruct_path(temp, puzzle_size, total_path)


def getNextStates(state,solution, puzzle_size):
    nextStates = []
    state_strns = ['up', 'down', 'right', 'left']
    for strn in state_strns :
        direction = getDirection(copy.deepcopy(state['state']), strn, puzzle_size)
        if direction :
            heuristic = get_heuristic(direction, solution)
            nextStates.append({
                'state': copy.deepcopy(direction), 
                'cost' : float("inf"), 
                'heur': heuristic, 
                'totalCost' : float("inf"),
                'parent' : state
                })
    return nextStates            
def print_states(solution, puzzle_size):
    if solution is not dict:
        state = solution
        print_state(state, puzzle_size)
        print('cost : '),
        print(state['cost'])
        print('heur : '),
        print(state['heur'])
        print('totalCost : '),
        print(state['totalCost'])
    else:
        for state in solution:
            print_state(state , puzzle_size)
            print('cost : '),
            print(state['cost'])
            print('heur : '),
            print(state['heur'])
            print('totalCost : '),
            print(state['totalCost'])
def A_Star(start, solution, puzzle_size):
    
    closedSet = []
    
    openSet = [start]   
    count = 0
    while openSet != [] :
        count += 1

        openSet.sort(key=itemgetter('totalCost', 'heur'))
        current = openSet[0]

        if current['heur'] == 0:
            print('==========SOLUTION_FOUND==========:')
            return reconstruct_path(current, puzzle_size)
        if count % 100 = 0    
            print count,
            print " NODES EXPANDED"   
        if count == 1000000:
            print('==========TRYING_SOlUTION==========:')
            return  reconstruct_path(current, puzzle_size)  

        openSet.pop(0)
        closedSet.append(current['state'])

        for state in getNextStates(current,solution,puzzle_size):
            if  state['state'] in closedSet:
                continue		# Ignore if the state which is already closed

            if not itemInSet(state,openSet) or current['cost'] + 1 < state['cost']:	# Discover a new node
                state['parent'] = current
                state['cost'] = current['cost'] + 1
                state['totalCost'] = state['cost'] + state['heur']
                if not itemInSet(state,openSet) and state['totalCost'] <= current['totalCost'] + 2:
                    openSet.insert(0, state)
                    if len(openSet) > puzzle_size ** 2 * 100:
                        openSet.pop(len(openSet) - 1)

            
            
def nPuzzle(file_name):
    try:
        with open (file_name, 'rt') as in_file: # Opens the file, reads it into the list file_data and closes the file afterwards
            file_data = in_file.readlines() # Reads the entire file into an list of strings
    except:
        print('ERROR: file "' + file_name + '" does not exist.')
        quit()
    inputs = [removeComments(i, '#') for i in file_data]# Removes all commented/new lines from inputs
    inputs = filter(None, inputs) # Filter is the most optimal way to remove empty strings from a  list of strings
    if len(inputs) == 1:
        print('Puzzle with one item is already solved!')
    for i, line in enumerate(inputs):
        if len(line) == 1:
            puzzle_size = line
    inputs.remove(puzzle_size)
    puzzle_size = int(puzzle_size)
    state = []
    y = puzzle_size
    if len(sys.argv) == 2:
        print("ERROR: No heuristic, please rerun with a heuristic.")
        quit()
    found_zero = False
    solution = generate_solution(puzzle_size)
    for line in inputs:
        y -= 1
        x = -1
        for num in line.split():
            x += 1
            if int(num) == 0:
                found_zero = True
            state.append({'currX': int(x), 'currY': int(y), 'goalX': int(x), 'goalY': int(y), 'heuristic' : sys.argv[2], 'num': int(num)})
            addGoals(state, solution)
    if found_zero == False:
        print('ERROR: Test file is invalid: no space to move')
        quit()
        
    # print solution
    count = 0
    heuristic = get_heuristic(state, solution)
    x = {'state': copy.deepcopy(state), 'cost' : count, 'heur': heuristic, 'totalCost' : heuristic + count, 'parent' : 'start'} 
    
   
    if isSolvable(x['state'], puzzle_size):
        grub = A_Star(x, solution, puzzle_size)
        # this for loop is for debugging so we keep a* clean for edits 
        for i,state in enumerate(reversed(grub)):
            # print 'this is the grub
            print '===CURRENT==='
            print_state(state['state'], puzzle_size)
            print('cost : '),
            print(state['cost'])
            print('heur : '),
            print(state['heur'])
            print('totalCost : '),
            print(state['totalCost'])
    else:
        print "puzzle is unsolvable"
if len(sys.argv) > 1:
    nPuzzle(sys.argv[1])

