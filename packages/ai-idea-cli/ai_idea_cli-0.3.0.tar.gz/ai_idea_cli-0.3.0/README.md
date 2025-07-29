# idea-cli: AI-Driven SDLC Engine

Transform project ideas into production-ready codebases through intelligent validation, planning, and automated implementation with comprehensive demo mode for immediate usage.

## 🚀 Key Features

- **🎭 Demo Mode**: Immediate usage without API keys - try all features with fallback implementations
- **🔍 Idea Validation**: Critical idea validation with external API integration and business viability scoring
- **🎯 Enhanced Planning**: AI-powered feature breakdown into epics and implementable stories
- **🏗️ Smart Scaffolding**: Language-aware project generation (Python/Node.js) with comprehensive templates
- **🔄 Micro-Prompt Queue**: Test-driven development automation with multi-provider LLM support
- **📊 Experience Learning**: Automatic failure analysis and guard-rail generation from development experiences
- **🐛 Issue Reporting**: Automated GitHub issue creation with system diagnostics and log collection
- **🔧 Configuration Management**: JSON schema validation with user-friendly setup

## Quick Start (Zero Configuration Required)

### 1. Installation

```bash
# Install from PyPI
pip install ai-idea-cli

# Or create a virtual environment first (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install ai-idea-cli
```

### 2. Try Demo Mode Immediately

```bash
# Initialize configuration (enables demo mode by default)
idea init-config

# Validate an idea (demo mode)
idea validate "AI-powered task management CLI"

# Create a project (demo mode)
idea new "AI-powered task management CLI" --dry-run
```

✅ **Success check**: All commands work immediately with demo responses and guidance

### 3. Upgrade to Full Features (Optional)

```bash
# Edit configuration file
nano ~/.idea-cli/config.json

# Set your API keys and disable demo mode:
{
  "demoMode": false,
  "validator": {
    "apiKeyEnv": "VALIDATOR_API_KEY"
  },
  "models": {
    "apiKeyEnv": "ANTHROPIC_API_KEY"
  }
}

# Set environment variables
export ANTHROPIC_API_KEY="your_claude_key"
export VALIDATOR_API_KEY="your_validator_key"
```

## Command Reference

### Essential Commands

| Command | Purpose | Demo Mode | Full Mode |
|---------|---------|-----------|-----------|
| `idea init-config` | Initialize user configuration | ✅ Always works | ✅ Creates config file |
| `idea validate` | Validate project idea | ✅ Demo validation | ✅ Real API validation |
| `idea new` | Create scaffolded project | ✅ Basic template | ✅ AI-enhanced planning |
| `idea report-issue` | Report bugs automatically | ✅ Manual instructions | ✅ GitHub CLI integration |

### Advanced Commands (Full Mode Only)

| Command | Purpose | Requirements |
|---------|---------|--------------|
| `idea run-queue` | Execute implementation queue | LLM API key |
| `idea queue-status` | Show queue progress | Project with queue |
| `idea experience collect` | Log development failure | Project directory |
| `idea experience summarise` | Generate lessons from failures | LLM API key |
| `idea upgrade` | Apply lessons as guard-rails | Project directory |

### Command Options

| Option | Purpose | Example |
|--------|---------|---------|
| `--dry-run` | Preview without execution | `idea new "test" --dry-run` |
| `--demo` | Force demo mode | `idea new "test" --demo` |
| `--skip-validation` | Bypass idea validation | `idea new "test" --skip-validation` |
| `--project-dir` | Specify project directory | `idea run-queue --project-dir ./my-project` |

## Architecture Overview

### Demo Mode vs Full Mode

**Demo Mode** (Default - No API keys required):
- ✅ Immediate usage for testing and exploration
- ✅ All CLI commands functional with fallback responses
- ✅ Basic project scaffolding with "hello world" templates
- ✅ Clear upgrade paths and configuration guidance
- ✅ Issue reporting with manual instructions

