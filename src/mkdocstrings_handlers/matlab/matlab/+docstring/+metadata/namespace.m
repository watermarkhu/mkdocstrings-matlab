function data = namespace(object)
    
    arguments
        object (1,1) matlab.metadata.Namespace
    end
    
    data.type = 'namespace';
    data.docstring = docstring.utils.parse_doc(object);

    data.classes = arrayfun(@(o) string(o.Name), object.ClassList);
    data.functions = arrayfun(@(o) string(o.Name), object.FunctionList);
    data.namespaces = arrayfun(@(o) string(o.Name), object.InnerNamespaces);
    data.path = docstring.utils.get_namespace_path(object);
end
