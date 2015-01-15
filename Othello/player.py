#Name: Shrijit Pillai

import gamePlay
import time
from copy import deepcopy
from random import randint

# Below is the evaluation function used to calculate the heuristic value of the board
# Strategy : If the current color is black, calculate the net black coins in the board (black - white) and vice-versa if the current color is white 
#            Find the subsequent board states that will be generated by the opponent's move.
#            If the initial color passed to the function was black, then calculate the net white coins on the board for each of the possible...
#                  opponent's move and vice-versa if the initial color was white            
#            Find the maximum of the net white coins(or net black coins) thus calculated
#            Subtract the initial net black coins calculated, from the maximum of the net white coins if the initial color is black and vice-versa ...
#                  if the initial color is white
         
def eval_fun(board,tmp_color):
    black = 0
    white = 0
    net = 0
    tmp_brd = []
    net_val = []
    tmp_moves = []
    
    tmp_brd = deepcopy(board)
    del net_val[:]
    
    if tmp_color == "B":
        for i in range(8):
            for j in range(8):
                if tmp_brd[i][j] == "B":
                    black = black + 1
                elif tmp_brd[i][j] == "W":
                    white = white + 1    
        
        net = black - white        # Calculating net black coins
        
        del tmp_moves[:]
        
        for i in range(8):
            for j in range(8):
                if gamePlay.valid(tmp_brd, "W", (i,j)): 
                    tmp_moves.append((i,j))
                    
        if len(tmp_moves) == 0:    # if opponent has no more moves then the current board has maximum utility value
            return 100
        
        black = 0
        white = 0
        for i in range(len(tmp_moves)):
            gamePlay.doMove(tmp_brd, "W", tmp_moves[i])    
                    
            for j in range(8):
                for k in range(8):
                    if tmp_brd[j][k]== "W":
                        white = white + 1  
                    elif tmp_brd[j][k]== "B":
                        black = black + 1
                        
            tmp_net = white - black         # Calculate net white coins for each of the opponent's move
            white = 0
            black = 0
            net_val.append(tmp_net)
            tmp_brd = deepcopy(board)
            
        return (net - max(net_val))         # Subtract net black coins from maximum of the net white coins
       
    else:   # Similar is the case if the color is white
        for i in range(8):
            for j in range(8):
                if tmp_brd[i][j] == "B":
                    black = black + 1
                elif tmp_brd[i][j] == "W":
                    white = white + 1    
        
        net = white - black
        
        del tmp_moves[:]
        
        for i in range(8):
            for j in range(8):
                if gamePlay.valid(tmp_brd, "B", (i,j)): 
                    tmp_moves.append((i,j))
                    
        if len(tmp_moves) == 0:
            return 100
        
        black = 0
        white = 0
        for i in range(len(tmp_moves)):
            gamePlay.doMove(tmp_brd, "B", tmp_moves[i])    
                    
            for j in range(8):
                for k in range(8):
                    if tmp_brd[j][k]== "W":
                        white = white + 1  
                    elif tmp_brd[j][k]== "B":
                        black = black + 1
                        
            tmp_net = black - white
            white = 0
            black = 0
            net_val.append(tmp_net)
            tmp_brd = deepcopy(board)
            
        return (net - max(net_val))
                   
# Below function returns the maximum utility value for a list of board states
def max_eval(temp_best_eval,color): 
    max_val = -1000
    for i in range(len(temp_best_eval)):
        m = eval_fun(temp_best_eval[i],color) 
        
        if m >= max_val:
            max_val = m
   
    return max_val          


