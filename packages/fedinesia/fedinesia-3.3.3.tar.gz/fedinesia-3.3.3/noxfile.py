# ruff: noqa: D100, D103


import nox

nox.options.default_venv_backend = "uv"
nox.options.sessions = [
    "mypy",
    "ruff",
    "refactor",
    "interrogate",
    "pip_audit",
    "bandit",
    "pytest",
    "detect_secrets",
    "dependency_versions",
]


@nox.session(python=["3.10", "3.11", "3.12", "3.13"])
def mypy(session):
    session.install("-e", ".")
    session.install("mypy", "types-python-dateutil", "types-toml")
    session.run("mypy", "src/")


@nox.session
def ruff(session):
    session.install("ruff")
    session.run("ruff", "format", "src/")
    session.run("ruff", "check", "src/")


@nox.session
def refactor(session):
    session.install("codelimit")
    session.run("codelimit", "--version")
    session.run("codelimit", "check", "src")


@nox.session
def interrogate(session):
    session.install("interrogate", "setuptools")
    session.run("interrogate", "-vv", "src/")


@nox.session(python=["3.10", "3.11", "3.12", "3.13"])
def pip_audit(session):
    session.install("pip-audit")
    session.run("pip-audit", "--version")
    session.run("pip-audit")


@nox.session(python=["3.10", "3.11", "3.12", "3.13"])
def bandit(session):
    session.install("bandit", "PyYAML", "tomli", "GitPython", "sarif-om", "jschema-to-python")
    session.run("bandit", "-r", "src/")


@nox.session(python=["3.10", "3.11", "3.12", "3.13"])
def pytest(session):
    session.install("-e", ".")
    session.install("pytest-cov", "freezegun")
    session.run("pytest", "-vv", "--cov-report", "term-missing", "--cov=fedinesia")


@nox.session
def detect_secrets(session):
    session.install("detect-secrets")
    session.run("detect-secrets", "scan", "--force-use-all-plugins", "--baseline", ".secrets.baseline", ".")


@nox.session
def dependency_versions(session):
    session.install("git+https://codeberg.org/marvin8/dependency-checker.git")
    session.run("check")
