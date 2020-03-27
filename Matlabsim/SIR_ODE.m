function out = SIR_ODE(t,Y,b,d,N,lambda,g)


out = [b*Y(1) - lambda*Y(1) - d*Y(1), lambda*Y(1) - g*Y(2) - d*Y(2), g*Y(2) - d*Y(3)]';
 #out = [b*(Y(1)+Y(2)+Y(3)) - lambda*Y(1) - d*Y(1), lambda*Y(1) - g*Y(2) - d*Y(2), g*Y(2) - d*Y(3), r*Y(2)]'; version where infective people can either recover or die
