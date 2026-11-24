import torch, torch.nn as nn, math, sys
torch.set_num_threads(1)
D,H,K,N=64,256,5,4000
def task(seed):
    g=torch.Generator().manual_seed(seed); X=torch.randn(N,D,generator=g)
    T=nn.Sequential(nn.Linear(D,64),nn.Tanh(),nn.Linear(64,K)); [p.data.copy_(torch.randn(p.shape,generator=g)) for p in T.parameters()]
    with torch.no_grad(): y=T(X).argmax(1)
    return X,y
def mk(seed): torch.manual_seed(seed); return nn.Sequential(nn.Linear(D,H),nn.ReLU(),nn.Linear(H,K))
def charges(m):
    a=m[0].weight.pow(2).sum(1)+m[0].bias.pow(2); b=m[2].weight.pow(2).sum(0); return a,b
def rescale(m,c):
    with torch.no_grad(): m[0].weight.mul_(c[:,None]); m[0].bias.mul_(c); m[2].weight.div_(c[None,:])
def train(m,X,y,opt,steps,bs=64):
    lf=nn.CrossEntropyLoss()
    for s in range(steps):
        i=torch.randint(0,N,(bs,)); opt.zero_grad(); lf(m(X[i]),y[i]).backward(); opt.step()
def acc(m,X,y):
    with torch.no_grad(): return (m(X).argmax(1)==y).float().mean().item()
def mkopt(name,m):
    if name=='sgd': return torch.optim.SGD(m.parameters(),lr=0.05)
    if name.startswith('sgd_'): return torch.optim.SGD(m.parameters(),lr=float(name.split('_')[1]))
    if name=='sgdm': return torch.optim.SGD(m.parameters(),lr=0.01,momentum=0.9)
    if name.startswith('adamw'): return torch.optim.AdamW(m.parameters(),lr=float(name.split('_')[1]),weight_decay=0.01)
    if name.startswith('adam'): return torch.optim.Adam(m.parameters(),lr=float(name.split('_')[1]))
A=task(1); BCD=[task(s) for s in (2,3,4)]
def base():
    m=mk(0); train(m,*A,torch.optim.SGD(m.parameters(),lr=0.05),3000); return m
m0=base(); print('taskA acc',acc(m0,*A))
a,b=charges(m0); d0=a-b; print('natural d spread(std)',d0.std().item())
torch.manual_seed(123); bits=torch.randint(0,2,(H,)).float()*2-1
def write(m,target,which):
    a,b=charges(m)
    if which=='d':   # want a c^2 - b/c^2 = t
        c2=(target+torch.sqrt(target**2+4*a*b))/(2*a)
    else:            # want a c^2 = t  (non-conserved readout ||w_in||^2)
        c2=target/a
    rescale(m,c2.sqrt())
def read(m,which):
    a,b=charges(m); return (a-b) if which=='d' else a
import copy
X,y=A
print('opt amp chan bitacc Aacc_after erase_bitacc')
for opt in sys.argv[1].split(','):
  for k in (3.0,1.0,0.3):
    amp=k*d0.std().item()
    for which in ('d','a'):
        m=copy.deepcopy(m0)
        before=m(X).detach()
        if which=='d': write(m,amp*bits,'d')
        else: write(m,charges(m)[0]*torch.exp(k*0.3*bits),'a')
        fdiff=(m(X).detach()-before).abs().max().item()
        ref=0 if which=='d' else charges(m0)[0]
        for t in BCD: train(m,*t,mkopt(opt,m),3000)
        r=read(m,which)-ref; ba=((r.sign()==bits).float().mean()).item()
        # erase attack: rebalance to d=0, function preserving
        m2=copy.deepcopy(m); a2,b2=charges(m2); rescale(m2,(b2/a2).pow(0.25)); ea=(((read(m2,'d')).sign()==bits).float().mean()).item()
        print(opt,k,which,f'{ba:.3f}',f'{acc(m,*A):.2f}',f'erase {ea:.3f}',f'fdiff {fdiff:.1e}',flush=True)
