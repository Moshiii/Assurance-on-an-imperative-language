import z3
## See https://en.wikipedia.org/wiki/Verbal_arithmetic
## cute: http://mathforum.org/library/drmath/view/60417.html

vars = dict()
def _mk_int_var (x):
    if x not in vars:
        vars[x] = z3.Int (str(x))
    return vars[x]

def mk_var (x):
    return _mk_int_var (x)

def get_vars ():
    return vars.values ()


def solve (s1, s2, s3):
    global vars
    vars = dict()
    list1=list(s1)   #list=[s,e,n,d]
    list2=list(s2)
    list3=list(s3)
    #initial list in z3
    for i in list1:
        mk_var(i)
        
    for i in list2:
        mk_var(i)

    for i in list3:
        mk_var(i)
    #equation
    lhs1=reduce(lambda a,b: 10*a+vars[b], list1, 0)
    lhs2=reduce(lambda a,b: 10*a+vars[b], list2, 0)
    rhs1=reduce(lambda a,b: 10*a+vars[b], list3, 0)
  
    solver=z3.Solver()
    #distinct
    solver.add(z3.Distinct(get_vars()))
    #equation
    solver.add(lhs1+lhs2==rhs1)
    solver.add(vars[list1[0]] != 0)
    solver.add(vars[list2[0]] != 0)
    solver.add(vars[list3[0]] != 0)
    #digital range
    for x in vars:
        solver.add(vars[x]>=z3.IntVal(0))
        solver.add(vars[x]<=z3.IntVal(9))


    res=solver.check()
    if res ==z3.sat :
        model=solver.model()

        result=[]
        result.append(int(reduce(lambda a,b : "%s%s" % (a,model[vars[b]]), list1, '')))
        result.append(int(reduce(lambda a,b : "%s%s" % (a,model[vars[b]]), list2, '')))  
        result.append(int(reduce(lambda a,b : "%s%s" % (a,model[vars[b]]), list3, '')))

        return result
    else:
        return None


def print_sum (s1, s2, s3):
    s1 = str(s1)
    s2 = str(s2)
    s3 = str(s3)
    print s1.rjust (len(s3) + 1)
    print '+'
    print s2.rjust (len(s3) + 1)
    print ' ' + ('-'*(len(s3)))
    print s3.rjust (len(s3) + 1)
    
def puzzle (s1, s2, s3):
    print_sum (s1, s2, s3)
    res = solve (s1, s2, s3)
    if res is None:
        print 'No solution'
    else:
        print 'Solution:'
        print_sum (res[0], res[1], res[2])
        
if __name__ == '__main__':
    puzzle ('SEND', 'MORE', 'MONEY')
    puzzle ('SEND', 'ORRE', 'MONEY')
    puzzle ('PLAYS', 'WELL', 'BETTER')
    puzzle ('CRACK', 'HACK', 'ERROR')