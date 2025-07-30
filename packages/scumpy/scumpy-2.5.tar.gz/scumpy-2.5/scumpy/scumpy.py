from sympy import *
from sympy.abc import x, Y

def MatrixOps(num:int, __MatrixName1__: str, __MatrixName2__: str, OPS: list[str]) -> str:
  if 'kron' in OPS:
    return [f'''
__ResultName1__ = {__MatrixName1__}*transpose({__MatrixName2__})
__ResultName2__ = transpose({__MatrixName1__})*{__MatrixName2__}
__ResultName3__ = kronecker_product(__ResultName1__, __ResultName2__)
print(trace(__ResultName1__))
print(trace(__ResultName3__))'''][num-1]
  else:
    return [f'''
__ResultName1__ = {__MatrixName1__}*transpose({__MatrixName2__})
__ResultName2__ = transpose({__MatrixName1__})*{__MatrixName2__}
print(max(__ResultName1__))
print(sum(__ResultName2__))'''][num-1]
  
def MatrixEquations(num: int, name1: str, name2: str, name3: str = None) -> str:
  if name3!=None:
    return [f'''
pretty_print({name1}.inv()*{name3}*({name2}.inv()))'''][num-1]
  else:
    return [f'''
Если у вас вид: AX=B, то код: pretty_print({name1}.inv()*{name2})
Если же вид: XA=B, то код: pretty_print({name2}*({name1}.inv()))'''][num-1]
    
def Deter(num:int, name1: str, name2: str = None) -> str:
  if name2!=None:
    return [f'''
name3={name1}*{name2}
__equationName__ = Eq(det(name3), 0)
VarName=solve(__equationName__)
В оформлении задания на бумаге самостоятельно найдите, линейной комбинацией 
каких строк/столбцов является столбец/строка с параметром'''][num-1]
  else:
    return [f'''
pretty_print(det({name1}))
'''][num-1]
    
def Permute(num: int, permName: str, index: int, btrace: int) -> str:

  return [f'''
# первое решение\n
name=Matrix([])
for i in {permName}:
  name=name.hstack(name, Matrix([0 if k+1!=i else 1 for k in range(len({permName}))]))
  
print(trace(name**{index}))
  
for varName in range(1, 100):
  if trace(name**varName) == {btrace}:
    print(varName)
    break
''',
          
f'''
# второе решение\n  
A=zeros(len({permName}))
for i in range(len({permName})):
    A[{permName}[i]-1,i]=1
print(trace(A**{index}))
m=1
while trace(A**m)!={btrace}:
  m+=1
print(m)
  '''][num-1]
    
def BigMatrices(num: int, order: int, diagstart: float, diagend: float, a12: float = None, a21: float = None, row1end: float = None) -> str:
  if row1end!=None:
    return [f'''
# Первое решение:\n   

VarName1={order} 
Name1={diagstart}
Name2={diagend}
Name3={row1end}

VarName2=(Name3-Name1)/(VarName1-1)
VarName3=(Name2/Name1)**(1/(VarName1-1))

diagonListName=[Name1*(VarName3**i) for i in range(VarName1)]
rowListName=[Name1 + VarName2*i for i in range(VarName1)]

inversed_diagListName=[1/i for i in diagonListName]
inversed_rowListName=[-i/(k*Name1) for i, k in zip(rowListName, diagonListName)]
print(sum(inversed_diagListName)+sum(inversed_rowListName[1:]))
print(min([min(inversed_diagListName), min(inversed_rowListName)]))
''',

f'''
a11 = {diagstart}
a1n = {row1end}
vsego_symbols = {order}
ann = {diagend}
q = solve(ann / x ** vsego_symbols - 1, x, minimal=True)
d = (a1n - a11) / vsego_symbols
spis_stroki = [1]
spis_diag = [1]
for i in range(vsego_symbols-1):
    spis_stroki.append(spis_stroki[-1] + d)
    spis_diag.append(spis_diag[-1] * q)

spis_stroki_B = [1]
spis_diag_B = [1]
for i in range(vsego_symbols-1):
    spis_diag_B.append(1 / spis_diag[1:][i])
    spis_stroki_B.append(-spis_stroki[1:][i] / spis_diag[1:][i])

print(round(min(min(spis_stroki_B), min(spis_diag_B)), 3), round(sum(spis_diag_B) + sum(spis_stroki_B) - 1, 3))'''][num-1]
  else:
    return [f'''
# Первое решение:\n 
            
VarName1={order}
Name2={diagstart}
name3={diagend}
d=(name3-Name2)/(VarName1-1)
listName=[Name2]
for i in range(VarName1-1):
  listName.append(listName[-1]+d)
listName=listName[2:]

VarName2=1
for i in listName:
  VarName2*=i
MatrixName=Matrix([[Name2, {a12}], [{a21}, Name2+d]])
VarName3=det(MatrixName)*VarName2

listName2=[1/i for i in listName]
MatrixName2=MatrixName.inv()

print(VarName3, trace(MatrixName2)+sum(listName2))
''',

f'''
# Второе решение:\n


dlina = {order}
a11 = {diagstart}
ann = {diagend}
a12 = {a12}
a21 = {a21}

spisochek = [i / (dlina - 1) * (ann - a11) + a11 for i in range(dlina)]
diagonal = spisochek[0] * spisochek[1] - a12 * a21
sled = (spisochek[0] + spisochek[1]) / diagonal
for i in spisochek[2:]:
  diagonal *= i
  sled += 1 / i
  
  
print(round(diagonal,3))
print(round(sled,3))
'''][num-1]
    
    
def MatrixRows(num: int, StarterMatrixName: str, symb: float, sm: int, sn: int, bm: int, lesserThan: float) -> str:
  return [f'''
# Первое решение:\n
  
__MatrixName__={symb}*{StarterMatrixName}

def FunctionName1(VarName1, VarName2):
  MatrixName1=zeros(2)
  for i in range(VarName1, VarName2+1):
      MatrixName1+=__MatrixName__**i
  return MatrixName1
    
def FunctionName2(VarName3):
  return (eye(2)-__MatrixName__).inv() * __MatrixName__**VarName3

for k in range(300):
  if max(FunctionName2(k))<{lesserThan}:
    print(k)
    break
print(max(FunctionName1({sm}, {sn})), max(FunctionName2({bm})))


''',
f'''
# Второе решение:\n
A={symb}*{StarterMatrixName}

def s(m,n):
  S = zeros(2)
  for i in range(m, n + 1):
    S += A**i
  return S
  
def b(m):
    B = ((eye(2) - A).inv()) * (A**m)
    return B
  
print(max(s({sm}, {sn})))
print(max(b({bm})))


for i in range(500):
    if max(b(i)) < {lesserThan}:
        print(i)
        break
'''][num-1]


def arifm_and_geom_matrix_progression(n: int, a11: float, a1n: float, ann: float):
  f'''
a11 = {a11}
a1n = {a1n}
vsego_symbols = {n}
ann = {ann}
q = solve(ann / x ** vsego_symbols - 1, x, minimal=True)
d = (a1n - a11) / vsego_symbols
spis_stroki = [1]
spis_diag = [1]
for i in range(vsego_symbols-1):
    spis_stroki.append(spis_stroki[-1] + d)
    spis_diag.append(spis_diag[-1] * q)

spis_stroki_B = [1]
spis_diag_B = [1]
for i in range(vsego_symbols-1):
    spis_diag_B.append(1 / spis_diag[1:][i])
    spis_stroki_B.append(-spis_stroki[1:][i] / spis_diag[1:][i])

print(round(min(min(spis_stroki_B), min(spis_diag_B)), 3), round(sum(spis_diag_B) + sum(spis_stroki_B) - 1, 3))'''

def arrayy(st: str) -> None:
  if st.lower() in '''
  решите систему уравнений В ответе укажите найденные значения неизвестных. 1) значение 2) значение 3) значение
  найдите значения переменных x,y,z,u,v,w, удовлетворяющие условиям в ответе укажите найденные значения: 1) значение ; 2) значение 
  пусть (x,y,z,u) – решение системы уравнений объясните, почему y можно представить как функцию от x вида y=a+bx, где a,b – константы, зависящие только от коэффициентов исходной системы уравнений. найдите: 1) константу a; 2) константу b
  ''':
    print('gaussian_elim(num: int = [1], __MatrixName__: str) - задания на процедуру Гаусса')
    
  elif st.lower() in '''
  найдите количество решений следующей системы уравнений при различных значениях параметра a в ответе укажите: 1) значение параметра a, при котором система имеет бесконечное число решений
  найдите количество решений следующей системы уравнений при различных значениях параметра a в ответе укажите: 1) значение параметра a, при котором система имеет единственное решение.
  ''':
    print('gaussian_elim_parameters(num: int = [1], __MatrixName__: str) - процедура Гаусса с параметрами')
  elif st.lower() in '''
  даны матрицы: произведение кронекера. найдите: 1) след матрицы c; 2) след матрицы d 
  даны матрицы: найдите: 1) максимум элементов матрицы c; 2) сумму элементов матрицы d
  ''':
    print('MatrixOps(num: int = [1], __MatrixName1__: str, __MatrixName2__: str, OPS: list["kron", если есть кронекер]) - произведение матриц, кронекера')
  elif st.lower() in '''
  даны матрицы: найдите матрицу x из уравнения axb=c. в ответе укажите: 1) след матрицы x; 2) сумму элементов матрицы x
  даны матрицы: Найдите матрицу x из уравнения ax=b. в ответе укажите: 1) наибольший элемент матрицы x; 2) сумму элементов матрицы x.
  ''':
    print('MatrixEquations(num: int = [1], name1: str, name2: str, name3: str = None) - матричные уравнения')
  elif st.lower() in '''
  даны матрицы: при каком t матрица c содержит столбец, являющийся линейной комбинацией других столбцов? 
  даны матрицы: запишите определитель матрицы m в виде многочлена ax2+bx+c. в ответе укажите: 1) значение коэффициента a; 2) значение коэффициента b.
  ''':
    print('Deter(num: int = [1], name1: str, name2: str = None) - задания про определитель')
  elif st.lower() in '''
  для каждого k обозначим ek вектор-столбец размерности n, такой, что его элемент с номером k равен 1, а все остальные элементы равны 0. Пусть σ:{1,…,n}→{1,…,n} некоторая перестановка первых n натуральных чисел. Матрица a однозначно определяется условиями: aek=eσ (k),k=1,…,n. Известно, что n= и результатом применения σ к последовательности будет следующий ряд чисел: Найдите: 1) след матрицы a6; 2) наименьшее натуральное m, такое, что след матрицы am равен
  ''':
    print('Permute(num: int = [1, 2], permName: str, index: int, btrace: int) - перестановки')
  elif st.lower() in '''
  матрица имеет размер n×n, где n=. известно, что ее диагональные элементы образуют арифметическую прогрессию с начальным элементом a1,1= и конечным элементом an,n=. Также известно, что все элементы матрицы a, расположенные вне главной диагонали, равны нулю за исключением двух элементов: a1,2= и a2,1=. Найдите: 1) определитель матрицы a; 2) след матрицы, обратной к a.
  матрица имеет размер n×n, где n=. известно, что: 1) диагональные элементы образуют геометрическую прогрессию с начальным элементом a1,1= и конечным элементом an,n=; 2) элементы первой строки образуют арифметическую прогрессию с конечным элементом a1,n=; 3) все элементы матрицы a, расположенные вне главной диагонали и вне первой строки, равны нулю. найдите обратную матрицу b=a−1 и укажите в ответе: 1) наименьший элемент матрицы b; 2) сумму элементов матрицы b.
  ''':
    print('BigMatrices(num: int = [1, 2], order: int, diagstart: float, diagend: float, a12: float = None, a21: float = None, row1end: float = None) - большие матрицы')
  elif st.lower() in '''
  даны матрицы: i= , a=, где y=. Пусть sm,n=∑ni=mai,bm=(i-a)-1am. 1) найдите наибольший элемент матрицы s=s3,90. 2) найдите наибольший элемент матрицы b=b3. 3) найдите наименьшее k, такое, что при любом n>k наибольший элемент матрицы sk,n меньше
  ''':
    print('MatrixRows(num: int = [1, 2], StarterMatrixName: str, symb: float, sm: int, sn: int, bm: int, lesserThan: float) - матричные ряды')
  elif st.lower() in '''
  пусть комплексный корень из 1 степени, такой, что его мнимая часть больше 0, а действительная часть максимальна среди подобных корней с положительной мнимой частью. даны матрицы: i=, a=. найдите определитель матрицы a+λi и укажите в ответе: 1) действительную часть этого определитля; 2) его мнимую часть
  ''':
    print('ComplexNumbers(num: int = [1, 2], index: int, MatrixName: Matrix) - комплексные числа')
  elif st.lower() in '''
  для многочлена p(x) найдите все его 11 корней: z1,…,z11∈c. в ответе укажите: 1) сумму модулей |z1|+…+|z11|; 2) действительную часть корня, у которого эта действительная часть максимальна.
  ''':
    print('Polynomials(num: int = [1], pol: any (полином вида: 2*x**11 - x**9 ...)) - многочлены')
    
  elif st.lower() in '''
  дана матрица: a=. пусть z - собственное значение матрицы a с наибольшей мнимой частью. найдите z и соответствующий этому собственному значению собственный вектор x, первая координата которого равна 1, x=(1,u,v). в ответе укажите: 1) мнимую часть z; 2) действительную часть u.
  ''':
    print('EigenValsAndVects(num: int = [1, 2], MatrixName:Matrix) - собственные значения + векторы')
    
  elif st.lower() in '''
  на двумерной координатной плоскости заданы точки: a, b и c. пусть d(x,y) - ближайшая к a точка прямой bc. Найдите точку d и расстояние r от a до d. ккажите в ответе: 1) x, первую координату точки d; 2) y, вторую координату точки d; 3) r, расстояние от a до d.
  ''':
    print('Cartesian(num: int = [1, 2], Point1: list, Point2: list, Point3: list) - 2D геометрия')
  else:
    arrayy(input())

def ComplexNumbers(num:int, index: int, MatrixName: Matrix) -> str:
  return [f'''
# Первое решение \n  

VarName1=x**{index} -1
VarName2=nroots(VarName1)
ListName1=[i for i in VarName2 if im(i)>0]
NumberName1=max(ListName1, key=lambda x: re(x))
MatrixName1={MatrixName}
VarName3=det(MatrixName1+NumberName1*eye(2))
print(re(VarName3))
print(im(VarName3))
''',
f'''
# Второе решение \n

from math import cos, sin, pi
stepen_kornya = {index}
roots = []
lambdich = []
maxcosinus = 0
A = {MatrixName}
for i in range(stepen_kornya):
    cosinus = cos(2 * i * pi / stepen_kornya)
    sinus = sin(2 * i * pi / stepen_kornya)
    if sinus > 0 and cosinus > maxcosinus:
        maxcosinus = cosinus
        lambdich = [cosinus, sinus]
lambda_matrix = eye(2)
lambda_matrix *= complex(lambdich[0], lambdich[1])
print(round((lambda_matrix + A).det(), 3))
'''][num-1]


def Polynomials(num:int, pol: any) -> str:
  return [f'''
VarName1={pol}
VarName2=nroots(VarName1)
ListName1=[abs(i) for i in VarName2]
NumberName1=max(VarName2, key=lambda x: re(x))
print(sum(ListName1))
print(re(NumberName1))
'''][num-1]


def gaussian_elim(num:int, __MatrixName__: str) -> str:
  return [f'''
  pretty_print({__MatrixName__}.rref())
  '''][num-1]

def gaussian_elim_parameters(num:int, __MatrixName__: str) -> str:
  return [f'''pretty_print({__MatrixName__}.echelon_form())
Если Необходимо решить непростое уравнение в echelon_form - функция solve() поможет.
'''][num-1]


def EigenValsAndVects(num: int, MatrixName:Matrix) -> str:
  return [f'''
# Первое решение:\n
  
__MatrixName1__={MatrixName}
NumberName1=max(list(__MatrixName1__.eigenvals().keys()), key=lambda x: im(x)).n()
VectorName=Matrix([1, x, y])
EndMatrixName=(__MatrixName1__-NumberName1*eye(3))*VectorName
solutionName=solve([EndMatrixName[0], EndMatrixName[1]])
print(im(NumberName1))
print(re(solutionName[x]))
''',
f'''
# Второе решение:\n

A = {MatrixName}
lambda_values = A.charpoly()

Z = max(solve(lambda_values.args[0]), key=lambda x: im(x))

B = A - (Z * eye(3))
own_vector = [i.n() for i in B.nullspace()[0]]
need_to_mul = solve(own_vector[0] * x - 1, (x))[0]
new_vector_values = [simplify(i * need_to_mul) for i in own_vector]
new_vector_X = Matrix(3, 1, new_vector_values)


print(round(im(Z).n(), 3))
print(round(re(new_vector_X[1]), 3))
'''][num-1]


