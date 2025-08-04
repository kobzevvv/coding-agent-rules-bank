# 🚀 CI/CD Setup Guide for Memory Bank System

This guide explains how to set up the cognitive complexity CI/CD pipeline for your Memory Bank System.

## 📋 Prerequisites

1. **GitHub Repository** with your Memory Bank System
2. **OpenAI API Key** for semantic analysis
3. **Python 3.11+** for running scripts locally

## 🔧 Setup Steps

### Step 1: Add OpenAI API Key to GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the secret with:
   - **Name**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key (starts with `sk-`)

### Step 2: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### Step 3: Test Locally (Optional)

```bash
# Run static analysis
python scripts/static-complexity-check.py

# Run GPT analysis (requires OPENAI_API_KEY environment variable)
export OPENAI_API_KEY="your-api-key-here"
python scripts/gpt-complexity-analyzer.py

# Check thresholds
python scripts/check-complexity-threshold.py
```

## 🔍 What the CI/CD Does

### Static Analysis (`static-complexity-check.py`)
- Analyzes all markdown files in your repository
- Calculates complexity scores based on:
  - Mermaid diagrams (high complexity)
  - Code blocks (medium complexity)
  - Nested headers (structure complexity)
  - Conditional logic (decision complexity)
  - Workflow steps (process complexity)
  - File size and line count
- Detects rule conflicts and best practice violations
- Generates detailed JSON reports

### Semantic Analysis (`gpt-complexity-analyzer.py`)
- Uses GPT-3.5 to analyze semantic complexity
- Detects rule conflicts in Cursor settings
- Identifies best practice violations
- Assesses Cursor compatibility issues
- Provides complexity ratings (1-10 scale)

### Threshold Checking (`check-complexity-threshold.py`)
- Compares current complexity against baseline
- Triggers alerts when complexity exceeds 2x baseline
- Generates detailed reports and recommendations
- Creates PR comments with summaries

## 📊 Baseline Complexity Scores

The system uses these baseline scores for threshold checking:

| File | Baseline Score |
|------|----------------|
| `workflow-level4.mdc` | 80 |
| `reflection-comprehensive.mdc` | 70 |
| `architectural-planning.mdc` | 90 |
| `phased-implementation.mdc` | 75 |
| `main-optimized.mdc` | 60 |
| `hierarchical-rule-loading.mdc` | 45 |
| `mode-transition-optimization.mdc` | 40 |
| `optimization-integration.mdc` | 50 |
| `optimized-workflow-level1.mdc` | 30 |
| `optimized-creative-template.mdc` | 35 |

## 🚨 Threshold Triggers

The CI/CD will trigger alerts when:

1. **Static complexity** exceeds 2x baseline
2. **Semantic complexity** is rated >7/10
3. **Cursor compatibility** is rated <5/10
4. **Rule conflicts** are detected
5. **Best practice violations** are found

## 📁 Generated Reports

The CI/CD generates these reports:

- `static-complexity-results.json` - Static analysis results
- `gpt-complexity-results.json` - Semantic analysis results
- `complexity-threshold-results.json` - Threshold check results
- `complexity-threshold-report.md` - Detailed threshold report
- `complexity-summary.md` - PR comment summary
- `complexity-alert.md` - Alert message (if threshold exceeded)

## 🔄 Workflow Triggers

The CI/CD runs on:
- **Push** to any branch
- **Pull Request** creation/update
- **Manual trigger** (can be added)

## 💡 Customization

### Adjusting Thresholds

Edit `scripts/check-complexity-threshold.py`:

```python
self.threshold_multiplier = 2.0  # Change to 1.5 for stricter checks
```

### Adding New Complexity Indicators

Edit `scripts/static-complexity-check.py`:

```python
self.complexity_indicators = {
    'your_new_indicator': 3,  # Add new indicators here
    # ... existing indicators
}
```

### Modifying Baseline Scores

Edit the baseline dictionary in `scripts/check-complexity-threshold.py`:

```python
self.baseline = {
    'your-file.mdc': 50,  # Add new baseline scores
    # ... existing baselines
}
```

## 🛠️ Troubleshooting

### Common Issues

1. **OpenAI API Key Missing**
   - Ensure `OPENAI_API_KEY` is set in GitHub secrets
   - Check that the secret name matches exactly

2. **Scripts Not Found**
   - Ensure all scripts are in the `scripts/` directory
   - Check file permissions (should be executable)

3. **Python Dependencies Missing**
   - Install requirements: `pip install -r requirements.txt`
   - Check Python version (3.11+ required)

4. **Rate Limiting**
   - GPT analysis includes delays to avoid rate limiting
   - If issues persist, increase delays in `gpt-complexity-analyzer.py`

### Debug Mode

Add debug output by modifying scripts:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Monitoring

### GitHub Actions Dashboard
- Go to **Actions** tab in your repository
- View workflow runs and logs
- Download artifacts for detailed reports

### Local Monitoring
```bash
# Run analysis locally
python scripts/static-complexity-check.py
python scripts/gpt-complexity-analyzer.py
python scripts/check-complexity-threshold.py
```

## 🎯 Best Practices

1. **Regular Reviews**: Check complexity reports weekly
2. **Incremental Changes**: Make small changes to avoid threshold spikes
3. **Documentation**: Keep baseline scores updated
4. **Testing**: Test changes locally before pushing
5. **Monitoring**: Watch for trends in complexity scores

## 🔗 Related Files

- `.github/workflows/complexity-check.yml` - GitHub Actions workflow
- `scripts/static-complexity-check.py` - Static analysis
- `scripts/gpt-complexity-analyzer.py` - Semantic analysis
- `scripts/check-complexity-threshold.py` - Threshold checking
- `scripts/generate-complexity-summary.py` - Summary generation
- `scripts/create-complexity-alert.py` - Alert creation
- `requirements.txt` - Python dependencies

---

**Ready to set up?** Follow the steps above and your CI/CD will be running on the next push! 