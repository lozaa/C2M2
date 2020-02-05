function robot_steering_controls

%Simulation of a robot following a straight line for purposes of testing accuracy of P/D coefficients.
%Originally authored by Dr Seibold, modified by Aidan Loza

% Robot equations      ----> linearization
% dx/dt     = v*cos(theta) ----> v
% dy/dt     = v*sin(theta) ----> v*theta
% dtheta/dt = v/l*tan(phi) ----> v/l*phi
% dphi/dt = u = alpha*ys + beta*dy/ds
% Here ys = y+ls*sin(theta) is the distance
% from y=0 measured at the sensor.

% Robot parameters
v = .1; % robot speed [m/s]
l = .1; % robot wheel base [m]
ls = .12; % distance rear axle to sensor [m]

% Study system matrix stability
na = 200; % number of values in alpha
nb = 200; % number of values in beta
va = linspace(-10,10,na); % alpha values
vb = linspace(-10,10,nb); % beta values
Mu = zeros(nb,na);
for ja = 1:na % loop over all alpha values
    for jb = 1:nb % loop over all beta values
        alpha = va(ja); beta = vb(jb);
        A = [0 v 0;0 0 v/l;alpha alpha*ls+beta*v beta*l/ls*v];
        mu = max(real(eig(A))); % largest real part of eigenvalues
        Mu(jb,ja) = mu;
    end
end

% Strongest decay parameters
[~,mi] = min(Mu(:));
[vA,vB] = meshgrid(va,vb);
alpha = vA(mi); beta = vB(mi);
A = [0 v 0;0 0 v/l;alpha alpha*ls+beta*v beta*l/ls*v];
eig(A)

% Plot control parameter space
clf
imagesc(va,vb,Mu)
hold on
contour(va,vb,Mu,[0,0],'r','LineWidth',2)
plot(alpha,beta,'r.','Markersize',20)
hold off
axis xy
grid on
xlabel('\alpha'), ylabel('\beta')
zlabel('max_j Re(\lambda_j)')
colorbar
