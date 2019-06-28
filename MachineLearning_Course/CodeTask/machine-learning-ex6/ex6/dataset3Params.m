function [C, sigma] = dataset3Params(X, y, Xval, yval)
%DATASET3PARAMS returns your choice of C and sigma for Part 3 of the exercise
%where you select the optimal (C, sigma) learning parameters to use for SVM
%with RBF kernel
%   [C, sigma] = DATASET3PARAMS(X, y, Xval, yval) returns your choice of C and 
%   sigma. You should complete this function to return the optimal C and 
%   sigma based on a cross-validation set.
%

% You need to return the following variables correctly.
C = 1;
sigma = 0.3;

% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return the optimal C and sigma
%               learning parameters found using the cross validation set.
%               You can use svmPredict to predict the labels on the cross
%               validation set. For example, 
%                   predictions = svmPredict(model, Xval);
%               will return the predictions on the cross validation set.
%
%  Note: You can compute the prediction error using 
%        mean(double(predictions ~= yval))
%
c = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30];
sigma = [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30];
errors = zeros(8,8);
trainingParams = zeros(64,1);
for(i = 1:length(c))
  for(j = 1:length(sigma))
    model= svmTrain(X, y, c(i), @(x1, x2) gaussianKernel(x1, x2, sigma(j)));
    visualizeBoundary(X, y, model);
    predictions = svmPredict(model, Xval);
    errors(i,j) = mean(double(predictions ~= yval));
    %trainingParams(i) = strcat(mat2str(sigma(j))," - ", mat2str(c(i)))
  end
end




[minErrorsPerColumn, irow] = min(errors);
[minGeneralError, icol] = min(minErrorsPerColumn);
plot(c, errors(:,irow(icol)),sigma,errors(icol,:));
fprintf('Program paused. Press enter to continue.\n');
pause;
c = c(irow(icol));
sigma = sigma(icol);


% =========================================================================

end
