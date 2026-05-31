import math
import os

# завдання 5.2.1: захищений словник
class protecteddictint:
    def __init__(self):
        self._data={}

    def __getitem__(self,key):
        return self._data[key]

    def __setitem__(self,key,value):
        if not isinstance(key,int):
            return
        if key in self._data:
            return
        self._data[key]=value

    def __add__(self,other):
        new_dict=protecteddictint()
        new_dict._data=self._data.copy()
        if isinstance(other,protecteddictint):
            new_dict._data.update(other._data)
        elif isinstance(other,tuple) and len(other)==2:
            new_dict[other[0]]=other[1]
        return new_dict

    def __sub__(self,key):
        new_dict=protecteddictint()
        new_dict._data={k:v for k,v in self._data.items() if k!=key}
        return new_dict

    def __contains__(self,key):
        return key in self._data

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return str(self._data)


# завдання 5.3.1: раціональні дроби
class rational:
    def __init__(self,n,d=1):
        if isinstance(n,str):
            if '/' in n:
                parts=n.split('/')
                n,d=int(parts[0]),int(parts[1])
            else:
                n,d=int(n),1
        g=math.gcd(n,d)
        self._n=n//g
        self._d=d//g
        if self._d<0:
            self._n=-self._n
            self._d=-self._d

    def __getitem__(self,key):
        if key=="n":
            return self._n
        return self._d

    def __setitem__(self,key,value):
        if key=="n":
            self._n=value
        else:
            self._d=value
        g=math.gcd(self._n,self._d)
        self._n=self._n//g
        self._d=self._d//g

    def __call__(self):
        return self._n/self._d

    def conv(self,obj):
        if isinstance(obj,rational):
            return obj
        return rational(obj,1)

    def __add__(self,o):
        o=self.conv(o)
        return rational(self._n*o._d+o._n*self._d,self._d*o._d)

    def __sub__(self,o):
        o=self.conv(o)
        return rational(self._n*o._d-o._n*self._d,self._d*o._d)

    def __mul__(self,o):
        o=self.conv(o)
        return rational(self._n*o._n,self._d*o._d)

    def __truediv__(self,o):
        o=self.conv(o)
        return rational(self._n*o._d,self._d*o._n)

    def __str__(self):
        if self._d==1:
            return str(self._n)
        return f"{self._n}/{self._d}"


# функція читання файлу
def run_file(name):
    if not os.path.exists(name):
        with open(name,"w") as f:
            f.write("4 - 92 - 79 * 59 * 90/16 * 75 - 55 * 82/41 * 19\n")
            
    with open(name,"r") as f:
        for line in f:
            t=line.strip().split()
            if not t:
                continue
            res=rational(t[0])
            for i in range(1,len(t),2):
                op=t[i]
                nxt=rational(t[i+1])
                if op=="+":
                    res=res+nxt
                elif op=="-":
                    res=res-nxt
                elif op=="*":
                    res=res*nxt
                elif op=="/":
                    res=res/nxt
            print(f"вираз: {line.strip()}")
            print(f"дріб: {res}")
            print(f"десятковий: {res():.4f}\n")


# запуск програми
if __name__ == "__main__":
    d=protecteddictint()
    d[1]="apple"
    d[2]="banana"
    d=d+(3,"cherry")
    d=d-2
    print("словник:",d)
    print("довжина:",len(d))
    print("чи є 1?:",1 in d)
    print("-" * 30)
    run_file("input01.txt")
