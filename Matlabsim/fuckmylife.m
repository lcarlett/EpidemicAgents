function out = SIR_ODE(t,Y,b,d,N,lambda,g)
 out = [b*N - lambda*Y(1) - d*Y(1), lambda*Y(1) - g*Y(2) - d*Y(2), g*Y(2) - d*Y(3)]';