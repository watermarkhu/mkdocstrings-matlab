classdef moduleClass < handle
% Docstring for moduleClass.

    properties
        class_property = 42
        % Docstring for moduleClass.class_property.

        instance_property
        % Docstring for moduleClass.instance_property.
    end

    methods
        function obj = moduleClass(a, b)
        % Docstring for moduleClass constructor.
        obj.instance_property = a + b;
        end

        function method1(obj, a, b)
        % Docstring for moduleClass.method1.
        end

        function method2(obj, a, b)
        % Docstring for moduleClass.method2.
        end
    end

    methods (Access = private)
        function private_method(obj)
        % Private method docstring.
        end
    end
end
