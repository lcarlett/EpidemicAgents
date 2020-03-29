a=0; #because fuck matlab

fileID = fopen('zizi.txt'); #rawdata est un vecteur colonne avec un coéfficient par composante;

rawdata = fscanf(fileID, '%f');

N= rawdata(1);            #initial population
lambda= rawdata(2);       #force of infection, linked in some way with R_0 (compute or y e e t ?)
g= rawdata(3);            #recovery rate
tf = rawdata(4);          #Final time of the solution (this sounds much more nazi that I tought it would)


if length(rawdata) > 4
try
  r=rawdata(5);             #immunization loss rate
  b = rawdata(6);           #birth rate
  d = rawdata(7);           #death rate
end
end

clear a;

try
SIS_ODE
SIR_ODE
SIRS_ODE
end
