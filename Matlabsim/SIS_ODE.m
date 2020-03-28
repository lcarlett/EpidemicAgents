#Population constants
b=0.001;     #birth rate: probability of a specific individual to birth another (fuck women we clone ourselves) in a generation
d=0.002;     #death rate: probability of a specific individual to yeet themselves from the living in a generation
N= 10000;    #initial population


#Disease constants
lambda=0.05;    #force of infection = 'probability that a specific susceptible individual gets sick after a generation'
g=0.02;         #recovery rate


#Initial conditions setup
I=  1;      #Initial number of ill individuals  #does not work as one would intuitively expec - this thing is fucking useless lmao

S=  N-I;    #Initial number of susceptible individuals


#ODE parameters setup
t0 = 0;       #Initial time of the solution
tf = 200;     #Final time of the solution

tspan = [t0,tf];
Y0 = [S,I];


#ODE solving
[ti,uai] = ode45(@(t,Y) SIS(t,Y,b,d,N,lambda,g),tspan,Y0);


#Plot component of solution
figure
hold on;
title('SIS model simulations');
xlabel('time (days)');
ylabel('people');

plot(ti,uai(:,1), 'r');      #plot S
plot(ti,uai(:,2), 'g');      #plot I

legend('Susceptible', 'Infected')
