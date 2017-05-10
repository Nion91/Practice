# -*- coding: utf-8 -*-

class gobang:
    def __init__(self,size=3,winpoint=3):
        self.size=size
        self.index=range(size)
        self.chessboard={}
        self.winpoint=winpoint
        self.win=False
        self.status=False

    def MakeBoard(self):
        for i in self.index:
            for j in self.index:
                self.chessboard[(i,j)]=' '

    def PrintBoard(self):
        print '   '+' '.join([str(x) for x in self.index])
        print '  +'+'-+'*self.size
        for i in self.index:
            print str(i)+' |'+'|'.join([self.chessboard[(i,j)] for j in self.index])+'|'
            print '  +'+'-+'*self.size
    
    def LineList(self,index):
        h,v=index
        lists=[[(x,v) for x in self.index],
               [(h,y) for y in self.index],
               [(x,x+v-h) for x in self.index if x+v-h<self.size and x+v-h>=0],
               [(x,v+h-x) for x in self.index if v+h-x<self.size and v+h-x>=0]]
        lists=[x for x in lists if len(x)>=self.winpoint]
        return lists

    def CheckLine(self,line):
        count=0
        sign=''
        for i in line:
            i=self.chessboard[i]
            if i==' ':
                count=0
                sign=''
            else:
                if i==sign:
                    count+=1
                    if count==self.winpoint:
                        self.win=True
                        break
                else:
                    sign=i
                    count=1

    def CheckWin(self,index):
        lines=self.LineList(index)
        if lines:
            for line in lines:
                self.CheckLine(line)
                if self.win:
                    break

    def PlayTurn(self,symbol):
        print 'Turn for %s. Which place:' % symbol
        while True:
            input_=raw_input()
            if input_=='q':
                self.status=True
                return None
            try:
                x,y=input_.split()
                index=(int(x),int(y))
            except:
                print 'Wrong input. Please try again:'
                continue

            if index not in self.chessboard:
                print 'Wrong index. Please try again:'
                continue

            if self.chessboard[index]!=' ':
                print 'Cannot choose this place. Please try another:'
                continue
            break

        self.chessboard[index]=symbol
        self.PrintBoard()
        self.CheckWin(index)
        if self.win:
            print 'You win!!!'

    def PlayWithPerson(self):
        self.MakeBoard()
        while True:
            self.PlayTurn('O')
            if self.status or self.win:
                break
            self.PlayTurn('X')
            if self.status or self.win:
                break
        return None


if __name__=='__main__':
    a=gobang(9,5)
    a.PlayWithPerson()

