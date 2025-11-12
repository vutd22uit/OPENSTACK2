# Contributing to DevSecOps Pipeline

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/organization/devsecops-pipeline/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, versions, etc.)
   - Relevant logs or screenshots

### Suggesting Enhancements

1. Check existing issues and discussions
2. Create an issue with:
   - Clear description of the enhancement
   - Use cases and benefits
   - Potential implementation approach

### Security Vulnerabilities

**Do NOT create public issues for security vulnerabilities.**

Email security@example.com with:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## Development Process

### 1. Fork and Clone

\`\`\`bash
# Fork the repository on GitHub
git clone https://github.com/YOUR_USERNAME/devsecops-pipeline.git
cd devsecops-pipeline
git remote add upstream https://github.com/organization/devsecops-pipeline.git
\`\`\`

### 2. Create a Branch

\`\`\`bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
\`\`\`

Branch naming convention:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions or changes

### 3. Make Changes

- Follow the coding standards (see below)
- Write/update tests
- Update documentation
- Add descriptive commit messages

### 4. Test Your Changes

\`\`\`bash
# Install dependencies
make install

# Run tests
make test

# Run linting
make lint

# Run security scans
make security-scan

# Run full CI suite
make ci
\`\`\`

### 5. Commit Your Changes

\`\`\`bash
git add .
git commit -m "feat: add new feature X"
\`\`\`

Commit message format:
\`\`\`
<type>: <subject>

<body>

<footer>
\`\`\`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes

### 6. Push and Create Pull Request

\`\`\`bash
git push origin feature/your-feature-name
\`\`\`

Create a pull request on GitHub with:
- Clear title and description
- Reference related issues
- Screenshots/demos if applicable
- Checklist of changes

## Coding Standards

### Python

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://github.com/psf/black) for formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Maximum line length: 120 characters
- Use type hints where possible

### Terraform

- Follow [Terraform Style Guide](https://www.terraform.io/docs/language/syntax/style.html)
- Use `terraform fmt` for formatting
- Document all variables and outputs
- Use modules for reusability

### Kubernetes

- Follow [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- Always define resource requests and limits
- Use security contexts
- Document all manifests

## Testing Requirements

### Unit Tests

- Minimum 80% code coverage
- Test edge cases and error conditions
- Use descriptive test names

### Integration Tests

- Test component interactions
- Use test fixtures for consistency
- Clean up resources after tests

### Security Tests

- Test authentication and authorization
- Validate input sanitization
- Test for common vulnerabilities (OWASP Top 10)

## Documentation

- Update README.md for user-facing changes
- Update relevant documentation in `docs/`
- Add inline comments for complex logic
- Document API changes in API documentation
- Update CHANGELOG.md

## Pull Request Process

1. **Automated Checks**: All CI checks must pass
   - Tests pass
   - Linting passes
   - Security scans pass
   - No critical/high vulnerabilities

2. **Code Review**: At least one approval required
   - Code quality
   - Test coverage
   - Documentation
   - Security considerations

3. **Security Review**: Required for:
   - Authentication/authorization changes
   - Cryptographic code
   - External dependencies
   - Infrastructure changes

4. **Merge**: Squash and merge after approval

## Review Criteria

### Code Quality
- [ ] Follows coding standards
- [ ] No code smells or anti-patterns
- [ ] Properly structured and organized
- [ ] DRY (Don't Repeat Yourself)

### Testing
- [ ] Tests added/updated
- [ ] Tests pass locally and in CI
- [ ] Coverage meets requirements
- [ ] Edge cases covered

### Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] No security vulnerabilities introduced
- [ ] Security best practices followed

### Documentation
- [ ] Code is self-documenting
- [ ] Complex logic explained
- [ ] User-facing changes documented
- [ ] API changes documented

## Getting Help

- 📖 Check [Documentation](docs/)
- 💬 Ask in [Discussions](https://github.com/organization/devsecops-pipeline/discussions)
- 🐛 Report issues in [Issues](https://github.com/organization/devsecops-pipeline/issues)
- 📧 Email: support@example.com

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md
- Release notes
- Project documentation

Thank you for contributing to making this project more secure! 🔒
