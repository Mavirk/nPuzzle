import sys # allows access to argv 
import re # allows access to regular expressions
import pprint # allows pretty printing of objects and lists
import copy # allows be to pass immutable objects by value by copying them into a new memory location
import pdb
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
            # print('right' + str(max_s) + ' ' + str(counter))
            counter += 1
            x += 1    
        min_s = min_s + 1 
        while y > min_s:
            puz.append({'num': counter, 'x': x, 'y': y})
            # print('down' + str(max_s) + ' ' + str(counter))
            counter += 1
            y -= 1   
        while x > min_s:
            puz.append({'num': counter, 'x': x, 'y': y})
            # print('left' + str(max_s) + ' ' + str(counter))
            counter += 1
            x -= 1   
        max_s = max_s - 1
        while y < max_s:
            puz.append({'num': counter, 'x': x, 'y': y})
            # print('up' + str(max_s) + ' ' + str(counter))
            counter += 1
            y += 1
        if counter == puzzle_size * puzzle_size :
            puz.append({'num': 0, 'x': x, 'y': y})
            return puz
     

def check_tile(node):
    if not (node['currX'] == node['goalX'] and node['currY'] == node['goalY']):
        return 1
    return 0

def manhattan_distance(node):
    return (node['currX'] - node['goalX']) + (node['currY'] - node['goalY'])

def tiles_out_row_column(node, hCounter):
    if node['currX'] != node['goalX']: 
        hCounter += 1
    if node['currY'] != node['goalY']: 
        hCounter += 1
    return hCounter

