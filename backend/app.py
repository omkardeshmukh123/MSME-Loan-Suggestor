"""
MSME Scheme Eligibility Suggester Bot
A simplified mini project using OpenAI GPT API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure OpenAI API
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    print("⚠️  WARNING: OPENAI_API_KEY not found in environment variables")
    print("   Please add your OpenAI API key to the .env file")
    OPENAI_API_KEY = None

@app.route("/")
def home():
    return "MSME Loan Suggestor Backend is Live 🚀"

    
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# MSME Scheme Rules
MSME_SCHEMES = {
    "PM-Mudra": {
        "name": "Pradhan Mantri MUDRA Yojana",
        "description": "Micro-financing for small businesses and entrepreneurs",
        "max_loan": 1000000,
        "min_revenue": 0,
        "min_credit_score": 600,
        "min_years": 0,
        "categories": ["Shishu (up to ₹50K)", "Kishore (₹50K-₹5L)", "Tarun (₹5L-₹10L)"]
    },
    "CGTSME": {
        "name": "Credit Guarantee Fund Trust for Micro and Small Enterprises",
        "description": "Collateral-free credit for MSMEs",
        "max_loan": 20000000,
        "min_revenue": 500000,
        "min_credit_score": 650,
        "min_years": 1,
        "requires_collateral": False
    },
    "PMEGP": {
        "name": "Prime Minister's Employment Generation Programme",
        "description": "Subsidy-based scheme for new enterprises",
        "max_loan": 2500000,
        "min_revenue": 0,
        "min_credit_score": 620,
        "min_years": 0,
        "is_for_new_enterprises": True,
        "subsidy_rate": "15-35%"
    },
    "Stand-Up-India": {
        "name": "Stand-Up India Scheme",
        "description": "Support for SC/ST/Women entrepreneurs",
        "max_loan": 10000000,
        "min_revenue": 200000,
        "min_credit_score": 650,
        "min_years": 0.5,
        "for_minorities_women": True
    }
}


def validate_business_data(data):
    """Validate incoming business data"""
    required_fields = ['annual_revenue', 'credit_score', 'years_in_business', 'industry_type']
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    # Type validation
    if not isinstance(data['annual_revenue'], (int, float)) or data['annual_revenue'] < 0:
        raise ValueError("Annual revenue must be a positive number")
    
    if not isinstance(data['credit_score'], int) or data['credit_score'] < 300 or data['credit_score'] > 900:
        raise ValueError("Credit score must be between 300 and 900")
    
    if not isinstance(data['years_in_business'], (int, float)) or data['years_in_business'] < 0:
        raise ValueError("Years in business must be a positive number")
    
    return True


def check_scheme_eligibility(business_data):
    """Check eligibility for each MSME scheme"""
    eligible_schemes = []
    rejected_schemes = []
    
    annual_revenue = business_data['annual_revenue']
    credit_score = business_data['credit_score']
    years_in_business = business_data['years_in_business']
    
    for scheme_id, scheme in MSME_SCHEMES.items():
        reasons = []
        
        # Check revenue requirement
        if annual_revenue < scheme['min_revenue']:
            reasons.append(f"Annual revenue (₹{annual_revenue:,}) is below minimum (₹{scheme['min_revenue']:,})")
        
        # Check credit score
        if credit_score < scheme['min_credit_score']:
            reasons.append(f"Credit score ({credit_score}) is below minimum ({scheme['min_credit_score']})")
        
        # Check years in business
        if years_in_business < scheme['min_years']:
            reasons.append(f"Years in business ({years_in_business}) is below minimum ({scheme['min_years']})")
        
        if len(reasons) == 0:
            eligible_schemes.append({
                'id': scheme_id,
                'name': scheme['name'],
                'description': scheme['description'],
                'max_loan': scheme['max_loan']
            })
        else:
            rejected_schemes.append({
                'id': scheme_id,
                'name': scheme['name'],
                'reasons': reasons
            })
    
    # Calculate overall eligibility score
    score = 0
    score += min(credit_score / 900 * 40, 40)  # 40% weight
    score += min(annual_revenue / 10000000 * 30, 30)  # 30% weight
    score += min(years_in_business / 5 * 20, 20)  # 20% weight
    score += 10 if len(eligible_schemes) > 0 else 0  # 10% bonus for any eligibility
    
    return {
        'overall_score': round(score, 1),
        'eligible_schemes': eligible_schemes,
        'rejected_schemes': rejected_schemes,
        'total_eligible': len(eligible_schemes),
        'business_profile': {
            'revenue': annual_revenue,
            'credit_score': credit_score,
            'years': years_in_business,
            'industry': business_data.get('industry_type', 'General')
        }
    }


def generate_ai_explanation(eligibility_data, language='english'):
    """Generate AI explanation using OpenAI GPT"""
    
    if not client:
        return "AI explanation unavailable. Please configure your OpenAI API key in the .env file."
    
    # Build prompt for GPT
    prompt = f"""