def Cartesian(num:int, Point1: list, Point2: list, Point3: list) -> str:
  return [f'''
# Первое решение:\n
  
PointName1=Matrix({Point1})
PointName2=Matrix({Point2})
PointName3=Matrix({Point3})
PointName4=Matrix([x, y])
LineName1=PointName3-PointName2
LineName2=PointName4-PointName1
VarName1, VarName2 = symbols('VarName1, VarName2')
__eqName1__=Eq(VarName1*PointName2[0] + VarName2, PointName2[1])
__eqName2__=Eq(VarName1*PointName3[0] + VarName2, PointName3[1])
solutionName1=solve([__eqName1__, __eqName2__])
__eqName3__=Eq(solutionName1[VarName1]*x + solutionName1[VarName2], y)
__eqName4__=Eq(LineName2.dot(LineName1), 0)
solutionName2=solve([__eqName3__, __eqName4__])
LineName2=LineName2.subs(solutionName2)
VarName3=(LineName2.dot(LineName2))**0.5
print(solutionName2[x].n())
print(solutionName2[y].n())
print(VarName3)
''',
f'''
# Второе решение:\n

A = {Point1}
B = {Point2}
C = {Point3}
urav_pryamoy_BC = ((x - B[0]) / (C[0] - B[0])) - ((y - B[1]) / (C[1] - B[1]))

tochka_x = A[0] + urav_pryamoy_BC.coeff(x) * t
tochka_y = A[1] + urav_pryamoy_BC.coeff(y) * t
t_numerical = solve(urav_pryamoy_BC.subs({{x:tochka_x, y:tochka_y}}))[0]
D = [tochka_x.subs({{t:t_numerical}}), tochka_y.subs({{t:t_numerical}})]
urav_pryamoy_BC.subs({{x:tochka_x, y:tochka_y}})

print(round(D[0], 3))
print(round(D[1], 3))
print(round(Point(A).distance(D), 3))
'''][num-1]


import pyperclip


