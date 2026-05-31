import math
import os

class rational:
    def __init__(self,n,d=1):
        if isinstance(n,rational):
            self._n=n._n
            self._d=n._d
            return
            
        if isinstance(n,str):
            if '/' in n:
                parts=n.split('/')
                n,d=int(parts[0]),int(parts[1])
            else:
                n,d=int(n),1

        if d==0:
            raise zerodivisionerror("знаменник не може бути нулем!")

        g=math.gcd(n,d)
        self._n=n//g
        self._d=d//g

        if self._d<0:
            self._n=-self._n
            self._d=-self._d

    def __getitem__(self,key):
        if key=="n":
            return self._n
        if key=="d":
            return self._d
        raise keyerror("ключ має бути тільки 'n' або 'd'!")

    def __setitem__(self,key,value):
        if key=="n":
            self._n=value
        elif key=="d":
            if value==0:
                raise zerodivisionerror("знаменник не може бути нулем!")
            self._d=value
        else:
            raise keyerror("ключ має бути тільки 'n' або 'd'!")
        g=math.gcd(self._n,self._d)
        self._n//=g
        self._d//=g

    def __call__(self):
        return self._n/self._d

    def _to_rational(self,other):
        if isinstance(other,rational):
            return other
        if isinstance(other,int):
            return rational(other,1)
        raise typeerror("операнд має бути цілим числом або rational!")

    def __add__(self,other):
        other=self._to_rational(other)
        return rational(self._n*other._d+other._n*self._d,self._d*other._d)

    def __sub__(self,other):
        other=self._to_rational(other)
        return rational(self._n*other._d-other._n*self._d,self._d*other._d)

    def __mul__(self,other):
        other=self._to_rational(other)
        return rational(self._n*other._n,self._d*other._d)

    def __truediv__(self,other):
        other=self._to_rational(other)
        return rational(self._n*other._d,self._d*other._n)

    def __str__(self):
        if self._d==1:
            return str(self._n)
        return f"{self._n}/{self._d}"


# функція читання файлу
def process_expression_file(filename):
    if not os.path.exists(filename):
        with open(filename,"w") as f:
            f.write("4 - 92 - 79 * 59 * 90/16 * 75 - 55 * 82/41 * 19\n")

    with open(filename,"r") as f:
        for line in f:
            line=line.strip()
            if not line:
                continue

            tokens=line.split()
            if not tokens:
                continue

            result=rational(tokens[0])
            i=1
            while i<len(tokens):
                operator=tokens[i]
                next_val=rational(tokens[i+1])

                if operator=="+":
                    result=result+next_val
                elif operator=="-":
                    result=result-next_val
                elif operator=="*":
                    result=result*next_val
                elif operator=="/":
                    result=result/next_val

                i+=2

            print(f"вираз: {line}")
            print(f"дріб: {result}")
            print(f"десяткове: {result():.4f}\n")


if __name__ == "__main__":
    process_expression_file("input01.txt")
