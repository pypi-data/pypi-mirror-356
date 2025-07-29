from collections import defaultdict
from typing import List
from copy import deepcopy
import warnings
from dataclasses import dataclass
from typing import Optional, Any
import inspect
from inspect import getdoc



@dataclass
class Field:
    name: str
    doc: str
    default: Any = None
    required: bool = True


class StepMeta(type):
    """
    Metaclass for registering and tracking subclasses in a workflow system.

    This metaclass automatically registers any class that uses it and maintains:
    - A registry of all registered class names and their corresponding class objects.
    - A map of subclass relationships, tracking which subclasses derive from which parents.
    - A record of root path locations for each registered class (e.g., for serialization or lookup).

    Attributes
    ----------
    registry : dict of str to type
        Maps class names to the corresponding class objects.

    subclass_map : defaultdict of set
        Maps parent class names to a set of subclass names.

    root_path : dict of str to list
        Maps class names to a list representing their associated root path (purpose may vary).

    Examples
    --------
    >>> class MyStep(metaclass=StepMeta):
    ...     pass

    >>> 'MyStep' in StepMeta.registry
    True
    """
    registry = {}                    # name -> class
    subclass_map = defaultdict(set)  # parent_name -> {subclass_name}
    root_path = {}                   # name -> [path]

    def __new__(cls, name, bases, namespace):
        # --- Merge inputs/outputs/params ---
        def merge_fields(attr):
            merged = []
            seen = set()
            # Accumulate fields from all bases, in MRO order
            for base in reversed(bases):
                for f in getattr(base, attr, []):
                    if f.name not in seen:
                        merged.append(f)
                        seen.add(f.name)
            # Add/override with this class's definitions
            for f in namespace.get(attr, []):
                if f.name not in seen:
                    merged.append(f)
                    seen.add(f.name)
            return merged

        for attr in ("inputs", "outputs", "params"):
            namespace[attr] = merge_fields(attr)

        # --- Create class ---
        new_cls = super().__new__(cls, name, bases, namespace)

        # --- Register in registry ---
        step_name = namespace.get("name")
        if step_name:
            if step_name in cls.registry:
                old_cls = cls.registry[step_name]
                if (old_cls.__qualname__ != new_cls.__qualname__
                    or old_cls.__module__ != new_cls.__module__):
                    raise ValueError(f"A step with name {step_name} already exists, please pick another one.")
            cls.registry[step_name] = new_cls

            # Register subclass relationships
            bases_names = []
            for base in bases:
                parent_name = getattr(base, "name", None)
                if parent_name:
                    cls.subclass_map[parent_name].add(step_name)
                    bases_names.append(parent_name)

            cls.root_path[step_name] = bases_names

        return new_cls

    @classmethod
    def get_step_class(cls, name: str) -> type:
        """
        Retrieve a registered step class by name.

        Parameters
        ----------
        name : str
            The name of the step class to retrieve.

        Returns
        -------
        type
            The class object associated with the given name.

        Raises
        ------
        ValueError
            If no class is registered under the given name.
        """
        if name not in cls.registry:
            raise ValueError(f"Could not find a step registered with name: {name}")
        return cls.registry[name]

    @classmethod
    def list_subclasses(cls, name: str) -> List[str]:
        """
        List the names of all subclasses registered under a given parent class name.

        Parameters
        ----------
        name : str
            The name of the parent class.

        Returns
        -------
        list of str
            A list of subclass names registered under the specified parent.
        """
        return [subname for subname in cls.subclass_map.get(name, [])]


def get_step_class(name: str) -> type:
    """Retrieves a step class from the registry by name."""
    return StepMeta.get_step_class(name)


def list_subclasses(name: str) -> List[str]:
    """Lists all subclasses of a given step class by name."""
    return StepMeta.list_subclasses(name)