def rv_discrete(snippet: str) -> None:
  if snippet in 'В группе региональных банков имеется банков, у которых нет проблем с выполнением нормативных показателей, и банков, у которых такие проблемы имеются. Для проверки случайным образом отобраны три банка. Найдите: 1) вероятность того, что в число отобранных банков попадет хотя бы один проблемный.' or snippet in 'Среди банков с относительно небольшим уровнем собственного капитала имеется банков, у которых все нормативные показатели удовлетворяют требованиям ЦБ, и банков, у которых имеются нарушения. Для проверки случайным образом отобраны три банка. Найдите: 1) вероятность P того, что в число отобранных банков попадет хотя бы один с нарушением требований.':
    A = '''
good_banks = 10
bad_banks = 13
banks_chosen_for_inspection = 3
ch = ['good']*good_banks + ['bad']*bad_banks
good=0
tot=0
for x in combinations(ch, r=banks_chosen_for_inspection):
  if x.count('bad')>0:
    good+=1
  tot+=1
  
good/tot
    '''
  elif snippet in 'Независимо друг от друга человека садятся в поезд, содержащий вагонов. 1) Найдите вероятность того, что по крайней мере двое из них окажутся в одном вагоне':
    A = '''
wagons = 13
people = 3
ch=list(range(1, wagons+1))
good=0
tot=0
for x in product(ch, repeat=people):
  if len(set(x))<people:
    good+=1
  tot+=1

good/tot
    '''
  elif snippet in 'Из первых натуральных чисел случайным образом выбираются числа. 1) Какова вероятность того, что по крайней мере два числа совпадут?':
    A = '''
max_number = 14
ch=list(range(1, max_number+1))
numbers_chosen = 3
good=0
tot=0
for x in product(ch, repeat=numbers_chosen):
  if len(set(x))<3:
    good+=1
  tot+=1

good/tot
    '''
  elif snippet in 'События A,B и C независимы, P(A)=; P(B)= и P(C)=. 1) Найдите вероятность события D=(A+B)(A+C)(B+C). 2) Найдите вероятность события D, если известно, что событие A уже наступило.':
    A = '''
A_Probability = 0.1
B_Probability = 0.4
C_Probability = 0.9
A = [True]*(10*A_Probability) + [False]*(10 - 10*A_Probability)
B = [True]*(10*B_Probability) + [False]*(10 - 10*B_Probability)
C = [True]*(10*C_Probability) + [False]*(10 - 10*C_Probability)
good=0
w_criterion = 0
tot=0
for x in product(A, B, C):
  if (x[0] | x[1]) & (x[0] | x[2]) & (x[1] | x[2]):
    good+=1
  if (x[0] | x[1]) & (x[0] | x[2]) & (x[1] | x[2]) & x[0]:
    w_criterion+=1
  tot+=1
good/tot, w_criterion/tot/(A.count(True)/10)
    '''
  elif snippet in 'События A,B и C независимы, P(A)=; P(B)= и P(C)=. 1) Найдите вероятность события D=(A+B¯)(B+C¯)(C+A¯). 2) Найдите вероятность события D, если известно, что событие A уже наступило.':
    A = '''
A_Probability = 0.1
B_Probability = 0.6
C_Probability = 0.9
A = [True]*(10*A_Probability) + [False]*(10 - 10*A_Probability)
B = [True]*(10*B_Probability) + [False]*(10 - 10*B_Probability)
C = [True]*(10*C_Probability) + [False]*(10 - 10*C_Probability)
good=0
w_criterion = 0
tot=0
for x in product(A, B, C):
  if (x[0] or not(x[1])) & (not(x[0]) or x[2]) & (x[1] or not(x[2])):
    good+=1
  if (x[0] or not(x[1])) & (not(x[0]) or x[2]) & (x[1] or not(x[2])) & x[0]:
    w_criterion+=1
  tot+=1
good/tot, w_criterion/tot/(A.count(True)/10)
    '''
  elif snippet in 'Имеется монет, из которых бракованные: вследствие заводского брака на этих монетах с обеих сторон отчеканен герб. Наугад выбранную монету, не разглядывая, бросают несколько раз. 1) Какова вероятность, что при бросках она ляжет гербом вверх? 2) При бросках монета легла гербом вверх. Какова вероятность того, что была выбрана монета с двумя гербами?':
    A = '''
A=0
times_thrown = 4
hypothesis = [6/37, 31/37]
dct={hypothesis[0]:1, hypothesis[1]:0.5}
for i in hypothesis:
  A+=i*dct[i]**times_thrown

BAY = hypothesis[0]*dct[hypothesis[0]]/A
A, BAY
    '''
  elif snippet in 'В первой корзине имеется шаров, при этом количество белых шаров равно либо, либо. Оба варианта равновероятны. Во второй корзине имеется шаров, а количество белых шаров равно, или . Эти три варианта также равновероятны. Из обеих корзин все шары перекладываются в третью корзину. 1) Какова вероятность P(A), что случайно вынутый из третьей корзины шар окажется белым (событие A)? 2) Найдите условную вероятность P(H|A), того, что случайно вынутый из третьей корзины шар первоначально находился в первой корзине (событие H), при условии, что он белый (событие A)?':
    A = '''
balls_in_basket_one = 7
balls_in_basket_two = 26
s = balls_in_basket_one + balls_in_basket_two
first = [2, 4]
second = [9, 11, 18]
A=0
for i in first:
  for k in second:
    A+=(i+k)/s * 1/len(first) * 1/len(second)

BAY = 0
for i in first:
  BAY += i/s * 1/len(first) / A
A, BAY
    '''
  elif snippet in 'Имеется две корзины с белыми и черными шарами. В первой корзине всего шаров, при этом количество белых шаров распределено по биномиальному закону с параметрами n и p. Во второй корзине имеется всего шаров, при этом количество белых шаров распределено по биномиальному закону с параметрами n и p. Из обеих корзин все шары перекладываются в третью корзину. 1) Какова вероятность P(A), что случайно вынутый из третьей корзины шар окажется белым (событие A)? 2) Найдите условную вероятность P(H|A), того, что случайно вынутый из третьей корзины шар первоначально находился в первой корзине (событие H), при условии, что он белый (событие A)?':
    A = '''
n1 = 5
n2 = 11
p1 = 0.3
p2 = 0.1
balls_in_first_basket = 13
balls_in_second_basket = 12
S = balls_in_first_basket + balls_in_second_basket
basket1 = binom(n1, p1)
basket2 = binom(n2, p2)
l3 = []
for i in range(n1+1):
  l3.append(basket1.pmf(i))


l4 = []
for i in range(n2+1):
  l4.append(basket2.pmf(i))  


sm=0
for i, val1 in enumerate(l4):
  for k, val2 in enumerate(l3):
    sm+=(i+k)/S * (val1*val2)

rev=0
for k, val2 in enumerate(l3):
  pA=sm
  pHk = val2
  pAHk = (k)/S
  rev+=(pHk*pAHk)/pA
sm, rev
    '''
  elif snippet in 'Имеется две корзины с белыми и черными шарами. В первой корзине количество белых –, количество черных –. Во второй корзине количество белых –, количество черных –. Из первой корзины случайно, без возвращения, излекаются шаров, а из второй – шаров. Отобранные из обеих корзин шары перекладываются в третью корзину. 1) Какова вероятность P(A), что случайно вынутый из третьей корзины шар окажется белым (событие A)? 2) Найдите условную вероятность P(H|A), того, что случайно вынутый из третьей корзины шар первоначально находился в первой корзине (событие H), при условии, что он белый (событие A)?':
    A = '''
black_first = 13
white_first = 12
black_second = 20
white_second = 17
taken_from_first = 8
taken_from_second = 11
S = taken_from_first + taken_from_second
First_sum = black_first + white_first
Second_sum = black_second + white_second
basket1 = binom(taken_from_first, white_first/First_sum)
basket2 = binom(taken_from_second, white_second/Second_sum)

sm=0

for i in range(taken_from_first+1):
  for k in range(taken_from_second+1):
    sm+=(i+k)/S * basket1.pmf(i) * basket2.pmf(k)

rev=0
for k in range(taken_from_first+1):
  pA=sm
  pHk = basket1.pmf(k)
  pAHk = (k)/S
  rev+=(pHk*pAHk)/pA
sm, rev
    '''
  elif snippet in 'Вероятность невозврата кредита равна. Банк выдал кредиты независимым заемщикам. Найдите: 1) наиболее вероятное число заемщиков, которые не вернут кредит' or snippet in 'Вероятность частичного возврата кредита равна. Банк выдал кредиты независимым заемщикам. Найдите: 1) наиболее вероятное число заемщиков, которые вернут кредит лишь частично.':
    A = '''
amount=46
probability = 1/8

probable = amount*probability - probability
probable
    '''
  elif snippet in 'Вероятность дефолта "мусорной" облигации равна. Биржевой игрок купил подобных облигаций, выпущенных независимыми компаниями. Найдите: 1) вероятность того, что среди купленных облигаций окажется менее трех дефолтных.' or snippet in 'Вероятность дефолта облигации, имещей аномально высокую доходность к погашению, равна. Биржевой игрок купил подобных облигаций, выпущенных независимыми компаниями. Найдите: 1) вероятность того, что среди купленных облигаций окажется менее трех дефолтных.':
    A = '''
amount = 5
probability = 0.4
less_then = 3

b = binom(amount, probability)
b.cdf(less_then-1)
    '''
  elif snippet in 'Банк совершил транзакций при ненадежной связи с сервером. Вероятность того, что транзакция будет ошибочной, равна. Используя приближенную формулу для числа успехов в схеме Бернулли, найдите вероятность того, что среди этих n транзакций имеется ошибочные транзакции (не больше и не меньше). В решении необходимо проверить условие применимости приближенной формулы.' or snippet in 'Банк совершил n транзакций по кредитным картам. Вероятность того, что транзакция будет ошибочной, равна. Используя приближенную формулу для числа успехов в схеме Бернулли, найдите вероятность того, что среди этих n транзакций имеется ошибочные транзакции (не больше и не меньше). В решении необходимо проверить условие применимости приближенной формулы.':
    A = '''
errors = 4
amount = 1000
probability = 0.001
dist = poisson(amount*probability)

p.pmf(errors)
    '''
  elif snippet in 'Банк совершил n транзакций по кредитным картам. Вероятность того, что транзакция будет ошибочной. Используя приближенную формулу для числа успехов в схеме Бернулли, найдите вероятность того, что среди этих n транзакций имеется не более ошибочных. В решении необходимо проверить условие применимости приближенной формулы.' or snippet in 'Банк совершил n транзакций при ненадежной связи с сервером. Вероятность того, что транзакция будет ошибочной, равна. Используя приближенную формулу для числа успехов в схеме Бернулли, найдите вероятность того, что среди этих n транзакций имеется не более ошибочных. В решении необходимо проверить условие применимости приближенной формулы.':
    A = '''
errors_or_lesser = 103
amount = 172000
probability = 0.00049
dist = poisson(amount*probability)

dist.cdf(errors_or_lesser)
    '''
  elif snippet in 'В прямоугольной области, заданной ограничениями |x| и |y|, случайным образом выбираются две точки: (x1,y1) и (x2,y2). Пусть A и B – события, состоящие в том, что: A – расстояние между выбранными точками меньше; B – модуль разности |x1−x2| меньше. Найдите приближенно, методом Монте-Карло: 1) вероятность P(A); 2) условную вероятность P(A|B). Указание: получите в заданной прямоугольной области 100000 пар точек и, используя все эти точки, найдите ответы, округляя их до одного знака после запятой.':
    A = '''
xabs = 20
yabs = 8


    
X = uniform(loc=-xabs, scale = xabs*2) 
Y = uniform(loc = -yabs, scale = yabs*2)
N = 100_000
good = 0
total = 0
good1=0
total1=0
good2=0
total2=0
for i in range(N+1):
    x = X.rvs(size=1)
    y = Y.rvs(size = 1)
    xt = X.rvs(size = 1)
    yt = Y.rvs(size=1)
    if ((x-xt)**2 + (y-yt)**2)**0.5 < 11:
        good+=2
    total+=2
    if abs(x - xt)<14:
        good1+=2
    total1+=2
    if abs(x - xt)<14 and ((x-xt)**2 + (y-yt)**2)**0.5 < 11:
        good2+=2
    total2+=2
pA = good/total
print(f' P(A) = {pA}')     

pB = good1/total1
print(f' P(B) = {pB}')

pAB = good2/total2
print(f' P(AB) = {pAB}')
pAatB = pAB/pB
print(f'P(A|B) = {pAatB}')
    '''
  elif snippet in 'В области, ограниченной эллипсом, случайным образом выбираются две точки. Пусть A и B – события, состоящие в том, что: A – расстояние между выбранными точками меньше; B – все координаты обеих точек. Найдите приближенно, методом Монте-Карло: 1) вероятность P(A); 2) условную вероятность P(A|B). Указание: получите внутри заданного эллипса 100000 пар точек и, используя все эти пары точек, найдите ответы, округляя их до одного знака после запятой.':
    A = '''
N = 400_000
def inside_ellipse(hrad: int, vrad: int, p: tuple) -> bool:
  return p[0]**2/hrad**2 + p[1]**2/vrad**2 <= 1
horizontal_radius = 14
vertical_radius = 6
good = 0
total = 0
good1=0
total1=0
good2=0
total2=0
X = uniform(loc=-horizontal_radius, scale=horizontal_radius*2)
Y = uniform(loc=-vertical_radius, scale = vertical_radius*2)

for i in range(N+1):
    x = X.rvs()
    y= Y.rvs()
    xt = X.rvs()
    yt = Y.rvs()
    if inside_ellipse(horizontal_radius, vertical_radius, (x, y)) and inside_ellipse(horizontal_radius, vertical_radius, (xt, yt)):
      if ((x-xt)**2 + (y-yt)**2)**0.5 < 8.7:
          good+=2
      total+=2
    if inside_ellipse(horizontal_radius, vertical_radius, (x, y)) and inside_ellipse(horizontal_radius, vertical_radius, (xt, yt)):
      if (x<0 and y<0) and (xt<0 and yt<0):
        good1+=2
      total1+=2
    if inside_ellipse(horizontal_radius, vertical_radius, (x, y)) and inside_ellipse(horizontal_radius, vertical_radius, (xt, yt)):
      if (x<0 and y<0) and (xt<0 and yt<0) and ((x-xt)**2 + (y-yt)**2)**0.5 < 8.7:
          good2+=2
      total2+=2
pA = good/total
print(f' P(A) = {pA}')

pB = good1/total1
print(f' P(B) = {pB} ')


pAB = good2/total2
print(f' P(AB) = {pAB}')

print(f'P(A|B) = {pAB/pB}')
    '''
    
  elif snippet in 'В кубе объема случайным образом выбираются точки A, B и C. Пусть R, S и T – события, состоящие в том, что: R – наименьший угол в треугольнике ABC меньше; S – наибольший угол в треугольнике ABC меньше; T– треугольник ABC остроугольный. Найдите приближенно, методом Монте-Карло: 1) условную вероятность P(R|T); 2) условную вероятность P(S|T). Указание: получите 100000 остроугольных треугольников ABC и, используя все эти треугольники, найдите ответы, округляя их до одного знака после запятой.':
    A = '''
from math import degrees, acos
 
def angle(d1, d2, d3):
    return degrees(acos((d2**2+d3**2-d1**2)/(2*d2*d3)))
cube_volume = 1
N = 200_000
good=0
total=0
good1=0
total1=0
good2=0
total2=0
dist = uniform(loc = 0, scale = cube_volume**(1/3))
for i in range(N+1):
    x = dist.rvs()
    y = dist.rvs()
    z = dist.rvs()
    x2 = dist.rvs()
    y2 = dist.rvs()
    z2 = dist.rvs()
    x3 = dist.rvs()
    y3 = dist.rvs()
    z3 = dist.rvs()
    leng1 = ((x-x2)**2 + (y-y2)**2 + (z-z2)**2)**0.5
    leng2 = ((x-x3)**2 + (y-y3)**2 + (z-z3)**2)**0.5
    leng3 = ((x2-x3)**2 + (y2-y3)**2 + (z2-z3)**2)**0.5
    angle1 = angle(leng1, leng2, leng3)
    angle2 = angle(leng2, leng1, leng3)
    angle3 = angle(leng3, leng2, leng1)
    if min(angle1, angle2, angle3)<26.7 and angle1<90 and angle2<90 and angle3<90:
        good+=3
    total+=3
    if angle1<90 and angle2<90 and angle3<90:
        good1+=3
    total1+=3
    if angle1<90 and angle2<90 and angle3<90 and max(angle1, angle2, angle3)<81.9:
        good2+=3
    total2+=3
pRT = good/total

pT = good1/total1
print(f'P(R|T) = {pRT/pT}')


pST = good2/total2
print(f'P(S|T) = {pST/pT}')
    '''
  elif snippet in '''В первом броске участвуют несимметричных монет. Во втором броске участвуют только те монеты, на которых в первом броске выпал "орел". Известно, что вероятность выпадения "орла" для данных несимметричных монет равна. Найдите: 1) математическое ожидание числа "орлов", выпавших во втором броске; 2) дисперсию условного математического ожидания числа "орлов", выпавших во втором броске, относительно числа "орлов", выпавших в первом броске''':
    A = '''
import numpy as np

results = {}

N = 160
p = 0.55

E = N * np.power(p, 2)
Var = N * np.power(p, 3) * (1 - p)
E_var = N * np.power(p, 2) * (1 - p)

print(f'Математическое ожидание числа "орлов", выпавших во втором броске: \n{E :.2f}')
print(f'Дисперсия условного математического ожидания числа "орлов": \n{Var :.3f}')
print(f'Математическое ожидание условной дисперсии числа "орлов": \n{E_var :.3f}')
    '''
  elif snippet in '''Средний ущерб от одного пожара составляет млн. руб. Предполагается, что ущерб распределен по показательному закону, а число пожаров за год - по закону Пуассона. Также известно, что за лет в среднем происходит пожаров. Найдите: 1) математическое ожидание суммарного ущерба от всех пожаров за один год; 2) стандартное отклонение суммарного ущерба от пожаров за год.''':
    A = '''
import numpy as np

mean_damage_per_fire = 2.1
years = 10
fires_in_years = 29
e_x = mean_damage_per_fire
var_x = np.power(e_x, 2)

lambda_poisson_yearly = fires_in_years / years
e_n = lambda_poisson_yearly
var_n = lambda_poisson_yearly

e_s = e_n * e_x
var_s = e_n * var_x + var_n * np.power(e_x, 2)
std_dev_s = np.sqrt(var_s)

print(f"Математическое ожидание суммарного ущерба: {e_s:.2f}")
print(f"Стандартное отклонение суммарного ущерба: {std_dev_s:.3f}")
    '''
  elif snippet in '''Максимальный ущерб от страхового случая составляет млн. руб. Предполагается, что фактический ущерб распределен равномерно от 0 до максимального ущерба, а число страховых случаев за год - по закону Пуассона. Также известно, что за лет в среднем происходит страховых случаев. Найдите: 1) математическое ожидание суммарного ущерба от всех страховых случаев за один год; 2) стандартное отклонение суммарного ущерба от страховых случаев за год.''':
    A = '''
import numpy as np

max_damage = 3.3
years = 10
claims_in_years = 12

a_uniform = 0
b_uniform = max_damage

e_x = (a_uniform + b_uniform) / 2
var_x = np.power((b_uniform - a_uniform), 2) / claims_in_years

lambda_poisson_yearly = claims_in_years / years
e_n = lambda_poisson_yearly
var_n = lambda_poisson_yearly

e_s = e_n * e_x
var_s = e_n * var_x + var_n * np.power(e_x, 2)
std_dev_s = np.sqrt(var_s)

print(f"Математическое ожидание суммарного ущерба: {e_s:.2f}")
print(f"Стандартное отклонение суммарного ущерба: {std_dev_s:.3f}") 
    '''

  elif snippet in '''Для случайной цены Y известны вероятности:. При условии, что Y=y, распределение выручки X является равномерным на отрезке. Найдите: 1) математическое ожидание E(XY); 2) ковариацию Cov(X,Y).''':
    A = '''
import numpy as np

y_values = np.array([9, 14])
y_probabilities = np.array([0.7, 0.3])
 uniform_upper_bound_factor = 14

E_Y = np.sum(y_values * y_probabilities)
E_Y_squared = np.sum(np.power(y_values, 2) * y_probabilities)

E_X = (uniform_upper_bound_factor / 2) * E_Y
E_XY = (uniform_upper_bound_factor / 2) * E_Y_squared

Cov_XY = E_XY - (E_X * E_Y)

print(f"E(Y) = {E_Y}")
print(f"E(Y^2) = {E_Y_squared}")
print(f"E(X) = {E_X}\n")

print(f"1) E(XY) = {E_XY:.2f}")
print(f"2) Cov(X,Y) = {Cov_XY:.3f}")
    '''

  elif snippet in '''Игральная кость и монет подбрасываются до тех пор, пока в очередном броске не выпадет ровно "орлов". Пусть S – суммарное число очков, выпавших на игральной кости при всех бросках. Найдите:  1) математическое ожидание E(S); 2) стандартное отклонение σS.''':
    A = '''
import numpy as np
from scipy.special import comb

num_coins = 29
target_heads = 8
prob_head_single_coin = 0.5

E_D_i = (1 + 2 + 3 + 4 + 5 + 6) / 6
E_D_i_sq = (1**2 + 2**2 + 3**2 + 4**2 + 5**2 + 6**2) / 6
Var_D_i = E_D_i_sq - (E_D_i)**2

p_success_trial = comb(num_coins, target_heads, exact=True) * \
              (prob_head_single_coin**target_heads) * \
              ((1 - prob_head_single_coin)**(num_coins - target_heads))

E_K = 1 / p_success_trial
Var_K = (1 - p_success_trial) / (p_success_trial**2)
E_S = E_K * E_D_i

Var_S = E_K * Var_D_i + (E_D_i**2) * Var_K
sigma_S = np.sqrt(Var_S)

print(f"1) E[S]: {E_S:.3f}")
print(f"2) sigma_S: {sigma_S:.3f}")
    '''
    
  elif snippet in "Распределение дискретного случайного вектора (X,Y) имеет вид: Найдите: 1) вероятность P1; 2) вероятность P2; 3) условное математическое ожидание E3; 4) условное математическое ожидание E4=E(X|Y=11); 5) математическое ожидание E5=E(E(X|Y)).":
    A = '''
import numpy as np

x_values = np.array([1, 5, 6])
y_values = np.array([9, 10])

joint_pmf = np.array([
    [0.19, 0.04, 0.34],
    [0.19, 0.09, 0.15]
]).T

P1 = np.sum(joint_pmf[:, 0])
P2 = np.sum(joint_pmf[:, 1])

pmf_X_given_Y7 = joint_pmf[:, 0] / P1
E3 = np.sum(x_values * pmf_X_given_Y7)

pmf_X_given_Y11 = joint_pmf[:, 1] / P2
E4 = np.sum(x_values * pmf_X_given_Y11)

E5 = E3 * P1 + E4 * P2

print(f"P1 = P(Y={y_values[0]}) = {P1:.2f}")
print(f"P2 = P(Y={y_values[1]}) = {P2:.2f}")
print(f"E3 = E(X|Y={y_values[0]}) = {E3:.3f}")
print(f"E4 = E(X|Y={y_values[1]}) = {E4:.3f}")
print(f"E5 = E(E(X|Y)) = {E5:.2f}")
    '''
  elif snippet in 'Абсолютно непрерывная случайная величина X может принимать значения только в отрезке. На этом отрезке плотность распределения случайной величины X имеет вид: f(x), где C – положительная константа. Найдите: 1) константу C; 2) математическое ожидание E(X); 3) стандартное отклонение σX; 4) квантиль уровня распределения X.':
    A = '''
f = lambda x: (1+7*x**0.5+8*x**0.7+4*x**0.9)**1.3
length = [4,9]
quantile = 0.9

C = 1/ quad(f, length[0], length[1])[0]

class Custom(rv_continuous):
  def _pdf(self, x):
    return C*(1+7*x**0.5+8*x**0.7+4*x**0.9)**1.3

custom = Custom(a = length[0], b = length[1])
print(f'C = {C:.5f}')
print(f'E(X) = {custom.expect():.3f}')
print(f'Std(X) = {custom.std():.3f}')
print(f'Quantile = {float(custom.ppf(quantile)):.3f}')       
    '''
  elif snippet in 'Случайная величина X равномерно распределена на отрезке. Случайная величина Y выражается через X следующим образом: Y. Найдите: 1) математическое ожидание E(Y); 2) стандартное отклонение σY; 3) асимметрию As(Y); 4) квантиль уровня 0,9распределения Y.':
    A = '''
from scipy.integrate import quad
from scipy.stats import uniform

a, b = 4, 7
quantile = 0.9
def base_function(x):
    return 1 + 3*x**0.5 + 4*x**0.7 + 9*x**0.9


Y = lambda x: base_function(x)**1.1
EY = (1/(b-a)) * quad(Y, a, b)[0]

fV2 = lambda x: Y(x)**2
VarY = (1/(b-a)) * quad(fV2, a, b)[0] - EY**2
stdY = VarY**0.5

fV3 = lambda x: Y(x)**3
v3 = (1/(b-a)) * quad(fV3, a, b)[0]
v2 = (1/(b-a)) * quad(fV2, a, b)[0]
CM = v3 - 3*EY*v2 + 2*EY**3

X = uniform(loc=a, scale=b-a)

print(f'E(Y) = {EY:.1f}')
print(f'Std(Y) = {stdY:.2f}')
print(f'Moment of Skewness = {CM/stdY**3:.4f}')
print(f'Quantile = {Y(X.ppf(0.9)):.3f}')        
    '''
  elif snippet in 'Распределение дискретного случайного вектора (X,Y) имеет вид: Найдите: 1) математическое ожидание E(X); 2) дисперсию Var(X); 3) математическое ожидание E(Y); 4) дисперсию Var(Y); 5) коэффициент корреляции ρ(X,Y).' \
        or snippet in 'Дано совместное распределение дискретных случайных величин X и Y: Найдите: 1) математическое ожидание E(X); 2) дисперсию Var(X); 3) математическое ожидание E(Y); 4) дисперсию Var(Y); 5) коэффициент корреляции ρ(X,Y).'\
        or snippet in 'Распределение дискретного случайного вектора (X,Y) имеет вид: Найдите: 1) математическое ожидание E(X); 2) дисперсию Var(X); 3) математическое ожидание E(XY); 4) ковариацию Cov(X,Y); 5) коэффициент корреляции ρ(X,Y).'\
        or snippet in 'Дано совместное распределение дискретных случайных величин X и Y: Найдите: 1) математическое ожидание E(X); 2) дисперсию Var(X); 3) математическое ожидание E(XY); 4) ковариацию Cov(X,Y); 5) коэффициент корреляции ρ(X,Y).'\
        or snippet in 'Распределение дискретного случайного вектора (X,Y) имеет вид: Найдите: 1) математическое ожидание E(X); 2) стандартное отклонение σ(X); 3) стандартное отклонение σ(Y); 4) ковариацию Cov(X,Y); 5) коэффициент корреляции ρ(X,Y).'\
        or snippet in 'Дано совместное распределение дискретных случайных величин X и Y: Найдите: 1) математическое ожидание E(X); 2) стандартное отклонение σ(X); 3) стандартное отклонение σ(Y); 4) ковариацию Cov(X,Y); 5) коэффициент корреляции ρ(X,Y).':
    A = '''
dct = {1:(1, 4), 2:(2, 4), 3:(3, 4), 
       4:(1, 8), 5:(2, 8), 6:(3, 8)}

probabilities = [0.05, 0.43, 0.24, 
                 0.19, 0.01, 0.08]

XandY = rv_discrete(values=(list(dct.keys()), probabilities))

X_dct = defaultdict(int)
for i in dct.keys():
  X_dct[dct[i][0]] += XandY.pmf(i)
  
X = rv_discrete(values=(list(X_dct.keys()), list(X_dct.values())))

Y_dct = defaultdict(int)
for i in dct.keys():
  Y_dct[dct[i][1]] += XandY.pmf(i)

Y = rv_discrete(values=(list(Y_dct.keys()), list(Y_dct.values())))

XY_dict = defaultdict(int)
for i in dct.keys():
  XY_dict[dct[i][0]*dct[i][1]] += XandY.pmf(i)
  
XY = rv_discrete(values=(list(XY_dict.keys()), list(XY_dict.values())))

EX = X.expect()
VarX = X.var()
EY = Y.expect()
VarY = Y.var()
EXY = XY.expect()
Cov_X_Y = (EXY - EX*EY)
corr_X_Y = Cov_X_Y/(X.std()*Y.std())

print(f'Expectation of X = {EX}')
print(f'Expectation of Y = {EY}')
print(f'Variance of X = {VarX}')
print(f'Variance of Y = {VarY}')
print(f'Std of X = {X.std()}')
print(f'Std of Y = {Y.std()}')
print(f'Covariance of X and Y = {Cov_X_Y}')
print(f'Expectation of XY = {EXY}')
print(f'Correlation coeff of X and Y = {corr_X_Y}')
    '''
  elif snippet in 'Распределение дискретного случайного вектора (X,Y) имеет вид: Найдите: 1) математическое ожидание E(X2); 2) стандартное отклонение σ(X2); 3) стандартное отклонение σ(Y2); 4) ковариацию Cov(X2,Y2); 5) коэффициент корреляции ρ(X2,Y2).'\
      or snippet in 'Дано совместное распределение дискретных случайных величин X и Y: Найдите: 1) математическое ожидание E(X2); 2) стандартное отклонение σ(X2); 3) стандартное отклонение σ(Y2); 4) ковариацию Cov(X2,Y2); 5) коэффициент корреляции ρ(X2,Y2).':
    A = '''
dct = {1:(2, 10), 2:(6, 10), 3:(8, 10), 
       4:(2, 11), 5:(6, 11), 6:(8, 11)}

probabilities = [0.17, 0.25, 0.26, 
                 0.11, 0.12, 0.09]


XandY = rv_discrete(values=(list(dct.keys()), probabilities))

X2_dct = defaultdict(int)
for i in dct.keys():
  X2_dct[dct[i][0]**2] += XandY.pmf(i) 
X2 = rv_discrete(values=(list(X2_dct.keys()), list(X2_dct.values())))


Y2_dct = defaultdict(int)
for i in dct.keys():
  Y2_dct[dct[i][1]**2] += XandY.pmf(i)
Y2 = rv_discrete(values=(list(Y2_dct.keys()), list(Y2_dct.values())))

X2Y2_dict = defaultdict(int)
for i in dct.keys():
  X2Y2_dict[dct[i][0]**2 * dct[i][1]**2] += XandY.pmf(i)  
X2Y2 = rv_discrete(values=(list(X2Y2_dict.keys()), list(X2Y2_dict.values())))

Cov_X2_Y2 = X2Y2.expect() - X2.expect() * Y2.expect()

corr_X2_Y2 = Cov_X2_Y2 / (X2.std()*Y2.std())

print(f'E(X^2) = {X2.expect()}')
print(f'Std(X^2) = {X2.std()}')
print(f'Std(Y^2) = {Y2.std()}')
print(f'Cov(X^2, Y^2) = {Cov_X2_Y2}')
print(f'Correlation Coeff of X^2, Y^2 = {corr_X2_Y2}')
    '''
  elif snippet in 'Распределение дискретного случайного вектора (X,Y) имеет вид: Найдите: 1) математическое ожидание E(X2); 2) математическое ожидание E(X4); 3) дисперсию Var(X2); 4) математическое ожидание E(X2Y); 5) ковариацию Cov(X2,Y).'\
      or snippet in 'Дано совместное распределение дискретных случайных величин X и Y: Найдите: 1) математическое ожидание E(X2); 2) математическое ожидание E(X4); 3) дисперсию Var(X2); 4) математическое ожидание E(X2Y); 5) ковариацию Cov(X2,Y).':
    A = '''
dct = {1:(2, 8), 2:(3, 8), 3:(6, 8), 
       4:(2, 9), 5:(3, 9), 6:(6, 9)}

probabilities = [0.05, 0.05, 0.08, 
                 0.06, 0.17, 0.59]

XandY = rv_discrete(values=(list(dct.keys()), probabilities))

X2_dct = defaultdict(int)
for i in dct.keys():
  X2_dct[dct[i][0]**2] += XandY.pmf(i) 
X2 = rv_discrete(values=(list(X2_dct.keys()), list(X2_dct.values())))

X4_dct = defaultdict(int)
for i in dct.keys():
  X4_dct[dct[i][0]**4] += XandY.pmf(i) 
X4 = rv_discrete(values=(list(X4_dct.keys()), list(X4_dct.values())))

Y_dct = defaultdict(int)
for i in dct.keys():
  Y_dct[dct[i][1]] += XandY.pmf(i)
Y = rv_discrete(values=(list(Y_dct.keys()), list(Y_dct.values())))

X2Y_dict = defaultdict(int)
for i in dct.keys():
  X2Y_dict[dct[i][0]**2 * dct[i][1]] += XandY.pmf(i)  
X2Y = rv_discrete(values=(list(X2Y_dict.keys()), list(X2Y_dict.values())))

Cov_X2_Y = X2Y.expect() - Y.expect()*X2.expect()

print(f'E(X^2) = {X2.expect()}')
print(f'E(X^4) = {X4.expect()}')
print(f'Var(X^2) = {X2.var()}')
print(f'E(X^2 * Y) = {X2Y.expect()}')
print(f'Cov(X^2, Y) = {Cov_X2_Y}')
    '''
  elif snippet in 'Распределение дискретного случайного вектора (X,Y) имеет вид: Найдите: 1) математическое ожидание E(X2); 2) математическое ожидание E(Y); 3) стандартное отклонение σ(X2); 4) стандартное отклонение σ(Y); 5) коэффициент корреляции ρ(X2,Y).' or snippet in 'Дано совместное распределение дискретных случайных величин X и Y: Найдите: 1) математическое ожидание E(X2); 2) математическое ожидание E(Y); 3) стандартное отклонение σ(X2); 4) стандартное отклонение σ(Y); 5) коэффициент корреляции ρ(X2,Y).':
    A = '''
 dct = {1:(2, 8), 2:(3, 8), 3:(6, 8), 
       4:(2, 9), 5:(3, 9), 6:(6, 9)}

probabilities = [0.4, 0.11, 0.01, 
                 0.29, 0.12, 0.07]

XandY = rv_discrete(values=(list(dct.keys()), probabilities))


X2_dct = defaultdict(int)
for i in dct.keys():
  X2_dct[dct[i][0]**2] += XandY.pmf(i) 
X2 = rv_discrete(values=(list(X2_dct.keys()), list(X2_dct.values())))


Y_dct = defaultdict(int)
for i in dct.keys():
  Y_dct[dct[i][1]] += XandY.pmf(i)
Y = rv_discrete(values=(list(Y_dct.keys()), list(Y_dct.values())))

X2Y_dict = defaultdict(int)
for i in dct.keys():
  X2Y_dict[dct[i][0]**2 * dct[i][1]] += XandY.pmf(i)  
X2Y = rv_discrete(values=(list(X2Y_dict.keys()), list(X2Y_dict.values())))

corr_X2_Y = (X2Y.expect() - X2.expect()*Y.expect())/(X2.std()*Y.std())

print(f'E(X^2) = {X2.expect()}')
print(f'E(Y) = {Y.expect()}')
print(f'Std(X^2) = {X2.std()}')
print(f'Std(Y) = {Y.std()}')
print(f'Corr(X^2, Y) = {corr_X2_Y}')   
    '''
  elif snippet in 'Для нормального случайного вектора (X,Y)∼N()найдите вероятность P<0.':
    A='''
# P((X-x_value)(Y-y_value))
Ex = -7
Ey = 17
varx = 81
vary = 16
corr = 0.6

# P((X-x_value)(Y-y_value))
x_value = 4
y_value = 3

X = norm(Ex, varx**0.5)
Y = norm(Ey, vary**0.5)
XY = multivariate_normal(mean=[Ex, Ey], cov=[[varx, corr*varx**0.5 * vary**0.5], [corr*varx**0.5 * vary**0.5, vary]])

print(round((X.cdf(4) - XY.cdf([x_value, y_value])) + (Y.cdf(y_value) - XY.cdf([x_value, y_value])),4))

#----------------------------------------------------------------------------------------
# P((X-x1_value)(X-x2_value)(Y-y_value))
Ex = -1
Ey = 2
VarX = 49
VarY = 25
p = -0.2

# P((X-x1_value)(X-x2_value)(Y-y_value))
x1_value = 5
x2_value = 13
y_value =1

sigX = VarX**0.5
sigY = VarY**0.5
mean = [Ex, Ey]
Cov = [[VarX, sigX*sigY*p], [sigX*sigY*p, VarY]]
X = norm(Ex, sigX)
Y = norm(Ey, sigY)
XY = multivariate_normal(mean=mean, cov=Cov)

print(round(XY.cdf([x1_value, y_value]) + (Y.cdf(y_value) - XY.cdf([x2_value, y_value])) + \
((X.cdf(x2_value) - XY.cdf([x2_value, y_value])) - \
(X.cdf(x1_value) - XY.cdf([x1_value, y_value]))),4))   
    '''
  elif snippet in 'Случайный вектор (X,Y) имеет плотность распределения fX,Y(x,y) Найдите: 1) математическое ожидание E(X); 2) математическое ожидание E(Y); 3) дисперсию Var(X); 4) дисперсию Var(Y); 5) ковариацию Cov(X,Y); 6) коэффициент корреляции ρ(X,Y).':
    A='''
from fractions import Fraction

# Из квадратичных членов: -(15/2)x² - 24xy - 30y² (пример)
x_power_2 = -15/2
xy = -24
y_power_2 = -30

# Из линейных членов: -6x + 5y (пример)
x = -6
y= 5

H = np.array([[-2*x_power_2, -1*xy],
                      [-1*xy, -2*y_power_2]])
L = [x,y]

mu = np.linalg.solve(H, L)
mu_X, mu_Y = mu

Sigma = np.linalg.inv(H)
var_X = Sigma[0, 0]
var_Y = Sigma[1, 1]
cov_XY = Sigma[0, 1]

rho_XY = cov_XY / np.sqrt(var_X * var_Y)

def to_fraction(x, limit_denominator=1000):
    return Fraction(x).limit_denominator(limit_denominator)


print(f"1. E(X) = {to_fraction(mu_X)}")
print(f"2. E(Y) = {to_fraction(mu_Y)}")
print(f"3. Var(X) = {to_fraction(var_X)}")
print(f"4. Var(Y) = {to_fraction(var_Y)}")
print(f"5. Cov(X, Y) = {to_fraction(cov_XY)}")
print(f"6. ρ(X, Y) = {to_fraction(rho_XY)}")   
    '''
  elif snippet in 'Распределение случайной величины X задано таблицей. Пусть Y – такая случайная величина, что Y=|X−|. Найдите: 1) математическое ожидание E(X); 2) математическое ожидание E(Y); 3) математическое ожидание E(XY); 4) дисперсию Var(X); 5) дисперсию Var(Y).':
    A = '''
X = rv_discrete(values=([2, 6, 9, 13, 15], [0.1, 0.2, 0.2, 0.3, 0.2]))
dct = defaultdict(int)

xy_dct = defaultdict(int)

for i in [2, 6, 9, 13, 15]:
  dct[abs(i-10)] += X.pmf(i)
  
for x in [2, 6, 9, 13, 15]:
  for y in dct.keys():
    if y == abs(x-10):
      xy_dct[x*y] += X.pmf(x)

XY = rv_discrete(values=(list(xy_dct.keys()), list(xy_dct.values())))

Y = rv_discrete(values=(list(dct.keys()), list(dct.values())))

print(f'Expected Value of X: {X.expect()}')
print(f'Expected Value of Y: {Y.expect()}')
print(f'Expected Value of XY: {XY.expect()}')
print(f'Variance of X: {X.var()}')
print(f'Variance of Y: {Y.var()}')
    '''
  elif snippet in 'События A, B и C имеют вероятности: P(A), P(B), P(C). Эти события попарно независимы, но все три одновременно наступить не могут. Пусть X – индикатор A, Y – индикатор B, Z – индикатор , а U=. Найдите: 1) математическое ожидание E(U); 2) дисперсию Var(U).':
    A = '''
dct = defaultdict(int)
X = {1: 2 / 10, 0: 8 / 10}
Y = {1: 4 / 10, 0: 6 / 10}
Z = {1: 4 / 10, 0: 6 / 10}
ch = [1, 0]
for x in product(ch, repeat=3):
    if x.count(1) == 3:
        impos = X[x[0]] * Y[x[1]] * Z[x[2]]
    else:
        if x.count(0)==3:
            dct[0] =+ impos + X[x[0]] * Y[x[1]] * Z[x[2]]
        else:
            if x[0] == 0 and x[1] == 0:
                dct[7*x[0] + 3*x[1] + 5*x[2]]  += Z[1] - X[1]*Z[1] - Y[1]*Z[1]
            elif x[0] == 0 and x[2] == 0:
                dct[7*x[0] + 3*x[1] + 5*x[2]]  += Y[1] - X[1]*Y[1] - Z[1]*Y[1]
            elif x[1] == 0 and x[2] == 0:
                dct[7*x[0] + 3*x[1] + 5*x[2]]  += X[1] - X[1]*Z[1] - Y[1]*X[1]
            elif x[0] == 0:
                dct[7*x[0] + 3*x[1] + 5*x[2]]  += Y[1]*Z[1]
            elif x[1] == 0:
                dct[7*x[0] + 3*x[1] + 5*x[2]]  += X[1] * Z[1]
            elif x[2] == 0:
                dct[7*x[0] + 3*x[1] + 5*x[2]]  += X[1] * Y[1]
                
X = rv_discrete(values=(list(dct.keys()), list(dct.values())))
print(f'Expected Value of X: {X.expect()}')
print(f'Variance of X: {X.var()}')
    '''
  elif snippet in 'Случайная величина X с равной вероятностью принимает все целые значения от до. Пусть Y=|X−|. Найдите: 1) наименьшее число Q1Min, для которого P(Y⩽Q1Min)⩾0,25; 2) наибольшее число Q1Max, для которого P(Y⩾Q1Max)⩾0,75; 3) наименьшее число Q3Min, для которого P(Y⩽Q3Min)⩾0,75; 4) наибольшее число Q3Ma, для которого P(Y⩾Q3Max)⩾0,25.':
    A = '''
E = 0.00000001
dct = defaultdict(int)

ch = list(range(1, 129))

for X in ch:
  dct[abs(X-89.5)] +=1/len(ch)


Y = rv_discrete(values=(list(dct.keys()), list(dct.values())))
Q1mn = []
Q3mn = []
Q1mx = []
Q3mx = []
for i in dct.keys():
    if Y.cdf(i) >= 0.25:
      Q1mn.append(i)
    if Y.cdf(i) >= 0.75:
      Q3mn.append(i)
    if Y.sf(i - E) >= 0.75:
      Q1mx.append(i)
    if Y.sf(i - E) >= 0.25:
      Q3mx.append(i)
print(Y.sf(16.5))
print(f'Q1Min = {min(Q1mn)}')
print(f'Q1Max = {max(Q1mx)}')
print(f'Q3Min = {min(Q3mn)}')
print(f'Q3Max = {max(Q3mx)}')
    '''
  elif snippet in 'Внутри квадрата площади расположены треугольник и круг. Площади этих фигур даны: треугольник, круг. Также известно, что площадь пересечения треугольника и круга равн. В квадрате случайным независимым образом выбираются точки ω1,...,ω. Определим случайные величины: Xi – индикатор попадания ωi в треугольник, Yi – индикатор попадания ωi в круг, Zi=Xi+Yi,. Определим также сумму U=Z1+...+Z и произведение V=Z1...Z. Найдите: 1) математическое ожидание E(U); 2) дисперсию Var(U); 3) математическое ожидание E(V); 4) дисперсию Var(V).':
    A = '''
c_area = 44
sq_area = 58
together_area = 26

total_area = 100

Z = {0: (total_area - (c_area + sq_area - together_area))/total_area, 1: (c_area + sq_area - 2*together_area) /total_area, 2:together_area/total_area}

U_dist = defaultdict(int)
V_dist = defaultdict(int)

ch = list(Z.keys())

for x in product(ch, repeat=5):
    sm = sum(x)
    prod = x[0]*x[1]*x[2]*x[3]*x[4] # тут может оказаться меньше сл. величин!
    U_dist[sm] += Z[x[0]]*Z[x[1]]*Z[x[2]]*Z[x[3]]*Z[x[4]] # тут может оказаться меньше сл. величин!
    V_dist[prod] += Z[x[0]]*Z[x[1]]*Z[x[2]]*Z[x[3]]*Z[x[4]] # тут может оказаться меньше сл. величин!

U = rv_discrete(values=(list(U_dist.keys()), list(U_dist.values())))
V = rv_discrete(values=(list(V_dist.keys()), list(V_dist.values())))

print(f'Expected Value of U: {U.expect()}')
print(f'Variance of U: {U.var()}')
print(f'Expected Value of V: {V.expect()}')
print(f'Variance of Y: {V.var()}')
    '''
  elif snippet in 'Случайные величины Xi, где i=1,2,3, независимы и одинаково распределены. Их общее распределение задано таблицей. Пусть S=X1+X2+X3. Найдите: 1) математическое ожидание E(S); 2) наименьшее число MedMin, для которого P(S⩽MedMin)⩾0,5; 3) наибольшее число MedMax, для которого P(S⩾MedMax)⩾0,5; 4) наименьшее число ModMin, вероятность которого, P(S=ModMin), максимальна; 5) наибольшее число ModMax, вероятность которого, P(S=ModMax), максимальна.':
    A = '''
X = {3: 0.15, 6: 0.45, 9: 0.15, 10: 0.25}
S_dist = defaultdict(int)
E= 0.000000000001
ch = list(X.keys())

for x in product(ch, repeat=3):
    sm = sum(x)
    S_dist[sm] += X[x[0]]*X[x[1]]*X[x[2]]

S = rv_discrete(values=(list(S_dist.keys()), list(S_dist.values())))
l=[]
l1=[]
l2=[]
for i in S_dist.keys():
  if S.cdf(i) >= 0.5:
      l1.append(i)
  if S.sf(i - E) >= 0.5:
      l2.append(i)
  if S.pmf(i) == max(S.pk):
      l.append(i)
print(f'Expected Value of S: {S.expect()}')
print(f'MedMin: {min(l1)}')
print(f'MedMax: {max(l2)}')
print(f'ModMin: {min(l)}')
print(f'ModMax: {max(l)}')       
    '''
  elif snippet in 'Доход по типовому контракту (в млн. рублей) описывается дискретной случайной величиной X c распределением. Фирма заключила типовых контрактов. Найдите: 1) мат. ожидание и 2) дисперсию среднего арифметического дохода по этим контрактам, считая доходы независимыми между собой.':
    A = '''
contracts = 9

X = rv_discrete(values=([6/contracts, 9/contracts, 13/contracts, 16/contracts, 18/contracts], [0.1, 0.1, 0.4, 0.2, 0.2]))

print(f'Expected Value: {X.expect()*contracts}')
print(f'Variance: {X.var()*contracts}')   
    '''
  elif snippet in 'Игрок начал игру с капиталом рублей. Известно, что в каждой партии вероятность выигрыша рублей равна; вероятность проигрыша рублей равна; а вероятность выигрыша рублей равна. Пусть K – капитал игрока после партий. Найдите: 1) математическое ожидание капитала К; 2) стандартное отклонение К.':
    A = '''
matches = 5
S = 11_000

X = rv_discrete(values=([400, -100, 7], [0.1, 0.4, 0.5]))

print(f'Expected Value: {S+X.expect()*matches}')
print(f'Standart Deviation: {(X.var()*matches)**0.5}')
    '''
  elif snippet in 'Вероятность повышения цены акции (от закрытия торгов в предыдущий рабочий день до текущего закрытия) на % равна; вероятность повышения на % равна; а вероятность понижения на % равна. Пусть S – цена акции после рабочих дней. Предполагая, что начальная цена акции составляет S0 рублей, а относительные изменения цены за различные рабочие дни (от закрытия до закрытия) – независимые случайные величины, найдите: 1) математическое ожидание цены S; 2) стандартное отклонение цены S.':
    A = '''
days = 160
S = 1_000
vals = np.array([1.01, 1.002, 0.98])
probs = [0.2, 0.7, 0.1]
X = rv_discrete(values=(vals, probs))
X2 = rv_discrete(values=(vals**2, probs))

print(f'Expected Value: {S* X.expect()**days}')
print(f'Standart Deviation: {S * (X2.expect()**days - X.expect()**(2*days))**0.5}')
    '''
  elif snippet in 'Корзина содержит пронумерованных шаров. Из корзины без возвращения извлекаются ⩽ шаров. Пусть S обозначает сумму номеров вынутых шаров. 1) Найдите математическое ожидание E(S). 2) Найдите дисперсию Var(S).':
    A = '''
from math import prod
dct=defaultdict(int)

for x in product(range(1, 53), repeat=2):
  if x[0] != x[1]:
    dct[prod(x)] += 1/52 * 1/51
    
X = rv_discrete(values=([i for i in range(1, 53)], [1/52]*52))

XY = rv_discrete(values=(list(dct.keys()), list(dct.values())))

cov = XY.expect() - X.expect()**2

print(f'EXPECTED VALUE OF S: {X.expect()*24}')
print(f'VARIANCE OF S: {X.var()*24 + cov*24*23}')
    '''
  elif snippet in 'Случайные величины могут принимать только три значения: . Известны вероятности : , где . Кроме того, известно, что ;  и  для . Пусть S=. Найдите: 1) ковариацию Cov(Xi,Xj), для i≠j; 2) дисперсию Var(S).':
    A = '''
X = rv_discrete(values=([0, 1, 7], [0.2, 0.4, 0.4]))
XY = rv_discrete(values=([0, 1, 7, 49], [0.33, 0.17, 0.31, 0.19]))

print(f'Covariance: {XY.expect() - X.expect()**2}')
print(f'Variance of S: {14*X.var()+14*13*(XY.expect() - X.expect()**2)}')
    '''
  elif snippet in 'Корзина содержит шаров, на которых изображены цифры: . Известно, что всего имеется шаров с ,  шаров с  и  шаров с . Из корзины без возвращения извлекаются  шаров. Цифру на первом извлеченном шаре обозначим X1, на втором – X2, на третьем – X3, ... Пусть S=. Найдите: 1) мат. ожидание E(S); 2) дисперсию Var(S).':
    A = '''
d = {2: 14, 5:16, 6: 10}

dct=defaultdict(int)

X = rv_discrete(values=([2, 5, 6], [14/40, 16/40, 10/40]))

for x in product([2, 5, 6], repeat=2):
  if x[0] != x[1]:
    dct[prod(x)] += X.pmf(x[0])*d[x[1]]/39
  else:
    dct[prod(x)] += X.pmf(x[0])*(d[x[0]]-1)/39

XY = rv_discrete(values=(list(dct.keys()), list(dct.values())))
cov = XY.expect() - X.expect()**2

print(f'EXPECTED VALUE OF S: {X.expect()*10}')
print(f'VARIANCE OF S: {10*X.var() + 10*9*cov}')
    '''
  elif snippet in 'Банк выдал кредиты двум группам заемщиков: заемщиков в первой группе и  – во второй. Известно, что заемщики из первой группы возвращают кредит с вероятностью , а заемщики из второй группы – с вероятностью . Пусть X – суммарное количество возвращенных кредитов для обеих групп. Предполагая независимость заемщиков, найдите: 1) стандартное отклонение X; 2) асимметрию X. Указание: используйте присущее третьему центральному моменту свойство аддитивности (основное свойство семиинвариантов).' or snippet in 'Селекционер отобрал для проращивания семена из двух партий: – из первой партии и – из второй. Известно, что семена из первой партии прорастают с вероятностью, а семена из второй партии – с вероятностью. Пусть S – суммарное количество проросших семян в обеих партиях. Предполагая независимость процессов прорастания, найдите: 1) стандартное отклонение S; 2) асимметрию S. Указание: используйте присущее третьему центральному моменту свойство аддитивности ':
    A = '''
O =  binom(70, 0.92)

T = binom(180, 0.93)

U3T = 0

U3O = 0

dct = defaultdict(int)

for i in range(181):
  U3T += (i - T.expect())**3 * T.pmf(i)
  for k in range(71):
    dct[i+k] += O.pmf(k)*T.pmf(i)
    
for k in range(71):
  U3O += (k - O.expect())**3 * O.pmf(k)
  
S =  rv_discrete(values=(list(dct.keys()), list(dct.values())))
U3S = U3O + U3T

print(f'Standart Deviation of S: {S.std()}')
print(f'Skewness of S: {U3S/S.std()**3}')
    '''
  elif snippet in 'Независимые пуассоновские случайные величины X,Y,Z имеют следующие стандартные отклонения: σX=; σY=; σZ=. Пусть S=X+Y+Z. Найдите: 1) вероятность P(S=7); 2) наиболее вероятное значение суммы S; 3) стандартное отклонение σS; 4) асимметрию As(S); 5) эксцесс Ex(S).' or snippet in 'Независимые пуассоновские случайные величины X,Y,Z имеют следующие стандартные отклонения: σX=; σY=; σZ=. Пусть S=X+Y+Z. Найдите: 1) вероятность P(S=9); 2) наиболее вероятное значение суммы S; 3) стандартное отклонение σS; 4) асимметрию As(S); 5) эксцесс Ex(S).':
    A = '''
dct = defaultdict(int)
X1 = poisson(1.9**2)
X2 = poisson(1.8**2)
X3 = poisson(1.5**2)

for x in range(100):
  for y in range(100):
    for z in range(100):
      if x+ y+ z == 9:
        dct[9] += X1.pmf(x)*X2.pmf(y)*X3.pmf(z)

Xstd = (X1.var() + X2.var() +X3.var())**0.5
print(f'P(X = 9): {float(dct[9])}')
print(f'THE MOST PROBABLE VALUE OF X: {int(X1.var() + X2.var() +X3.var())}')
print(f'Standart Deviation of X: {Xstd}')

U3X1 = X1.moment(3) - 3*X1.expect()*X1.moment(2) + 2*X1.expect()**3
U3X2 = X2.moment(3) - 3*X2.expect()*X2.moment(2) + 2*X2.expect()**3
U3X3 = X3.moment(3) - 3*X3.expect()*X3.moment(2) + 2*X3.expect()**3
U3X = U3X1 + U3X2 + U3X3 
kurt = X1.var() / (X1.var() + X2.var() +X3.var())**2 + X2.var()/(X1.var() + X2.var() +X3.var())**2 + X3.var()/(X1.var() + X2.var() +X3.var())**2
print(f'Moment of Skewness of X: {U3X/Xstd**3}')

print(f'Kurtosis Excess of X: {kurt}')
    '''
  elif snippet in  'Монеты в количестве штук подбрасываются до тех пор, пока раз не выпадет  гербов. Пусть X – число бросков до первого появления  гербов, а Y – число бросков до последнего появления  гербов (Y = общее число бросков). Найдите: 1) математическое ожидание X; 2) стандартное отклонение X; 3) коэффициент корреляции между X и Y; 4) математическое ожидание XY.':
    A = '''
p = (comb(8, 5) * (1/2)**5 * (1/2)**(8-5))

q = 1 - p

X=geom(p)

EY = 10*X.expect()

EXY = X.moment(2) + 9*X.expect()**2

Yvar = 10*X.var()

cov = EXY - 10*X.expect()**2
print(f'EXPECTED VALUE OF X: {1/p}')
print(f'STANDART DEVIATION OF X: {(q/p**2)**0.5}')
print(f'CORRELATION COEFFICIENT OF (X, Y): {cov/(X.std()*Yvar**0.5)}') 
print(f'EXPECTED VALUE OF (XY): {EXY}')
    '''
  elif snippet in 'Корзина содержит шаров, среди которых – красных и – синих. Из корзины, случайным образом, без возвращения извлекаются  шаров. Пусть X и Y обозначают количество красных и синих шаров среди извлеченных, соответственно. Найдите ковариацию Cov(X,Y).':
    A = '''
red = hypergeom(34, 14, 12)
blue = hypergeom(34, 5, 12)

dct = defaultdict(int)

for rd in range(15):
  for bl in range(6):
    dct[rd*bl] += multivariate_hypergeom.pmf(x=[rd, bl, 12-rd-bl], m=[14, 5, 15], n=12)
    
XY = rv_discrete(values=(list(dct.keys()), list(dct.values())))

print(f'Covariance: {XY.expect() - red.expect()*blue.expect()}')
    '''
  elif snippet in 'Инвестор сформировал портфель из акций компаний А и В, затратив на приобретение акций А в  раз больше средств чем на покупку акций В. Ожидаемая доходность за период владения акциями А и В составляет % и %, при этом стандартное отклонение доходности равно % и %, соответственно. 1) Найдите (в %) стандартное отклонение доходности портфеля инвестора, если известно, что коэффициент корреляции доходностей акций А и В равен .':
    A = '''
from sympy import *
stdA = 0.02
stdB = 0.05
VarB = stdB**2
VarA = stdA**2

Cov = 0.4 * stdA*stdB
Cov_matrix = Matrix([[VarA, Cov], [Cov, VarB]])
vect = Matrix([10/11, 1/11])
VarP = det(transpose(vect)*Cov_matrix*vect)

print(f'STANDART DEVIATION OF P: {rrstr(VarP**0.5 * 100, 2)}')
    '''
  elif snippet in 'Ожидаемая доходность и стандартное отклонение доходности за период для акций компаний А, В, С составляют %, %, % и %, %, %, соответственно. 1) Предполагая независимость доходностей акций А, В и С, найдите (в %) ожидаемую доходность портфеля, составленного из этих акций так, чтобы дисперсия его доходности была минимальной.':
    A = '''
from sympy import *

EA = 0.02
EB = 0.02
EC = 0.03

VarA = 0.03**2
VarB = 0.04**2
VarC = 0.05**2

x, y, z = symbols('x, y, z')
vect = Matrix([x ,y, z])

Cov_matrix = Matrix([[VarA, 0, 0], [0, VarB, 0], [0, 0, VarC]])
f = det(transpose(vect)*Cov_matrix*vect)
f = expand(f.subs({z: 1-y-x}))
FX = Derivative(f, x, evaluate=True)
FY = Derivative(f, y, evaluate=True)
eq1 = Eq(FX, 0)
eq2 = Eq(FY, 0)
solution = solve([eq1, eq2])
z = 1 - solution[x] - solution[y]
Ep = solution[x]*EA + solution[y]*EB + z*EC
    '''
  elif snippet in 'Математическое ожидание доходности акций компаний А и В составляет % и %, при этом стандартное отклонение доходности равно % и %, соответственно. Также известен коэффициент корреляции ρAB доходностей акций А и В, ρAB=. Найдите (короткие позиции допускаются): 1) доли акций А и В в портфеле с минимальной дисперсией доходности; 2) ожидаемую доходность и стандартное отклонение доходности такого портфеля.':
    A = '''
from sympy import *

EA = 0.01
EB = 0.04
stdA = 0.03
stdB=0.07
VarA = stdA**2
VarB = stdB**2

Cov = 0.21 * stdA*stdB

Cov_matrix = Matrix([[VarA, Cov], [Cov, VarB]])
x, y = symbols('x, y')
vect = Matrix([x ,y])

f = simplify(det(transpose(vect)*Cov_matrix*vect))
f = simplify(f.subs(y, 1-x))
der = Derivative(f, x ,evaluate=True)
eq = Eq(der, 0)
solution = solve(eq)
VarP = f.subs({x: solution[0], y: 1-solution[0]})
print(f'Wight of X: {solution[0]}, Weight of Y:{1-solution[0]} ')
print(f'Profit %: {(EA*solution[0] + EB*(1-solution[0]))*100}')
print(f'Standart deviation of  P: {VarP**0.5 * 100}')
    '''
  pyperclip.copy(A)
















































































































