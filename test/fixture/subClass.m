classdef SubClass < moduleClass
% Docstring for SubClass.

    methods
        function obj = SubClass(a, b)
        % SubClass constructor.
            obj@moduleClass(a, b);
        end
    end
end
