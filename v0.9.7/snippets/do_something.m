function do_something(whatever)
% Do something.
%
% Parameters:
%     whatever: Some integer.
    arguments
        whatever (1,1) double {mustBeInteger} = 1 % A integer
    end
end
