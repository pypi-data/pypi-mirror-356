from tespy.tools.helpers import _get_dependents
from tespy.connections import Connection
from tespy.tools.helpers import _get_vector_dependents
from tespy.tools.helpers import _partial_derivative
from tespy.tools.helpers import _partial_derivative_vecvar
from tespy.tools.logger import logger
from tespy.components.component import Component
from tespy.tools.data_containers import FluidProperties as dc_prop
from tespy.tools.helpers import TESPyConnectionError
import numpy as np


class PowerConnection(Connection):

    def __init__(self, source, outlet_id, target, inlet_id, label=None, **kwargs):
        self._check_types(source, target)
        self._check_self_connect(source, target)
        self._check_connector_id(source, outlet_id, source.poweroutlets())
        self._check_connector_id(target, inlet_id, target.powerinlets())

        self.label = f"{source.label}:{outlet_id}_{target.label}:{inlet_id}"
        if label is not None:
            self.label = label
            if not isinstance(label, str):
                msg = "Please provide the label as string."
                logger.error(msg)
                raise TypeError(msg)

        # set specified values
        self.source = source
        self.source_id = outlet_id
        self.target = target
        self.target_id = inlet_id

        # defaults
        self.new_design = True
        self.design_path = None
        self.design = []
        self.offdesign = []
        self.local_design = False
        self.local_offdesign = False
        self.printout = True

        # set default values for kwargs
        self.property_data = self.get_parameters()
        self.parameters = {
            k: v for k, v in self.get_parameters().items()
            if hasattr(v, "func") and v.func is not None
        }
        self.__dict__.update(self.property_data)
        msg = (
            f"Created connection from {self.source.label} ({self.source_id}) "
            f"to {self.target.label} ({self.target_id})."
        )
        logger.debug(msg)

    def _check_types(self, source, target):
        # check input parameters
        if not (isinstance(source, Component) and
                isinstance(target, Component)):
            msg = (
                "Error creating connection. Check if source and target are "
                "tespy.components."
            )
            logger.error(msg)
            raise TypeError(msg)

    def _check_self_connect(self, source, target):
        if source == target:
            msg = (
                "Error creating connection. Cannot connect component "
                f"{source.label} to itself."
            )
            logger.error(msg)
            raise TESPyConnectionError(msg)

    def _check_connector_id(self, component, connector_id, connecter_locations):
        if connector_id not in connecter_locations:
            msg = (
                "Error creating connection. Specified connector for "
                f"{component.label} of class {component.__class__.__name__} "
                f"({connector_id})  is not available. Select one of the "
                f"following connectors {', '.join(connecter_locations)}."
            )
            logger.error(msg)
            raise ValueError(msg)

    def _precalc_guess_values(self):
        pass

    def _presolve(self):
        return []

    def _prepare_for_solver(self, system_dependencies, eq_counter):
        self.num_eq = 0
        self.it = 0
        self.equations = {}
        self._equation_lookup = {}
        self._equation_scalar_dependents_lookup = {}
        self._equation_vector_dependents_lookup = {}

        for eq_num, value in self._equation_set_lookup.items():
            if eq_num in system_dependencies:
                continue

            if value not in self.equations:
                data = self.parameters[value]
                self.equations.update({value: data})
                self._assign_dependents_and_eq_mapping(
                    value, data, self.equations, eq_counter
                )
                self.num_eq += data.num_eq
                eq_counter += data.num_eq

        self.residual = {}
        self.jacobian = {}

        return eq_counter

    def _assign_dependents_and_eq_mapping(self, value, data, eq_dict, eq_counter):
        if data.dependents is None:
            scalar_dependents = [[] for _ in range(data.num_eq)]
            vector_dependents = [{} for _ in range(data.num_eq)]
        else:
            dependents = data.dependents(**data.func_params)
            if type(dependents) == list:
                scalar_dependents = _get_dependents(dependents)
                vector_dependents = [{} for _ in range(data.num_eq)]
            else:
                scalar_dependents = _get_dependents(dependents["scalars"])
                vector_dependents = _get_vector_dependents(dependents["vectors"])

                # this is a temporary fix
                if len(vector_dependents) < data.num_eq:
                    vector_dependents = [{} for _ in range(data.num_eq)]

        eq_dict[value]._scalar_dependents = scalar_dependents
        eq_dict[value]._vector_dependents = vector_dependents
        eq_dict[value]._first_eq_index = eq_counter

        for i in range(data.num_eq):
            self._equation_lookup[eq_counter + i] = (value, i)
            self._equation_scalar_dependents_lookup[eq_counter + i] = scalar_dependents[i]
            self._equation_vector_dependents_lookup[eq_counter + i] = vector_dependents[i]

    def _partial_derivative(self, var, eq_num, value, increment_filter=None, **kwargs):
        result = _partial_derivative(var, value, increment_filter, **kwargs)
        if result is not None:
            self.jacobian[eq_num, var.J_col] = result

    def _partial_derivative_fluid(self, var, eq_num, value, dx, increment_filter=None, **kwargs):
        result = _partial_derivative_vecvar(var, value, dx, increment_filter, **kwargs)
        if result is not None:
            self.jacobian[eq_num, var.J_col[dx]] = result

    def _reset_design(self, redesign):
        for value in self.get_variables().values():
            value.design = np.nan

        self.new_design = True

        # switch connections to design mode
        if redesign:
            for var in self.design:
                self.get_attr(var).is_set = True

            for var in self.offdesign:
                self.get_attr(var).is_set = False

    def get_variables(self):
        return {"e": self.e}

    def get_parameters(self):
        return {"e": dc_prop(d=1e-4)}



class Generator(Component):

    def inlets(self):
        return []

    def outlets(self):
        return []

    def powerinlets(self):
        return ["power_in"]


from tespy.components import Turbine, Source, Sink
from tespy.networks import Network


nw = Network(T_unit="C", p_unit="bar")

so = Source("source")
turbine = Turbine("turbine")
si = Sink("sink")

c1 = Connection(so, "out1", turbine, "in1")
c2 = Connection(turbine, "out1", si, "in1")

generator = Generator("generator")
e1 = PowerConnection(turbine, "power", generator, "power_in")

nw.add_conns(c1, c2, e1)

c1.set_attr(fluid={"water": 1}, m=1, p=50, T=500)
c2.set_attr(p=10, T=200)
e1.set_attr(e=1e6)

nw.solve("design")

print(generator.power_outl)