**Full Mode** (API keys configured):
- 🚀 Real idea validation with business scoring
- 🚀 AI-enhanced planning with detailed breakdowns
- 🚀 Complete TDD implementation cycle
- 🚀 Automatic lesson generation and guard-rail updates
- 🚀 Automated GitHub issue reporting

### How It Works

#### 1. **Configuration Stage**
- JSON schema validation ensures configuration integrity
- User config stored in `~/.idea-cli/config.json`
- Auto-detection of demo mode vs full mode based on API key availability

#### 2. **Validation Stage**
- **Demo Mode**: Provides neutral scoring with upgrade guidance
- **Full Mode**: Real validation using external validator API with business viability scoring
- Configurable score thresholds and acceptance criteria

#### 3. **Planning Stage**
- **Demo Mode**: Basic project structure with common patterns
- **Full Mode**: AI-powered breakdown into epics and implementable stories
- Technology stack recommendations based on idea analysis

#### 4. **Implementation Stage**
- **Demo Mode**: Static templates with development guidance
- **Full Mode**: Micro-prompt queue drives TDD implementation
- Support for multiple LLM providers (Anthropic Claude, OpenAI GPT)

#### 5. **Learning Stage**
- Experience collection from development failures
- AI summarization into actionable lessons
- Auto-generated guard-rails from lessons

## Configuration

### Quick Setup Guide

**For Demo Mode (Default - No Setup Required):**
```bash
idea init-config  # Creates config with demo mode enabled
idea validate "test idea"  # Works immediately
```

**For Full Mode (API Keys Required):**
```bash
# 1. Initialize configuration
idea init-config

# 2. Set environment variables
export ANTHROPIC_API_KEY="your_claude_api_key_here"
export VALIDATOR_API_KEY="your_validator_api_key_here"  # Optional

# 3. Edit config to disable demo mode
nano ~/.idea-cli/config.json
# Change: "demoMode": false
```

### Configuration File (`~/.idea-cli/config.json`)

The configuration file is automatically created when you run `idea init-config`. Here's what each section does:

**Demo Mode Configuration (Default):**
```json
{
  "demoMode": true,
  "retentionDays": 30,
  "scaffold": {
    "templateVersion": "main"
  }
}
```

**Full Mode Configuration:**
```json
{
  "demoMode": false,
  "validator": {
    "endpoint": "https://api.example.com/validate",
    "apiKeyEnv": "VALIDATOR_API_KEY",
    "minScore": 0.7
  },
  "models": {
    "plan": "claude-3-5-sonnet-20241022",
    "queue": "claude-3-5-sonnet-20241022",
    "summarise": "claude-3-5-sonnet-20241022",
    "apiKeyEnv": "ANTHROPIC_API_KEY"
  },
  "scaffold": {
    "templateVersion": "main"
  },
  "retentionDays": 30
}
```

### Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `ANTHROPIC_API_KEY` | Full mode | Claude API for planning, queue execution, summarization |
| `OPENAI_API_KEY` | Alternative | OpenAI API as alternative to Claude |
| `VALIDATOR_API_KEY` | Optional | Custom validator API for real idea validation |

### Supported LLM Providers

**Anthropic Claude (Recommended):**
- Models: `claude-3-5-sonnet-20241022`, `claude-3-haiku-20240307`
- Get API key: https://console.anthropic.com/
- Install: `pip install anthropic`

**OpenAI GPT:**
- Models: `gpt-4`, `gpt-3.5-turbo`
- Get API key: https://platform.openai.com/api-keys
- Install: `pip install openai`

## Project Structure

