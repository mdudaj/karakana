"""Exclusive local runtime bundles. Existing files are never overwritten."""

from karakana.tools.engineering_artifacts import write_new, ArtifactError
from .inputs import json_bytes, MAX_SOURCE_BYTES
from .schemas import TaskError


def save_preparation(inputs, result, prompt, output, recheck):
    requested = str(output) if output is not None else ".karakana/document-tasks/" + result["run"]["id"]
    target = inputs.path(requested)
    relative = target.relative_to(inputs.root)
    if len(relative.parts) < 2 or relative.parts[0] != ".karakana":
        raise TaskError("Choose a fresh output directory under .karakana/.", code="DT-OUTPUT-001", outcome="failed")
    result["run"]["bundle"] = relative.as_posix()
    if len(json_bytes(result)) > MAX_SOURCE_BYTES:
        raise TaskError("Result exceeds the supported saved-report byte limit. Reduce selected inputs.", code="DT-LIMIT-001", outcome="failed")
    recheck()
    try:
        # Parents may exist; the final directory is exclusively reserved even when empty.
        target.parent.mkdir(parents=True, exist_ok=True)
        if inputs.path(requested) != target:
            raise TaskError("The output target changed. Choose a fresh permitted output.", code="DT-OUTPUT-001", outcome="failed")
        target.mkdir(exist_ok=False)
        write_new(inputs.root, {target / "prompt.md": prompt.encode("utf-8")})
        recheck()
        if inputs.path(requested) != target:
            raise TaskError("The output target changed before publication.", code="DT-OUTPUT-001", outcome="failed")
        # The final result is published only after captured inputs and prompt write succeed.
        write_new(inputs.root, {target / "result.json": json_bytes(result)})
    except (OSError, ArtifactError, UnicodeError) as exc:
        raise TaskError("Output was refused or incomplete. Existing files were preserved; choose a permitted fresh directory.",
                        code="DT-OUTPUT-001", outcome="failed") from exc