def get_full_path_from_class(class_name: str) -> List[str]:
    """
    Compute all hierarchical paths from a given class name to its leaf subclasses.

    This function returns all possible inheritance paths starting from the given class name,
    using the subclass relationships tracked in StepMeta. Each path is a list of class names
    representing a chain from the specified class to a leaf subclass.

    Parameters
    ----------
    class_name : str
        The name of the root class from which to compute inheritance paths.

    Returns
    -------
    list of list of str
        A list of paths, where each path is a list of class names from the root to a leaf subclass.
    """
    root_path = deepcopy(StepMeta.root_path.get(class_name, []))
    root_path.append(class_name)

    # Find all paths from current class to leaves
    def find_paths_from_class(current_class, path):
        subclasses = list_subclasses(current_class)
        if not subclasses:
            yield path
        for subclass in subclasses:
            yield from find_paths_from_class(subclass, path + [subclass])

    # Find all paths from class_name to leaves
    result = []
    for path_from_cls in find_paths_from_class(class_name, []):
        result.append(root_path + path_from_cls)

    return result


class Step(metaclass=StepMeta):
    """
    Base class for defining reusable processing steps in a workflow.

    A `Step` declares the input and output fields it expects and produces. 
    Subclasses must implement the `_execute` method to define the step's logic. 
    Input validation is performed before execution to ensure all required fields are present.

    Attributes
    ----------
    name : str or None
        A unique identifier for the step. Must be set by subclasses.

    inputs : set of str
        The set of input field names this step expects.

    outputs : set of str
        The set of output field names this step will produce.

    logged_metrics : dict
        Optional dictionary for storing metrics during execution. Useful for logging or tracking.

    Notes
    -----
    - Steps must be registered by subclassing `Step`, which uses the `StepMeta` metaclass.
    - Subclasses should define `name`, `inputs`, `outputs`, and implement `_execute(self, inputs, **params) -> dict`.
    - Output validation is optional; strict mode can be added to enforce it.
    """
    # Must be defined in subclasses
    name = None
    inputs: list[Field] = []
    outputs: list[Field] = []
    params: list[Field] = []

    def __init__(self, **kwargs):
        """
        Initialize a Step with declared input and output field names.

        Parameters
        ----------
        inputs : list of str, optional
            The list of input field names this step expects. Defaults to an empty list.

        outputs : list of str, optional
            The list of output field names this step is expected to produce. Defaults to an empty list.
        """
        for field in self.params:
            value = kwargs.get(field.name, field.default)
            self.set_parameter(field.name, value)

        self._returned_outputs = {}
        self.logged_metrics = {}
        self.namespace = None


    def set_parameter(self, name, value):
        for field in self.params:
            if field.name == name:
                setattr(self, field.name, value)
                return
        else:
            raise ValueError(f'Unknown parameter {name} for step {self.name}')

    def set_namespace(self, namespace):
        self.namespace = namespace

    def get_inputs_outputs(self):
        inputs = set(field.name for field in self.inputs if (field.required and field.default is None))
        outputs = set(field.name for field in self.outputs)
        if self.namespace:
            inputs = set([f'{key}_{self.namespace}' for key in inputs])
            outputs = set([f'{key}_{self.namespace}' for key in outputs])
        return inputs, outputs

    def run(self, inputs: dict[str, any]) -> dict[str, any]:
        """
        Execute the step by applying the internal `_execute` method with input validation.

        Parameters
        ----------
        inputs : dict of str to any
            A dictionary mapping input field names to their values.

        Returns
        -------
        dict of str to any
            A dictionary containing the step's output fields.

        Raises
        ------
        KeyError
            If any of the required input fields are missing.

        Notes
        -----
        - The actual computation is delegated to the `_execute` method, which must be implemented in a subclass.
        - If `returned_outputs` is used during `_execute`, it will be merged into the final output.
        """

        # Resolve inputs with optional namespace and default values
        resolved_inputs = {}

        for field in self.params:
            if not hasattr(self, field.name):
                raise ValueError(f"Missing required parameter: {field.name}")

        for field in self.inputs:
            # Determine the expected key in the input dict
            input_key = f"{field.name}_{self.namespace}" if self.namespace else field.name

            if input_key in inputs:
                resolved_inputs[field.name] = inputs[input_key]
            elif field.default is not None:
                resolved_inputs[field.name] = field.default
            elif field.required:
                ns_msg = f" with namespace '{self.namespace}'" if self.namespace else ""
                raise KeyError(f"[Step {self.name}] Missing required input field{ns_msg}: '{input_key}'")

        namespaced_inputs = resolved_inputs

        # Initialize the outputs
        self._returned_outputs = {}
        self.logged_metrics = {}

        # Execute the step
        fun_outputs = self._execute(namespaced_inputs)
        if fun_outputs is not None:
            warnings.warn(f'[Step {self.name}] Method _execute should return nothing.')

        # Prepare outputs with namespace suffix
        base_outputs = self._returned_outputs
        if self.namespace:
            namespaced_outputs = {
                f"{k}_{self.namespace}": v for k, v in base_outputs.items()
            }
        else:
            namespaced_outputs = base_outputs

        # Optionally: check for unexpected outputs
        unexpected = set(base_outputs.keys()) - set(field.name for field in self.outputs)
        # if unexpected:
        #     raise ValueError(f"Step produced unexpected fields: {unexpected}")

        # Clean up
        self._returned_outputs = {}

        return namespaced_outputs


    def output(self, name: str, value: object):
        """
        Store a data field to be returned at the end of the execution.

        Parameters
        ----------
        name : str
            The name associated with the data to be returned.
        
        value : object
            The data object to store. Can be any serializable Python object.

        """
        self._returned_outputs[name] = value

    def log_metric(self, name: str, value: object):
        """
        Log a metric for later inspection or reporting.

        Parameters
        ----------
        name : str
            The name of the metric to log.
        
        value : object
            The value of the metric. Typically a float or int, but can be any serializable object.

        Returns
        -------
        None
        """
        self.logged_metrics[name] = value

    def _execute(self, inputs: dict) -> dict:
        """
        Subclasses must override this method to implement step logic.
        It must return a dict containing only the produced fields.
        """
        raise NotImplementedError("Subclasses must implement _execute.")
    
    @classmethod
    def list_variants(self_or_cls):
        """
        List sibling step variants if this step is a leaf class.

        This method helps users explore alternative implementations (variants) of the same abstract step.
        If called on a non-leaf step, it warns the user and still shows its known subclasses.

        Returns
        -------
        None
        """

        # Determine if called from class or instance
        if isinstance(self_or_cls, type):
            cls = self_or_cls
        else:
            cls = self_or_cls.__class__

        step_name = cls.name
        if not step_name:
            print(f"[{cls.__name__}] has no 'name' defined.")
            return

        # Check if the current step is a leaf class
        children = StepMeta.subclass_map.get(step_name, [])
        if children:
            print(f"[{step_name}] is not a leaf step. This method is intended to be used on leaf steps.")
            print(f"Known variants (subclasses of {step_name}):")
            for child in sorted(children):
                cls = StepMeta.registry.get(child)
                doc = getdoc(cls) or ""
                first_line = doc.splitlines()[0] if doc else "(No docstring)"
                print(f"- {cls.__name__} (name='{cls.name}'): {first_line}")
            return

        # Not a parent — list siblings
        parent_names = StepMeta.root_path.get(step_name, [])
        if not parent_names:
            print(f"No known parent found for [{step_name}], cannot list variants.")
            return

        parent = parent_names[-1]  # Closest direct parent
        siblings = StepMeta.subclass_map.get(parent, set())
        print(f"Step [{step_name}] is a leaf step. Listing sibling variants from parent [{parent}]:")
        for sibling in sorted(siblings):
            cls = StepMeta.registry.get(sibling)
            doc = getdoc(cls) or ""
            first_line = doc.splitlines()[0] if doc else "(No docstring)"
            print(f"- {cls.__name__} (name='{cls.name}'): {first_line}")

    @classmethod
    def describe(self_or_cls) -> str:
        import inspect

        # Determine if called from class or instance
        if isinstance(self_or_cls, type):
            cls = self_or_cls
        else:
            cls = self_or_cls.__class__

        doc = inspect.getdoc(cls) or ""
        summary = doc.split("\n", 1)[0] if doc else "No summary available."

        def format_field(field: Field) -> str:
            line = f"- {field.name}: {field.doc or 'No description'}"
            if not field.required or field.default is not None:
                line += " (optional)"
            return line

        inputs_section = "\n".join(format_field(f) for f in cls.inputs)
        outputs_section = "\n".join(format_field(f) for f in cls.outputs)
        params_section = "\n".join(format_field(f) for f in cls.params)

        return f"""{summary}

Inputs:
{inputs_section or '  None'}

Outputs:
{outputs_section or '  None'}

Parameters:
{params_section or '  None'}"""