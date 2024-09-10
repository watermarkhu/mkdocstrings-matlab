function data = property(object)
    arguments
        object (1,:) meta.property
    end

    data.name = string(object.Name);
    data.class = string(object.DefiningClass.Name);
    data.docstring = docstring.utils.parse_doc(object);

    if iscell(object.GetAccess)
        data.get_access = 'private';
    else
        data.get_access = object.GetAccess;
    end
    if iscell(object.SetAccess)
        data.set_access = 'private';
    else
        data.set_access = object.SetAccess;
    end
    data.dependent = object.Dependent;
    data.constant = object.Constant;
    data.abstract = object.Abstract;
    data.transient = object.Transient;
    data.hidden = object.Hidden;

    if ~isempty(object.Validation) && ~isempty(object.Validation.Class)
        data.annotation = string(object.Validation.Class.Name);
    else
        data.annotation = "";
    end

    if ~isempty(object.Validation) && ~isempty(object.Validation.Size)
        for iSize = numel(object.Validation.Size):-1:1
            if isprop(object.Validation.Size(iSize), 'Length')
                sizeStr(iSize) = string(object.Validation.Size(iSize).Length);
            else
                sizeStr(iSize) = ":";
            end
        end
        data.size = sprintf("[%s]", join(sizeStr, ","));
    else
        data.size = "";
    end

    if ~isempty(object.Validation) && ~isempty(object.Validation.ValidatorFunctions)
        data.validation = join(cellfun(@(f) string(char(f)), object.Validation.ValidatorFunctions), ", ");
    else
        data.validation = "";
    end
end
