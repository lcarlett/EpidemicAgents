#Population constants
b=1.03;     #birth rate
d=1.09;     #death rate
N=10000;    #initial population



#Disease constants
lambda=0.002;    #force of infection
g=0.75;           # ?????



#initial conditions for ODE specifically

S=  N-1; #Initial number of susceptible people
I=  1  ; #Initial number of ill people
R=  0  ; #Initial number of recovered/immunized people

#Time parameters
t0 = 0 ;      #Initial time of the solution
tf = 20;     #Final time of the solution



#RESOLUTION EQUATION DIFFERENTIELLE. DON TACCH
tspan = [t0,tf];
Y0 = [S,I,R];
[ti,uai] = ode23(@(t,Y) SIR_ODE(t,Y,b,d,N,lambda,g),tspan,Y0);



#Plot component of solution
#plot(ti,uai(:,1));      #plot S
#plot(ti,uai(:,2));      #plot I
#plot(ti,uai(:,3));      #plot R
l = 1;


while l <tf
  #plot3(uai(l,1),uai(l,2),uai(l,3),col ='green');
  #hold on;
  try
    scatter(uai(l,1));
    #scatter3(uai(l,:));
  end
  l = l+1;
  hold on;
#  pause(0.1);
  end
  #THE THING WORKS, BUT CONSTANTS ARE FULLY RANDOMIZED NONSENSE; PICK THEM CAREFULLY