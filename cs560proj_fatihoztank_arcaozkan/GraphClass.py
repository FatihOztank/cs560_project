import networkx as nx

def createDictFromLog(log):
    depDict = {}
    with open(log, 'r',encoding="utf-8") as file:
        for line in file:
            arr = line.split()
            if "elasticsearch" in arr[2]:
                if arr[0] in depDict:
                    depDict[arr[0]].append(arr[2])
                else:
                    depDict[arr[0]] = [arr[2]]

    return depDict


def updateDictAccToClassAndDepth(logDict, className, depth):
    returnDict = {}
    returnDict[className] = logDict[className]
    for i in range(depth - 1):
        for key, value in returnDict.items():
            tmpDict = {}
            for item in value:
                if item not in returnDict:
                    try:
                        tmpDict[item] = logDict[item]
                    except:
                        pass
        returnDict = returnDict | tmpDict

    return returnDict



class GraphReader():
    def compareGraphs(self, graph1, graph2):
        diff = set(graph1.graph.edges()) ^ set(graph2.graph.edges())
        added = diff - set(graph1.graph.edges())
        removed = diff - set(graph2.graph.edges())
        print("added: ", len(added))
        print("\n")
        print("removed: ",len(removed))
        print("diff: ", len(diff))


    

class DependencyGraph():
    def __init__(self, logfile, className = None, depth = 1):
        
        logdict = createDictFromLog(logfile)
        if className != None:
            #className takes a class name from dependency analyses, for ex:
            # org.elasticsearch.action.bulk 
            # org.elasticsearch.action.admin.indices.upgrade.post
            if className not in logdict:
                print("Invalid class name...")
                return
            if depth < 1:
                print("Invalid depth value. Depth has to be greater than 0.")
                return
            logdict = updateDictAccToClassAndDepth(logdict, className, depth)

        zip_iterator = zip(logdict.keys(), range(len(logdict.keys())))
        class_encodings = dict(zip_iterator)

        g = nx.DiGraph()
        for key, value in logdict.items():
            for item in value:
                if item in class_encodings:
                    g.add_edge(class_encodings[key], class_encodings[item])
                else:
                    class_encodings[item] = len(class_encodings)
                    g.add_edge(class_encodings[key], class_encodings[item])
         
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(sorted(g.nodes(data=True)))
        self.graph.add_edges_from(g.edges(data=True)) 
        self.class_encodings = class_encodings
        

    def __str__(self): # only for debugging purposes
        #print("Nodes: " + str(self.graph.nodes()))
        #print("Edges: " + str(self.graph.edges()))

        print(str(len(self.graph.nodes())))
        print(str(len(self.graph.edges())))
        return ""

    

           

if __name__ == "__main__":

    logFile = "elasticsearchReports/dep_analysis_report2021-02-17"
    depGraph = DependencyGraph(logFile,className="org.elasticsearch.index.query", 
        depth=2)
    #depGraph = DependencyGraph(logFile)
    print(depGraph.class_encodings, end="\n\n\n")
    print(depGraph)