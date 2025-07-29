import sys
import types
import importlib
from pathlib import Path


def load_extract_sql():
    stub_names = {
        "rich": types.ModuleType("rich"),
        "rich.console": types.ModuleType("rich.console"),
        "rich.panel": types.ModuleType("rich.panel"),
        "rich.prompt": types.ModuleType("rich.prompt"),
        "rich.table": types.ModuleType("rich.table"),
        "transqlate.schema_pipeline.extractor": types.ModuleType("dummy"),
        "transqlate.schema_pipeline.formatter": types.ModuleType("dummy"),
        "transqlate.schema_pipeline.orchestrator": types.ModuleType("dummy"),
        "transqlate.schema_pipeline.selector": types.ModuleType("dummy"),
        "transqlate.inference": types.ModuleType("dummy"),
        "transformers": types.ModuleType("dummy"),
    }
    stub_names["rich.console"].Console = object
    stub_names["rich.panel"].Panel = object
    stub_names["rich.prompt"].Prompt = object
    stub_names["rich.table"].Table = object
    stub_names["transqlate.schema_pipeline.extractor"].get_schema_extractor = lambda *a, **k: None
    stub_names["transqlate.schema_pipeline.formatter"].format_schema = lambda *a, **k: ""
    stub_names["transqlate.schema_pipeline.orchestrator"].SchemaRAGOrchestrator = object
    stub_names["transqlate.schema_pipeline.selector"].build_table_embeddings = lambda *a, **k: None
    stub_names["transqlate.inference"].NL2SQLInference = object
    stub_names["transformers"].AutoTokenizer = object

    saved = {name: sys.modules.get(name) for name in stub_names}
    sys.modules.update(stub_names)
    sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
    try:
        cli = importlib.import_module("transqlate.cli.cli")
    finally:
        for name, mod in saved.items():
            if mod is None:
                del sys.modules[name]
            else:
                sys.modules[name] = mod
    return cli.extract_sql


_extract_sql = load_extract_sql()


def test_regex_extracts_full_statement():
    sql_text = ""
    cot_text = "Some reasoning SELECT name FROM users LIMIT 5; More text"
    assert _extract_sql(sql_text, cot_text) == "SELECT name FROM users LIMIT 5;"


def test_one_liner_not_rejected():
    sql_text = "SELECT id FROM t;"
    cot_text = ""
    assert _extract_sql(sql_text, cot_text) == sql_text
