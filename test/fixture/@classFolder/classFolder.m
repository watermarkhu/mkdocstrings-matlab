classdef TestClass
    properties
        class_property = 42
    end

    methods
        function obj = TestClass(a, b)
            obj.instance_property = a + b;
        end

        function method1(obj, a, b)
        end
    end
end
