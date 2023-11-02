from board.move import move
from pieces.nullpiece import nullpiece
from pieces.queen import queen
import random

class AI:

    global tp
    tp=[]


    def __init__(self):
        pass


    def evaluate(self,gametiles):
        min=100000
        count=0
        count2=0
        chuk=[]
        movex=move()
        tp.clear()
        xp=self.minimax(gametiles,3,-1000000000,1000000000,False)

        for zoom in tp:
            if zoom[4]<min:
                chuk.clear()
                chuk.append(zoom)
                min=zoom[4]
            if zoom[4]==min:
                chuk.append(zoom)
        fx=random.randrange(len(chuk))
        print(tp)
        return chuk[fx][0],chuk[fx][1],chuk[fx][2],chuk[fx][3]


    def reset(self,gametiles):
        for x in range(8):
            for y in range(8):
                if gametiles[x][y].pieceonTile.tostring()=='k' or gametiles[x][y].pieceonTile.tostring()=='r':
                    gametiles[x][y].pieceonTile.moved=False


    def updateposition(self,x,y):
        a=x*8
        b=a+y
        return b

    def checkmate(self,gametiles):
        movex=move()
        if movex.checkw(gametiles)[0]=='checked':
            array=movex.movesifcheckedw(gametiles)
            if len(array)==0:
                return True

        if movex.checkb(gametiles)[0]=='checked' :
            array=movex.movesifcheckedb(gametiles)
            if len(array)==0:
                return True

    def stalemate(self,gametiles,player):
        movex=move()
        if player==False:
            if movex.checkb(gametiles)[0]=='notchecked':
                check=False
                for x in range(8):
                    for y in range(8):
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                            lx1=movex.pinnedb(gametiles,moves1,y,x)
                            if len(lx1)==0:
                                continue
                            else:
                                check=True
                            if check==True:
                                break
                    if check==True:
                        break

                if check==False:
                    return True

        if player==True:
                if movex.checkw(gametiles)[0]=='notchecked':
                    check=False
                    for x in range(8):
                        for y in range(8):
                            if gametiles[y][x].pieceonTile.alliance=='White':
                                moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                                lx1=movex.pinnedw(gametiles,moves1,y,x)
                                if len(lx1)==0:
                                    continue
                                else:
                                    check=True
                                if check==True:
                                    break
                        if check==True:
                            break

                    if check==False:
                        return True






    def minimax(self,gametiles, depth,alpha , beta ,player):
        if depth==0 or self.checkmate(gametiles)==True or self.stalemate(gametiles,player)==True:
            return self.calculateb(gametiles)
        if not player:
            minEval=100000000
            kp,ks=self.eva(gametiles,player)
            for lk in kp:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.move(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,True)
                    if evalk<minEval and depth==3:
                        tp.clear()
                        tp.append(move)
                    if evalk==minEval and depth==3:
                        tp.append(move)
                    minEval=min(minEval,evalk)
                    beta=min(beta,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break

                if beta<=alpha:
                    break
            return minEval

        else:
            maxEval=-100000000
            kp,ks=self.eva(gametiles,player)
            for lk in ks:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.movew(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,False)
                    maxEval=max(maxEval,evalk)
                    alpha=max(alpha,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break
                if beta<=alpha:
                    break

            return maxEval



    def printboard(self,gametilles):
        count = 0
        for rows in range(8):
            for column in range(8):
                print('|', end=gametilles[rows][column].pieceonTile.tostring())
            print("|",end='\n')


    def checkeva(self,gametiles,moves):
        arr=[]
        for move in moves:
            lk=[[move[2],move[3]]]
            arr.append(self.calci(gametiles,move[0],move[1],lk))

        return arr



    def eva(self,gametiles,player):
        lx=[]
        moves=[]
        kp=[]
        ks=[]
        movex=move()
        for x in range(8):
            for y in range(8):
                    if gametiles[y][x].pieceonTile.alliance=='Black' and player==False:
                        if movex.checkb(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedb(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            kp=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='K'):
                                ax=movex.castlingb(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([0,6])
                                        if l=='qs':
                                            moves.append([0,2])
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            lx=movex.pinnedb(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        kp.append(self.calci(gametiles,y,x,moves))


                    if gametiles[y][x].pieceonTile.alliance=='White' and player==True:
                        if movex.checkw(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedw(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            ks=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if moves==None:
                            print(y)
                            print(x)
                            print(gametiles[y][x].pieceonTile.position)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='k'):
                                ax=movex.castlingw(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([7,6])
                                        if l=='qs':
                                            moves.append([7,2])
                        if gametiles[y][x].pieceonTile.alliance=='White':
                            lx=movex.pinnedw(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        ks.append(self.calci(gametiles,y,x,moves))

        return kp,ks



    def calci(self,gametiles,y,x,moves):
        arr=[]
        jk=object
        for move in moves:
            jk=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            mk=self.calculateb(gametiles)
            gametiles[y][x].pieceonTile=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=jk
            arr.append([y,x,move[0],move[1],mk])
        return arr


    def calculateb(self,gametiles):
        value=0

        def inRange(y,x):
            if(y < 8 and y > 0):
                if(x < 8 and x > 0):
                    return True
            return False
        def protectedByPawn(piece):
            protectors = 0
            piece_text = piece.pieceonTile.tostring()
            if(piece_text.upper() == piece_text):
                left = [y-1,x-1]
                if(inRange(left[0],left[1])):
                    if(gametiles[y-1][x-1].pieceonTile.tostring()=='P'):
                        protectors += 1
                right = [y-1,x+1]
                if(inRange(right[0],right[1])):
                    if(gametiles[y-1][x+1].pieceonTile.tostring()=='P'):    
                        protectors += 1
                return protectors * -1
            else:
                left = [y+1,x-1]
                if(inRange(left[0],left[1])):
                    if(gametiles[y+1][x-1].pieceonTile.tostring()=='p'):
                        protectors += 1
                right = [y+1,x+1]
                if(inRange(right[0],right[1])):
                    if(gametiles[y+1][x+1].pieceonTile.tostring()=='p'):    
                        protectors += 1
                return protectors * 1
        def attackedByPawn(piece):
            attackers = 0
            piece_text = piece.pieceonTile.tostring()
            if(piece_text.lower() == piece_text):
                left = [y-1,x-1]
                if(inRange(left[0],left[1])):
                    if(gametiles[y-1][x-1].pieceonTile.tostring()=='P'):
                        attackers += 1
                right = [y-1,x+1]
                if(inRange(right[0],right[1])):
                    if(gametiles[y-1][x+1].pieceonTile.tostring()=='P'):    
                        attackers += 1
                return attackers * -1
            else:
                left = [y+1,x-1]
                if(inRange(left[0],left[1])):
                    if(gametiles[y+1][x-1].pieceonTile.tostring()=='p'):
                        attackers += 1
                right = [y+1,x+1]
                if(inRange(right[0],right[1])):
                    if(gametiles[y+1][x+1].pieceonTile.tostring()=='p'):    
                        attackers += 1
                return attackers * 1
        def protectedByBishop(piece):
            protectors = 0
            piece_text = piece.pieceonTile.tostring()
            location = piece.pieceonTile.calculatecoordinates()
            directions = [[-1,-1],[1,-1],[-1,1],[1,1]]
            upLeft = [-1,-1] #(x,y)
            upright = [1,-1] #(x,y)
            downLeft = [-1,1] #(x,y)
            downright = [1,1] #(x,y)
            for i in range(0,4):
                for j in range(0,8):
                    targety,targetx = location[0]+(j*directions[i][1]),location[1]+(j*directions[i][0])
                    if(inRange(targety,targetx)):
                        target = gametiles[targety][targetx].pieceonTile.tostring()
                        if(target != None):
                            if (piece.pieceonTile.alliance == "Black"):
                                if(target != "B"):
                                    continue
                                else:
                                    protectors -= 1
                            if (piece.pieceonTile.alliance == "White"):
                                if(target != "W"):
                                    continue
                                else:
                                    protectors += 1
            return protectors
        def queenDeepEval(piece):
            val = 0
            moves = piece.pieceonTile.legalmoveb(gametiles)
            alliance = piece.pieceonTile.alliance
            if moves != None:
                for move in moves:
                    target = getPieceOnTile(move[1],move[0])
                    if(target.tostring() != None and target.alliance != alliance):
                        target_text = target.tostring().upper()
                        if target_text == "N":
                            val += 1
                        if target_text == "Q":
                            val -= 5
                        if target_text == "K":
                            val += 10
            val += len(moves)/2 if moves != None else 0# the more mobility the better the square
            return val*-1 if piece.pieceonTile.tostring() == "Q" else val
        
        def rookDeepEval(piece):
            val = 0
            moves = piece.pieceonTile.legalmoveb(gametiles)
            alliance = piece.pieceonTile.alliance
            if moves != None:
                for move in moves:
                    target = getPieceOnTile(move[1],move[0])
                    if(target.tostring() != None and target.alliance != alliance):
                        target_text = target.tostring().upper()
                        if  target_text == "B" or target_text == "N":
                            val += 1
                        if target_text == "Q":
                            val -= 2
                        if target_text == "K":
                            val += 4
            val += len(moves)/2 if moves != None else 0# the more mobility the better the square
            return val*-1 if piece.pieceonTile.tostring() == "R" else val
        def knightDeepEval(piece):
            val = 0
            moves = piece.pieceonTile.legalmoveb(gametiles)
            alliance = piece.pieceonTile.alliance
            if moves != None:
                for move in moves:
                    target = getPieceOnTile(move[1],move[0])
                    if(target.tostring() != None and target.alliance != alliance):
                        target_text = target.tostring().upper()
                        if  target_text == "B":
                            val += 1
                        if target_text == "R":
                            val += 2
                        if target_text == "Q":
                            val += 3
                        if target_text == "K":
                            val += 4
            val += len(moves)/2 if moves != None else 0# the more mobility the better the square
            return val*-1 if piece.pieceonTile.tostring() == "N" else val
        def bishopDeepEval(piece):
            val = 0
            moves = piece.pieceonTile.legalmoveb(gametiles)
            alliance = piece.pieceonTile.alliance
            if moves != None:
                for move in moves:
                    target = getPieceOnTile(move[1],move[0])
                    if(target.tostring() != None and target.alliance != alliance):
                        target_text = target.tostring().upper()
                        if target_text == "N":
                            val += 2
                        if target_text == "R":
                            val += 3
                        if target_text == "Q":
                            val -= 2
                        if target_text == "K":
                            val += 5
            val += len(moves)/2 if moves != None else 0# the more mobility the better the square
            return val*-1 if piece.pieceonTile.tostring() == "B" else val
        def pawnDeepEval(piece):
            val = 0
            moves = piece.pieceonTile.legalmoveb(gametiles)
            alliance = piece.pieceonTile.alliance
            if moves != None:
                for move in moves:
                    target = getPieceOnTile(move[1],move[0])
                    if(target.tostring() != None and target.alliance != alliance):
                        target_text = target.tostring().upper()
                        if  target_text == "B" or target_text == "N":
                            val += 1
                        if target_text == "R":
                            val += 1
                        if target_text == "Q":#CHANGE THIS TO MAKE SURE IT IS TARGETIUNG THE CORREC TEAM 
                            val += 1
                        if target_text == "K":
                            val += 1
            val += len(moves) if moves != None else 0# the more mobility the better the square
            return val*-1 if piece.pieceonTile.tostring() == "P" else val
        def boardControl(piece):
            val = 0
            if piece.pieceonTile.tostring() == "P":
                position = piece.pieceonTile.calculatecoordinates()
                val = -1*(val + position[1])*2
                if position[1] == 7:
                    val = val - 100
            elif piece.pieceonTile.tostring() == "p":
                position = piece.pieceonTile.calculatecoordinates()
                val = (val + 7 - position[1])*2
                if position[1] == 0:
                    val = val + 100
            return val
        def getPieceOnTile(y,x):
            return gametiles[y][x].pieceonTile
        








        # Functions below here were made by Heckers, might need some refining
        # I'll make sure to leave comments to let you walk through my thought process
        # NOTICE: None of these are implemented into evaluating each moves value, just created the functions


        def attackedByKnight(piece):
            attackers = 0
            piece_text = piece.pieceonTile.tostring()
            if(piece_text.lower() == piece_text):
                
            # First part is the 2 space move, second is the one space: Ex: LeftUp = attacker moves 2 spaces left, 1 space up
            # This is just following the same pattern as the pawn version of the attack function
                upLeft = [y-2,x+1] 
                upRight = [y-2,x-1] 
                rightUp = [y-1,x-2] 
                rightDown = [y+1,x-2] 
                downRight = [y+2,x-1] 
                downLeft = [y+2,x+1] 
                leftDown = [y+1, x+2] 
                leftUp = [y-1,x+2]

                # Not sure what the inRange line exactly does so it is not currently included

                # inRange just makes sure the space you are checking is actually a spot on the board because the game crashes if it's not

                # This code checks each of the spots an attacking knight could be
                # If there is a knight in a position to attack any opposing piece, the number of attackers += 1
            #     if(gametiles[y-2][x+1].pieceonTile.tostring()=='N'):
            #         attackers += 1
            #     if(gametiles[y-2][x-1].pieceonTile.tostring()=='N'):
            #         attackers += 1
            #     if(gametiles[y-1][x-2].pieceonTile.tostring()=='N'):
            #         attackers += 1
            #     if(gametiles[y+1][x-2].pieceonTile.tostring()=='N'):
            #         attackers += 1
            #     if(gametiles[y+2][x-1].pieceonTile.tostring()=='N'):
            #         attackers += 1
            #     if(gametiles[y+2][x+1].pieceonTile.toString()=='N'):
            #         attackers += 1
            #     if(gametiles[y+1][x+2].pieceonTile.toString()=='N'):
            #         attackers += 1
            #     if(gametiles[y-1][x+2].pieceonTile.toString()=='N'):
            #         attackers += 1

            #     return attackers * -1
            
            # # This is the same as the previous group of code but for the other player
            # else:
            #     if(gametiles[y+2][x-1].pieceonTile.toString()=='n'):
            #         attackers += 1
            #     if(gametiles[y+2][x+1].pieceonTile.toString()=='n'):
            #         attackers += 1
            #     if(gametiles[y+1][x+2].pieceonTile.toString()=='n'):
            #         attackers += 1
            #     if(gametiles[y-1][x+2].pieceonTile.toString()=='n'):
            #         attackers += 1
            #     if(gametiles[y-2][x+1].pieceonTile.toString()=='n'):
            #         attackers += 1
            #     if(gametiles[y-2][x-1].pieceonTile.toString()=='n'):
            #         attackers += 1
            #     if(gametiles[y-1][x-2].pieceonTile.toString()=='n'):
            #         attackers += 1
            #     if(gametiles[y+1][x-2].pieceonTile.toString()=='n'):
            #         attackers += 1
            #     return attackers * 1
        # Will add attack functions for other pieces








        def countOpponentPieces():
            opponentPieces = 0
            for x in range(8):     # going through all the rows and columns on the board (all squares on board)
                for y in range(8):
                    piece = gametiles[y][x]
                    piece_text = piece.pieceonTile.tostring()


                    if(gametiles[y][x].pieceonTile.tostring() == 'k'): # checking the piece string, if its an opponent piece, add 1 to count
                        opponentPieces += 1
                    if(gametiles[y][x].pieceonTile.tostring() == 'q'): # checking the piece string, if its an opponent piece, add 1 to count
                        opponentPieces += 1
                    if(gametiles[y][x].pieceonTile.tostring() == 'b'): # checking the piece string, if its an opponent piece, add 1 to count
                        opponentPieces += 1
                    if(gametiles[y][x].pieceonTile.tostring() == 'n'): # checking the piece string, if its an opponent piece, add 1 to count
                        opponentPieces += 1
                    if(gametiles[y][x].pieceonTile.tostring() == 'r'): # checking the piece string, if its an opponent piece, add 1 to count
                        opponentPieces += 1
                    if(gametiles[y][x].pieceonTile.tostring() == 'p'): # checking the piece string, if its an opponent piece, add 1 to count
                        opponentPieces += 1
                    return opponentPieces





        # Ends the group of functions made by Heckers












        for x in range(8):
            for y in range(8):
                    if gametiles[y][x].pieceonTile.tostring()=='P':
                        value=value-100

                        if(countOpponentPieces() == 1):
                            value = value + protectedByPawn(piece)
                            value = value + boardControl(piece)  
                           
                        else:
                             # Improves evaluation when pawns protect a piece
                             value = value + protectedByPawn(piece)
                             value = value + pawnDeepEval(piece)
                             value = value + boardControl(piece)
                             #value = value + protectedByBishop(piece)
                        
                    if gametiles[y][x].pieceonTile.tostring()=='N':
                        value=value-350

                        if(countOpponentPieces() == 1):
                            value = value + protectedByPawn(piece)*2
                            value = value + attackedByPawn(piece)
                        
                        else:

                            value = value + protectedByPawn(piece)*2
                            value = value + knightDeepEval(piece)
                            value = value + attackedByPawn(piece)
                            #value = value + protectedByBishop(piece)
                        

                    if gametiles[y][x].pieceonTile.tostring()=='B':
                        value=value-350

                        if(countOpponentPieces() == 1):
                            value = value + protectedByPawn(piece)*2
                            value = value + attackedByPawn(piece)
                        
                        else:

                            value = value + protectedByPawn(piece)*2
                            value = value + bishopDeepEval(piece)
                            value = value + attackedByPawn(piece)
                            #value = value + protectedByBishop(piece)

                

                    if gametiles[y][x].pieceonTile.tostring()=='R':
                        value=value-525

                        if(countOpponentPieces() == 1):
                            value = value + protectedByPawn(piece)*3
                            value = value + attackedByPawn(piece)
                        
                        else:

                            value = value + protectedByPawn(piece)*3
                            value = value + rookDeepEval(piece)
                            value = value + attackedByPawn(piece)
                            #value = value + protectedByBishop(piece)

                    if gametiles[y][x].pieceonTile.tostring()=='Q':
                        value=value-1000

                        if(countOpponentPieces() == 1):
                            value = value + protectedByPawn(piece)*4
                            value = value + attackedByPawn(piece)
                        
                        else:

                            value = value + protectedByPawn(piece)*4
                            value = value + queenDeepEval(piece)
                            value = value + attackedByPawn(piece)
                            #value = value + protectedByBishop(piece)

                    if gametiles[y][x].pieceonTile.tostring()=='K':
                        value=value-10000


                    if gametiles[y][x].pieceonTile.tostring()=='p':
                        value=value+100

                        if(countOpponentPieces() == 1):
                            value = value + protectedByPawn(piece)
                            value = value + boardControl(piece)


                        else:

                            # Improves evaluation when pawns protect eachother forming chains
                            value = value + protectedByPawn(piece)
                            value = value + pawnDeepEval(piece)
                            value = value + boardControl(piece)
                            #value = value + protectedByBishop(piece)

                    if gametiles[y][x].pieceonTile.tostring()=='n':
                        value=value+350

                        if(countOpponentPieces() == 1):
                            value = value + protectedByPawn(piece)*2
                            value = value + attackedByPawn(piece)


                        else:

                            value = value + protectedByPawn(piece)*2
                            value = value + knightDeepEval(piece)
                            value = value + attackedByPawn(piece)
                            #value = value + protectedByBishop(piece)

                    if gametiles[y][x].pieceonTile.tostring()=='b':
                        value=value+350

                        if(countOpponentPieces() == 1):
                            value = value + protectedByPawn(piece)*2
                            value = value + attackedByPawn(piece)

                        else:

                            value = value + protectedByPawn(piece)*2
                            value = value + bishopDeepEval(piece)
                            value = value + attackedByPawn(piece)
                        #value = value + protectedByBishop(piece)

                    if gametiles[y][x].pieceonTile.tostring()=='r':
                        value=value+525

                        if(countOpponentPieces() == 1):
                            value = value + protectedByPawn(piece)*3
                            value = value + attackedByPawn(piece)

                        else:

                            value = value + protectedByPawn(piece)*3
                            value = value + rookDeepEval(piece)
                            value = value + attackedByPawn(piece)
                            #value = value + protectedByBishop(piece)

                    if gametiles[y][x].pieceonTile.tostring()=='q':
                        value=value+1000

                        if(countOpponentPieces() == 1):

                            value = value + protectedByPawn(piece)*4
                            value = value + attackedByPawn(piece)

                        else:

                            value = value + protectedByPawn(piece)*4
                            value = value + queenDeepEval(piece)
                            value = value + attackedByPawn(piece)
                            #value = value + protectedByBishop(piece)

                    if gametiles[y][x].pieceonTile.tostring()=='k':
                        value=value+10000



        return value


    def move(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='K' or gametiles[y][x].pieceonTile.tostring()=='R':
            gametiles[y][x].pieceonTile.moved=True

        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='P' and y+1==n and y==6:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='P':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('Black',self.updateposition(n,m))
                promotion=False

        return gametiles



    def revmove(self,gametiles,x,y,n,m,mts):
        if gametiles[x][y].pieceonTile.tostring()=='K':
            if m==y-2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[n][7].pieceonTile.moved=False

                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            elif m==y+2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(m,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[n][0].pieceonTile.moved=False
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts

            return gametiles

        if gametiles[x][y].pieceonTile.tostring()=='k':
            if m==y-2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            elif m==y+2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(n,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts


            return gametiles

        gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
        s=self.updateposition(n,m)
        gametiles[n][m].pieceonTile.position=s
        gametiles[x][y].pieceonTile=mts

        return gametiles



    def movew(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='k' or gametiles[y][x].pieceonTile.tostring()=='r':
            pass

        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='p' and y-1==n and y==1:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='p':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('White',self.updateposition(n,m))
                promotion=False

        return gametiles
























                        
