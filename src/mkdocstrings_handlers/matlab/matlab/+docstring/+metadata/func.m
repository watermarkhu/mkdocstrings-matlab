function data = func(object)
    
    arguments
        object (1,1) % meta.MetaData matlab.metadata.MetaData
    end
    
    data.type = 'function';
    data.name = object.Name;
    data.docstring = docstring.utils.parse_doc(object);
    data.path = object.Location;
    
    data.inputs = docstring.metadata.argument(object.Signature.Inputs);
    data.outputs = docstring.metadata.argument(object.Signature.Outputs);
end
