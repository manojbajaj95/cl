exec(open('noether_check.py').read().split("import copy")[0].replace("m0=base()","m0=base()\nimport sys"))
import copy
X,y=BCD[0]
for k in (0,0.3,1.0,3.0):
    m=copy.deepcopy(m0)
    if k>0: write(m,k*d0.std().item()*bits,'d')
    a,b=charges(m); 
    opt=torch.optim.SGD(m.parameters(),lr=0.05); lf=nn.CrossEntropyLoss(); ls=[]
    for s in range(3000):
        i=torch.randint(0,N,(64,)); opt.zero_grad(); L=lf(m(X[i]),y[i]); L.backward(); opt.step(); ls.append(L.item())
    a2,b2=charges(m); dd=(a2-b2)-(a-b)
    print(f"k={k} c-range a/b ratio med {(a/b).median():.2f} max {(a/b).max():.1f}  loss start {sum(ls[:50])/50:.3f} end {sum(ls[-200:])/200:.3f} Bacc {acc(m,X,y):.2f}  |drift d| mean {dd.abs().mean():.4f} vs write amp {k*d0.std().item():.4f}",flush=True)
