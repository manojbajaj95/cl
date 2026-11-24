# Noether memory pilot: write payload into per-unit balancedness d_i=||w_in_i||^2-||w_out_i||^2
# of a 2-layer ReLU MLP via function-preserving rescaling, then train on other tasks and decode.
import numpy as np, sys
rng=np.random.default_rng(0)
D,H,K=20,256,5
def task(seed,n=2000):
    r=np.random.default_rng(seed); W=r.normal(size=(D,K)); X=r.normal(size=(n,D)); y=np.argmax(X@W+0.5*r.normal(size=(n,K)),1); return X,y
def fwd(P,X):
    h=X@P['W1']+P['b1']; a=np.maximum(h,0); return h,a,a@P['W2']+P['b2']
def loss_grad(P,X,y):
    h,a,o=fwd(P,X); o=o-o.max(1,keepdims=True); p=np.exp(o); p/=p.sum(1,keepdims=True)
    n=len(y); L=-np.log(p[np.arange(n),y]+1e-12).mean(); g=p; g[np.arange(n),y]-=1; g/=n
    G={'W2':a.T@g,'b2':g.sum(0)}; da=g@P['W2'].T*(h>0); G['W1']=X.T@da; G['b1']=da.sum(0); return L,G
def acc(P,X,y): return (fwd(P,X)[2].argmax(1)==y).mean()
def bal(P): return (P['W1']**2).sum(0)+P['b1']**2-(P['W2']**2).sum(1)
def train(P,X,y,steps,lr,opt='sgd',wd=0.0,bs=64,seed=0):
    r=np.random.default_rng(seed); m={k:0*v for k,v in P.items()}; v2={k:0*v for k,v in P.items()}
    for t in range(1,steps+1):
        idx=r.integers(0,len(y),bs); _,G=loss_grad(P,X[idx],y[idx])
        for k in P:
            g=G[k]+wd*P[k]
            if opt=='sgd': P[k]-=lr*g
            else:
                m[k]=0.9*m[k]+0.1*g; v2[k]=0.999*v2[k]+0.001*g*g
                P[k]-=lr*(m[k]/(1-0.9**t))/(np.sqrt(v2[k]/(1-0.999**t))+1e-8)
    return P
def write(P,target):
    # choose c_i>0: c^2 a - b/c^2 = target  -> a u^2 - target u - b=0, u=c^2
    a=(P['W1']**2).sum(0)+P['b1']**2; b=(P['W2']**2).sum(1)
    u=(target+np.sqrt(target**2+4*a*b))/(2*a); c=np.sqrt(u)
    P['W1']*=c; P['b1']*=c; P['W2']/=c[:,None]; return P
def run(opt,lr,wd,steps):
    P={'W1':rng.normal(size=(D,H))/np.sqrt(D),'b1':np.zeros(H),'W2':rng.normal(size=(H,K))/np.sqrt(H),'b2':np.zeros(K)}
    XA,yA=task(1); P=train(P,XA,yA,2000,0.05)
    payload=np.sign(np.random.default_rng(7).normal(size=H))  # 1 bit per unit
    accA0=acc(P,XA,yA); before=fwd(P,XA)[2].copy()
    P=write(P,payload*1.0)
    fn_err=np.abs(fwd(P,XA)[2]-before).max()
    for s in (2,3,4):
        X,y=task(s); P=train(P,X,y,steps,lr,opt,wd,seed=s)
    dec=bal(P); bits=(np.sign(dec)==payload).mean(); corr=np.corrcoef(dec,payload)[0,1]
    # control: same pipeline without writing -> what does balancedness look like
    print(f"{opt:4s} lr={lr} wd={wd} steps/task={steps}: write fn_err={fn_err:.1e} accA {accA0:.2f}->{acc(P,XA,yA):.2f} bit-acc={bits:.3f} corr={corr:.3f}")
for opt,lr,wd in [('sgd',0.05,0),('sgd',0.2,0),('sgd',0.05,1e-3),('adam',1e-3,0)]:
    run(opt,lr,wd,3000)
print("--- amplitude sweep + non-conserved baseline (bits in sign of col-norm deviation)")
def run2(opt,lr,amp,steps):
    P={'W1':rng.normal(size=(D,H))/np.sqrt(D),'b1':np.zeros(H),'W2':rng.normal(size=(H,K))/np.sqrt(H),'b2':np.zeros(K)}
    XA,yA=task(1); P=train(P,XA,yA,2000,0.05)
    payload=np.sign(np.random.default_rng(7).normal(size=H))
    nat=bal(P).copy()
    P=write(P,nat+payload*amp)   # differential encoding relative to natural spread
    ref=bal(P)-payload*amp       # decoder doesn't know nat; use zero-ref below
    # baseline: non-conserved statistic s_i = ||W1_i||^2 (function-changing write is not allowed, so mimic by reading the same stat)
    n1=(P['W1']**2).sum(0)
    for s in (2,3,4):
        X,y=task(s); P=train(P,X,y,steps,lr,opt,0,seed=s)
    d=bal(P)-nat; bitc=(np.sign(d)==payload).mean()
    dn=(P['W1']**2).sum(0)-n1+payload*amp; bitn=(np.sign(dn)==payload).mean()
    print(f"{opt} amp={amp}: conserved-channel bit-acc={bitc:.3f} | W1-norm channel bit-acc={bitn:.3f} | spread of nat bal={nat.std():.3f}")
for amp in (0.3,0.1,0.03):
    run2('sgd',0.05,amp,3000); run2('adam',1e-3,amp,3000)
