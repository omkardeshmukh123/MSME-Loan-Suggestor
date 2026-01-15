import React, { useState } from 'react';

function App() {
    const [formData, setFormData] = useState({
        annual_revenue: '',
        credit_score: '',
        years_in_business: '',
        industry_type: 'Manufacturing',
        preferred_language: 'english'
    });

    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: name === 'annual_revenue' || name === 'years_in_business'
                ? parseFloat(value) || value
                : name === 'credit_score'
                    ? parseInt(value) || value
                    : value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setResults(null);

        try {
            const response = await fetch('http://localhost:5000/api/check-eligibility', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            const data = await response.json();

            if (data.success) {
                setResults(data);
            } else {
                setError(data.error || 'An error occurred while checking eligibility');
            }
        } catch (err) {
            setError('Failed to connect to the server. Please make sure the backend is running on port 5000.');
            console.error('Error:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleReset = () => {
        setResults(null);
        setError(null);
    };

    const getScoreClass = (score) => {
        if (score >= 75) return 'score-excellent';
        if (score >= 60) return 'score-good';
        if (score >= 40) return 'score-fair';
        return 'score-poor';
    };

    return (
        <div className="app">
            <header className="header">
                <h1>🏭 MSME Scheme Eligibility Suggester</h1>
                <p>
                    Discover which government MSME schemes your business qualifies for with AI-powered insights.
                </p>
            </header>

            <div className="container">
                {!results ? (
                    <div className="card">
                        <h2 style={{ marginBottom: '1.5rem', color: 'var(--neutral-900)' }}>
                            Enter Your Business Details
                        </h2>

                        {error && (
                            <div className="error-box">
                                <strong>Error:</strong> {error}
                            </div>
                        )}

                        <form onSubmit={handleSubmit}>
                            <div className="form-group">
                                <label htmlFor="annual_revenue">Annual Revenue (₹)</label>
                                <input
                                    type="number"
                                    id="annual_revenue"
                                    name="annual_revenue"
                                    value={formData.annual_revenue}
                                    onChange={handleChange}
                                    required
                                    min="0"
                                    placeholder="e.g., 750000"
                                />
                                <span className="help-text">Your business's yearly income</span>
                            </div>

                            <div className="form-group">
                                <label htmlFor="credit_score">Credit Score</label>
                                <input
                                    type="number"
                                    id="credit_score"
                                    name="credit_score"
                                    value={formData.credit_score}
                                    onChange={handleChange}
                                    required
                                    min="300"
                                    max="900"
                                    placeholder="e.g., 680"
                                />
                                <span className="help-text">CIBIL score (300-900)</span>
                            </div>

                            <div className="form-group">
                                <label htmlFor="years_in_business">Years in Business</label>
                                <input
                                    type="number"
                                    id="years_in_business"
                                    name="years_in_business"
                                    value={formData.years_in_business}
                                    onChange={handleChange}
                                    required
                                    min="0"
                                    step="0.5"
                                    placeholder="e.g., 2.5"
                                />
                                <span className="help-text">How long you've been operating</span>
                            </div>

                            <div className="form-group">
                                <label htmlFor="industry_type">Industry Type</label>
                                <select
                                    id="industry_type"
                                    name="industry_type"
                                    value={formData.industry_type}
                                    onChange={handleChange}
                                    required
                                >
                                    <option value="Manufacturing">Manufacturing</option>
                                    <option value="Services">Services</option>
                                    <option value="Retail">Retail</option>
                                    <option value="Technology">Technology</option>
                                    <option value="Agriculture">Agriculture</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>

                            <div className="form-group">
                                <label>Preferred Language</label>
                                <div className="language-selector">
                                    <button
                                        type="button"
                                        className={`language-btn ${formData.preferred_language === 'english' ? 'active' : ''}`}
                                        onClick={() => setFormData(prev => ({ ...prev, preferred_language: 'english' }))}
                                    >
                                        English
                                    </button>
                                    <button
                                        type="button"
                                        className={`language-btn ${formData.preferred_language === 'hindi' ? 'active' : ''}`}
                                        onClick={() => setFormData(prev => ({ ...prev, preferred_language: 'hindi' }))}
                                    >
                                        हिंदी
                                    </button>
                                </div>
                            </div>

                            <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
                                {loading ? (
                                    <>
                                        <span className="spinner"></span>
                                        Checking Eligibility...
                                    </>
                                ) : (
                                    '🔍 Check MSME Scheme Eligibility'
                                )}
                            </button>
                        </form>
                    </div>
                ) : (
                    <div className="results">
                        <div className="card">
                            <h2>📊 Your Eligibility Results</h2>

                            <div style={{ textAlign: 'center', margin: '2rem 0' }}>
                                <div className={`score-badge ${getScoreClass(results.eligibility_score)}`}>
                                    {results.eligibility_score}/100
                                </div>
                                <p style={{ color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                                    Eligibility Score
                                </p>
                            </div>

                            {/* AI Explanation */}
                            <div className="ai-explanation">
                                <h3>✨ AI-Powered Analysis</h3>
                                <p>{results.ai_explanation}</p>
                            </div>

                            {/* Eligible Schemes */}
                            {results.eligible_schemes && results.eligible_schemes.length > 0 && (
                                <div style={{ marginTop: '2rem' }}>
                                    <h3 style={{ marginBottom: '1rem', color: 'var(--success)' }}>
                                        ✅ Eligible Schemes ({results.eligible_schemes.length})
                                    </h3>
                                    <div className="loans-grid">
                                        {results.eligible_schemes.map((scheme) => (
                                            <div key={scheme.id} className="loan-card loan-card-eligible">
                                                <h4>{scheme.name}</h4>
                                                <p>{scheme.description}</p>
                                                <div className="loan-meta">
                                                    <strong>Max Loan:</strong> ₹{scheme.max_loan.toLocaleString('en-IN')}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Rejected Schemes */}
                            {results.rejected_schemes && results.rejected_schemes.length > 0 && (
                                <div style={{ marginTop: '2rem' }}>
                                    <h3 style={{ marginBottom: '1rem', color: 'var(--danger)' }}>
                                        ❌ Not Eligible ({results.rejected_schemes.length})
                                    </h3>
                                    <div className="loans-grid">
                                        {results.rejected_schemes.map((scheme) => (
                                            <div key={scheme.id} className="loan-card">
                                                <h4>{scheme.name}</h4>
                                                <div className="loan-meta">
                                                    <strong>Reasons:</strong>
                                                    <ul style={{ marginTop: '0.5rem', paddingLeft: '1.25rem' }}>
                                                        {scheme.reasons.map((reason, idx) => (
                                                            <li key={idx}>{reason}</li>
                                                        ))}
                                                    </ul>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            <button
                                onClick={handleReset}
                                className="btn btn-primary btn-full"
                                style={{ marginTop: '2rem' }}
                            >
                                🔄 Check Another Business
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default App;
