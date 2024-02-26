import sympy

def user_input():
    prime = int(input("What prime modulus are we working with? \n"))
    while not (sympy.isprime(prime)):
        prime = int(input(str(prime) + " is not a prime. What prime modulus are we working with? \n"))
    power = int(input("What prime power are we lifting from?"))
    degree = int(input("What degree polynomial is this? \n"))
    coefficients = []
    for i in range(degree, -1, -1):
        coefficients.insert(0, int(input("Enter the coefficient of x^"+str(i)+ " as an integer. \n")))
    #print (str(coefficients))
    # ans = int(input("Enter the root of the original solution you would like to lift \n"))
    # (is_ans, ret_val, x) = check_root(ans, coefficients, (prime**power))
    # while not is_ans:
    #     print (str(ans) + " is not a root, its output mod "+str(prime**power)+ " is: "+str(ret_val))
    #     ans = int(input("Enter the root of the original solution you would like to lift \n"))
    #     (is_ans, ret_val, x) = check_root(ans, coefficients, (prime**power))
    ans = find_sols(coefficients, prime**power)
    print("Solutions to ", end='')
    print_eq(coefficients)
    print(" are: "+str(ans))
    return (prime, coefficients, ans, power)

def find_sols(coefficients, mod):
    answers = []
    for i in range(0, mod):
        if check_root(i, coefficients, mod)[0]:
            answers.append(i)
    if len(answers) == 0:
        print("No solutions to ", end='')
        print_eq(coefficients)
    return answers

def print_eq(coefficients):
    strout = ""
    if coefficients[0] != 0:
        strout = str(coefficients[0])
    for i in range(1, len(coefficients)):
        if coefficients[i]!=0:
            strout = strout + " + " +(str(coefficients[i]))+"x^"+str(i) + " "
    print(strout, end='')

def check_root(ans, coefficients, mod):
    res = eval_eq(ans, coefficients)
    res_mod = res%mod
    return res_mod==0, res_mod, res

def eval_eq(ans, coefficients):
    ret_ans = 0
    for i in range(len(coefficients)-1, -1, -1):
        ret_ans+= (ans**i)*coefficients[i]
    return ret_ans

def mod_inverse(val, prime):
    for i in range(0, prime, 1):
        if (val*i)%prime == 1:
            return i
    raise Exception("No modular inverse to "+str(val)+" mod "+str(prime))

def apply_lemma(prime, coefficients, ans, power):
    print("Finding lift of "+str(ans)+" from mod "+str(prime**power)+" to mod "+str(prime**(power+1)))
    deriv = []
    for i in range(len(coefficients)-1, 0, -1):
        deriv.insert(0, (coefficients[i]*i)%prime)
    (is_root, mod_ans, deriv_ans) = check_root(ans, deriv, prime)
    if is_root:
        print("f'("+str(ans)+"=0, so either no such lift exists or all possible lifts are solutions.")
        if(check_root(ans, coefficients, (prime**(power+1)))[0]):
            print("All lifts are solutions")
            cur_sols = []
            for i in range(0, prime**(power+1), prime**power):
                cur_sols.append(i+ans)
            print("Lifts are: "+str(cur_sols))
        else:
            print("No lifts are solutions")
    else:
        t_1 = -1*(mod_inverse(deriv_ans, prime))
        t_2 = (eval_eq(ans, coefficients))/(prime**power)
        t = (t_1*t_2)%prime
        lift = ans + t*(prime**power)
        print("t is: "+str(t)+", lift is: "+str(lift)+", so "+str(lift)+" = 0 mod "+str(prime**(power+1)))
    lift_again = input("Would you like to lift again? Type yes if so or anything else if not \n")
    if(lift_again.lower() == "yes"):
        apply_lemma(prime, coefficients, lift, power+1)
        #print(str(check_root(lift, coefficients, (prime**(power+1)))))

def main():
    (prime, coefficients, ans_arr, power) = user_input()
    for ans in ans_arr:
        apply_lemma(prime, coefficients, ans, power)


#(prime, coefficients, ans, power) = user_input()
#apply_lemma(prime, coefficients, ans, power)

#print(str(eval_eq(4, [87,1,0,1])))
#print(str(check_root(4, [87,1,0,1], 25)))
#print(str(apply_lemma(2, [0,0,-1,1], 1, 3)))
#print_eq([45, 0, 0, 3, 2])
#print(str(find_sols([0,0,-1,1], 4)))
main()