# Below function returns the best move after alpha-beta pruning 
def genRemChildNodes(color):
    
    global temp_child        # Currently left-most nodes till depth 2 present in temp_child
    global max_depth
    global best_move
    global temp_best_moves
    global depth
    global best_eval
    
    prev_child = []
    temp_rem_child = []
    moves = []
    visited = []
    temp_best_eval = []
    best_move_index = 1
    v1 = 0
    child_cnt = 1
    parent_child_cnt = 1
    left_flag = 1
    right_flag = 0
    temp_cnt = 0
    root_child_cnt = 1
    
    index = len(temp_child) - 2   # Initialized to left-most node at depth 1 
    prev_child = temp_child[index]
    temp_depth = depth - 1        # Currently depth will be 2
    
    for i in range(len(temp_child)):
        visited.append(temp_child[i])
        
    del temp_rem_child[:]    
    
    while 1:
        if left_flag == 1:  # Checking for left-most node at depth 1.
            for d in range(1,max_depth):
                
                if color == "B":
                    if temp_depth % 2 == 1:
                        if (d+1) % 2 == 1:
                            temp_color = "B"
                        else:
                            temp_color = "W"
                    else:
                        if (d+1) % 2 == 1:
                            temp_color = "W"
                        else:
                            temp_color = "B"
                                
                else:
                    if temp_depth % 2 == 1:
                        if (d+1) % 2 == 1:
                            temp_color = "W"
                        else:
                            temp_color = "B"
                    else:
                        if (d+1) % 2 == 1:
                            temp_color = "B"
                        else:
                            temp_color = "W"
                       
                            
                for i in range(8):
                    for j in range(8):
                        if gamePlay.valid(prev_child, temp_color, (i,j)):    
                            moves.append((i,j))
                
                if len(moves) == 0:
                    child_cnt = child_cnt - 1
                    temp_child.pop()
                    prev_child = temp_child[index]
                    continue
                    
                                
                if parent_child_cnt == 1:
                    total_child_nodes = len(moves)  # Calculating no. of child nodes of left-most node at depth 1 
                
                temp_depth = temp_depth + 1
                
                if temp_depth < (max_depth-1):
                    continue
                
                if temp_depth == (max_depth-1):      # Current depth is depth 2
                    child_cnt = child_cnt + 1
                    
                    for i in range(0,len(moves)):
                        temp_prev_child = deepcopy(prev_child)
                        gamePlay.doMove(temp_prev_child, temp_color, moves[i])
                    
                        if temp_prev_child not in visited:
                            temp_child.append(deepcopy(temp_prev_child))    # Appending the subsequent child nodes of node at depth 1...
                                                                            # Left-most child node of node at depth 1 was initially inserted
                            visited.append(deepcopy(temp_prev_child))
                            prev_child = deepcopy(temp_prev_child)
                            
                            parent_child_cnt = parent_child_cnt + 1         # Incrementing child nodes of node at depth 1
                            break
                    
                else:    # Depth of leaf nodes reached
                    for i in range(0,len(moves)):
                        temp_prev_child = deepcopy(prev_child)        
                        gamePlay.doMove(temp_prev_child, temp_color, moves[i])
                        
                        v1 = 0
                        if temp_prev_child not in visited:
                            temp_rem_child.append(deepcopy(temp_prev_child))  #Appending leaf nodes
                            visited.append(deepcopy(temp_prev_child))
                            prev_child = deepcopy(temp_prev_child)
                            v1 = eval_fun(temp_rem_child[0],temp_color)       # Calculating the utility value of the left-most leaf node
                            break
                    
                    
                    temp_depth = temp_depth - 1
                    
                    if  best_eval < v1:  # alpha-beta pruning at depth 2
                        if len(temp_rem_child) > 0:
                            temp_rem_child.pop()  # Popping leaf nodes
                        
                        temp_child.pop() # pruning the node to the right of left-most node at depth 2 (popping parent of leaf node) 
                        
                        child_cnt = child_cnt - 1
                        
                        if len(temp_child) <= index:
                            return best_move
                        
                        prev_child = temp_child[index]  # Continue process to check for remaining right nodes
                            
                    else:   # No alpha-beta pruning
                        best_eval = v1
                        temp_child.pop()  # Popping parent of leaf node 
                        child_cnt = child_cnt - 1
                        
                        if len(temp_child) <= index:
                            return best_move
                        
                        prev_child = temp_child[index]  # Continue process to check for remaining right nodes
                    
                            
            del moves[:]
            del temp_rem_child[:]
                
            if parent_child_cnt == total_child_nodes:  # All child nodes of left-most node at depth 1 checked 
                visited.append(temp_child[index])
                    
                for i in range(len(temp_child)-1):
                    temp_child.pop()    # Remove nodes till root node reached.
                    
                index = index - 1
                
                child_cnt = 0
                depth = depth - 1
                index = max(index,0)
                
                if len(temp_child) <= index:
                    return best_move  
                
                prev_child = temp_child[index]
                         
                if index == 0:     # Root node
                    prev_child = temp_child[index]
                    left_flag = 0  # Start traversing for nodes to the right of the left-most node at depth 1
                    parent_child_cnt = 0
                    del temp_rem_child[:]
                
            temp_depth = depth - 1  
            
            if left_flag == 0:
                temp_depth = 0 
        
        else:   # Nodes to the right of the left-most node at depth 1
            left_child = 0   
             
            if right_flag == 1:
                end_index = max_depth
            else:
                end_index = max_depth + 1  
                 
            for d in range(1,end_index):
                temp_cnt = temp_cnt + 1
                
                if color == "B":
                    if temp_depth % 2 == 0:
                        temp_color = "B"
                    else:
                        temp_color = "W"
                                
                else:
                    if temp_depth % 2 == 0:
                        temp_color = "W"
                    else:
                        temp_color = "B"
                
                for i in range(8):
                    for j in range(8):
                        if gamePlay.valid(prev_child, temp_color, (i,j)):    
                            moves.append((i,j))
                                          
                   
                if len(moves) == 0:   
                    if temp_depth == max_depth-1:   # Current depth is 2
                        temp_child.pop()            # Popping parent of leaf node
                        temp_depth = temp_depth - 1
                        
                        if len(temp_child) <= index:
                            return best_move
                        
                        prev_child = temp_child[index]
                        continue
                     
                    else:   
                        root_child_cnt = root_child_cnt + 1  # No. of nodes at depth 1 traversed
                        break       
                    
                 
                if root_child_cnt == 1:
                    total_root_cnt = len(moves)   #Total no. of nodes at depth 1
                                   
                if temp_cnt == max_depth-1:
                    total_child_nodes = len(moves)  # Total no. of nodes at depth 2
                   
                temp_depth = temp_depth + 1
                
                 
                if temp_cnt == 1:
                    left_child = 1  # Flag indicating traversal thru left-most path of right nodes at depth 1
                   
                if temp_depth <= max_depth-1:      # Traversing through nodes at depth 1 and 2
                         
                    for i in range(0,len(moves)):
                        temp_prev_child = deepcopy(prev_child)
                        gamePlay.doMove(temp_prev_child, temp_color, moves[i])   
                      
                        if temp_prev_child not in visited:
                            temp_child.append(deepcopy(temp_prev_child))  # Append nodes at depth 1 and 2
                            
                            visited.append(deepcopy(temp_prev_child))
                            prev_child = deepcopy(temp_prev_child)
                             
                            child_cnt = child_cnt + 1
                              
                            if temp_depth == max_depth-1:
                                parent_child_cnt = parent_child_cnt + 1  # No. of nodes traversed at depth 2
                          
                            if temp_cnt == 1:
                                root_child_cnt = root_child_cnt + 1      # No. of nodes traversed at depth 1
                                 
                            if temp_depth < max_depth-1 and temp_cnt == 1:
                                index = index + 1                        # To traverse 1 level deeper
                                
                            if temp_cnt == 1:
                                temp_best_move = moves[i] 
                                 
                         
                            del moves[:]   
                            break
                        
                      
                else:    # Nodes at depth 3 (Leaf Nodes)
                    for i in range(0,len(moves)):
                        temp_prev_child = deepcopy(prev_child)
                        gamePlay.doMove(temp_prev_child, temp_color, moves[i])
                      
                        if temp_prev_child not in visited:
                            temp_rem_child.append(deepcopy(temp_prev_child))  # Append child nodes
                            visited.append(deepcopy(temp_prev_child))
                            
                            v1 = 0
                            if left_child == 1:   # Flag indicating traversal thru left-most path of right nodes at depth 1
                                temp_best_eval = deepcopy(temp_rem_child)     
                            else:
                                v1 = eval_fun(temp_rem_child[0],temp_color) # Find utility value for left-most child of right nodes of depth 1
                                break
                             
                    temp_depth = temp_depth - 1 
                    
                    if left_child == 1:  
                        v1 = max_eval(temp_best_eval,temp_color)  # Calculating the max of the utility value of the leaf nodes
                         
                        del temp_best_eval[:]
                        del temp_rem_child[:]
                         
                        if best_eval > v1:  # alpha-beta pruning at depth 1
                            for k in range(len(temp_child)-1):
                                temp_child.pop()  # Remove nodes till root node 
                            
                            index = 0
                            
                            if best_move_index >= len(temp_best_moves):
                                return best_move
                            
                            best_move_index = best_move_index + 1  # Incrementing the best move index until the end of list is reached
                                
                            temp_cnt = 0
                            parent_child_cnt = 0
                            temp_depth = 0
                            break
                         
                        else:
                            best_eval = v1   # Assigning the new utility value 
                            left_child = 0
                            temp_depth = temp_depth - 1
                            right_flag = 1    # Flag indicating to traverse the right part of the tree
                            
                            temp_child.pop()  # Pop parent of leaf node
                            
                            if len(temp_child) <= index:
                                return best_move
                            
                            prev_child = temp_child[index]
                            
                            if best_move_index >= len(temp_best_moves):
                                return best_move
                            
                            best_move = temp_best_moves[best_move_index]  # if pruning does not happen, change the best move
                            best_move_index = best_move_index + 1  
                            
                            break
                     
                    
                    if  best_eval < v1:  # alpha-beta pruning at depth 2
                        
                        temp_rem_child.pop()   # Remove child node of node at depth 2
                        temp_child.pop()       # Remove parent of leaf node just popped above
                        temp_depth = temp_depth - 1
                        
                        child_cnt = child_cnt - 1
                        if len(temp_child) <= index:
                            return best_move
                        
                        prev_child = temp_child[index]
                            
                    else:
                        best_eval = v1
                        
                        temp_child.pop()  # Remove parent of leaf node   
                        temp_depth = temp_depth - 1
                        
                        child_cnt = child_cnt - 1
                        if len(temp_child) <= index:
                            return best_move
                        
                        prev_child = temp_child[index]    
                        
                        
                    del moves[:]    
 
            del moves[:] 
             
            if root_child_cnt == total_child_nodes:   # All nodes at depth 1 traversed
                return best_move 
             
            if parent_child_cnt == total_child_nodes: # All child nodes at depth 2 traversed for a given node at depth 1
                for k in range(len(temp_child)-1):
                    temp_child.pop()   # Popping nodes till root node is reached
                
                index = index - 1
                 
                temp_cnt = 0
                parent_child_cnt = 0
                right_flag = 0
                temp_depth = 0
                total_child_nodes = 0
                prev_child = temp_child[index]
              
    return best_move       
                
                
