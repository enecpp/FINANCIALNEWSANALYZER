# Contributing to Financial News Analyzer

First off, thank you for considering contributing to Financial News Analyzer! 🎉

## 🌟 Ways to Contribute

### 🐛 Bug Reports
- Use GitHub Issues to report bugs
- Include detailed steps to reproduce
- Provide system information and screenshots

### 💡 Feature Requests
- Suggest new features through GitHub Issues
- Explain the use case and expected behavior
- Consider implementation complexity

### 🔧 Code Contributions
- Fork the repository
- Create a feature branch
- Follow coding standards
- Add comprehensive tests
- Submit a pull request

## 📋 Development Guidelines

### 🏗️ Architecture Principles
- Follow Clean Architecture patterns
- Implement SOLID principles
- Use dependency injection
- Maintain separation of concerns

### 🎨 Code Style
- Follow PEP 8 guidelines
- Use type hints where applicable
- Write descriptive variable names
- Add docstrings for functions and classes

### 🧪 Testing
- Write unit tests for new features
- Maintain test coverage above 80%
- Test edge cases and error conditions
- Use pytest framework

### 📚 Documentation
- Update README for new features
- Add inline comments for complex logic
- Document API changes
- Include usage examples

## 🚀 Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/mleng-financial_news_analyzer.git
   cd financial_news_analyzer
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Run Tests**
   ```bash
   pytest tests/
   ```

5. **Start Development Server**
   ```bash
   streamlit run Start.py
   ```

## 📝 Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make Changes**
   - Implement your feature
   - Add tests
   - Update documentation

3. **Test Your Changes**
   ```bash
   pytest tests/
   flake8 src/
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

5. **Push and Submit PR**
   ```bash
   git push origin feature/amazing-feature
   ```

## 🎯 Commit Message Convention

Use conventional commits for clear history:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Maintenance tasks

## 🔍 Code Review Process

1. All PRs require at least one review
2. Automated tests must pass
3. Code coverage should not decrease
4. Documentation must be updated
5. Breaking changes require discussion

## 🏷️ Issue Labels

- `bug` - Bug reports
- `enhancement` - Feature requests
- `documentation` - Documentation improvements
- `good first issue` - Beginner-friendly issues
- `help wanted` - Issues needing assistance

## 📞 Getting Help

- 💬 Join our Discord server
- 📧 Email the maintainers
- 📖 Check the documentation
- 🔍 Search existing issues

## 🙏 Recognition

All contributors will be:
- Added to the contributors list
- Mentioned in release notes
- Recognized in the README

Thank you for making Financial News Analyzer better! 🚀
