from neuralk_foundry_ce.workflow.step import Step, get_step_class, StepMeta, get_full_path_from_class, Field


def test_step_registration_and_retrieval():
    class DummyStep(Step):
        name = "dummy"

        def _execute(self, inputs):
            self.output("out", inputs["in"] + 1)

    # Should be registered
    assert "dummy" in StepMeta.registry
    cls = get_step_class("dummy")
    assert issubclass(cls, Step)


def test_subclass_path_resolution():
    class ParentStep(Step):
        name = "parent"

    class ChildStep1(ParentStep):
        name = "child1"

    class ChildStep2(ParentStep):
        name = "child2"

    class GrandChild(ChildStep1):
        name = "grandchild"

    subclasses = StepMeta.list_subclasses("parent")
    assert set(subclasses) >= {"child1", "child2"}

    paths = get_full_path_from_class("parent")
    assert any(path[-1] == "grandchild" for path in paths)
    assert any(path == ["parent", "child2"] for path in paths)


def test_step_execution_and_output():
    class AddStep(Step):
        name = "add"
        inputs = [Field('a', ''), Field('b', '')]
        outputs = [Field('results', '')]

        def _execute(self, inputs):
            self.output("result", inputs["a"] + inputs["b"])

    step = AddStep()
    out = step.run({"a": 2, "b": 3})
    assert out["result"] == 5


def test_step_namespace_behavior():
    class MultiplyStep(Step):
        name = "multiply"
        inputs = [Field('x', ''), Field('y', '')]
        outputs = [Field('product', '')]

        def _execute(self, inputs):
            self.output("product", inputs["x"] * inputs["y"])

    step = MultiplyStep()
    step.set_namespace("ns")
    out = step.run({"x_ns": 4, "y_ns": 5})
    assert out == {"product_ns": 20}
