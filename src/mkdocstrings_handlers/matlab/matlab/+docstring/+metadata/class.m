function data = class(object)
    arguments
        object (1,1) % meta.class matlab.metadata.Class
    end
    data.type = 'class';
    
    namespaces = split(object.Name, '.');
    data.name = namespaces{end};
    
    data.docstring = docstring.utils.parse_doc(object);
    data.path = matlab.internal.metafunction(object.Name).Location;
    data.hidden = object.Hidden;
    data.sealed = object.Sealed;
    data.abstract = object.Abstract;
    data.enumeration = object.Enumeration;
    data.superclasses = arrayfun(@(o) string(o.Name), object.SuperclassList);
    data.handle = object.HandleCompatible;
    data.aliases = object.Aliases;
    
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
    for iProp = numProp:-1:1
        data.properties(iProp) = docstring.metadata.property(object.PropertyList(iProp));
    end

    nameparts = split(object.Name, '.');
    data.constructor = any(strcmp(nameparts(end), [data.methods.name]));

end
