from pymaze import maze,COLOR,agent,textLabel
m=maze()
m.CreateMaze(loopPercent=100)

a=agent(m,footprints=True,filled=True)

l1=textLabel(m,'Total Cells',m.rows*m.cols)

m.tracePath({a:m.path},delay=100)

m.run()