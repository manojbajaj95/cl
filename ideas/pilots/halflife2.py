import numpy as np, scipy.linalg as sl
exec(open('halflife.py').read().split('XB,yB=task(2)')[0])
XB,yB=task(2); XA,yA=task(1,600)
P0=init(); sgd(P0,XB,yB,20000,0.2); print('B acc after pretrain',acc(P0,XB,yB))
def mom(X,y,n):
    M=np.zeros((D*H,D*H))
    for j in range(n):
        g=grads(P0,X[j:j+1],y[j:j+1])['W1'].ravel(); M+=np.outer(g,g)
    return M/n
MB=mom(XB,yB,1500); MA=mom(XA,yA,600)
w,V=sl.eigh(MA,MB+1e-6*np.trace(MB)/len(MB)*np.eye(len(MB))); V=V[:,np.argsort(w)[::-1]]
k=96
cands=[('gen-eig A/B top',np.linalg.qr(V[:,:k])[0]),('B-top',np.linalg.eigh(MB)[1][:,::-1][:,:k]),('A-top',np.linalg.eigh(MA)[1][:,::-1][:,:k]),('random',np.linalg.qr(rng.normal(size=(D*H,k)))[0])]
for name,U in cands:
    P={kk:v.copy() for kk,v in P0.items()}
    sgd(P,XA,yA,3000,0.5,proj=U,seed=3); a1=acc(P,XA,yA); b1=acc(P,XB,yB)
    tr=sgd(P,XB,yB,6000,0.2,seed=4,trace=500,XA=XA,yA=yA)
    print(f"{name:16s} A after write {a1:.2f}, B after write {b1:.2f}; A during B-training:",' '.join(f'{x:.2f}' for x in tr), f"| B end {acc(P,XB,yB):.2f}")
