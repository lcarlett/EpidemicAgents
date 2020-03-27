#Population constants
b=0.01;     #birth rate: probability of a specific individual to birth another (fuck women we clone ourselves) in a generation
d=0.01;     #death rate: probability of a specific individual to yeet themselves from the living in a generation
N= 10000;     #initial population


#Disease constants
lambda=0.5;    #force of infection = 'probability that a specific susceptible individual gets sick after a generation'
g=0.02;        #recovery rate

#Initial conditions setup
I=  1  ;  #Initial number of ill individuals  #does not work as one would intuitively expec - this thing is fucking useless lmao
R=  0  ;    #Initial number of recovered/immunized individuals
S=  N-I;    #Initial number of susceptible individuals


#ODE parameters setup
t0 = 0 ;      #Initial time of the solution
tf = 200;     #Final time of the solution

tspan = [t0,tf];
Y0 = [S,I,R];


#ODE solving
[ti,uai] = ode45(@(t,Y) SIR_ODE(t,Y,b,d,N,lambda,g),tspan,Y0);


#Plot component of solution
figure
hold on;
title('SIR model simulations');
xlabel('time (days)');
ylabel('people');

plot( ti, uai(:,1), 'r');    #plot S
plot(ti,uai(:,2), 'g');      #plot I
plot(ti,uai(:,3), 'b');      #plot R
legend('Susceptible', 'Infected', 'Recovered')