```
idea-cli/
├── idea/                          # Core package
│   ├── cli.py                     # Main CLI with global error handling
│   ├── config.py                  # Configuration management with JSON schema
│   ├── demo.py                    # Demo mode implementations
│   ├── validator.py               # Idea validation with demo support
│   ├── llm.py                     # Multi-provider LLM integration
│   ├── issue_reporter.py          # GitHub issue reporting
│   ├── planner.py                 # AI-powered planning
│   ├── queue.py                   # Queue management
│   ├── runner.py                  # Story implementation engine
│   ├── experience.py              # Learning system
│   └── scaffold/                  # Project scaffolding
│       ├── python.py              # Python project scaffolder
│       └── node.py                # Node.js project scaffolder
├── config/                        # Configuration schema and defaults
│   ├── schema.json                # JSON schema for validation
│   └── default.json               # Default configuration template
├── templates/                     # Copier templates
├── .github/workflows/             # CI/CD pipelines
└── scripts/                       # Development scripts
```

## Generated Project Structure

```
my-project/
├── .idea/                        # Project metadata
│   ├── plan.json                 # Enhanced plan with epics/stories
│   ├── queue.json                # Implementation queue
│   └── _logs/                    # Development logs and failures
├── src/                          # Source code
├── tests/                        # Test files
├── lessons/                      # Project-specific lessons
├── .github/workflows/            # CI/CD for the project
└── README.md                     # ADHD-friendly instructions
```

## Error Handling & Issue Reporting

### Automatic Issue Reporting

When errors occur, idea-cli can automatically create GitHub issues with:
- System information (OS, Python version, architecture)
- Configuration summary (sanitized, no secrets)
- Recent log files from `.idea/_logs/`
- Steps to reproduce template

```bash
# Report an issue manually
idea report-issue "CLI command failed" --dry-run

# Automatic issue reporting on unexpected errors
# (triggered automatically with user confirmation)
```

### Manual Issue Creation

If GitHub CLI is not available, idea-cli provides:
- Pre-formatted issue content
- System diagnostics
- Copy-paste ready templates

## Troubleshooting

### Common Issues

**"Command 'idea' not found"**
- Fix: Ensure package is installed: `pip install ai-idea-cli`
- Check: `pip show ai-idea-cli` should show installation
- Try: Restart your terminal or source your shell profile

**"Configuration error: API key environment variable not configured"**
- **For Demo Mode:** Run `idea init-config` and verify `"demoMode": true` in config
- **For Full Mode:** Set `export ANTHROPIC_API_KEY=your_key` and ensure `"demoMode": false`

**"Failed to initialize config"**
- Fix: Check permissions: `ls -la ~/` (should be writable)
- Try: `mkdir -p ~/.idea-cli && idea init-config`
- Alternative: Use `--config-dir` flag to specify different location

**"Import errors for anthropic/openai packages"**
- Fix: `pip install anthropic` (for Claude) or `pip install openai` (for GPT)
- Note: Only needed for full mode, demo mode works without these packages

**Commands work but show demo responses**
- This is normal! Demo mode is the default
- To upgrade: Set API keys and change `"demoMode": false` in config
- Verify: `echo $ANTHROPIC_API_KEY` should show your key

### Performance Tips

- Use `--dry-run` for testing without API calls
- Use `--demo` flag to force demo mode temporarily
- Set appropriate model choices in config (haiku for speed, sonnet for quality)

### Debug Mode

```bash
# Enable verbose logging
export IDEA_CLI_DEBUG=1
idea validate "test idea"

# Check configuration
idea init-config  # Shows current config path and status
```

## Contributing

We welcome contributions! Here's how to get started:

### Quick Setup
```bash
# Fork the repository on GitHub
git clone https://github.com/yourusername/ai-idea-cli.git
cd ai-idea-cli

# Install in development mode
pip install -e .

# Test the installation
idea --help
```

### Development Workflow
1. **Test demo mode**: All commands should work without API keys
2. **Test full mode**: Set API keys and test enhanced features
3. **Run quality checks**: `ruff check . && ruff format --check .`
4. **Test error handling**: Verify issue reporting functionality
5. **Update documentation**: Keep README and docstrings current

### Pull Request Guidelines
- Test both demo and full modes
- Include tests for new features
- Update documentation for user-facing changes
- Follow existing code style and patterns

## License

MIT License - see LICENSE file for details.

---

**🎭 Start in demo mode, upgrade when ready!**