You are a helpful MSME (Micro, Small, and Medium Enterprises) advisor in India. 
Analyze the following business profile and scheme eligibility results, then provide a clear, empathetic explanation.

BUSINESS PROFILE:
- Annual Revenue: ₹{eligibility_data['business_profile']['revenue']:,}
- Credit Score: {eligibility_data['business_profile']['credit_score']}
- Years in Business: {eligibility_data['business_profile']['years']}
- Industry: {eligibility_data['business_profile']['industry']}
- Overall Eligibility Score: {eligibility_data['overall_score']}/100

ELIGIBLE SCHEMES ({eligibility_data['total_eligible']}):
"""
    
    for scheme in eligibility_data['eligible_schemes']:
        prompt += f"\n- {scheme['name']}: {scheme['description']} (Max: ₹{scheme['max_loan']:,})"
    
    if eligibility_data['rejected_schemes']:
        prompt += f"\n\nREJECTED SCHEMES ({len(eligibility_data['rejected_schemes'])}):\n"
        for scheme in eligibility_data['rejected_schemes']:
            prompt += f"\n- {scheme['name']}:"
            for reason in scheme['reasons']:
                prompt += f"\n  • {reason}"
    
    prompt += f"""

INSTRUCTIONS:
1. Provide a warm, encouraging introduction
2. Explain which schemes they qualify for and why (if any)
3. If they were rejected from any schemes, explain what needs improvement
4. Give 2-3 specific, actionable recommendations
5. End with an encouraging message

Language: {'Hindi (Devanagari script)' if language == 'hindi' else 'English'}
Tone: Professional yet friendly and empathetic
Length: 250-350 words
Format: Use paragraphs, NOT bullet points
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using GPT-3.5 (cheaper and faster)
            messages=[
                {"role": "system", "content": "You are a helpful MSME advisor in India who explains government schemes in simple, friendly language."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI explanation temporarily unavailable. Error: {str(e)}"


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'MSME Scheme Eligibility Suggester',
        'schemes_available': len(MSME_SCHEMES)
    })


@app.route('/api/schemes', methods=['GET'])
def get_schemes():
    """Get all available MSME schemes"""
    schemes_list = []
    for scheme_id, scheme in MSME_SCHEMES.items():
        schemes_list.append({
            'id': scheme_id,
            'name': scheme['name'],
            'description': scheme['description'],
            'max_loan': scheme['max_loan']
        })
    
    return jsonify({
        'success': True,
        'schemes': schemes_list
    })


@app.route('/api/check-eligibility', methods=['POST'])
def check_eligibility():
    """
    Main endpoint: Check MSME scheme eligibility
    
    Expected request body:
    {
        "annual_revenue": 750000,
        "credit_score": 680,
        "years_in_business": 2.5,
        "industry_type": "Retail",
        "preferred_language": "english"
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate business data
        try:
            validate_business_data(data)
        except ValueError as ve:
            return jsonify({
                'success': False,
                'error': str(ve)
            }), 400
        
        # Check eligibility
        eligibility_result = check_scheme_eligibility(data)
        
        # Generate AI explanation
        language = data.get('preferred_language', 'english')
        ai_explanation = generate_ai_explanation(eligibility_result, language)
        
        # Combine results
        response = {
            'success': True,
            'eligibility_score': eligibility_result['overall_score'],
            'eligible_schemes': eligibility_result['eligible_schemes'],
            'rejected_schemes': eligibility_result['rejected_schemes'],
            'ai_explanation': ai_explanation,
            'total_schemes': len(MSME_SCHEMES)
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error in check_eligibility: {e}")
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred. Please check server logs.'
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║     MSME Scheme Eligibility Suggester Bot - Mini Project     ║
╚══════════════════════════════════════════════════════════════╝

🚀 Server starting on http://localhost:{port}
📊 Available MSME Schemes: {len(MSME_SCHEMES)}

📝 API Endpoints:
   - GET  /api/health             → Health check
   - GET  /api/schemes            → Get all schemes
   - POST /api/check-eligibility  → Check eligibility

🔑 OpenAI GPT API: {'✓ Configured' if OPENAI_API_KEY else '✗ NOT FOUND - Add to .env file'}

Ready to help MSMEs find the right schemes!
""")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
