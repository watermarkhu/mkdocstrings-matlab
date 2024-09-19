function [jsonString, data] = resolve(identifier, cwd)
% Resolve the docstring for a given MATLAB entity
%
% ```matlab
% jsonString = resolve(name, cwd)
% ```
%
% Parameters:
%   identifier (string): Name of the MATLAB entity
%   cwd (string): Current working directory
%
% Returns:
%   jsonString(string): JSON-encoded metadata object
%   data(struct): metadata object

arguments
    identifier (1, :) char
    cwd (1,1) string {mustBeFolder} = pwd()
end

if isempty(identifier)
    docstring.exception("<empty>");
end

cd(cwd);

% Check if namespace
if strcmp(identifier(1), '+')
    data = docstring.case.namespace(identifier);
    jsonString = jsonencode(data);
    return;
end

% Try namespace functions
if contains(identifier, '.')
    object = matlab.internal.metafunction(identifier);
    if ~isempty(object) && isa(object, 'matlab.internal.metadata.Function')
        if isempty(object.Signature)
            data = docstring.metadata.script(object);
        else
            data = docstring.metadata.func(object);
        end
        jsonString = jsonencode(data);
        return;
    end
end

% Try built-in aliases with which
if contains(which(identifier), {' built-in ', matlabroot})
    data = docstring.case.builtin(identifier);
    jsonString = jsonencode(data);
    return
end

switch exist(identifier) %#ok<EXIST>
    case 2
        % if NAME is a file with extension .m, .mlx, .mlapp, or .sfx, or NAME
        % is the name of a file with a non-registered file extension 
        % (.mat, .fig, .txt).

        % Try with metafunction
        object = matlab.internal.metafunction(identifier);
        if ~isempty(object)
            if isa(object, 'matlab.internal.metadata.Function')
                if isempty(object.Signature)
                    data = docstring.metadata.script(object);
                else
                    data = docstring.metadata.func(object);
                end
                data.name = identifier;
            elseif isa(object, 'matlab.internal.metadata.Method')
                data = docstring.case.class(identifier);
            else
                docstring.exception(identifier);
            end
        else
            docstring.exception(identifier);
        end
    case 5
        % if NAME is a built-in MATLAB function. This does not include classes
        data = docstring.case.builtin(identifier);
    case 8
        % if NAME is a class (exist returns 0 for Java classes if you
        % start MATLAB with the -nojvm option.)
        data = docstring.case.class(identifier);
    case 0
        if contains(identifier, '.')
            nameparts = split(identifier, '.');
            tryclassname = strjoin(nameparts(1:end-1), '.');
            if exist(tryclassname, 'class')
                data = docstring.case.method(identifier);
            else
                docstring.exception(identifier);
            end
        else
            docstring.exception(identifier);
        end
    otherwise
        docstring.exception(identifier);
end

jsonString = jsonencode(data);

end
