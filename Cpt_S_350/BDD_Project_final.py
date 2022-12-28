from pyeda.inter import *


def Prime(num):
    if num < 3: return False
    n = num // 2 + 1
    for i in range(2, n):
        if num % i == 0:
            return False
    return True


def Edges():
    set_edges = []
    for i in range(0, 32):
        for j in range(0, 32):
            if (i + 3) % 32 == j % 32 or (i + 8) % 32 == j % 32:
                node_X = encode_bool(i, 'x')
                node_Y = encode_bool(j, 'y')
                edge = node_X + '&' + node_Y
                set_edges.append(edge)
    return '|'.join(set_edges)

def encode_bool(per, P):
    if P is None: P = 'x'
    five_bit = format(per, '05b')
    my_list = []
    for i, c in enumerate(five_bit):
        index = i + 1
        rep = P
        if c == '0':
            rep = '~' + rep + str(index)
        else:
            rep = rep + str(index)
        my_list.append(rep)
    return "&".join(my_list)


def encode_bool_2(per, P_2):
    if P_2 is None: P_2 = 'x'
    five_bit_2 = format(per, '05b')
    my_list_2 = []
    for u, v in enumerate(five_bit_2):
        index = u + 1
        temp = P_2
        if v == '0':  # remember negation
            temp = '~' + temp + str(index)
        else:
            temp = temp + str(index)
        my_list_2.append(temp)
    return ", ".join(my_list_2)


def list(m_list, prefix_l):
    list = []
    for num in m_list:
        l_temp = encode_bool(num, prefix_l)
        list.append(l_temp)
    return '|'.join(list)


def BDD(X):
    expression = expr(X)
    bdd = expr2bdd(expression)
    return bdd


def composed(bdd1, bdd2):
    X = [bddvar("x1"), bddvar("x2"), bddvar("x3"), bddvar("x4"), bddvar("x5")]
    Y = [bddvar("y1"), bddvar("y2"), bddvar("y3"), bddvar("y4"), bddvar("y5")]
    Z = [bddvar("z1"), bddvar("z2"), bddvar("z3"), bddvar("z4"), bddvar("z5")]

    composed_X_Z = bdd2.compose({X[0]: Z[0], X[1]: Z[1], X[2]: Z[2], X[3]: Z[3], X[4]: Z[4]})
    composed_Y_Z = bdd1.compose({Y[0]: Z[0], Y[1]: Z[1], Y[2]: Z[2], Y[3]: Z[3], Y[4]: Z[4]})
    return (composed_X_Z & composed_Y_Z).smoothing(Z)


def closure(bdd):
    h = bdd
    while True:
        prime_h = h
        h = prime_h or composed(prime_h, bdd)
        if h.equivalent(prime_h):
            break
    return h


def bdd_check(bdd, num_1, num_2):
    b_num1 = encode_bool_2(num_1, 'x')
    b_num2 = encode_bool_2(num_2, 'y')

    search = "And(" + b_num1 + ", " + b_num2 + ")"
    expr = bdd2expr(bdd)

    if search in str(expr):
        return 1
    else:
        return 0


def even_check(bdd, num):
    n = format(num, "05b")
    if str(n[4]) == '0':
        return 1
    else:
        return 0


def check_prime(bdd, num):
    num_1 = encode_bool_2(num, 'y')
    search = "And(" + num_1 + ")"
    expr = bdd2expr(bdd)

    if search in str(expr):
        return 1
    else:
        search = search.replace(', y4', '')
        if search in str(expr):
            return 1
        else:
            return 0


def validate_BDD(even, prime, rr):
    for u in range(0, 32):
        for v in range(0, 32):
            if check_prime(prime, u) == 0:
                continue
            else:
                ans = even_check(even, v) & bdd_check(rr, u, v)
                if ans == 0 & v == 31:
                    return False
    return True




def void_main():
    
    R = Edges()

    even_list = [val for val in range(0, 32) if val % 2 == 0]
    prime_list = [val for val in range(0, 32) if Prime(val)]

    
    prime = list(prime_list, 'y')
    even = list(even_list, 'x')

    
    RR = BDD(R)
    EVEN_BDD = expr2bdd(expr(even))
    PRIME_BDD = expr2bdd(expr(prime))
    

    
    RR2 = composed(RR, RR)

    
    RR2star = closure(RR2)

    


    print("1 -> True | 0 -> False")
    print("{}".format(bdd_check(RR, 27, 3)) + " -> RR(27, 3)")
    print("{}".format(bdd_check(RR, 16, 20)) + "-> RR(16, 20)")
    print("{}".format(even_check(EVEN_BDD, 14)) + "-> EVEN(14)")
    print("{}".format(even_check(EVEN_BDD, 13)) + "-> EVEN(13)")
    print("{}".format(check_prime(PRIME_BDD, 7)) + "-> PRIME(7)")
    print("{}".format(check_prime(PRIME_BDD, 2)) + "-> PRIME(2)")
    print("{}".format(bdd_check(RR2, 27, 6)) + "-> RR2(27, 6)")
    print("{}".format(bdd_check(RR2, 27, 9)) + "-> RR2(27, 9)")
    print("{}".format(validate_BDD(EVEN_BDD, PRIME_BDD, RR2star)) + " is validation for statement a.")

if __name__ == '__main__':
    void_main()
