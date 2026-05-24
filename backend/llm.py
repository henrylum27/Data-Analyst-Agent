import requests


def ask_local_llm(prompt: str, model: str = "llama3.2") -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )

    response.raise_for_status()
    return response.json()["response"]


def generate_executive_summary(profile: dict, anomalies: list) -> str:
    prompt = f"""
You are a senior business data analyst.

You are reviewing a company sales dataset. Your job is to write a useful executive summary for business users, not a technical summary.

Use ONLY the information provided below. Do not invent exact facts that are not supported by the data.

Dataset profile:
{profile}

Detected anomalies:
{anomalies}

Write the report using this exact structure:

1. Dataset Overview
Explain what the dataset appears to contain based on the columns, number of rows, and available fields.

2. Key Data Quality Issues
Focus especially on missing values. Mention which fields have missing values, and explain why those missing values matter.

3. Business Impact of Missing Values
Explain how missing values could affect company decisions. For example:
- Missing region can affect regional sales performance analysis.
- Missing product can affect product profitability analysis.
- Missing sales or profit can affect revenue and margin reporting.
- Missing sales rep can affect employee performance tracking.
- Missing payment method or sales channel can affect customer behavior analysis.

4. Anomalies and Risk Areas
Explain any unusual values or outliers detected. Discuss how very high sales, negative profit, or unusual quantities could affect reporting.

5. Recommendations
Give clear and practical recommendations. Include:
- Data cleaning actions
- Validation rules
- Required fields
- Follow-up checks
- Dashboard/reporting improvements
- Business process improvements

6. Suggested Next Analysis
Suggest useful follow-up analysis the company should perform, such as:
- Sales by region
- Profit by product
- Missing value trend by date
- Sales rep performance
- Negative profit investigation
- Channel and payment method analysis

Tone:
- Professional
- Practical
- Business-focused
- Clear enough for a manager to understand

Avoid saying the dataset is perfect if there are missing values or anomalies.
Do not only describe the data. Explain why it matters to the company.
"""

    return ask_local_llm(prompt)