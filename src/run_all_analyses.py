"""
Run all project scripts and generate consolidated artifacts:
- JSON responses
- explainability JSON grounded in Rel_prag
- PDF test report

All element structure and weight vectors are loaded from data/theseus_ontology.ttl.
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from rdflib import Graph

from demo_relevance import SIMULATION_WEIGHTS, TTL_PATH, calculate_relevance, get_element_values

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "output"
JSON_OUTPUT = OUTPUT_DIR / "all_responses.json"
EXPLAINABILITY_OUTPUT = OUTPUT_DIR / "explainability.json"
TEST_RESULTS_OUTPUT = OUTPUT_DIR / "test_results.json"
PDF_OUTPUT = OUTPUT_DIR / "execution_report.pdf"

SCRIPT_COMMANDS = [
    ["python", "src/create_theseus_ontology.py"],
    ["python", "src/demo_relevance.py"],
    ["python", "src/semantic_query_example.py"],
    ["python", "src/recommendation_example.py"],
    ["python", "src/knowledge_graph_example.py"],
    ["python", "src/decision_support_example.py"],
    ["python", "src/explanation_example.py"],
    ["python", "src/maintenance_evolution_example.py"],
]

JSON_SCRIPT_NAMES = {
    "semantic_query_example.py",
    "recommendation_example.py",
    "knowledge_graph_example.py",
    "decision_support_example.py",
    "explanation_example.py",
    "maintenance_evolution_example.py",
}

def run_all_scripts() -> tuple[Dict[str, object], List[Dict[str, str]]]:
    outputs: Dict[str, object] = {}
    checks: List[Dict[str, str]] = []

    for cmd in SCRIPT_COMMANDS:
        completed = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True, check=False)
        script_name = Path(cmd[-1]).name
        command_str = " ".join(cmd)

        check_item = {
            "command": command_str,
            "status": "PASS" if completed.returncode == 0 else "FAIL",
            "details": "",
        }
        checks.append(check_item)

        if completed.returncode != 0:
            outputs[script_name] = {"error": completed.stderr.strip(), "stdout": completed.stdout.strip()}
            check_item["details"] = completed.stderr.strip() or "O script retornou erro sem mensagem."
            continue

        stdout = completed.stdout.strip()
        if script_name in JSON_SCRIPT_NAMES:
            try:
                outputs[script_name] = json.loads(stdout)
                check_item["details"] = "O script gerou JSON válido e o resultado foi exportado."
            except json.JSONDecodeError:
                outputs[script_name] = {"raw_output": stdout, "error": "Non-JSON output."}
                check_item["details"] = "O script executou, mas não retornou JSON válido."
                checks.append(
                    {
                        "command": f"json-parse:{script_name}",
                        "status": "FAIL",
                        "details": "Script did not emit valid JSON.",
                    }
                )
        else:
            outputs[script_name] = {"text_output": stdout}
            first_line = stdout.splitlines()[0] if stdout else "Script executado sem saída textual."
            check_item["details"] = first_line[:180]

    return outputs, checks


def build_explainability() -> Dict[str, object]:
    graph = Graph()
    graph.parse(TTL_PATH, format="turtle")
    values = get_element_values(graph)

    profiles = {}
    for profile_name, weights in SIMULATION_WEIGHTS.items():
        total = calculate_relevance(values, weights)
        contributions = []

        for element_name, element_value in values.items():
            weight = weights.get(element_name, 0)
            relevance = float(weight) * float(element_value)
            contributions.append(
                {
                    "element_id": element_name,
                    "weight": float(weight),
                    "ontological_value": float(element_value),
                    "rel_prag_contribution": round(relevance, 4),
                }
            )

        contributions.sort(key=lambda item: item["rel_prag_contribution"], reverse=True)
        profiles[profile_name] = {
            "vector": f"W_{profile_name}",
            "rel_prag_total": float(total),
            "formula": "Rel_prag(I,A,C) = sum(w_i(A,C) * v(p_i))",
            "top_contributors": contributions[:3],
            "all_contributions": contributions,
        }

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "ontology_source": str(TTL_PATH.relative_to(BASE_DIR)),
        "profiles": profiles,
    }


def _format_console_summary(checks: List[Dict[str, str]]) -> str:
    passed = sum(1 for item in checks if item["status"] == "PASS")
    failed = sum(1 for item in checks if item["status"] == "FAIL")

    summary_lines = [
        "A execução completa foi concluída.",
        "",
        (
            "Os artefatos foram salvos na pasta output com os seguintes arquivos: "
            f"{JSON_OUTPUT.name}, {EXPLAINABILITY_OUTPUT.name}, {TEST_RESULTS_OUTPUT.name} e {PDF_OUTPUT.name}."
        ),
        "",
        f"No total, {passed} verificações passaram e {failed} falharam.",
        "Resumo por script:",
    ]
    for item in checks:
        status_label = "passou" if item["status"] == "PASS" else "falhou"
        summary_lines.append(f"O comando '{item['command']}' {status_label}.")
        if item["details"]:
            summary_lines.append(f"Detalhes: {item['details']}")
    return "\n".join(summary_lines)


def _build_execution_report_lines(checks: List[Dict[str, str]], outputs: Dict[str, object]) -> List[str]:
    report_lines = [
        "Rel_prag execution report",
        f"Generated at UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Checks:",
    ]
    report_lines.extend([f"- {item['status']}: {item['command']} | {item['details']}" for item in checks])
    report_lines.append("")
    report_lines.append("Outputs:")
    for script_name, payload in outputs.items():
        payload_text = json.dumps(payload, ensure_ascii=False)
        report_lines.append(f"- {script_name}")
        report_lines.append(f"  {payload_text[:260]}")
    return report_lines


def write_minimal_pdf(lines: List[str], path: Path) -> None:
    safe_lines = [line.replace("(", "[").replace(")", "]") for line in lines]
    y = 760
    text_commands = ["BT", "/F1 11 Tf", "72 790 Td"]
    for idx, line in enumerate(safe_lines):
        if idx == 0:
            text_commands.append(f"({line}) Tj")
        else:
            text_commands.append(f"0 -14 Td ({line}) Tj")
        y -= 14
        if y < 40:
            break
    text_commands.append("ET")
    stream = "\n".join(text_commands).encode("latin-1", errors="replace")

    objects = []
    objects.append(b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n")
    objects.append(b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n")
    objects.append(b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n")
    objects.append(b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n")
    objects.append(f"5 0 obj << /Length {len(stream)} >> stream\n".encode("ascii") + stream + b"\nendstream endobj\n")

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf.extend(obj)

    xref_pos = len(pdf)
    pdf.extend(f"xref\n0 {len(offsets)}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        pdf.extend(f"{off:010d} 00000 n \n".encode("ascii"))

    pdf.extend(f"trailer << /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("ascii"))
    path.write_bytes(pdf)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    outputs, checks = run_all_scripts()
    JSON_OUTPUT.write_text(json.dumps(outputs, indent=2, ensure_ascii=False), encoding="utf-8")

    test_results_payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
    }
    TEST_RESULTS_OUTPUT.write_text(json.dumps(test_results_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    explainability = build_explainability()
    EXPLAINABILITY_OUTPUT.write_text(json.dumps(explainability, indent=2, ensure_ascii=False), encoding="utf-8")

    report_lines = _build_execution_report_lines(checks, outputs)
    write_minimal_pdf(report_lines, PDF_OUTPUT)

    print(_format_console_summary(checks))


if __name__ == "__main__":
    main()