# Below function calculates the utility value of the left-most child nodes at depth 3(maximum depth)                    
def genChildNodes(board,child,color):    
    
    global temp_child
    global best_eval
    moves = []
    temp_board = []
    temp_visited = []
    temp_rem_child = []
    temp_board = deepcopy(temp_child[len(temp_child)-1])  # Currently at depth 2
    
    if color == "B":
        other_color = "W"
    else:
        other_color = "B"    
    
    for i in range(8):
        for j in range(8):
            if gamePlay.valid(temp_board, color, (i,j)):
                moves.append((i,j))
    
    for i in range(0,len(moves)):
        gamePlay.doMove(temp_board, color, moves[i])
                      
        if temp_board not in temp_visited:
            temp_rem_child.append(deepcopy(temp_board))   # Append leaf nodes (nodes at depth 3)
            temp_visited.append(deepcopy(temp_board))
            temp_board = deepcopy(temp_child[len(temp_child)-1])
    
    if len(temp_rem_child) > 0:        
        best_eval = max_eval(temp_rem_child,color)   # Determines max utility value of the nodes at depth 3
    else:
        best_eval = eval_fun(temp_child[len(temp_child)-1], other_color)    # If nodes at depth 3(leaf nodes) are not present, then...
                                                                            # find the utility value of left-most node at depth 2
    del temp_rem_child[:]
    del temp_visited[:]
    
    return genRemChildNodes(color)      # Get the Best move 
                
    
