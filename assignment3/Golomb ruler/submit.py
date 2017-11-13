#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value alongside the marker positions
#Or return -1,[] if no solution exists for the given L

#Your backtracking function implementation
def BT(L, M):
    "*** YOUR CODE HERE ***"
    import sys
    optimal_length = sys.maxint
    finalList = []
    optimal_length, finalList = BTHelper(0, L, M-1, [0], optimal_length, finalList)
    if len(finalList) is 0:
        optimal_length = -1
    print(optimal_length, finalList)


# A recursive function to perform backtracking
# starrt :- index to start from
# mark_list :- to keep track of marks we have explored
# optimall_length :- most optimal length for the golomb ruler
# final_mark_list :- list to keep track of the final indexes
def BTHelper(start, L, M, mark_list, optimal_length, final_mark_list):

    if M is 0:
        if mark_list[len(mark_list)-1] < optimal_length:
            optimal_length = mark_list[len(mark_list) - 1]
            final_mark_list = mark_list
        return (optimal_length, final_mark_list)

    copy_mark_list = list(mark_list)
    for i in range(L+1):
        if i > start and is_legal_distance(list(copy_mark_list), i):
            copy_mark_list.append(i)
            optimal_length, final_mark_list = BTHelper(i, L, M - 1, list(copy_mark_list), optimal_length, final_mark_list)
            copy_mark_list.remove(i)
    return (optimal_length, final_mark_list)

# check if the chosen distance is already taken or not
def is_legal_distance(mark_list, number):
    if not mark_list:
        return True
    mark_list.append(number)
    check = {}
    i = 0
    while(i < len(mark_list)):
        j = i+1
        while(j < len(mark_list)):
            dist = mark_list[j]-mark_list[i]
            if check.has_key(dist):
                return False
            else:
                check[dist] = 1
            j += 1
        i += 1
    return True


def FC(L, M):
    import sys
    optimal_length = sys.maxint
    finalList = []
    domain = initDomain(L,M)
    optimal_length, finalList = FCHelper(0, L, M-1, [0], optimal_length, finalList, domain, M)
    if len(finalList) is 0:
        optimal_length = -1
    print(optimal_length, finalList)


def initDomain(L, M):
    domain = {}
    for i in range(M):
        domain_val = []
        for j in range(L+1):
            domain_val.append(j)
        domain[i] = list(domain_val)
    return dict(domain)

# A recursive function to perform forward checking
# start :- index to start from
# mark_list :- to keep track of marks we have explored
# optimal_length :- most optimal length for the golomb ruler
# final_mark_list :- list to keep track of the final indexes
def FCHelper(start, L, M, mark_list, optimal_length, final_mark_list, domain, totalMark):
    if M is 0:
        if mark_list[len(mark_list)-1] < optimal_length:
            optimal_length = mark_list[len(mark_list) - 1]
            final_mark_list = mark_list
        return (optimal_length, final_mark_list)

    local_mark_list = list(mark_list)
    for i in range(L+1):
        # newDomain = copy.deepcopy(domain)
        if i > start and is_legal_distance(list(local_mark_list), i) and forwardCheck(list(local_mark_list), i, domain, totalMark):
            local_mark_list.append(i)
            optimal_length, final_mark_list = FCHelper(i, L, M - 1, list(local_mark_list), optimal_length, final_mark_list, domain, totalMark)
            local_mark_list.remove(i)
    return (optimal_length, final_mark_list)

# check if the next node will left with any value in domain or not
def forwardCheck(mark_list, number, newDomain, totalMark):
    mark_list.append(number)
    if len(mark_list) == totalMark:
        return True
    return_val = True

    for i in range(len(newDomain.keys())):
        domain_val = newDomain[i]

        # check all the numbers from the lengths we have already explored
        length = len(domain_val[number:])

        for val in list(domain_val[number:]):
            if not is_legal_distance(list(mark_list), val):
                length -= 1
            if length <= 0:
                return False
    return return_val


#Bonus: backtracking + constraint propagation
def CP(L, M):
    "*** YOUR CODE HERE ***"
    return -1,[]

if __name__ == '__main__':
    BT(6, 4)
    FC(55, 10)

    #L = 6, M = 4,      BT = ~0 sec,    Nodes = 21          FC = ~0 sec,    Nodes = 19
    #L = 11, M = 5,     BT = ~0 sec,    Nodes = 146         FC = ~0 sec,    Nodes = 129
    #L = 17, M = 6,     BT = ~0 sec,    Nodes = 1028        FC = ~1 sec,    Nodes = 914
    #L = 25, M = 7,     BT = ~1 sec,    Nodes = 9014        FC = ~2 min,    Nodes = 8280
    #L = 34, M = 8,     BT = ~4 sec,    Nodes = 74619       FC = ~7 min,    Nodes = 70733
    #L = 44, M = 9,     BT = ~30 sec,   Nodes = 606615      FC = ~60 sec,   Nodes =
    #L = 55, M = 10,    BT = ~7 min,    Nodes = 4832742     FC = ~10 min,   Nodes =