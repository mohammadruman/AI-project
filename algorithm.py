from pymaze import maze,agent,textLabel,COLOR
from collections import deque
from queue import PriorityQueue


def DFS_FUNCTION(maz,start=None):
    if start is None:
        start=(maz.rows,maz.cols) 
    frontier=[start]
    explored=[start]
    DfsPath={}
    DSearch=[]
    while len(frontier)>0:
        CurrCell=frontier.pop()
        DSearch.append(CurrCell)
        if CurrCell==maz._goal:
            break
        pos=0
        for d in 'ENSW':
            if maz.maze_map[CurrCell][d]==True:
                if d=='E':
                    ChildCell=(CurrCell[0],CurrCell[1]+1)
                elif d=='W':
                    ChildCell=(CurrCell[0],CurrCell[1]-1)
                elif d=='S':
                    ChildCell=(CurrCell[0]+1,CurrCell[1])
                elif d=='N':
                    ChildCell=(CurrCell[0]-1,CurrCell[1])
                if ChildCell in explored:
                    continue
                pos+=1
                explored.append(ChildCell)
                frontier.append(ChildCell)
                DfsPath[ChildCell]=CurrCell
        if pos>1:
            maz.markCells.append(CurrCell)
    FwdPath={}
    Cell=maz._goal
    while Cell!=start:
        FwdPath[DfsPath[Cell]]=Cell
        Cell=DfsPath[Cell]
    return DSearch,DfsPath,FwdPath


def BFS_FUNCTION(maz,start=None):
    if start is None:
        start=(maz.rows,maz.cols)
    frontier = deque()
    frontier.append(start)
    BfsPath = {}
    explored = [start]
    BSearch=[]

    while len(frontier)>0:
        CurrCell=frontier.popleft()
        if CurrCell==maz._goal:
            break
        for d in 'ENSW':
            if maz.maze_map[CurrCell][d]==True:
                if d=='E':
                    ChildCell=(CurrCell[0],CurrCell[1]+1)
                elif d=='W':
                    ChildCell=(CurrCell[0],CurrCell[1]-1)
                elif d=='S':
                    ChildCell=(CurrCell[0]+1,CurrCell[1])
                elif d=='N':
                    ChildCell=(CurrCell[0]-1,CurrCell[1])
                if ChildCell in explored:
                    continue
                frontier.append(ChildCell)
                explored.append(ChildCell)
                BfsPath[ChildCell] = CurrCell
                BSearch.append(ChildCell)
   
    FwdPath={}
    Cell=maz._goal
    while Cell!=(maz.rows,maz.cols):
        FwdPath[BfsPath[Cell]]=Cell
        Cell=BfsPath[Cell]
    return BSearch,BfsPath,FwdPath

