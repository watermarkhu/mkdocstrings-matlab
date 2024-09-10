function data = argument(object)
    arguments
        object (1,:) matlab.internal.metadata.Argument
    end

    if isempty(object)
        data = struct.empty();
        return
    elseif numel(object) > 1
       for iArg = numel(object):-1:1
           data(iArg) = docstring.metadata.argument(object(iArg));
       end
       return
    end 

    data.name = object.Name;
    data.kind = string(object.Kind);
    data.presence = string(object.Presence);

    if contains(data.presence, ["required", "unspecified"])
        data.default = "";
    else
        if ~isempty(object.DefaultValue) && object.DefaultValue.IsConstant
            value = object.DefaultValue.Value;
            if isstring(value) 
                data.default = sprintf("""%s""", value);
            elseif ischar(value)
                data.default = sprintf("'%s'", value);
            else
                data.default = string(value);
            end
        else
            data.default = "...";
        end
    end
    
    if ~isempty(object.Validation)
        if ~isempty(object.Validation.Class)
            data.class = string(object.Validation.Class.Name);
        else
            data.class = "";
        end
        if ~isempty(object.Validation.Size)
            for iSize = numel(object.Validation.Size):-1:1

                if isprop(object.Validation.Size(iSize), 'Length')
                    data.size(iSize) = object.Validation.Size(iSize).Length;
                else
                    data.size(iSize) = ":";
                end
            end
        else
            data.size = "";
        end

        if ~isempty(object.Validation.Functions)
            data.validators = arrayfun(@(f) string(f.Name), object.Validation.Functions);
        else
            data.validators = "";
        end
    else
        data.class = "";
        data.size = "";
        data.validators = "";
    end

end
