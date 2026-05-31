import math
import os

# лінійне рівняння ax + b = 0
class equation:
    def __init__(self,a,b):
        self.a=a
        self.b=b

    def solve(self):
        if self.a==0:
            if self.b==0:
                return "inf" # нескінченно багато
            return () # немає розв'язків
        return (-self.b/self.a,)

    def show(self):
        return f"{self.a}x + {self.b} = 0"


# квадратне рівняння ax^2 + bx + c = 0
class quadraticequation(equation):
    def __init__(self,a,b,c):
        super().__init__(b,c)
        self.qa=a

    def solve(self):
        if self.qa==0:
            return super().solve()
        d=self.b**2-4*self.qa*self.b
        # тут self.b це коефіцієнт при x (батьківський a), а self.b з формули d — це self.b
        # але для простоти і уникнення плутанини використаємо змінні з умови
        a,b,c=self.qa,self.a,self.b
        d=b**2-4*a*c
        if d<0:
            return ()
        if d==0:
            return (-b/(2*a),)
        x1=(-b-math.sqrt(d))/(2*a)
        x2=(-b+math.sqrt(d))/(2*a)
        return tuple(sorted((x1,x2)))

    def show(self):
        if self.qa==0:
            return super().show()
        return f"{self.qa}x^2 + {self.a}x + {self.b} = 0"


# біквадратне рівняння ax^4 + bx^2 + c = 0
class biquadraticequation(quadraticequation):
    def __init__(self,a,b,c):
        super().__init__(a,b,c)

    def solve(self):
        if self.qa==0:
            # якщо a=0, то ax^4+bx^2+c=0 стає bx^2+c=0
            # для цього робимо заміну у лінійному батьківському класі
            # але у нас коефіцієнти змістилися, тому простіше вирішити через t
            # де t — це корені лінійного рівняння self.a * t + self.b = 0
            t_roots=super(quadraticequation,self).solve()
        else:
            # отримуємо t за допомогою методу квадратного рівняння
            t_roots=super().solve()

        if t_roots=="inf":
            return "inf"
            
        roots=set()
        for t in t_roots:
            if t>0:
                roots.add(math.sqrt(t))
                roots.add(-math.sqrt(t))
            elif t==0:
                roots.add(0.0)
                
        return tuple(sorted(list(roots)))

    def show(self):
        return f"{self.qa}x^4 + {self.a}x^2 + {self.b} = 0"


# функція створення тестових файлів, якщо їх немає
def create_inputs():
    data1="2 1\n3 1 6\n3 0 5 0 6\n0 0\n1 -4 4\n"
    data2="1 0 -4\n1 0 0 0 0\n0 5 0\n1 -5 4\n"
    data3="1 0 5\n1 -2 1\n1 0 -10 0 9\n0 0 0\n"
    for name,content in [("input01.txt",data1),("input02.txt",data2),("input03.txt",data3)]:
        if not os.path.exists(name):
            with open(name,"w") as f:
                f.write(content)


# функція обробки файлу
def process_file(filename):
    print(f"\n=== аналіз файлу: {filename} ===")
    if not os.path.exists(filename):
        return
        
    categories={
        "0": [], "1": [], "2": [], "3": [], "4": [], "inf": []
    }
    one_root_solutions=[]

    with open(filename,"r") as f:
        for line in f:
            coef=[float(x) for x in line.strip().split()]
            if not coef:
                continue
                
            # визначаємо тип рівняння за кількістю коефіцієнтів
            if len(coef)==2:
                eq=equation(coef[0],coef[1])
            elif len(coef)==3:
                eq=quadraticequation(coef[0],coef[1],coef[2])
            elif len(coef)==5:
                eq=biquadraticequation(coef[0],coef[2],coef[4])
            else:
                continue

            roots=eq.solve()
            
            if roots=="inf":
                categories["inf"].append(eq)
            else:
                count=str(len(roots))
                if count in categories:
                    categories[count].append(eq)
                if len(roots)==1:
                    one_root_solutions.append((roots[0],eq))

    # виведення груп рівнянь за кількістю коренів
    titles={
        "0": "не мають розв'язків",
        "1": "мають один розв'язок",
        "2": "мають два розв'язки",
        "3": "мають три розв'язки",
        "4": "мають чотири розв'язки",
        "inf": "мають нескінченну кількість розв'язків"
    }
    
    for k,v in categories.items():
        print(f"\n* рівняння, що {titles[k]} ({len(v)} шт):")
        for eq in v:
            print(f"  {eq.show()} -> розв'язок: {eq.solve()}")

    # пошук min та max серед тих, де 1 корінь
    if one_root_solutions:
        min_root=min(one_root_solutions,key=lambda x: x[0])
        max_root=max(one_root_solutions,key=lambda x: x[0])
        print(f"\nсеред рівнянь з одним розв'язком:")
        print(f"  найменший розв'язок ({min_root[0]}): {min_root[1].show()}")
        print(f"  найбільший розв'язок ({max_root[0]}): {max_root[1].show()}")
    else:
        print("\nрівнянь з рівно одним розв'язком не знайдено.")


# головний запуск
if __name__ == "__main__":
    create_inputs()
    process_file("input01.txt")
    process_file("input02.txt")
    process_file("input03.txt")