def nextMove(board, color, time):
    
    global temp_child
    global depth
    global best_move
    global temp_best_moves
    global max_depth
    moves = []
    
    del temp_child[:]
    temp_child.append(deepcopy(board))  #Appends the initial board state
    temp_board = deepcopy(board)     
        
    for i in range(8):
        for j in range(8):
            if gamePlay.valid(temp_board, color, (i,j)):    
                moves.append((i,j))
                  
    if len(moves) == 0:
        return "pass"
    else:
        temp_best_moves = deepcopy(moves)

    best_move = temp_best_moves[0] # Initialized to left-most mode at depth 1

    
    for d in range(max_depth-1):   # Determines the left-most node at depth 2. If depth 2 cannot be reached, then return the best move
        
        if color == "B":
            if (d+1) % 2 == 1:
                temp_color = "B"
            else:
                temp_color = "W"
        else:
            if (d+1) % 2 == 1:
                temp_color = "W"
            else:
                temp_color = "B"
                
        del moves[:]
        for i in range(8):
            for j in range(8):
                if gamePlay.valid(temp_board, temp_color, (i,j)):    
                    moves.append((i,j))
                    
        if len(moves) == 0 and d == 1:   # If no moves are available and we are currently at depth 1,        
            return best_move             # then return the move which took us to depth 1 as the best move
                
        
        for i in range(len(moves)):
            gamePlay.doMove(temp_board, temp_color, moves[i])
            
            if gamePlay.gameOver(temp_board):
                return best_move
            
            temp_child.append(deepcopy(temp_board))  # Append the next left-most child node
            depth = depth + 1
            break
       
    return genChildNodes(board,child,color)       
                 
    

temp_board = []     
temp_child = []
best_move = []
temp_best_moves = []
child = []
depth = []

best_eval = -1
depth = 0
max_depth = 3  # Depth for the tree is 3 
        
       
                
        
        
    
    
