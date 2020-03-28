function out = SIS(t,Y,b,d,N,lambda,g)

out = [b*(Y(1)+Y(2)) - lambda*Y(1) - d*Y(1) + g*Y(2), #susceptible people
        lambda*Y(1) - g*Y(2) - d*Y(2)];               #infectous people
