classdef (Hidden, Abstract=false, Sealed, (AllowedSubclasses = {?ClassName1,?ClassName2}) DocumentationFramework < handle & AbstractFramework
% DocumentationFramework - A class that represents the state of a documentation framework.
%
% This class provides a way to manage and organize documentation for a software project.
% It allows users to create, update, and retrieve documentation for different components
% of the project.
%
% Attributes:
%   projectName: The name of the software project.
%   components: A cell array containing the names of the components in the project.
%   documentation: A struct that stores the documentation for each component.
%
% Methods:
%   addComponent: Adds a new component to the documentation framework.
%   updateDocumentation: Updates the documentation for a specific component.
%   getDocumentation: Retrieves the documentation for a specific component.
%
% ## Example
% 
% ```matlab
%  % Create a new documentation framework
%  framework = DocumentationFramework('MyProject');
%  % Add a component to the framework
%  framework.addComponent('Component1');
%  % Update the documentation for the component
%  framework.updateDocumentation('Component1', 'This is the documentation for Component1.');
%  % Retrieve the documentation for the component
%  doc = framework.getDocumentation('Component1');
% ```

    enumeration
        foo
        bar
    end
    
    properties (Access = public)
        projectName (1,:) char = 'foo'
            % The name of the software project
        components 
            % A cell array containing the names of the components in the project
        documentation (1,1) string {mustBeText} = "fdsa" % Doc
            % A struct that stores the documentation for each component
    end
    properties (Dependent)
        projectSummary
    end


    methods (Static, Access = public)
        function obj = DocumentationFramework(projectName)
            % DocumentationFramework - Constructor for the DocumentationFramework class.
            %
            % Args:
            %   projectName: The name of the software project.
            %
            % Example:
            %   
            %   ```matlab 
            %   framework = DocumentationFramework('MyProject');
            %   ```

            obj.projectName = projectName;
            obj.components = {};
            obj.documentation = struct();
        end
        
        function addComponent(obj, componentName)
            % addComponent - Adds a new component to the documentation framework.
            %
            %   Syntax:
            %       addComponent(obj, componentName)
            %
            %   Inputs:
            %       - componentName: The name of the component to be added.
            %
            %   Example:
            %       framework.addComponent('Component1');
            
            obj.components = [obj.components, componentName];
            obj.documentation.(componentName) = '';
        end
        
        function updateDocumentation(obj, componentName, docString)
            % updateDocumentation - Updates the documentation for a specific component.
            %
            %   Syntax:
            %       updateDocumentation(obj, componentName, docString)
            %
            %   Inputs:
            %       - componentName: The name of the component to update the documentation for.
            %       - docString: The new documentation string for the component.
            %
            %   Example:
            %       framework.updateDocumentation('Component1', 'This is the updated documentation for Component1.');
            
            obj.documentation.(componentName) = docString;
        end
        
        function doc = getDocumentation(obj, componentName)
            % getDocumentation - Retrieves the documentation for a specific component.
            %
            %   Syntax:
            %       doc = getDocumentation(obj, componentName)
            %
            %   Inputs:
            %       - componentName: The name of the component to retrieve the documentation for.
            %
            %   Outputs:
            %       - doc: The documentation string for the component.
            %
            %   Example:
            %       doc = framework.getDocumentation('Component1');
            
            doc = obj.documentation.(componentName);
        end
    end

    methods
        function summary = get.projectSummary(obj)
            % get.projectSummary - Getter for the projectSummary property.
            %
            %   Outputs:
            %       - summary: A summary of the project, including the project name and the number of components.
            %
            %   Example:
            %       summary = framework.projectSummary;
            
            summary = sprintf('Project: %s, Number of components: %d', obj.projectName, numel(obj.components));
        end
        
        function set.projectSummary(obj, ~)
            % set.projectSummary - Setter for the projectSummary property.
            % This property is read-only and cannot be set directly.
            %
            %   Example:
            %       framework.projectSummary = 'New Summary'; % This will produce an error.
            
            error('projectSummary is a read-only property.');
        end
    end
end
