from baselayeros.regulus.templates import compliance_company_mvp_template
from baselayeros.regulus.builder import RegulusBuilder

def build_compliance_actiongraph():
    template = compliance_company_mvp_template()
    spec = type("Spec", (), template)  # quick hack: mimic WorkflowSpec
    builder = RegulusBuilder()
    return builder.build_actiongraph(spec)