def get_heuristic(state, puzzle):
    # pprint.pprint(puzzle)
    hCounter = 0
    hFinal = 0
    for node in state:
        node['goalX'] = puzzle[node['num'] - 1]['x']
        node['goalY'] = puzzle[node['num'] - 1]['y']
        if node['heuristic'] == 'man':
            hFinal = hFinal + abs(manhattan_distance(node))
        elif node['heuristic'] == 'mis' :
            hFinal = hFinal + check_tile(node)
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
    # print_state(current['state'], puzzle_size)
    # print('cost : '),
    # print(current['cost'])
    # print('heur : '),
    # print(current['heur'])
    # print('totalCost : '),
    # print(current['totalCost'])
    # print current['parent']
    # print len(total_path)
    
    
    if  current == 'start' :
        # print 'yes'
        # current = current['parent']
        return total_path
    else: 
        # print 'no'
        temp = copy.deepcopy(current)
        total_path.append(temp)
        temp = temp['parent']
        # print current
        # print current['parent']
        # print 'yes'
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
        # print count    
        if count == 10000:
            print('==========TRYING_SOlUTION==========:')
            return  reconstruct_path(current, puzzle_size)  

        openSet.pop(0)
        closedSet.append(current)

        for state in getNextStates(current,solution,puzzle_size):
            # print count
            # pprint.pprint(state) 
            if  itemInSet(state,closedSet):
                continue		# Ignore if the state which is already closed

            if not itemInSet(state,openSet) or current['cost'] + 1 < state['cost']:	# Discover a new node
                state['parent'] = current
                state['cost'] = current['cost'] + 1
                state['totalCost'] = state['cost'] + state['heur']
                if state not in openSet and state['totalCost'] <= current['totalCost'] + 3:
                    openSet.append(state)
            
               
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
    for line in inputs:
        y -= 1
        x = -1
        for num in line.split():
            x += 1
            if int(num) == 0:
                found_zero = True
            state.append({'currX': int(x), 'currY': int(y), 'goalX': int(x), 'goalY': int(y), 'heuristic' : sys.argv[2], 'num': int(num)})
    if found_zero == False:
        print('ERROR: Test file is invalid: no space to move')
        quit()
    solution = generate_solution(puzzle_size)   
    # print solution
    count = 0
    heuristic = get_heuristic(state, solution)
    x = {'state': copy.deepcopy(state), 'cost' : count, 'heur': heuristic, 'totalCost' : heuristic + count, 'parent' : 'start'} 
    
    opened = [x]
    closed = []
    tries = 4
    parents = []
    
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
        # print( '====NEXT_STATES====')
        # ns = getNextStates(state, solution, puzzle_size)
        
        # for state in ns :
        #     print_state(state['state'], puzzle_size)
        #     print('cost : '),
        #     print(i + 1)
        #     print('heur : '),
        #     print(state['heur'])
        #     print('totalCost : '),
        #     print(i + 1 + state['heur'])

         # print '===NODES OPENED===: ',
        # print("\r" + '===NODES_OPENED===' + str(count)),
        # print '===OPENED===: ',
        # print '{0}\r'.format(len(openSet)),
        # print '===CLOSED===: '
        # print '{0}\r'.format(len(closedSet)),

    # while opened != [] and count < tries:
    #     opened.sort(key=itemgetter('totalCost')
    #     print("=====OPENED:")
    #     for c in opened:
    #         if c['heur'] == 0:
    #             print 'dipshit'
    #             quit()
    #         print_state(c['state'], puzzle_size)
    #         print('cost : '),
    #         print(c['cost'])
    #         print('heur : '),
    #         print(c['heur'])
    #         print('totalCost : '),
    #         print(c['totalCost'])
    #     print('')    
    #     current = opened[0]
    #     closed.append(current)
    #     opened.pop(0)
    #     nextStates = []
    #     if current['heur'] == 0:
    #         closed.append(current)
    #         print('======SOlUTION FOUND :')
    #         for step in closed:
    #             print_state(step['state'], puzzle_size)
    #             print(step['name'])
    #             print('')
    #         return True
    #     print('======CURRENT_STATE : On Step '),
    #     print(count)
    #     print_state(current['state'], puzzle_size)
    #     print('cost : '),
    #     print(current['cost'])
    #     print('heur : '),
    #     print(current['heur'])
    #     print('totalCost : '),
    #     print(current['totalCost'])
    #     count += 1 
        
    #     print('')
    #     print('')        change alt s to save in vs code
    #     print('======NEXT_STATES : ')        
    #     for nState in nextStates:
    #         print_state(nState['state'], puzzle_size)
    #         print('cost : '),
    #         print(nState['cost'])
    #         print('heur : '),
    #         print(nState['heur'])
    #         print('totaCost : '),
    #         print(nState['totalCost'])
    #         print('')
    #         if nState in closed:
    #             continue
    #         if nState not in opened:
    #             opened.append(nState)
    #         temp_cost = current['cost'] + 1
    #         if temp_cost >= nState['cost']:
    #             continue
    #         nState['parent'] = current
    #         nState['cost'] = temp_cost
    #         nState['totalCost'] = nState['cost']
         
    #     print('======CLOSED : ')
    #     for k in closed:
    #         print_state(k['state'], puzzle_size)
    #         print('cost : '),
    #         print(k['cost'])
    #         print('heur : '),
    #         print(k['heur'])
    #         print('totaCost : '),
    #         print(k['totalCost'])
    #         print('')        
        
    # if current['heur'] != 0:
    #     print('=====NOT_SOLVED')
                    


    #     print('==================')
    #     print('opened[0]')
    #     for x in opened:
    #         print_state(x['state'], puzzle_size)
    #         print(x['totalCost'])

    #     current = opened[0]
    #     if current in lastStates:
    #         opened.pop(0)
       
    #     # print('')
    #     # pprint.pprint(opened[0])
        
    #     if current['heur'] == 0:
    #         closed.append(current)
    #         print('SOlUTION FOUND :')
    #         for step in closed:
    #             # print(step['name'])
    #             print_state(step['state'], puzzle_size)
    #         return True
    #     print('CURRENT_STATE : On Step '),
    #     print(current['name'])
    #     print(current['totalCost'])
    #     print_state(current['state'], puzzle_size)
    #     # pprint.pprint(current)
    #     #get next states as full diciotnaries
    #     nextStates = []
    #     for strn in state_strns:
        
    #         direction = getDirection(copy.deepcopy(current['state']), strn, puzzle_size)
    #         if direction : 
    #             # print(strn)
    #             # print_state(direction, puzzle_size)
    #             heuristic = get_heuristic(direction, solution)
    #             nextStates.append({'name': count, 'state': direction, 'heur': heuristic, 'totalCost' : heuristic + count})
      
    #     print('NEXT_STATES : ')
    #     for state in nextStates:
    #         if (state not in closed) and (state not in opened):
    #             opened.append(state)
    #             print(state['totalCost'])
    #             print_state(state['state'], puzzle_size)
    #     lastStates = nextStates        
    #     closed.append(current)
    
    #         # pprint.pprint(nextStates)
    #     # print('Extending Opened............')
    #     # pprint.pprint(opened)
       
    #     # pprint.pprint(opened)
    #     # print('OPENED : ')
    #     # for k in opened:
    #     #     print(k['name'])
    #     #     print(k['heur'])
    #     #     print_state(k['state'], puzzle_size)
        
    #     opened.sort(key=itemgetter('totalCost'))
    #     # print('OPENED : ')
    #     # for k in opened:
    #     #     print(k['name'])
    #     #     print(k['heur'])
    #     #     print_state(k['state'], puzzle_size)
            
        
    #     # print('CLOSED : ')
    #     # for k in closed:
    #     #     print(k['name'])
    #     #     print(k['heur'])
    #     #     print_state(k['state'], puzzle_size)
        
        
    #     count += 1    

