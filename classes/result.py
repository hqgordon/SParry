import numpy as np

from utils.debugger import Logger

logger = Logger(__name__)

class Result(object):
    """
    function: 
        to store the result of different algorithm.

    parameters:
        dist: list, the shortest path distance answer for algorithm.
        timeCostNum: float, a float data of time cost of getting the answer, so it can use to calculate.
        timeCost: str, a str data of time cost of getting the answer.
        memoryCost: str, memory cost of getting the answer.
        graph: str/list/tuple, must, the graph data that you want to get the shortest path.(more info please see the developer documentation).
        graphType: str, must, type of the graph data, only can be [matrix, CSR, edgeSet].(more info please see the developer documentation).
        msg: str, the info of the graph.
    
    method:
        display: show the detail of this calculation.
        drawPath: draw the path from vertices to the sources.
        calcPath: calc the path through the graph and dist.
    
    return: 
        class, Result object. (see the 'SPoon/classes/result.py/Result') 
    """
    def __init__(self, 
                dist = None, 
                timeCost = None, 
                memoryCost = None, 
                graph = None): # class Graph

        logger.info("class.Result initializing.")

        self.dist = np.array(dist).flatten() # 距离记录
        self.path = None # 路径记录
        self.timeCostNum = timeCost
        self.timeCost = str(timeCost * 100000 // 100 / 1000) + ' sec' # 时间花费 保留两位小数  str(timeCost * 100000 // 100 / 1000) + ' sec'
        self.memoryCost = memoryCost # 内存的开销
        
        # 待补充 更多关于图的特点
        self.graph = graph # 图数据

    
    def display(self):
        """
        function: 
            show the detail of the graph, parameters and calc time.

        parameters:
            None, but 'self'.
        
        return: 
            str, the msg info.       
        """

        return f"{self.graph.msg}\n\n[+] timeCost = {self.timeCost}"
    
    def drawPath(self):
        """
        function: 
            to get the path.

        parameters:
            None, but 'self'.
        
        return: 
            None, no return.        
        """

        if self.path is None:
            self.calcPath()
        
        from utils.showPath import draw
        
        # 先就只展示一个源
        for i in range(self.dist.size):
            if self.dist[i] == 0:
                s = i % self.graph.n
                
        draw(path = self.path, s = s, graph = self.graph)

    def calcPath(self):
        """
        function: 
            to get the path.

        parameters:
            None, but 'self'.
        
        return: 
            None, no return.
        """
   
        logger.info("turning to func calcPath.")

        if(self.dist is None):
            raise Exception("can not calc path without dist")
        
        if(self.graph is None):
            raise Exception("can not calc path without graph")

        # calc path with dist and graphic data
        if(self.graph.method == "edge"):
            self.calcPathFromEdgeSet()
        else:
            self.calcPathFromCSR()

    def calcPathFromCSR(self):
        """
        function: 
            to get the path.

        parameters:
            None, but 'self'.
        
        return: 
            None, no return.        
        """

        V, E, W = self.graph.graph[0], self.graph.graph[1], self.graph.graph[2]
        n = self.graph.n
        self.path = np.full((self.dist.size, ), -1)
        sNum = self.dist.size // n # 源点个数

        for i in range(n):
            for j in range(V[i], V[i + 1]):
                for k in range(sNum):
                    kn = k * n
                    if(self.path[E[j] + kn] == -1 and self.dist[E[j] + kn] == self.dist[i + kn] + W[j]):
                        self.path[E[j] + kn] = i # E[j] 这个点在某个源的问题中的前驱是结点i
        
    def calcPathFromMatrix(self):
        """
        function: 
            to get the path.

        parameters:
            None, but 'self'.
        
        return: 
            None, no return.         
        """

        raise Exception("there should not be a matrix graph data.")

        # 这里就不再检验数据的正确性了
        n = np.array(self.graph).shape[0]

        self.path = np.full((self.dist.size, ), -1)
        sNum = self.dist.size // n # 源点个数

        for i in range(n):
            for j in range(n):
                for k in range(sNum):
                    kn = k * n
                    if(self.path[j + kn] == -1 and self.dist[j + kn] == self.dist[i + kn] + self.matrix[i][j]):
                        self.path[j + kn] = i # E[j] 这个点在某个源的问题中的前驱是结点i

    def calcPathFromEdgeSet(self):
        """
        function: 
            to get the path.

        parameters:
            None, but 'self'.
        
        return: 
            None, no return.         
        """

        # 这里就不再检验数据的正确性了
        src, des, w = self.graph.graph[0], self.graph.graph[1], self.graph.graph[2]
        m = self.graph.m

        self.path = np.full((self.dist.size, ), -1)
        n = self.graph.n

        sNum = self.dist.size // n # 源点个数

        for i in range(m):
            for k in range(sNum):
                kn = k * n
                if(self.path[des[i] + kn] == -1 and self.dist[des[i] + kn] == self.dist[src[i] + kn] + w[i]):
                    self.path[des[i] + kn] = src[i]# E[j] 这个点在某个源的问题中的前驱是结点i        
