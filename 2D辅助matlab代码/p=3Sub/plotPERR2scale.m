clc;
clear all
close all
meshData = load('meshXY6.mat');
meshXY = meshData.meshXY;

data2point_err = load('pERR2Scale.mat');
perr2scale = data2point_err.pERR2s2ReLU;

% %plot the solution in 3D with dot
% figure('name','utrue_dot')
% plot3(meshXY(1,:),meshXY(2,:),utrue, 'r.');
% hold on

figure('name', 'PERR2sscale_surf')
surfAndPlot_U(meshXY, perr2scale)
caxis([0 5e-4])
hold on