if len(sys.argv) > 1:
        nPuzzle(sys.argv[1])






    # up = getDirection(x['state'], 'up', puzzle_size)
    # down =  getDirection(x['state'], 'down', puzzle_size)
    # right = getDirection(x['state'], 'right', puzzle_size)
    # left = getDirection(x['state'], 'left', puzzle_size) 

            # print('down')
            # print_state(down, puzzle_size)
            # # pprint.pprint(down)

            # print('up')
            # print_state(up, puzzle_size)
            # # pprint.pprint(up)

            # print('right')
            # print_state(right, puzzle_size)
            # # pprint.pprint(right)

            # print('left')
            # print_state(left, puzzle_size)
            # # pprint.pprint(left)

        # {'state': up, 'heur': get_heuristic(up, solution)},
        # {'state': down, 'heur': get_heuristic(down, solution)},
        # {'state': right, 'heur': get_heuristic(right, solution)},
        # {'state': left, 'heur': get_heuristic(left, solution)}
        













    # next_states = {'up': up, 'down': down, 'right': right, 'left': left}
    # next_states = {key:value for key, value in next_states.iteritems() if value}
    # next_state_heuristic = {key: count + get_heuristic(value, puzzle) for key, value in next_states.iteritems()}
    # for key, value in next_states.iteritems(): 
    #     print(key)
    #     print(value)
    # for key, value in next_state_heuristic.iteritems(): 
    #     print(str(key) + ': ' +  str(value))
    # sorted_d = sorted(next_state_heuristic.items(), key=lambda (k,v): v)  
    # print(sorted_d)  
    # # for key, value in sorted_d.iteritems(): 
    #     print(str(key) + ': ' +  str(value))
    # for i in next_states:
    #     next_state_heuristic.append(get_heuristic(i, puzzle) + abs(get_heuristic(i, puzzle) - get_heuristic(state, puzzle)))
    # for i in next_state_heuristic: print(i)
    # for key, value in all_states.iteritems():
    #     if value != False:
    #         next_state[key] = value
    # state = sorted(state, key=lambda k: k['num']) 
    # print_state(state, puzzle_size)
    # insert_heuristic( state, puzzle)
    # print('=======')       
    # try:
    #     insert_heuristic(state)
    # except:
    #     print 'Failed running robs function on file: ' + file_name

    # print('CURRENT')
    # print_state(state, puzzle_size)
    # insert_heuristic( state, puzzle)
    # print('=======')     
    
    # print('UP')
    # up = getDirection(copy.deepcopy(state), 'up')
    # print_state(up, puzzle_size)
    # insert_heuristic( up, puzzle)
    # print('=======')

    # print('DOWN')
    # down = getDirection(copy.deepcopy(state), 'down')
    # print_state(down, puzzle_size)
    # insert_heuristic(down, puzzle)
    # print('=======')

    # print('RIGHT')        
    # right = getDirection(copy.deepcopy(state), 'right')
    # print_state(right, puzzle_size)
    # insert_heuristic(right, puzzle)
    # print('=======')
    
    # print('LEFT')
    # left = getDirection(copy.deepcopy(state), 'left')
    # print_state(left, puzzle_size)
    # insert_heuristic(left, puzzle)
    # print('=======')    