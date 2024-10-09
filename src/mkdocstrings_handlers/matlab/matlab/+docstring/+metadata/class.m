function data = class(object, opts)
    arguments
        object (1,1) % meta.class matlab.metadata.Class
        opts.builtin (1,1) logical = false
    end
    data.type = 'class';
    
    namespaces = split(object.Name, '.');
    data.name = namespaces{end};
    
    data.docstring = docstring.utils.parse_doc(object);
    data.hidden = object.Hidden;
    data.sealed = object.Sealed;
    data.abstract = object.Abstract;
    data.enumeration = object.Enumeration;
    data.properties = arrayfun(@(prop) docstring.metadata.property(prop), object.PropertyList);
    data.superclasses = arrayfun(@(o) string(o.Name), object.SuperclassList);
    data.handle = object.HandleCompatible;
    data.aliases = object.Aliases;
    if opts.builtin
        data.path = '';
    else
        data.path = matlab.internal.metafunction(object.Name).Location;
    end
    
    data.methods = [];
    for methodObject = object.MethodList'
        if any(strcmp(methodObject.Name, {'empty', 'forInteractiveUse'}))
            break
        else
            method.name = string(methodObject.Name);
            method.class = string(methodObject.DefiningClass.Name);
            if iscell(methodObject.Access)
                method.access = "private";
            else
                method.access = methodObject.Access;
            end
            method.static = methodObject.Static;
            method.abstract = methodObject.Abstract;
            method.sealed = methodObject.Sealed;
            method.hidden = methodObject.Hidden;
            data.methods = [data.methods, method];
        end
    end

    numProp = numel(object.PropertyList);

    nameparts = split(object.Name, '.');
    data.constructor = any(strcmp(nameparts(end), [data.methods.name]));

end
