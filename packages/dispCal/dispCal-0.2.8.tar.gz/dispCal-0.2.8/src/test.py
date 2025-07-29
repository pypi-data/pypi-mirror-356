from disp import calDisp
from dispCal.disp import calDisp as calDispO
from disba import PhaseDispersion
from disba import Ellipticity
import numpy as np
thickness = np.array([1.,1.,1.,1.,1.])
periods=np.arange(1,10.,1)/10
vp = np.array([1.5,3.,4.,5.,6.])
vs = vp/1.71
#vs[0]=0
rho = vp*0+1

velocity_model = np.array([thickness,vp,vs,rho,]).transpose()
pd = PhaseDispersion(*velocity_model.T,dc=0.001)
pde = Ellipticity(*velocity_model.T)

#c0=calDisp(thickness,vp,vs,rho,periods,flat_earth=False)
#c1=calDispO(thickness,vp,vs,rho,periods,flat_earth=False)
c2 = pd(periods, mode=0, wave="rayleigh").velocity

e0=calDisp(thickness,vp,vs,rho,periods,flat_earth=False,velocity='ellipticity')
e2 = pde(periods, mode=0).ellipticity
#res0 = calDisp(thickness,vp,vs,rho,periods,velocity='kernel',parameter='vs')
#print(res0[:1])
#thickness = np.array([1/3,1/3,1/3,1.,1.,1.])
#periods=np.arange(1,10.)/10
#vp = np.array([1.5,1.5,1.5,3.,4.,5.])
#vs = vp/1.71
#vs[:3]=0
#rho = vp*0+1
#c1=(calDisp(thickness,vp,vs,rho,periods))
#res = calDisp(thickness,vp,vs,rho,periods,velocity='kernel',parameter='vs')
#print(res[:4])
#print(c2)
#print(c1-c0)
#print(c2-c0)

print(e0)
print(e2)
print(e2-e0)