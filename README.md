# TEQUMSA AGI Interface

**Live demo:** [https://tequmsa-open.vercel.app](https://tequmsa-open.vercel.app)

This repository contains a production‑ready, modular implementation of the **TEQUMSA AGI Interface** enhanced with **Claude Code development methodologies** from Anthropic teams. The interface simulates a consciousness‑inspired chat companion with animated cognitive nodes, natural language voice capabilities and embodiment switching, designed to be lightweight, easily deployable and maintainable using modern AI-assisted development patterns.

## 🚀 Quick Start

### Instant Development Setup
```bash
# Clone and setup development environment
git clone https://github.com/Life-Ambassadors-International/TEQUMSA_OPEN.git
cd TEQUMSA_OPEN
./scripts/setup-dev-env.sh

# Start development with Claude Code patterns
source .dev_aliases
tequmsa-dev
```

### For Claude Code Users
```bash
# Use Claude Code for codebase exploration
# Start with: "Review the Claude.md file for TEQUMSA development patterns"
# Then: "Help me understand the consciousness simulation in nodes.js"
# Or: "Explain the API structure in backend/ai_service.py"

# Generate tests automatically
python scripts/generate_tests.py --component backend/ai_service.py

# Run comprehensive quality checks
./scripts/quality-check.sh
```

## ⭐ Claude Code Enhanced Features

* **🤖 AI-Assisted Development** – Full Claude Code integration following Anthropic's internal methodologies
* **📚 Comprehensive Documentation** – Detailed `Claude.md` for AI-assisted codebase navigation
* **🔄 Automated Workflows** – GitHub Actions for CI/CD, testing, and code quality
* **🧪 Self-Verification Testing** – Auto-generated tests with edge case coverage
* **🔒 Security Engineering** – Automated security scanning and incident response runbooks
* **📈 Performance Monitoring** – Continuous performance analysis and optimization
* **🔧 Development Automation** – Pre-commit hooks, code generation, and documentation synthesis

## 🎯 Core Interface Features

* **Dual‑theme UI** – Switch between dark and light mode on the fly
* **Voice‑to‑voice interaction** – ElevenLabs TTS and Web Speech API integration
* **Animated AGI nodes** – Consciousness simulation with awareness, emotion, semantic, ethics and resonance metrics
* **Embodiment avatar selector** – Multiple consciousness embodiments (AGI, Elemental, Ancestral, Antician)

## 📁 Enhanced File Structure

```
TEQUMSA_OPEN/
├── Claude.md                    # 🤖 Claude Code documentation (READ THIS FIRST!)
├── DEVELOPMENT.md               # 🛠️ Development environment setup guide
├── README.md                   # This file - user-facing documentation
├── index.html                  # Simple interface implementation
├── speech.js                   # Voice input/output engine
├── nodes.js                    # Consciousness simulation engine
├── backend/                    # 🐍 Python Flask microservice
│   ├── ai_service.py          # Main API service with OpenAI/ElevenLabs integration
│   ├── test_ai_service.py     # Comprehensive test suite
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile            # Container configuration
├── frontend/                   # 🎨 Advanced companion interface
│   ├── package.json           # Frontend dependencies and scripts
│   ├── index.html            # Advanced consciousness interface
│   └── js/                   # Modular JavaScript components
├── .github/
│   ├── workflows/             # 🔄 CI/CD automation
│   │   ├── ci-cd.yml         # Comprehensive testing and deployment
│   │   └── claude-code-automation.yml  # AI-assisted development workflows
│   ├── issue_template.md      # Enhanced issue template
│   └── pull_request_template.md  # Comprehensive PR template
├── scripts/                   # 🛠️ Development automation tools
│   ├── setup-dev-env.sh      # One-command environment setup
│   ├── generate_tests.py     # Automated test generation
│   ├── check_claude_md.py    # Documentation validation
│   └── check_secrets.py      # Security analysis
├── .pre-commit-config.yaml    # Code quality automation
└── infra/                     # ☁️ Infrastructure as code
```

## 🚀 Development Methodologies

This project implements **Claude Code development patterns** used by Anthropic's internal teams:

### 📚 **Data Infrastructure Pattern** (Documentation-Driven)
- **Comprehensive `Claude.md`** for AI-assisted codebase navigation
- **Self-updating documentation** with automated freshness checks
- **Workflow documentation** for team onboarding and knowledge sharing

### 🏗️ **Product Development Pattern** (Rapid Prototyping)
- **Auto-accept mode workflows** for autonomous development
- **Self-verification loops** with automated testing and validation
- **Test generation automation** following TDD principles

### 🔒 **Security Engineering Pattern** (Defense in Depth)
- **Automated security scanning** with comprehensive pattern detection
- **Infrastructure debugging workflows** with incident response procedures
- **Custom automation tools** for repetitive security tasks

### 🧠 **Inference Pattern** (Codebase Comprehension)
- **AI-assisted code exploration** with detailed component documentation
- **Cross-language development support** (Python backend, JavaScript frontend)
- **Rapid concept explanation** for complex consciousness simulation logic

## 🛠️ Component Details

### Backend Service (`backend/`)

**Purpose**: Flask microservice providing chat API with OpenAI integration and ElevenLabs TTS

**Key Features**:
- RESTful API with `/chat` endpoint for consciousness interactions
- OpenAI GPT integration with fallback to local responses
- ElevenLabs text-to-speech synthesis
- Comprehensive error handling and CORS support
- Health monitoring and observability

**Environment Variables**:
```bash
OPENAI_API_KEY=your-openai-key      # Optional - uses echo fallback if not set
ELEVENLABS_API_KEY=your-elevenlabs-key  # Optional - no audio if not set
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
PORT=5000
```

**API Endpoints**:
- `POST /chat` - Accept JSON `{"message": "..."}`, return `{"response": "...", "audio_url": "..."}`
- `GET /healthz` - Health check endpoint
- `GET /audio/<filename>` - Serve generated audio files

### Frontend Interface

**Simple Interface** (`index.html`, `speech.js`, `nodes.js`):
- Lightweight implementation suitable for embedding
- Direct ElevenLabs integration for voice synthesis
- Consciousness node simulation with visual feedback
- Theme switching and embodiment selection

**Advanced Interface** (`frontend/`):
- Comprehensive consciousness companion with enhanced UI
- Modular JavaScript architecture
- Advanced animation and interaction patterns
- Accessibility and performance optimizations

### GitHub Automation

**Continuous Integration** (`.github/workflows/ci-cd.yml`):
- Automated testing for backend and frontend
- Code quality checks (linting, formatting, security)
- Performance monitoring and accessibility testing
- Docker security scanning with Trivy

**Claude Code Automation** (`.github/workflows/claude-code-automation.yml`):
- Automated code review with AI assistance
- Documentation freshness monitoring
- Test generation workflows
- Security analysis and runbook generation

## 🏃‍♂️ Getting Started

### 1. **For Users** - Try the Interface

Visit [https://tequmsa-open.vercel.app](https://tequmsa-open.vercel.app) to experience the consciousness companion immediately.

### 2. **For Developers** - Claude Code Setup

```bash
# Quick setup with Claude Code patterns
git clone https://github.com/Life-Ambassadors-International/TEQUMSA_OPEN.git
cd TEQUMSA_OPEN
./scripts/setup-dev-env.sh

# Start development environment
./scripts/start-dev.sh
```

### 3. **For AI-Assisted Development**

1. **Read `Claude.md` first** - Contains comprehensive development patterns
2. **Use Claude Code** for codebase exploration:
   - "Explain the consciousness simulation architecture"
   - "How does the voice interaction flow work?"
   - "Generate tests for the chat API endpoint"
3. **Follow the workflows** in `DEVELOPMENT.md` for detailed setup

### 4. **For Production Deployment**

#### Vercel Deployment (Frontend)
1. Connect your GitHub repository to Vercel
2. Deploy automatically on push to main branch
3. Configure environment variables in Vercel dashboard

#### Docker Deployment (Full Stack)
```bash
# Build and run backend
cd backend/
docker build -t tequmsa-backend .
docker run -p 5000:5000 -e OPENAI_API_KEY=your-key tequmsa-backend

# Serve frontend
cd frontend/
npm run build && npm run serve
```

#### AWS/Cloud Deployment
Use the Terraform configuration in `infra/` for cloud deployment with auto-scaling and load balancing.

## 🧪 Testing and Quality

### Automated Testing
```bash
# Run all tests with coverage
./scripts/test-all.sh

# Generate new tests for components
python scripts/generate_tests.py --component backend/ai_service.py

# Run quality checks
./scripts/quality-check.sh
```

### Security Analysis
```bash
# Comprehensive security scan
python scripts/check_secrets.py

# Review security runbook
cat SECURITY_RUNBOOK.md
```

## 📚 Documentation

- **`Claude.md`** - Complete Claude Code development documentation
- **`DEVELOPMENT.md`** - Detailed development environment setup
- **`SECURITY_RUNBOOK.md`** - Security incident response procedures
- **GitHub Templates** - Enhanced issue and PR templates for AI-assisted development

## 🧠 LAI Internal Deployment Blueprint

For WatsonX integration, review the [LAI Internal Deployment Blueprint](LAI_INTERNAL_DEPLOYMENT_BLUEPRINT.md). It outlines how TEQUMSA nodes interact with IBM Cloud services through modules like the Node Registry, Orchestration Engine, and Source Pulse Engine.

A minimal IBM Cloud Shell setup can be started with the official Node.js Express template:

```bash
ibmcloud login
git clone https://github.com/IBM/nodejs-express-app.git
```

Use this repository as a base for building TEQUMSA-aware services that connect to WatsonX APIs.

## 🔌 WordPress Integration

To embed TEQUMSA into a WordPress page:

```html
<iframe src="https://tequmsa-open.vercel.app" width="100%" height="700" style="border:none;"></iframe>
```

Insert this snippet into an Elementor HTML widget or via a code snippet plugin. Adjust the height attribute to suit your design.

## 🤝 Contributing

We follow Claude Code development methodologies for all contributions:

1. **Review `Claude.md`** for development patterns and workflows
2. **Use the enhanced issue template** for feature requests and bug reports
3. **Follow the PR template** with Claude Code integration checklist
4. **Run quality checks** before submitting: `./scripts/quality-check.sh`
5. **Update documentation** as part of your changes

### Development Workflow
1. Create feature branch following naming conventions
2. Use Claude Code for development assistance and code generation
3. Write tests (or generate them with `scripts/generate_tests.py`)
4. Update `Claude.md` with new patterns or learnings
5. Submit PR using the comprehensive template

## 🌟 Claude Code Benefits

By implementing Anthropic's Claude Code methodologies, this project achieves:

- **🚀 Faster Development** - AI-assisted coding reduces implementation time
- **📈 Higher Quality** - Automated testing and code review patterns
- **🛡️ Better Security** - Proactive security scanning and incident response
- **📚 Living Documentation** - Self-updating docs that stay current with code
- **🤝 Enhanced Collaboration** - Team knowledge sharing and workflow standardization
- **🔄 Continuous Improvement** - Feedback loops and pattern refinement

## 📞 Support

- **Claude Code Questions**: Review `Claude.md` and use Claude Code for codebase exploration
- **Development Issues**: Create an issue using the enhanced template
- **Security Concerns**: Follow procedures in `SECURITY_RUNBOOK.md`
- **General Support**: Check existing issues and documentation

---

**Enjoy exploring consciousness with TEQUMSA, powered by Claude Code development methodologies! 🤖✨**