def dis(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return (abs(x1 - x2) + abs(y1 - y2))
    
def aStar(maz,start=None):
    if start is None:
        start=(maz.rows,maz.cols)
    Openn = PriorityQueue()
    Openn.put((dis(start, maz._goal), dis(start, maz._goal), start))
    APath = {}
    G_Score = {row: float("inf") for row in maz.grid}
    G_Score[start] = 0
    F_Score = {row: float("inf") for row in maz.grid}
    F_Score[start] = dis(start, maz._goal)
    SearchPath=[start]
    while not Openn.empty():
        CurrCell = Openn.get()[2]
        SearchPath.append(CurrCell)
        if CurrCell == maz._goal:
            break        
        for d in 'ENSW':
            if maz.maze_map[CurrCell][d]==True:
                if d=='E':
                    ChildCell=(CurrCell[0],CurrCell[1]+1)
                elif d=='W':
                    ChildCell=(CurrCell[0],CurrCell[1]-1)
                elif d=='N':
                    ChildCell=(CurrCell[0]-1,CurrCell[1])
                elif d=='S':
                    ChildCell=(CurrCell[0]+1,CurrCell[1])

                Temp_G_Score = G_Score[CurrCell] + 1
                Temp_F_Score = Temp_G_Score + dis(ChildCell, maz._goal)

                if Temp_F_Score < F_Score[ChildCell]:   
                    APath[ChildCell] = CurrCell
                    G_Score[ChildCell] = Temp_G_Score
                    F_Score[ChildCell] = Temp_G_Score + dis(ChildCell, maz._goal)
                    Openn.put((F_Score[ChildCell], dis(ChildCell, maz._goal), ChildCell))


    FwdPath={}
    Cell=maz._goal
    while Cell!=start:
        FwdPath[APath[Cell]]=Cell
        Cell=APath[Cell]
    return SearchPath,APath,FwdPath


if __name__ == "__main__":

 while True:
  print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
  print("..................WELCOME TO MAZE..................")
  print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
  print("____________________________________________________")
  print("         Select The Algorithm To Search.            ")
  print("____________________________________________________")
  print("\n")
  print("1. Breadth First Search (BFS).")
  print("2. Depth First Search (DFS).")
  print("3. A* Search(A*).")
  print("4. Exit.\n")
  choice=input("Enter your choice ::-")
  if choice =="DFS" or choice =="dfs" :
     maz=maze(20,40)
     maz.CreateMaze()
     DSearch,DfsPath,FwdPath=DFS_FUNCTION(maz)
     agnt1=agent(maz,footprints=True,shape='square',color=COLOR.blue)
     agnt2=agent(maz,1,1,goal=(5,5),footprints=True,filled=True,color=COLOR.green)
     agnt3=agent(maz,footprints=True,color=COLOR.yellow)
     maz.tracePath({agnt1:DSearch},showMarked=True,delay=50)
     maz.tracePath({agnt2:DfsPath},delay=75)
     maz.tracePath({agnt3:FwdPath},delay=100)

     DFS_FUNCTION(maz)
     lab=textLabel(maz,'A DFS Path Length',len(FwdPath)+1)
     lab=textLabel(maz,'A DFS Search Length',len(DSearch))
     maz.run()

  elif choice =="BFS" or choice=="bfs" :
      maz=maze(20,40)
      maz.CreateMaze()
      BSearch,BfsPath,FwdPath=BFS_FUNCTION(maz)
      agnt1=agent(maz,footprints=True,color=COLOR.blue,shape='square')
      agnt2=agent(maz,footprints=True,color=COLOR.red,shape='arrow',filled=False)
      agnt3=agent(maz,1,1,footprints=True,color=COLOR.yellow,shape='square',filled=True,goal=(maz.rows,maz.cols))
      maz.tracePath({agnt1:BSearch},delay=50)
      maz.tracePath({agnt3:BfsPath},delay=75)
      maz.tracePath({agnt2:FwdPath},delay=100)

      lab=textLabel(maz,'A BFS Path Length',len(FwdPath)+1)
      lab=textLabel(maz,'A BFS Search Length',len(BSearch))

      maz.run()

  elif choice =="A*" or choice=="a*":
      maz=maze(20,40)
      maz.CreateMaze()
      SearchPath,APath,FwdPath=aStar(maz)
      agnt1=agent(maz,footprints=True,color=COLOR.blue,)
      agnt2=agent(maz,1,1,footprints=True,color=COLOR.yellow,filled=True,goal=(maz.rows,maz.cols))
      agnt3=agent(maz,footprints=True,color=COLOR.red,shape='arrow')

      maz.tracePath({agnt1:SearchPath},delay=50)
      maz.tracePath({agnt2:APath},delay=75)
      maz.tracePath({agnt3:FwdPath},delay=100)

      lab=textLabel(maz,'A Star Path Length',len(FwdPath)+1)
      lab=textLabel(maz,'A Star Search Length',len(SearchPath))
      maz.run()

  elif choice =="Exit" or choice == "exit":
      exit()