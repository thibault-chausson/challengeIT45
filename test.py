'''
Method to take two equally-sized lists and return just the elements which lie 
on the Pareto frontier, sorted into order.
Default behaviour is to find the maximum for both X and Y, but the option is
available to specify maxX = False or maxY = False to find the minimum for either
or both of the parameters.
'''
def pareto_frontier(Xs, Ys, maxX = True, maxY = True):
# Sort the list in either ascending or descending order of X
    myList = sorted([[Xs[i], Ys[i]] for i in range(len(Xs))], reverse=maxX)
# Start the Pareto frontier with the first value in the sorted list
    p_front = [myList[0]]    
# Loop through the sorted list
    for pair in myList[1:]:
        if maxY: 
            if pair[1] >= p_front[-1][1]: # Look for higher values of Y…
                p_front.append(pair) # … and add them to the Pareto frontier
        else:
            if pair[1] <= p_front[-1][1]: # Look for lower values of Y…
                p_front.append(pair) # … and add them to the Pareto frontier
# Turn resulting pairs back into a list of Xs and Ys
    p_frontX = [pair[0] for pair in p_front]
    p_frontY = [pair[1] for pair in p_front]
    return p_frontX, p_frontY


import matplotlib.pyplot as plt
Xs = [ 5.16478757,  6.17605695,  5.98117115,  4.34084136,  6.26172972 , 5.69453693,
   5.96983248,  3.88568802, 10.48808275,  6.53983584 ]

Ys = [132.94335445, 137.72940963, 137.01104522, 133.5484552,  135.61765744,
  133.26613336, 134.46457897, 133.3384147,  140.35968568, 136.06612801,

 ]

# get your data from somewhere to go here
# Find lowest values for cost and highest for savings
p_front = pareto_frontier(Xs, Ys, maxX = False, maxY = True)
# Plot a scatter graph of all results
plt.scatter(Xs, Ys)
# Then plot the Pareto frontier on top
plt.plot(p_front[0], p_front[1])
plt.show()