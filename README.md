# 🏭 MSME Scheme Eligibility Suggester Bot

A simplified GenAI mini project that helps MSME businesses discover government schemes they qualify for using **OpenAI GPT API**.

## 🌟 Features

- **4 MSME Schemes**: PM-Mudra, CGTSME, PMEGP, Stand-Up India
- **AI-Powered Explanations**: Uses OpenAI GPT-3.5 for personalized insights
- **Multi-Language Support**: English and Hindi
- **Simple & Clean**: Single-file backend and frontend
- **Beautiful UI**: Modern gradient design with smooth animations

## 🚀 Quick Setup

### 1. Get OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Click "Create new secret key"
4. Copy your API key (starts with `sk-...`)

### 2. Setup Backend

```bash
cd "d:\GenAI Project"

# Create virtual environment (if not already done)
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
# Edit .env file and replace 'your_openai_api_key_here' with your actual OpenAI API key
```

### 3. Setup Frontend

```bash
cd "d:\GenAI Project\frontend"
npm install
```

### 4. Run the App

**Terminal 1 - Backend:**
```bash
cd "d:\GenAI Project\backend"
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd "d:\GenAI Project\frontend"
npm run dev
```

Open **http://localhost:3000** in your browser!

## 📁 Project Structure

```
GenAI Project/
├── backend/
│   └── app.py                 # Single-file Flask backend
├── frontend/
│   └── src/
│       ├── App.jsx            # Single-page React app
│       └── styles/index.css   # Styles
├── requirements.txt           # Python dependencies
└── .env                       # API keys
```

## 🎯 MSME Schemes Included

1. **PM-Mudra** - Micro-financing (up to ₹10L)
2. **CGTSME** - Collateral-free credit (up to ₹2Cr)
3. **PMEGP** - Subsidy for new enterprises (up to ₹25L)
4. **Stand-Up India** - For SC/ST/Women entrepreneurs (up to ₹1Cr)

## 🧪 Test Scenarios

**Scenario 1: Small Business**
- Revenue: ₹5,00,000
- Credit Score: 680
- Years: 2

**Scenario 2: Startup**
- Revenue: ₹2,00,000
- Credit Score: 620
- Years: 0.5

## 🔧 Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: React + Vite
- **AI**: OpenAI GPT-3.5 Turbo
- **Styling**: Vanilla CSS

## 💰 OpenAI Pricing

GPT-3.5 Turbo is very affordable:
- **Input**: $0.50 / 1M tokens
- **Output**: $1.50 / 1M tokens
- Typical request: ~$0.001 (less than 1 cent!)

Free tier: $5 credit for new accounts

## 📝 License

Educational mini project - feel free to modify and use!

---

**Built for learning GenAI development** ✨
