function out = SIRS(t,Y,b,d,N,lambda,g,r)
out = [b*(Y(1)+Y(2)+Y(3)) - lambda*Y(1) - d*Y(1) + r*Y(3),    #susceptible people
          lambda*Y(1) - g*Y(2) - d*Y(2),                      #infectous people
          g*Y(2) - d*Y(3) - r*Y(3)];                          #recovered people
