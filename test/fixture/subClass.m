classdef SubClass < moduleClass
% Docstring for SubClass.

    properties
        instance_property = 100
        % Docstring for SubClass.instance_property.
    end

    methods
        function obj = SubClass(a, b)
        % SubClass constructor.
            obj@moduleClass(a, b);
        end
    end

    methods (Hidden)
        function hidden_method(obj)
        % Docstring for moduleClass.hidden_method.
        end
    end
end
