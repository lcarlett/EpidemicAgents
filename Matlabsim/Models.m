file = fopen('../Matlabsim/values.txt', 'r');
formatSpec = '%f';
values = fscanf(file, formatSpec);
fclose(file);

#Population constants
b=values(2);     #birth rate: probability of a specific individual to birth another (fuck women we clone ourselves) in a generation
d=values(3);     #death rate: probability of a specific individual to yeet themselves from the living in a generation
N=values(4);     #initial population


#Disease constants
lambda=values(5);    #force of infection = 'probability that a specific susceptible individual gets sick after a generation'
g=values(6)     ;    #recovery rate
r=values(7)     ;    #immunization loss rate


#Initial conditions setup
I=  values(8)  ;    #Initial number of ill individuals  #does not work as one would intuitively expec-this thing is fucking useless lmao
R=  values(9)  ;    #Initial number of recovered/immunized individuals
S=  N-I;    #Initial number of susceptible individuals


#ODE parameters setup
t0 = 0  ;     #Initial time of the solution
tf = 200;     #Final time of the solution

tspan = [t0,tf];
if (values(1) != 0)
    Y0 = [S,I,R];
else
    Y0 = [S, I];
endif

#ODE solving
switch(values(1))
    case 0
        [ti,uai] = ode45(@(t,Y) SIS(t,Y,b,d,N,lambda,g),tspan,Y0);
        tit = 'SIS model simulations';
    case 1
        [ti,uai] = ode45(@(t,Y) SIRS(t,Y,b,d,N,lambda,g,r),tspan,Y0);
        tit = 'SIRS model simulations';
    case 2
        [ti,uai] = ode45(@(t,Y) SIR(t,Y,b,d,N,lambda,g),tspan,Y0);
        tit = 'SIR model simulations';
        
endswitch
#Plot component of solution
figure;
hold on;
title(tit);
xlabel('time (days)');
ylabel('people');

plot(ti,uai(:,1), 'r');      #plot S
plot(ti,uai(:,2), 'g');      #plot I
if (values(1) != 0)
    plot(ti,uai(:,3), 'b');      #plot R
    legend('Susceptible', 'Infected', 'Recovered');
else
    legend('Susceptible', 'Infected');
endif
saveas(gcf, "result.png");
 

