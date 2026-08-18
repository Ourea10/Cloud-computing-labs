import re

from experiments.ch11_data_security_mechanisms.models import (
    CodeAnalysisReport,
    FileObject,
)


class MaliciousCodeAnalyzer:

    PATTERNS = {
        "shell_execution": (
            r"os\.system|subprocess\."
        ),
        "file_deletion": (
            r"os\.remove|shutil\.rmtree"
        ),
        "network_execution": (
            r"socket\.|requests\."
        ),
        "dynamic_execution": (
            r"eval\(|exec\("
        ),
    }

    def analyze(
        self,
        file: FileObject,
    ) -> CodeAnalysisReport:

        try:

            source = file.content.decode()

        except UnicodeDecodeError:

            return CodeAnalysisReport(
                file_id=file.file_id,
                suspicious_patterns=[],
                risk_score=0,
            )

        findings = []

        for name, pattern in self.PATTERNS.items():

            if re.search(
                pattern,
                source,
            ):

                findings.append(name)

        risk_score = min(
            len(findings) * 30,
            100,
        )

        return CodeAnalysisReport(
            file_id=file.file_id,
            suspicious_patterns=findings,
            risk_score=risk_score,
        )