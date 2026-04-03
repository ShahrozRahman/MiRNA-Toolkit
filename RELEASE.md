# Release Checklist

Use this checklist before publishing a new version of mirna-toolkit.

## 1. Prepare

- [ ] Update version in pyproject.toml
- [ ] Update README.md and docs/usage.html if behavior changed
- [ ] Confirm install name is mirna-toolkit and import name is mirna_toolkit

## 2. Validate Locally

- [ ] Run lint: python -m ruff check src tests
- [ ] Run tests: python -m pytest
- [ ] Build package: python -m build
- [ ] Verify package metadata: python -m twine check dist/*

## 3. Publish

- [ ] Create and push a release tag (for example, v0.1.1)
- [ ] Publish a GitHub Release (triggers publish workflow)
- [ ] Confirm .github/workflows/publish-pypi.yml succeeds

## 4. Verify Public Install

- [ ] Install from PyPI: pip install mirna-toolkit
- [ ] Verify import: python -c "import mirna_toolkit; print(mirna_toolkit.__version__)"
- [ ] Verify CLI: mirna-toolkit help

## Notes

- PyPI publishing uses GitHub OIDC trusted publishing.
- Configure the PyPI project to trust this GitHub repository/workflow before first release.