def rvs(snippet: str) -> None:
  if snippet in 'В группе региональных банков имеется банков, у которых нет проблем с выполнением нормативных показателей, и банков, у которых такие проблемы имеются. Для проверки случайным образом отобраны три банка. Найдите: 1) вероятность того, что в число отобранных банков попадет хотя бы один проблемный.' or snippet in 'Среди банков с относительно небольшим уровнем собственного капитала имеется банков, у которых все нормативные показатели удовлетворяют требованиям ЦБ, и банков, у которых имеются нарушения. Для проверки случайным образом отобраны три банка. Найдите: 1) вероятность P того, что в число отобранных банков попадет хотя бы один с нарушением требований.':
    A = '''
good_banks = 10
bad_banks = 13
banks_chosen_for_inspection = 3
ch = ['good']*good_banks + ['bad']*bad_banks
good=0
tot=0
for x in combinations(ch, r=banks_chosen_for_inspection):
  if x.count('bad')>0:
    good+=1
  tot+=1
  
good/tot
    '''
  elif snippet in 'Независимо друг от друга человека садятся в поезд, содержащий вагонов. 1) Найдите вероятность того, что по крайней мере двое из них окажутся в одном вагоне':
    A = '''
wagons = 13
people = 3
ch=list(range(1, wagons+1))
good=0
tot=0
for x in product(ch, repeat=people):
  if len(set(x))<people:
    good+=1
  tot+=1

good/tot
    '''
  elif snippet in 'Из первых натуральных чисел случайным образом выбираются числа. 1) Какова вероятность того, что по крайней мере два числа совпадут?':
    A = '''
max_number = 14
ch=list(range(1, max_number+1))
numbers_chosen = 3
good=0
tot=0
for x in product(ch, repeat=numbers_chosen):
  if len(set(x))<3:
    good+=1
  tot+=1

good/tot
    '''
  elif snippet in 'События A,B и C независимы, P(A)=; P(B)= и P(C)=. 1) Найдите вероятность события D=(A+B)(A+C)(B+C). 2) Найдите вероятность события D, если известно, что событие A уже наступило.':
    A = '''
A_Probability = 0.1
B_Probability = 0.4
C_Probability = 0.9
A = [True]*(10*A_Probability) + [False]*(10 - 10*A_Probability)
B = [True]*(10*B_Probability) + [False]*(10 - 10*B_Probability)
C = [True]*(10*C_Probability) + [False]*(10 - 10*C_Probability)
good=0
w_criterion = 0
tot=0
for x in product(A, B, C):
  if (x[0] | x[1]) & (x[0] | x[2]) & (x[1] | x[2]):
    good+=1
  if (x[0] | x[1]) & (x[0] | x[2]) & (x[1] | x[2]) & x[0]:
    w_criterion+=1
  tot+=1
good/tot, w_criterion/tot/(A.count(True)/10)
    '''
  elif snippet in 'События A,B и C независимы, P(A)=; P(B)= и P(C)=. 1) Найдите вероятность события D=(A+B¯)(B+C¯)(C+A¯). 2) Найдите вероятность события D, если известно, что событие A уже наступило.':
    A = '''
A_Probability = 0.1
B_Probability = 0.6
C_Probability = 0.9
A = [True]*(10*A_Probability) + [False]*(10 - 10*A_Probability)
B = [True]*(10*B_Probability) + [False]*(10 - 10*B_Probability)
C = [True]*(10*C_Probability) + [False]*(10 - 10*C_Probability)
good=0
w_criterion = 0
tot=0
for x in product(A, B, C):
  if (x[0] or not(x[1])) & (not(x[0]) or x[2]) & (x[1] or not(x[2])):
    good+=1
  if (x[0] or not(x[1])) & (not(x[0]) or x[2]) & (x[1] or not(x[2])) & x[0]:
    w_criterion+=1
  tot+=1
good/tot, w_criterion/tot/(A.count(True)/10)
    '''
  elif snippet in 'Имеется монет, из которых бракованные: вследствие заводского брака на этих монетах с обеих сторон отчеканен герб. Наугад выбранную монету, не разглядывая, бросают несколько раз. 1) Какова вероятность, что при бросках она ляжет гербом вверх? 2) При бросках монета легла гербом вверх. Какова вероятность того, что была выбрана монета с двумя гербами?':
    A = '''
A=0
times_thrown = 4
hypothesis = [6/37, 31/37]
dct={hypothesis[0]:1, hypothesis[1]:0.5}
for i in hypothesis:
  A+=i*dct[i]**times_thrown

BAY = hypothesis[0]*dct[hypothesis[0]]/A
A, BAY
    '''
  elif snippet in 'В первой корзине имеется шаров, при этом количество белых шаров равно либо, либо. Оба варианта равновероятны. Во второй корзине имеется шаров, а количество белых шаров равно, или . Эти три варианта также равновероятны. Из обеих корзин все шары перекладываются в третью корзину. 1) Какова вероятность P(A), что случайно вынутый из третьей корзины шар окажется белым (событие A)? 2) Найдите условную вероятность P(H|A), того, что случайно вынутый из третьей корзины шар первоначально находился в первой корзине (событие H), при условии, что он белый (событие A)?':
    A = '''
balls_in_basket_one = 7
balls_in_basket_two = 26
s = balls_in_basket_one + balls_in_basket_two
first = [2, 4]
second = [9, 11, 18]
A=0
for i in first:
  for k in second:
    A+=(i+k)/s * 1/len(first) * 1/len(second)

BAY = 0
for i in first:
  BAY += i/s * 1/len(first) / A
A, BAY
    '''
  elif snippet in 'Имеется две корзины с белыми и черными шарами. В первой корзине всего шаров, при этом количество белых шаров распределено по биномиальному закону с параметрами n и p. Во второй корзине имеется всего шаров, при этом количество белых шаров распределено по биномиальному закону с параметрами n и p. Из обеих корзин все шары перекладываются в третью корзину. 1) Какова вероятность P(A), что случайно вынутый из третьей корзины шар окажется белым (событие A)? 2) Найдите условную вероятность P(H|A), того, что случайно вынутый из третьей корзины шар первоначально находился в первой корзине (событие H), при условии, что он белый (событие A)?':
    A = '''
n1 = 5
n2 = 11
p1 = 0.3
p2 = 0.1
balls_in_first_basket = 13
balls_in_second_basket = 12
S = balls_in_first_basket + balls_in_second_basket
basket1 = binom(n1, p1)
basket2 = binom(n2, p2)
l3 = []
for i in range(n1+1):
  l3.append(basket1.pmf(i))


l4 = []
for i in range(n2+1):
  l4.append(basket2.pmf(i))  


sm=0
for i, val1 in enumerate(l4):
  for k, val2 in enumerate(l3):
    sm+=(i+k)/S * (val1*val2)

rev=0
for k, val2 in enumerate(l3):
  pA=sm
  pHk = val2
  pAHk = (k)/S
  rev+=(pHk*pAHk)/pA
sm, rev
    '''
  elif snippet in 'Имеется две корзины с белыми и черными шарами. В первой корзине количество белых –, количество черных –. Во второй корзине количество белых –, количество черных –. Из первой корзины случайно, без возвращения, излекаются шаров, а из второй – шаров. Отобранные из обеих корзин шары перекладываются в третью корзину. 1) Какова вероятность P(A), что случайно вынутый из третьей корзины шар окажется белым (событие A)? 2) Найдите условную вероятность P(H|A), того, что случайно вынутый из третьей корзины шар первоначально находился в первой корзине (событие H), при условии, что он белый (событие A)?':
    A = '''
black_first = 13
white_first = 12
black_second = 20
white_second = 17
taken_from_first = 8
taken_from_second = 11
S = taken_from_first + taken_from_second
First_sum = black_first + white_first
Second_sum = black_second + white_second
basket1 = binom(taken_from_first, white_first/First_sum)
basket2 = binom(taken_from_second, white_second/Second_sum)

sm=0

for i in range(taken_from_first+1):
  for k in range(taken_from_second+1):
    sm+=(i+k)/S * basket1.pmf(i) * basket2.pmf(k)

rev=0
for k in range(taken_from_first+1):
  pA=sm
  pHk = basket1.pmf(k)
  pAHk = (k)/S
  rev+=(pHk*pAHk)/pA
sm, rev
    '''
  elif snippet in 'Вероятность невозврата кредита равна. Банк выдал кредиты независимым заемщикам. Найдите: 1) наиболее вероятное число заемщиков, которые не вернут кредит' or snippet in 'Вероятность частичного возврата кредита равна. Банк выдал кредиты независимым заемщикам. Найдите: 1) наиболее вероятное число заемщиков, которые вернут кредит лишь частично.':
    A = '''
amount=46
probability = 1/8

probable = amount*probability - probability
probable
    '''
  elif snippet in 'Вероятность дефолта "мусорной" облигации равна. Биржевой игрок купил подобных облигаций, выпущенных независимыми компаниями. Найдите: 1) вероятность того, что среди купленных облигаций окажется менее трех дефолтных.' or snippet in 'Вероятность дефолта облигации, имещей аномально высокую доходность к погашению, равна. Биржевой игрок купил подобных облигаций, выпущенных независимыми компаниями. Найдите: 1) вероятность того, что среди купленных облигаций окажется менее трех дефолтных.':
    A = '''
amount = 5
probability = 0.4
less_then = 3

b = binom(amount, probability)
b.cdf(less_then-1)
    '''
  elif snippet in 'Банк совершил транзакций при ненадежной связи с сервером. Вероятность того, что транзакция будет ошибочной, равна. Используя приближенную формулу для числа успехов в схеме Бернулли, найдите вероятность того, что среди этих n транзакций имеется ошибочные транзакции (не больше и не меньше). В решении необходимо проверить условие применимости приближенной формулы.' or snippet in 'Банк совершил n транзакций по кредитным картам. Вероятность того, что транзакция будет ошибочной, равна. Используя приближенную формулу для числа успехов в схеме Бернулли, найдите вероятность того, что среди этих n транзакций имеется ошибочные транзакции (не больше и не меньше). В решении необходимо проверить условие применимости приближенной формулы.':
    A = '''
errors = 4
amount = 1000
probability = 0.001
dist = poisson(amount*probability)

p.pmf(errors)
    '''
  elif snippet in 'Банк совершил n транзакций по кредитным картам. Вероятность того, что транзакция будет ошибочной. Используя приближенную формулу для числа успехов в схеме Бернулли, найдите вероятность того, что среди этих n транзакций имеется не более ошибочных. В решении необходимо проверить условие применимости приближенной формулы.' or snippet in 'Банк совершил n транзакций при ненадежной связи с сервером. Вероятность того, что транзакция будет ошибочной, равна. Используя приближенную формулу для числа успехов в схеме Бернулли, найдите вероятность того, что среди этих n транзакций имеется не более ошибочных. В решении необходимо проверить условие применимости приближенной формулы.':
    A = '''
errors_or_lesser = 103
amount = 172000
probability = 0.00049
dist = poisson(amount*probability)

dist.cdf(errors_or_lesser)
    '''
  elif snippet in 'В прямоугольной области, заданной ограничениями |x| и |y|, случайным образом выбираются две точки: (x1,y1) и (x2,y2). Пусть A и B – события, состоящие в том, что: A – расстояние между выбранными точками меньше; B – модуль разности |x1−x2| меньше. Найдите приближенно, методом Монте-Карло: 1) вероятность P(A); 2) условную вероятность P(A|B). Указание: получите в заданной прямоугольной области 100000 пар точек и, используя все эти точки, найдите ответы, округляя их до одного знака после запятой.':
    A = '''
xabs = 20
yabs = 8


    
X = uniform(loc=-xabs, scale = xabs*2) 
Y = uniform(loc = -yabs, scale = yabs*2)
N = 100_000
good = 0
total = 0
good1=0
total1=0
good2=0
total2=0
for i in range(N+1):
    x = X.rvs(size=1)
    y = Y.rvs(size = 1)
    xt = X.rvs(size = 1)
    yt = Y.rvs(size=1)
    if ((x-xt)**2 + (y-yt)**2)**0.5 < 11:
        good+=2
    total+=2
    if abs(x - xt)<14:
        good1+=2
    total1+=2
    if abs(x - xt)<14 and ((x-xt)**2 + (y-yt)**2)**0.5 < 11:
        good2+=2
    total2+=2
pA = good/total
print(f' P(A) = {pA}')     

pB = good1/total1
print(f' P(B) = {pB}')

pAB = good2/total2
print(f' P(AB) = {pAB}')
pAatB = pAB/pB
print(f'P(A|B) = {pAatB}')
    '''
  elif snippet in 'В области, ограниченной эллипсом, случайным образом выбираются две точки. Пусть A и B – события, состоящие в том, что: A – расстояние между выбранными точками меньше; B – все координаты обеих точек. Найдите приближенно, методом Монте-Карло: 1) вероятность P(A); 2) условную вероятность P(A|B). Указание: получите внутри заданного эллипса 100000 пар точек и, используя все эти пары точек, найдите ответы, округляя их до одного знака после запятой.':
    A = '''
N = 400_000
def inside_ellipse(hrad: int, vrad: int, p: tuple) -> bool:
  return p[0]**2/hrad**2 + p[1]**2/vrad**2 <= 1
horizontal_radius = 14
vertical_radius = 6
good = 0
total = 0
good1=0
total1=0
good2=0
total2=0
X = uniform(loc=-horizontal_radius, scale=horizontal_radius*2)
Y = uniform(loc=-vertical_radius, scale = vertical_radius*2)

for i in range(N+1):
    x = X.rvs()
    y= Y.rvs()
    xt = X.rvs()
    yt = Y.rvs()
    if inside_ellipse(horizontal_radius, vertical_radius, (x, y)) and inside_ellipse(horizontal_radius, vertical_radius, (xt, yt)):
      if ((x-xt)**2 + (y-yt)**2)**0.5 < 8.7:
          good+=2
      total+=2
    if inside_ellipse(horizontal_radius, vertical_radius, (x, y)) and inside_ellipse(horizontal_radius, vertical_radius, (xt, yt)):
      if (x<0 and y<0) and (xt<0 and yt<0):
        good1+=2
      total1+=2
    if inside_ellipse(horizontal_radius, vertical_radius, (x, y)) and inside_ellipse(horizontal_radius, vertical_radius, (xt, yt)):
      if (x<0 and y<0) and (xt<0 and yt<0) and ((x-xt)**2 + (y-yt)**2)**0.5 < 8.7:
          good2+=2
      total2+=2
pA = good/total
print(f' P(A) = {pA}')

pB = good1/total1
print(f' P(B) = {pB} ')


pAB = good2/total2
print(f' P(AB) = {pAB}')

print(f'P(A|B) = {pAB/pB}')
    '''
    
  elif snippet in 'В кубе объема случайным образом выбираются точки A, B и C. Пусть R, S и T – события, состоящие в том, что: R – наименьший угол в треугольнике ABC меньше; S – наибольший угол в треугольнике ABC меньше; T– треугольник ABC остроугольный. Найдите приближенно, методом Монте-Карло: 1) условную вероятность P(R|T); 2) условную вероятность P(S|T). Указание: получите 100000 остроугольных треугольников ABC и, используя все эти треугольники, найдите ответы, округляя их до одного знака после запятой.':
    A = '''
from math import degrees, acos
 
def angle(d1, d2, d3):
    return degrees(acos((d2**2+d3**2-d1**2)/(2*d2*d3)))
cube_volume = 1
N = 200_000
good=0
total=0
good1=0
total1=0
good2=0
total2=0
dist = uniform(loc = 0, scale = cube_volume**(1/3))
for i in range(N+1):
    x = dist.rvs()
    y = dist.rvs()
    z = dist.rvs()
    x2 = dist.rvs()
    y2 = dist.rvs()
    z2 = dist.rvs()
    x3 = dist.rvs()
    y3 = dist.rvs()
    z3 = dist.rvs()
    leng1 = ((x-x2)**2 + (y-y2)**2 + (z-z2)**2)**0.5
    leng2 = ((x-x3)**2 + (y-y3)**2 + (z-z3)**2)**0.5
    leng3 = ((x2-x3)**2 + (y2-y3)**2 + (z2-z3)**2)**0.5
    angle1 = angle(leng1, leng2, leng3)
    angle2 = angle(leng2, leng1, leng3)
    angle3 = angle(leng3, leng2, leng1)
    if min(angle1, angle2, angle3)<26.7 and angle1<90 and angle2<90 and angle3<90:
        good+=3
    total+=3
    if angle1<90 and angle2<90 and angle3<90:
        good1+=3
    total1+=3
    if angle1<90 and angle2<90 and angle3<90 and max(angle1, angle2, angle3)<81.9:
        good2+=3
    total2+=3
pRT = good/total

pT = good1/total1
print(f'P(R|T) = {pRT/pT}')


pST = good2/total2
print(f'P(S|T) = {pST/pT}')
    '''
  elif snippet in '''В первом броске участвуют несимметричных монет. Во втором броске участвуют только те монеты, на которых в первом броске выпал "орел". Известно, что вероятность выпадения "орла" для данных несимметричных монет равна. Найдите: 1) математическое ожидание числа "орлов", выпавших во втором броске; 2) дисперсию условного математического ожидания числа "орлов", выпавших во втором броске, относительно числа "орлов", выпавших в первом броске''':
    A = '''
tries = 165
p=0.35
A = binom(tries, p)

expectations = defaultdict(int)
variations = defaultdict(int)

EA = A.expect()
for i in range(tries+1):
  expectations[binom(i, p).expect()] += A.pmf(i)
  variations[binom(i, p).var()] += A.pmf(i)
  
E = rv_discrete(values=(list(expectations.keys()), list(expectations.values())))
V = rv_discrete(values=(list(variations.keys()), list(variations.values())))
print(f'E[E(B|A)] = {E.expect()}')
print(f'Var[E(B|A)] = {E.var()}')
print(f'E[Var(B|A)] = {V.expect()}')
print(f'Var(B) = {V.expect() + E.var()}')
    '''
  elif snippet in '''Средний ущерб от одного пожара составляет млн. руб. Предполагается, что ущерб распределен по показательному закону, а число пожаров за год - по закону Пуассона. Также известно, что за лет в среднем происходит пожаров. Найдите: 1) математическое ожидание суммарного ущерба от всех пожаров за один год; 2) стандартное отклонение суммарного ущерба от пожаров за год.''':
    A = '''
average_damage = 2.1
years = 10
fires = 29
fire_per_year = fires/years

expectations = defaultdict(int)
variations = defaultdict(int)

damage = expon(loc=0, scale=average_damage)
fire = poisson(fire_per_year)


for c in range(fires*1000):
  expectations[c*damage.expect()] += fire.pmf(c)
  variations[c*damage.var()] += fire.pmf(c)

  
E = rv_discrete(values=(list(expectations.keys()), list(expectations.values())))
V = rv_discrete(values=(list(variations.keys()), list(variations.values())))

print(f'E[E(S|A)] = {E.expect()}')
print(f'Std(S) = {(V.expect() + E.var())**0.5}')
    '''
  elif snippet in '''Максимальный ущерб от страхового случая составляет млн. руб. Предполагается, что фактический ущерб распределен равномерно от 0 до максимального ущерба, а число страховых случаев за год - по закону Пуассона. Также известно, что за лет в среднем происходит страховых случаев. Найдите: 1) математическое ожидание суммарного ущерба от всех страховых случаев за один год; 2) стандартное отклонение суммарного ущерба от страховых случаев за год.''':
    A = '''
max_damage = 4.8
min_damage = 0
years = 5
accidents = 15
accidents_per_year = accidents/years

expectations = defaultdict(int)
variations = defaultdict(int)

damage = uniform(loc=min_damage, scale = max_damage-min_damage)
acc = poisson(accidents_per_year)


for c in range(accidents*1000):
  expectations[c*damage.expect()] += acc.pmf(c)
  variations[c*damage.var()] += acc.pmf(c)

  
E = rv_discrete(values=(list(expectations.keys()), list(expectations.values())))
V = rv_discrete(values=(list(variations.keys()), list(variations.values())))

print(f'E[E(S|A)] = {E.expect()}')
print(f'Std(S) = {(V.expect() + E.var())**0.5}')
    '''

  elif snippet in '''Для случайной цены Y известны вероятности:. При условии, что Y=y, распределение выручки X является равномерным на отрезке. Найдите: 1) математическое ожидание E(XY); 2) ковариацию Cov(X,Y).''':
    A = '''
Y = rv_discrete(values=([9, 14], [0.7, 0.3]))
uniform_border = 14

EY = Y.expect()
X_dict = defaultdict(int)

for y in Y.xk:
  X_dict[uniform(loc=0, scale=uniform_border*y).expect()] += Y.pmf(y)

X = rv_discrete(values=(list(X_dict.keys()), list(X_dict.values())))
EX = X.expect()

# E(XY) = E[ Y * E(X|Y) ]

XY_dict = defaultdict(int)
for y in Y.xk:
  XY_dict[y * uniform(loc=0, scale=uniform_border*y).expect()] += Y.pmf(y)

XY = rv_discrete(values=(list(XY_dict.keys()), list(XY_dict.values())))
EXY = XY.expect()

print(f'E(XY) = {EXY}')
print(f'Cov(X, Y) = {EXY - EX*EY}')
    '''

  elif snippet in '''Игральная кость и монет подбрасываются до тех пор, пока в очередном броске не выпадет ровно "орлов". Пусть S – суммарное число очков, выпавших на игральной кости при всех бросках. Найдите:  1) математическое ожидание E(S); 2) стандартное отклонение σS.''':
    A = '''
desired_coin_outcomes=20
coins=27

p = binom(coins, 0.5).pmf(desired_coin_outcomes)

Coinflips = geom(p)
Dice_rolls = rv_discrete(values=([1, 2, 3, 4, 5, 6], [1/6]*6))


expectations = defaultdict(int)
variations = defaultdict(int)

for t in range(coins*1005):
  expectations[t*Dice_rolls.expect()] +=Coinflips.pmf(t)
  variations[t*Dice_rolls.var()] += Coinflips.pmf(t)

E = rv_discrete(values=(list(expectations.keys()), list(expectations.values())))
V = rv_discrete(values=(list(variations.keys()), list(variations.values())))

print(f'E[E(S|X)] = {E.expect()}')
print(f'Std(S) = {(V.expect() + E.var())**0.5}')
    '''
  elif snippet in "Распределение дискретного случайного вектора (X,Y) имеет вид: Найдите: 1) вероятность P1; 2) вероятность P2; 3) условное математическое ожидание E3; 4) условное математическое ожидание E4=E(X|Y=11); 5) математическое ожидание E5=E(E(X|Y)).":
    A = '''
combs = {1:(1, 9), 2:(5, 9), 3:(6, 9), 4:(1, 10), 5:(5, 10), 6:(6, 10)}
probs = [0.19, 0.04, 0.34, 0.19, 0.09, 0.15]

XY = rv_discrete(values=(list(combs.keys()), probs))

XcY1 = defaultdict(int)
XcY2 = defaultdict(int)

Y1 = sum(probs[:3])
Y2 = sum(probs[3:])

for key, value in combs.items():
  if value[1] == combs[2][1]:
    XcY1[value[0]]+=XY.pmf(key)/Y1
  elif value[1] == combs[5][1]:
    XcY2[value[0]]+=XY.pmf(key)/Y2

XY1 = rv_discrete(values=(list(XcY1.keys()), list(XcY1.values())))
XY2 = rv_discrete(values=(list(XcY2.keys()), list(XcY2.values())))

total = rv_discrete(values=([XY1.expect(), XY2.expect()], [Y1, Y2]))

print(f'P(Y = {combs[2][1]}) = {Y1}')
print(f'P(Y = {combs[6][1]}) = {Y2}')
print(f'E(X|Y = {combs[2][1]}) = {XY1.expect()}')
print(f'E(X|Y = {combs[6][1]}) = {XY2.expect()}')
print(f'E[E(X|Y)] = {total.expect()}')
    '''
  elif snippet in 'Абсолютно непрерывная случайная величина X может принимать значения только в отрезке. На этом отрезке плотность распределения случайной величины X имеет вид: f(x), где C – положительная константа. Найдите: 1) константу C; 2) математическое ожидание E(X); 3) стандартное отклонение σX; 4) квантиль уровня распределения X.':
    A = '''
f = lambda x: (1+7*x**0.5+8*x**0.7+4*x**0.9)**1.3

C = 1/ quad(f, 4, 9)[0]


class Custom(rv_continuous):
  def _pdf(self, x):
    return C*(1+7*x**0.5+8*x**0.7+4*x**0.9)**1.3

custom = Custom(a = 4, b = 9)
print(f'C = {C}')
print(f'E(X) = {custom.expect()}')
print(f'Std(X) = {custom.std()}')
print(f'Quantile = {float(custom.ppf(0.9))}')      
    '''
  elif snippet in 'Случайная величина X равномерно распределена на отрезке. Случайная величина Y выражается через X следующим образом: Y. Найдите: 1) математическое ожидание E(Y); 2) стандартное отклонение σY; 3) асимметрию As(Y); 4) квантиль уровня 0,9распределения Y.':
    A = '''
a, b = 4, 7
Y = lambda x: (1 + 3*x**0.5 + 4*x**0.7 + 9*x**0.9)**1.1

EY = (1/(b-a))*quad(Y, a, b)[0]

fV2 = lambda x: ((1 + 3*x**0.5 + 4*x**0.7 + 9*x**0.9)**1.1)**2

VarY = (1/(b-a))*quad(fV2, a, b)[0] - EY**2
stdY = VarY**0.5

v3 = (1/(b-a))* quad(lambda x: ((1 + 3*x**0.5 + 4*x**0.7 + 9*x**0.9)**1.1)**3, a, b)[0]
v2 = (1/(b-a)) * quad(fV2, a, b)[0]
CM = v3 - 3*EY*v2 + 2*EY**3

X = uniform(loc=a, scale=b-a)

print(f'E(Y) = {EY}')
print(f'Std(Y) = {stdY}')
print(f'Moment of Skewness  = {CM/stdY**3}')
print(f'Quantile  = {Y(X.ppf(0.9))}')
     
    '''
  elif snippet in 'Распределение дискретного случайного вектора (X,Y) имеет вид: Найдите: 1) математическое ожидание E(X); 2) дисперсию Var(X); 3) математическое ожидание E(Y); 4) дисперсию Var(Y); 5) коэффициент корреляции ρ(X,Y).' \
        or snippet in 'Дано совместное распределение дискретных случайных величин X и Y: Найдите: 1) математическое ожидание E(X); 2) дисперсию Var(X); 3) математическое ожидание E(Y); 4) дисперсию Var(Y); 5) коэффициент корреляции ρ(X,Y).'\
        or snippet in 'Распределение дискретного случайного вектора (X,Y) имеет вид: Найдите: 1) математическое ожидание E(X); 2) дисперсию Var(X); 3) математическое ожидание E(XY); 4) ковариацию Cov(X,Y); 5) коэффициент корреляции ρ(X,Y).'\
        or snippet in 'Дано совместное распределение дискретных случайных величин X и Y: Найдите: 1) математическое ожидание E(X); 2) дисперсию Var(X); 3) математическое ожидание E(XY); 4) ковариацию Cov(X,Y); 5) коэффициент корреляции ρ(X,Y).'\
        or snippet in 'Распределение дискретного случайного вектора (X,Y) имеет вид: Найдите: 1) математическое ожидание E(X); 2) стандартное отклонение σ(X); 3) стандартное отклонение σ(Y); 4) ковариацию Cov(X,Y); 5) коэффициент корреляции ρ(X,Y).'\
        or snippet in 'Дано совместное распределение дискретных случайных величин X и Y: Найдите: 1) математическое ожидание E(X); 2) стандартное отклонение σ(X); 3) стандартное отклонение σ(Y); 4) ковариацию Cov(X,Y); 5) коэффициент корреляции ρ(X,Y).':
    A = '''
dct = {1:(1, 4), 2:(2, 4), 3:(3, 4), 
       4:(1, 8), 5:(2, 8), 6:(3, 8)}

probabilities = [0.05, 0.43, 0.24, 
                 0.19, 0.01, 0.08]

XandY = rv_discrete(values=(list(dct.keys()), probabilities))

X_dct = defaultdict(int)
for i in dct.keys():
  X_dct[dct[i][0]] += XandY.pmf(i)
  
X = rv_discrete(values=(list(X_dct.keys()), list(X_dct.values())))

Y_dct = defaultdict(int)
for i in dct.keys():
  Y_dct[dct[i][1]] += XandY.pmf(i)

Y = rv_discrete(values=(list(Y_dct.keys()), list(Y_dct.values())))

XY_dict = defaultdict(int)
for i in dct.keys():
  XY_dict[dct[i][0]*dct[i][1]] += XandY.pmf(i)
  
XY = rv_discrete(values=(list(XY_dict.keys()), list(XY_dict.values())))

EX = X.expect()
VarX = X.var()
EY = Y.expect()
VarY = Y.var()
EXY = XY.expect()
Cov_X_Y = (EXY - EX*EY)
corr_X_Y = Cov_X_Y/(X.std()*Y.std())

print(f'Expectation of X = {EX}')
print(f'Expectation of Y = {EY}')
print(f'Variance of X = {VarX}')
print(f'Variance of Y = {VarY}')
print(f'Std of X = {X.std()}')
print(f'Std of Y = {Y.std()}')
print(f'Covariance of X and Y = {Cov_X_Y}')
print(f'Expectation of XY = {EXY}')
print(f'Correlation coeff of X and Y = {corr_X_Y}')
    '''
  elif snippet in 'Распределение дискретного случайного вектора (X,Y) имеет вид: Найдите: 1) математическое ожидание E(X2); 2) стандартное отклонение σ(X2); 3) стандартное отклонение σ(Y2); 4) ковариацию Cov(X2,Y2); 5) коэффициент корреляции ρ(X2,Y2).'\
      or snippet in 'Дано совместное распределение дискретных случайных величин X и Y: Найдите: 1) математическое ожидание E(X2); 2) стандартное отклонение σ(X2); 3) стандартное отклонение σ(Y2); 4) ковариацию Cov(X2,Y2); 5) коэффициент корреляции ρ(X2,Y2).':
    A = '''
dct = {1:(2, 10), 2:(6, 10), 3:(8, 10), 
       4:(2, 11), 5:(6, 11), 6:(8, 11)}

probabilities = [0.17, 0.25, 0.26, 
                 0.11, 0.12, 0.09]


XandY = rv_discrete(values=(list(dct.keys()), probabilities))

X2_dct = defaultdict(int)
for i in dct.keys():
  X2_dct[dct[i][0]**2] += XandY.pmf(i) 
X2 = rv_discrete(values=(list(X2_dct.keys()), list(X2_dct.values())))


Y2_dct = defaultdict(int)
for i in dct.keys():
  Y2_dct[dct[i][1]**2] += XandY.pmf(i)
Y2 = rv_discrete(values=(list(Y2_dct.keys()), list(Y2_dct.values())))

X2Y2_dict = defaultdict(int)
for i in dct.keys():
  X2Y2_dict[dct[i][0]**2 * dct[i][1]**2] += XandY.pmf(i)  
X2Y2 = rv_discrete(values=(list(X2Y2_dict.keys()), list(X2Y2_dict.values())))

Cov_X2_Y2 = X2Y2.expect() - X2.expect() * Y2.expect()

corr_X2_Y2 = Cov_X2_Y2 / (X2.std()*Y2.std())

print(f'E(X^2) = {X2.expect()}')
print(f'Std(X^2) = {X2.std()}')
print(f'Std(Y^2) = {Y2.std()}')
print(f'Cov(X^2, Y^2) = {Cov_X2_Y2}')
print(f'Correlation Coeff of X^2, Y^2 = {corr_X2_Y2}')
    '''
  elif snippet in 'Распределение дискретного случайного вектора (X,Y) имеет вид: Найдите: 1) математическое ожидание E(X2); 2) математическое ожидание E(X4); 3) дисперсию Var(X2); 4) математическое ожидание E(X2Y); 5) ковариацию Cov(X2,Y).'\
      or snippet in 'Дано совместное распределение дискретных случайных величин X и Y: Найдите: 1) математическое ожидание E(X2); 2) математическое ожидание E(X4); 3) дисперсию Var(X2); 4) математическое ожидание E(X2Y); 5) ковариацию Cov(X2,Y).':
    A = '''
dct = {1:(2, 8), 2:(3, 8), 3:(6, 8), 
       4:(2, 9), 5:(3, 9), 6:(6, 9)}

probabilities = [0.05, 0.05, 0.08, 
                 0.06, 0.17, 0.59]

XandY = rv_discrete(values=(list(dct.keys()), probabilities))

X2_dct = defaultdict(int)
for i in dct.keys():
  X2_dct[dct[i][0]**2] += XandY.pmf(i) 
X2 = rv_discrete(values=(list(X2_dct.keys()), list(X2_dct.values())))

X4_dct = defaultdict(int)
for i in dct.keys():
  X4_dct[dct[i][0]**4] += XandY.pmf(i) 
X4 = rv_discrete(values=(list(X4_dct.keys()), list(X4_dct.values())))

Y_dct = defaultdict(int)
for i in dct.keys():
  Y_dct[dct[i][1]] += XandY.pmf(i)
Y = rv_discrete(values=(list(Y_dct.keys()), list(Y_dct.values())))

X2Y_dict = defaultdict(int)
for i in dct.keys():
  X2Y_dict[dct[i][0]**2 * dct[i][1]] += XandY.pmf(i)  
X2Y = rv_discrete(values=(list(X2Y_dict.keys()), list(X2Y_dict.values())))

Cov_X2_Y = X2Y.expect() - Y.expect()*X2.expect()

print(f'E(X^2) = {X2.expect()}')
print(f'E(X^4) = {X4.expect()}')
print(f'Var(X^2) = {X2.var()}')
print(f'E(X^2 * Y) = {X2Y.expect()}')
print(f'Cov(X^2, Y) = {Cov_X2_Y}')
    '''
  elif snippet in 'Распределение дискретного случайного вектора (X,Y) имеет вид: Найдите: 1) математическое ожидание E(X2); 2) математическое ожидание E(Y); 3) стандартное отклонение σ(X2); 4) стандартное отклонение σ(Y); 5) коэффициент корреляции ρ(X2,Y).' or snippet in 'Дано совместное распределение дискретных случайных величин X и Y: Найдите: 1) математическое ожидание E(X2); 2) математическое ожидание E(Y); 3) стандартное отклонение σ(X2); 4) стандартное отклонение σ(Y); 5) коэффициент корреляции ρ(X2,Y).':
    A = '''
 dct = {1:(2, 8), 2:(3, 8), 3:(6, 8), 
       4:(2, 9), 5:(3, 9), 6:(6, 9)}

probabilities = [0.4, 0.11, 0.01, 
                 0.29, 0.12, 0.07]

XandY = rv_discrete(values=(list(dct.keys()), probabilities))


X2_dct = defaultdict(int)
for i in dct.keys():
  X2_dct[dct[i][0]**2] += XandY.pmf(i) 
X2 = rv_discrete(values=(list(X2_dct.keys()), list(X2_dct.values())))


Y_dct = defaultdict(int)
for i in dct.keys():
  Y_dct[dct[i][1]] += XandY.pmf(i)
Y = rv_discrete(values=(list(Y_dct.keys()), list(Y_dct.values())))

X2Y_dict = defaultdict(int)
for i in dct.keys():
  X2Y_dict[dct[i][0]**2 * dct[i][1]] += XandY.pmf(i)  
X2Y = rv_discrete(values=(list(X2Y_dict.keys()), list(X2Y_dict.values())))

corr_X2_Y = (X2Y.expect() - X2.expect()*Y.expect())/(X2.std()*Y.std())

print(f'E(X^2) = {X2.expect()}')
print(f'E(Y) = {Y.expect()}')
print(f'Std(X^2) = {X2.std()}')
print(f'Std(Y) = {Y.std()}')
print(f'Corr(X^2, Y) = {corr_X2_Y}')   
    '''
  elif snippet in 'Для нормального случайного вектора (X,Y)∼N()найдите вероятность P<0.':
    A='''
# P((X-x_value)(Y-y_value))
Ex = -7
Ey = 17
varx = 81
vary = 16
corr = 0.6

# P((X-x_value)(Y-y_value))
x_value = 4
y_value = 3

X = norm(Ex, varx**0.5)
Y = norm(Ey, vary**0.5)
XY = multivariate_normal(mean=[Ex, Ey], cov=[[varx, corr*varx**0.5 * vary**0.5], [corr*varx**0.5 * vary**0.5, vary]])

print(round((X.cdf(4) - XY.cdf([x_value, y_value])) + (Y.cdf(y_value) - XY.cdf([x_value, y_value])),4))

#----------------------------------------------------------------------------------------
# P((X-x1_value)(X-x2_value)(Y-y_value))
Ex = -1
Ey = 2
VarX = 49
VarY = 25
p = -0.2

# P((X-x1_value)(X-x2_value)(Y-y_value))
x1_value = 5
x2_value = 13
y_value =1

sigX = VarX**0.5
sigY = VarY**0.5
mean = [Ex, Ey]
Cov = [[VarX, sigX*sigY*p], [sigX*sigY*p, VarY]]
X = norm(Ex, sigX)
Y = norm(Ey, sigY)
XY = multivariate_normal(mean=mean, cov=Cov)

print(round(XY.cdf([x1_value, y_value]) + (Y.cdf(y_value) - XY.cdf([x2_value, y_value])) + \
((X.cdf(x2_value) - XY.cdf([x2_value, y_value])) - \
(X.cdf(x1_value) - XY.cdf([x1_value, y_value]))),4))   
    '''
  elif snippet in 'Случайный вектор (X,Y) имеет плотность распределения fX,Y(x,y) Найдите: 1) математическое ожидание E(X); 2) математическое ожидание E(Y); 3) дисперсию Var(X); 4) дисперсию Var(Y); 5) ковариацию Cov(X,Y); 6) коэффициент корреляции ρ(X,Y).':
    A='''
x, y, U1, U2, a, b, c, d = symbols('x, y, U1, U2, a, b, c, d')
given_power = (-Rational(51, 2)*x**2-45*x*y -9*x-Rational(51, 2)*y**2-7*y-Rational(5, 6)) * -2

vec = Matrix([[x - U1, y - U2]])
Cinv = Matrix([[a, b], [c, d]])
eq = expand(vec * Cinv * transpose(vec))[0]
given_power
eq
eq.subs({a:51, d:51, c:45, b:45})
Cov_matrix = Matrix([[51, 45], [45, 51]]).inv()
Cov_matrix
eq1 = Eq(-102*U1 -90*U2, 18)
eq2 = Eq(-102*U2 -90*U1, 14)
solve([eq1, eq2])
corr = Cov_matrix[2] / (sqrt(Cov_matrix[0]) * sqrt(Cov_matrix[3]))
corr
    '''
  elif snippet in 'Распределение случайной величины X задано таблицей. Пусть Y – такая случайная величина, что Y=|X−|. Найдите: 1) математическое ожидание E(X); 2) математическое ожидание E(Y); 3) математическое ожидание E(XY); 4) дисперсию Var(X); 5) дисперсию Var(Y).':
    A = '''
X = rv_discrete(values=([2, 6, 9, 13, 15], [0.1, 0.2, 0.2, 0.3, 0.2]))
dct = defaultdict(int)

xy_dct = defaultdict(int)

for i in [2, 6, 9, 13, 15]:
  dct[abs(i-10)] += X.pmf(i)
  
for x in [2, 6, 9, 13, 15]:
  for y in dct.keys():
    if y == abs(x-10):
      xy_dct[x*y] += X.pmf(x)

XY = rv_discrete(values=(list(xy_dct.keys()), list(xy_dct.values())))

Y = rv_discrete(values=(list(dct.keys()), list(dct.values())))

print(f'Expected Value of X: {X.expect()}')
print(f'Expected Value of Y: {Y.expect()}')
print(f'Expected Value of XY: {XY.expect()}')
print(f'Variance of X: {X.var()}')
print(f'Variance of Y: {Y.var()}')
    '''
  elif snippet in 'События A, B и C имеют вероятности: P(A), P(B), P(C). Эти события попарно независимы, но все три одновременно наступить не могут. Пусть X – индикатор A, Y – индикатор B, Z – индикатор , а U=. Найдите: 1) математическое ожидание E(U); 2) дисперсию Var(U).':
    A = '''
dct = defaultdict(int)
X = {1: 2 / 10, 0: 8 / 10}
Y = {1: 4 / 10, 0: 6 / 10}
Z = {1: 4 / 10, 0: 6 / 10}
ch = [1, 0]
for x in product(ch, repeat=3):
    if x.count(1) == 3:
        impos = X[x[0]] * Y[x[1]] * Z[x[2]]
    else:
        if x.count(0)==3:
            dct[0] =+ impos + X[x[0]] * Y[x[1]] * Z[x[2]]
        else:
            if x[0] == 0 and x[1] == 0:
                dct[7*x[0] + 3*x[1] + 5*x[2]]  += Z[1] - X[1]*Z[1] - Y[1]*Z[1]
            elif x[0] == 0 and x[2] == 0:
                dct[7*x[0] + 3*x[1] + 5*x[2]]  += Y[1] - X[1]*Y[1] - Z[1]*Y[1]
            elif x[1] == 0 and x[2] == 0:
                dct[7*x[0] + 3*x[1] + 5*x[2]]  += X[1] - X[1]*Z[1] - Y[1]*X[1]
            elif x[0] == 0:
                dct[7*x[0] + 3*x[1] + 5*x[2]]  += Y[1]*Z[1]
            elif x[1] == 0:
                dct[7*x[0] + 3*x[1] + 5*x[2]]  += X[1] * Z[1]
            elif x[2] == 0:
                dct[7*x[0] + 3*x[1] + 5*x[2]]  += X[1] * Y[1]
                
X = rv_discrete(values=(list(dct.keys()), list(dct.values())))
print(f'Expected Value of X: {X.expect()}')
print(f'Variance of X: {X.var()}')
    '''
  elif snippet in 'Случайная величина X с равной вероятностью принимает все целые значения от до. Пусть Y=|X−|. Найдите: 1) наименьшее число Q1Min, для которого P(Y⩽Q1Min)⩾0,25; 2) наибольшее число Q1Max, для которого P(Y⩾Q1Max)⩾0,75; 3) наименьшее число Q3Min, для которого P(Y⩽Q3Min)⩾0,75; 4) наибольшее число Q3Ma, для которого P(Y⩾Q3Max)⩾0,25.':
    A = '''
E = 0.00000001
dct = defaultdict(int)

ch = list(range(1, 129))

for X in ch:
  dct[abs(X-89.5)] +=1/len(ch)


Y = rv_discrete(values=(list(dct.keys()), list(dct.values())))
Q1mn = []
Q3mn = []
Q1mx = []
Q3mx = []
for i in dct.keys():
    if Y.cdf(i) >= 0.25:
      Q1mn.append(i)
    if Y.cdf(i) >= 0.75:
      Q3mn.append(i)
    if Y.sf(i - E) >= 0.75:
      Q1mx.append(i)
    if Y.sf(i - E) >= 0.25:
      Q3mx.append(i)
print(Y.sf(16.5))
print(f'Q1Min = {min(Q1mn)}')
print(f'Q1Max = {max(Q1mx)}')
print(f'Q3Min = {min(Q3mn)}')
print(f'Q3Max = {max(Q3mx)}')
    '''
  elif snippet in 'Внутри квадрата площади расположены треугольник и круг. Площади этих фигур даны: треугольник, круг. Также известно, что площадь пересечения треугольника и круга равн. В квадрате случайным независимым образом выбираются точки ω1,...,ω. Определим случайные величины: Xi – индикатор попадания ωi в треугольник, Yi – индикатор попадания ωi в круг, Zi=Xi+Yi,. Определим также сумму U=Z1+...+Z и произведение V=Z1...Z. Найдите: 1) математическое ожидание E(U); 2) дисперсию Var(U); 3) математическое ожидание E(V); 4) дисперсию Var(V).':
    A = '''
c_area = 44
sq_area = 58
together_area = 26

total_area = 100

Z = {0: (total_area - (c_area + sq_area - together_area))/total_area, 1: (c_area + sq_area - 2*together_area) /total_area, 2:together_area/total_area}

U_dist = defaultdict(int)
V_dist = defaultdict(int)

ch = list(Z.keys())

for x in product(ch, repeat=5):
    sm = sum(x)
    prod = x[0]*x[1]*x[2]*x[3]*x[4] # тут может оказаться меньше сл. величин!
    U_dist[sm] += Z[x[0]]*Z[x[1]]*Z[x[2]]*Z[x[3]]*Z[x[4]] # тут может оказаться меньше сл. величин!
    V_dist[prod] += Z[x[0]]*Z[x[1]]*Z[x[2]]*Z[x[3]]*Z[x[4]] # тут может оказаться меньше сл. величин!

U = rv_discrete(values=(list(U_dist.keys()), list(U_dist.values())))
V = rv_discrete(values=(list(V_dist.keys()), list(V_dist.values())))

print(f'Expected Value of U: {U.expect()}')
print(f'Variance of U: {U.var()}')
print(f'Expected Value of V: {V.expect()}')
print(f'Variance of Y: {V.var()}')
    '''
  elif snippet in 'Случайные величины Xi, где i=1,2,3, независимы и одинаково распределены. Их общее распределение задано таблицей. Пусть S=X1+X2+X3. Найдите: 1) математическое ожидание E(S); 2) наименьшее число MedMin, для которого P(S⩽MedMin)⩾0,5; 3) наибольшее число MedMax, для которого P(S⩾MedMax)⩾0,5; 4) наименьшее число ModMin, вероятность которого, P(S=ModMin), максимальна; 5) наибольшее число ModMax, вероятность которого, P(S=ModMax), максимальна.':
    A = '''
X = {3: 0.15, 6: 0.45, 9: 0.15, 10: 0.25}
S_dist = defaultdict(int)
E= 0.000000000001
ch = list(X.keys())

for x in product(ch, repeat=3):
    sm = sum(x)
    S_dist[sm] += X[x[0]]*X[x[1]]*X[x[2]]

S = rv_discrete(values=(list(S_dist.keys()), list(S_dist.values())))
l=[]
l1=[]
l2=[]
for i in S_dist.keys():
  if S.cdf(i) >= 0.5:
      l1.append(i)
  if S.sf(i - E) >= 0.5:
      l2.append(i)
  if S.pmf(i) == max(S.pk):
      l.append(i)
print(f'Expected Value of S: {S.expect()}')
print(f'MedMin: {min(l1)}')
print(f'MedMax: {max(l2)}')
print(f'ModMin: {min(l)}')
print(f'ModMax: {max(l)}')     
    '''
  elif snippet in 'Доход по типовому контракту (в млн. рублей) описывается дискретной случайной величиной X c распределением. Фирма заключила типовых контрактов. Найдите: 1) мат. ожидание и 2) дисперсию среднего арифметического дохода по этим контрактам, считая доходы независимыми между собой.':
    A = '''
contracts = 9

X = rv_discrete(values=([6/contracts, 9/contracts, 13/contracts, 16/contracts, 18/contracts], [0.1, 0.1, 0.4, 0.2, 0.2]))

print(f'Expected Value: {X.expect()*contracts}')
print(f'Variance: {X.var()*contracts}')    
    '''
  elif snippet in 'Игрок начал игру с капиталом рублей. Известно, что в каждой партии вероятность выигрыша рублей равна; вероятность проигрыша рублей равна; а вероятность выигрыша рублей равна. Пусть K – капитал игрока после партий. Найдите: 1) математическое ожидание капитала К; 2) стандартное отклонение К.':
    A = '''
matches = 5
S = 11_000

X = rv_discrete(values=([400, -100, 7], [0.1, 0.4, 0.5]))

print(f'Expected Value: {S+X.expect()*matches}')
print(f'Standart Deviation: {(X.var()*matches)**0.5}')
    '''
  elif snippet in 'Вероятность повышения цены акции (от закрытия торгов в предыдущий рабочий день до текущего закрытия) на % равна; вероятность повышения на % равна; а вероятность понижения на % равна. Пусть S – цена акции после рабочих дней. Предполагая, что начальная цена акции составляет S0 рублей, а относительные изменения цены за различные рабочие дни (от закрытия до закрытия) – независимые случайные величины, найдите: 1) математическое ожидание цены S; 2) стандартное отклонение цены S.':
    A = '''
days = 160
S = 1_000
vals = np.array([1.01, 1.002, 0.98])
probs = [0.2, 0.7, 0.1]
X = rv_discrete(values=(vals, probs))
X2 = rv_discrete(values=(vals**2, probs))

print(f'Expected Value: {S* X.expect()**days}')
print(f'Standart Deviation: {S * (X2.expect()**days - X.expect()**(2*days))**0.5}')
    '''
  elif snippet in 'Корзина содержит пронумерованных шаров. Из корзины без возвращения извлекаются ⩽ шаров. Пусть S обозначает сумму номеров вынутых шаров. 1) Найдите математическое ожидание E(S). 2) Найдите дисперсию Var(S).':
    A = '''
from math import prod
dct=defaultdict(int)

for x in product(range(1, 53), repeat=2):
  if x[0] != x[1]:
    dct[prod(x)] += 1/52 * 1/51
    
X = rv_discrete(values=([i for i in range(1, 53)], [1/52]*52))

XY = rv_discrete(values=(list(dct.keys()), list(dct.values())))

cov = XY.expect() - X.expect()**2

print(f'EXPECTED VALUE OF S: {X.expect()*24}')
print(f'VARIANCE OF S: {X.var()*24 + cov*24*23}')
    '''
  elif snippet in 'Случайные величины могут принимать только три значения: . Известны вероятности : , где . Кроме того, известно, что ;  и  для . Пусть S=. Найдите: 1) ковариацию Cov(Xi,Xj), для i≠j; 2) дисперсию Var(S).':
    A = '''
X = rv_discrete(values=([0, 1, 7], [0.2, 0.4, 0.4]))
XY = rv_discrete(values=([0, 1, 7, 49], [0.33, 0.17, 0.31, 0.19]))

print(f'Covariance: {XY.expect() - X.expect()**2}')
print(f'Variance of S: {14*X.var()+14*13*(XY.expect() - X.expect()**2)}')
    '''
  elif snippet in 'Корзина содержит шаров, на которых изображены цифры: . Известно, что всего имеется шаров с ,  шаров с  и  шаров с . Из корзины без возвращения извлекаются  шаров. Цифру на первом извлеченном шаре обозначим X1, на втором – X2, на третьем – X3, ... Пусть S=. Найдите: 1) мат. ожидание E(S); 2) дисперсию Var(S).':
    A = '''
d = {2: 14, 5:16, 6: 10}

dct=defaultdict(int)

X = rv_discrete(values=([2, 5, 6], [14/40, 16/40, 10/40]))

for x in product([2, 5, 6], repeat=2):
  if x[0] != x[1]:
    dct[prod(x)] += X.pmf(x[0])*d[x[1]]/39
  else:
    dct[prod(x)] += X.pmf(x[0])*(d[x[0]]-1)/39

XY = rv_discrete(values=(list(dct.keys()), list(dct.values())))
cov = XY.expect() - X.expect()**2

print(f'EXPECTED VALUE OF S: {X.expect()*10}')
print(f'VARIANCE OF S: {10*X.var() + 10*9*cov}')
    '''
  elif snippet in 'Банк выдал кредиты двум группам заемщиков: заемщиков в первой группе и  – во второй. Известно, что заемщики из первой группы возвращают кредит с вероятностью , а заемщики из второй группы – с вероятностью . Пусть X – суммарное количество возвращенных кредитов для обеих групп. Предполагая независимость заемщиков, найдите: 1) стандартное отклонение X; 2) асимметрию X. Указание: используйте присущее третьему центральному моменту свойство аддитивности (основное свойство семиинвариантов).' or snippet in 'Селекционер отобрал для проращивания семена из двух партий: – из первой партии и – из второй. Известно, что семена из первой партии прорастают с вероятностью, а семена из второй партии – с вероятностью. Пусть S – суммарное количество проросших семян в обеих партиях. Предполагая независимость процессов прорастания, найдите: 1) стандартное отклонение S; 2) асимметрию S. Указание: используйте присущее третьему центральному моменту свойство аддитивности ':
    A = '''
O =  binom(70, 0.92)

T = binom(180, 0.93)

U3T = 0

U3O = 0

dct = defaultdict(int)

for i in range(181):
  U3T += (i - T.expect())**3 * T.pmf(i)
  for k in range(71):
    dct[i+k] += O.pmf(k)*T.pmf(i)
    
for k in range(71):
  U3O += (k - O.expect())**3 * O.pmf(k)
  
S =  rv_discrete(values=(list(dct.keys()), list(dct.values())))
U3S = U3O + U3T

print(f'Standart Deviation of S: {S.std()}')
print(f'Skewness of S: {U3S/S.std()**3}')
    '''
  elif snippet in 'Независимые пуассоновские случайные величины X,Y,Z имеют следующие стандартные отклонения: σX=; σY=; σZ=. Пусть S=X+Y+Z. Найдите: 1) вероятность P(S=7); 2) наиболее вероятное значение суммы S; 3) стандартное отклонение σS; 4) асимметрию As(S); 5) эксцесс Ex(S).' or snippet in 'Независимые пуассоновские случайные величины X,Y,Z имеют следующие стандартные отклонения: σX=; σY=; σZ=. Пусть S=X+Y+Z. Найдите: 1) вероятность P(S=9); 2) наиболее вероятное значение суммы S; 3) стандартное отклонение σS; 4) асимметрию As(S); 5) эксцесс Ex(S).':
    A = '''
dct = defaultdict(int)
X1 = poisson(1.9**2)
X2 = poisson(1.8**2)
X3 = poisson(1.5**2)

for x in range(100):
  for y in range(100):
    for z in range(100):
      if x+ y+ z == 9:
        dct[9] += X1.pmf(x)*X2.pmf(y)*X3.pmf(z)

Xstd = (X1.var() + X2.var() +X3.var())**0.5
print(f'P(X = 9): {float(dct[9])}')
print(f'THE MOST PROBABLE VALUE OF X: {int(X1.var() + X2.var() +X3.var())}')
print(f'Standart Deviation of X: {Xstd}')

U3X1 = X1.moment(3) - 3*X1.expect()*X1.moment(2) + 2*X1.expect()**3
U3X2 = X2.moment(3) - 3*X2.expect()*X2.moment(2) + 2*X2.expect()**3
U3X3 = X3.moment(3) - 3*X3.expect()*X3.moment(2) + 2*X3.expect()**3
U3X = U3X1 + U3X2 + U3X3 
kurt = X1.var() / (X1.var() + X2.var() +X3.var())**2 + X2.var()/(X1.var() + X2.var() +X3.var())**2 + X3.var()/(X1.var() + X2.var() +X3.var())**2
print(f'Moment of Skewness of X: {U3X/Xstd**3}')

print(f'Kurtosis Excess of X: {kurt}')
    '''
  elif snippet in  'Монеты в количестве штук подбрасываются до тех пор, пока раз не выпадет  гербов. Пусть X – число бросков до первого появления  гербов, а Y – число бросков до последнего появления  гербов (Y = общее число бросков). Найдите: 1) математическое ожидание X; 2) стандартное отклонение X; 3) коэффициент корреляции между X и Y; 4) математическое ожидание XY.':
    A = '''
p = (comb(8, 5) * (1/2)**5 * (1/2)**(8-5))

q = 1 - p

X=geom(p)

EY = 10*X.expect()

EXY = X.moment(2) + 9*X.expect()**2

Yvar = 10*X.var()

cov = EXY - 10*X.expect()**2
print(f'EXPECTED VALUE OF X: {1/p}')
print(f'STANDART DEVIATION OF X: {(q/p**2)**0.5}')
print(f'CORRELATION COEFFICIENT OF (X, Y): {cov/(X.std()*Yvar**0.5)}') 
print(f'EXPECTED VALUE OF (XY): {EXY}')
    '''
  elif snippet in 'Корзина содержит шаров, среди которых – красных и – синих. Из корзины, случайным образом, без возвращения извлекаются  шаров. Пусть X и Y обозначают количество красных и синих шаров среди извлеченных, соответственно. Найдите ковариацию Cov(X,Y).':
    A = '''
red = hypergeom(34, 14, 12)
blue = hypergeom(34, 5, 12)

dct = defaultdict(int)

for rd in range(15):
  for bl in range(6):
    dct[rd*bl] += multivariate_hypergeom.pmf(x=[rd, bl, 12-rd-bl], m=[14, 5, 15], n=12)
    
XY = rv_discrete(values=(list(dct.keys()), list(dct.values())))

print(f'Covariance: {XY.expect() - red.expect()*blue.expect()}')
    '''
  elif snippet in 'Инвестор сформировал портфель из акций компаний А и В, затратив на приобретение акций А в  раз больше средств чем на покупку акций В. Ожидаемая доходность за период владения акциями А и В составляет % и %, при этом стандартное отклонение доходности равно % и %, соответственно. 1) Найдите (в %) стандартное отклонение доходности портфеля инвестора, если известно, что коэффициент корреляции доходностей акций А и В равен .':
    A = '''
from sympy import *
stdA = 0.02
stdB = 0.05
VarB = stdB**2
VarA = stdA**2

Cov = 0.4 * stdA*stdB
Cov_matrix = Matrix([[VarA, Cov], [Cov, VarB]])
vect = Matrix([10/11, 1/11])
VarP = det(transpose(vect)*Cov_matrix*vect)

print(f'STANDART DEVIATION OF P: {rrstr(VarP**0.5 * 100, 2)}')
    '''
  elif snippet in 'Ожидаемая доходность и стандартное отклонение доходности за период для акций компаний А, В, С составляют %, %, % и %, %, %, соответственно. 1) Предполагая независимость доходностей акций А, В и С, найдите (в %) ожидаемую доходность портфеля, составленного из этих акций так, чтобы дисперсия его доходности была минимальной.':
    A = '''
from sympy import *

EA = 0.02
EB = 0.02
EC = 0.03

VarA = 0.03**2
VarB = 0.04**2
VarC = 0.05**2

x, y, z = symbols('x, y, z')
vect = Matrix([x ,y, z])

Cov_matrix = Matrix([[VarA, 0, 0], [0, VarB, 0], [0, 0, VarC]])
f = det(transpose(vect)*Cov_matrix*vect)
f = expand(f.subs({z: 1-y-x}))
FX = Derivative(f, x, evaluate=True)
FY = Derivative(f, y, evaluate=True)
eq1 = Eq(FX, 0)
eq2 = Eq(FY, 0)
solution = solve([eq1, eq2])
z = 1 - solution[x] - solution[y]
Ep = solution[x]*EA + solution[y]*EB + z*EC
    '''
  elif snippet in 'Математическое ожидание доходности акций компаний А и В составляет % и %, при этом стандартное отклонение доходности равно % и %, соответственно. Также известен коэффициент корреляции ρAB доходностей акций А и В, ρAB=. Найдите (короткие позиции допускаются): 1) доли акций А и В в портфеле с минимальной дисперсией доходности; 2) ожидаемую доходность и стандартное отклонение доходности такого портфеля.':
    A = '''
from sympy import *

EA = 0.01
EB = 0.04
stdA = 0.03
stdB=0.07
VarA = stdA**2
VarB = stdB**2

Cov = 0.21 * stdA*stdB

Cov_matrix = Matrix([[VarA, Cov], [Cov, VarB]])
x, y = symbols('x, y')
vect = Matrix([x ,y])

f = simplify(det(transpose(vect)*Cov_matrix*vect))
f = simplify(f.subs(y, 1-x))
der = Derivative(f, x ,evaluate=True)
eq = Eq(der, 0)
solution = solve(eq)
VarP = f.subs({x: solution[0], y: 1-solution[0]})
print(f'Wight of X: {solution[0]}, Weight of Y:{1-solution[0]} ')
print(f'Profit %: {(EA*solution[0] + EB*(1-solution[0]))*100}')
print(f'Standart deviation of  P: {VarP**0.5 * 100}')
    '''
  pyperclip.copy(A)