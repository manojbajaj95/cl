# Programmable half-life: write task A into subspaces of W1 chosen by the generic stream's gradient second moment
import numpy as np
rng=np.random.default_rng(0); D,H,K=16,48,4
def task(seed,n=3000):
    r=np.random.default_rng(seed); W=r.normal(size=(D,K)); X=r.normal(size=(n,D)); return X,np.argmax(X@W,1)
def init():
    return {'W1':rng.normal(size=(D,H))/np.sqrt(D),'W2':rng.normal(size=(H,K))/np.sqrt(H)}
def grads(P,X,y):
    h=X@P['W1']; a=np.maximum(h,0); o=a@P['W2']; o-=o.max(1,keepdims=True); p=np.exp(o); p/=p.sum(1,keepdims=True)
    n=len(y); g=p.copy(); g[np.arange(n),y]-=1; g/=n
    return {'W2':a.T@g,'W1':X.T@((g@P['W2'].T)*(h>0))}
def acc(P,X,y): return (np.maximum(X@P['W1'],0)@P['W2']).argmax(1).__eq__(y).mean()
def sgd(P,X,y,steps,lr,proj=None,seed=0,trace=None,XA=None,yA=None):
    r=np.random.default_rng(seed); out=[]
    for t in range(steps):
        i=r.integers(0,len(y),32); G=grads(P,X[i],y[i])
        g1=G['W1'].ravel()
        if proj is not None: g1=proj@(proj.T@g1); P['W1']-=lr*g1.reshape(D,H)
        else: P['W1']-=lr*G['W1']; P['W2']-=lr*G['W2']
        if trace and t%trace==0: out.append(acc(P,XA,yA))
    return out
XB,yB=task(2); XA,yA=task(1,600)
P0=init(); sgd(P0,XB,yB,3000,0.1)           # generic pretraining on B
# per-example W1 gradient second moment on B
M=np.zeros((D*H,D*H))
for j in range(0,1500,1):
    g=grads(P0,XB[j:j+1],yB[j:j+1])['W1'].ravel(); M+=np.outer(g,g)
evals,evecs=np.linalg.eigh(M/1500); order=np.argsort(evals)[::-1]; evecs=evecs[:,order]; evals=evals[order]
k=96
for name,U in [('top-k (fragile)',evecs[:,:k]),('mid-k',evecs[:,300:300+k]),('bottom-k (stable)',evecs[:,-k:]),('random-k',np.linalg.qr(rng.normal(size=(D*H,k)))[0])]:
    P={kk:v.copy() for kk,v in P0.items()}
    a0=acc(P,XA,yA); sgd(P,XA,yA,4000,0.5,proj=U,seed=3); a1=acc(P,XA,yA)
    accB=acc(P,XB,yB)
    tr=sgd(P,XB,yB,6000,0.1,seed=4,trace=500,XA=XA,yA=yA)
    lam=(U.T@ (M/1500) @U).trace()/k
    print(f"{name:18s} mean-eig={lam:.2e} A: {a0:.2f}->{a1:.2f} (B {accB:.2f}) retention trace:",' '.join(f'{x:.2f}' for x in tr))
