# AI-Assisted Web Credibility Scorer

An AI-assisted Python application that evaluates the credibility of web
sources using rule-based scoring, webpage-level evidence, and an optional
large language model (LLM).

The project improves a baseline URL credibility scorer by examining the
actual content and metadata of webpages rather than relying only on URL and
domain characteristics.

---

## Project Overview

Determining whether an online source is credible cannot reliably be
accomplished using a single characteristic.

The original credibility scorer primarily evaluated:

- Domain reputation
- Top-level domain
- HTTPS usage
- DOI presence
- URL path characteristics

Although these features provided a useful baseline, the original system had
several limitations. It relied heavily on URL characteristics, treated `.edu`
domains too favorably, did not adequately distinguish preprints from
peer-reviewed research, provided limited explanations, and did not evaluate
score calibration.

This project improves the system by combining multiple credibility signals
into a more comprehensive scoring process.

---

## Project Goals

The main goals of the project were to:

- Improve the accuracy of automated credibility scoring
- Analyze webpage-level evidence
- Improve handling of `.edu` websites
- Distinguish preprints from peer-reviewed publications
- Generate clearer credibility explanations
- Evaluate score calibration
- Integrate an optional LLM credibility assessment
- Preserve the required `score_url()` interface

---

## How the Credibility Scorer Works

The improved system evaluates several categories of evidence.

### 1. URL-Based Analysis

The original URL-based rules remain part of the scoring system.

The scorer considers signals such as:

- Publisher reputation
- Top-level domain
- HTTPS
- DOI patterns
- Suspicious URL paths

Known publishers can receive reputation-based scores, while unknown websites
are evaluated using more general URL and domain characteristics.

---

### 2. Improved `.edu` Handling

The scorer does not automatically assume that every page hosted on an `.edu`
domain is highly authoritative.

The improved algorithm reduces the default credibility assigned to educational
domains and checks for patterns that may indicate:

- Personal pages
- Student pages
- Individually maintained content

This helps distinguish institutional content from personal content hosted on a
university domain.

---

### 3. Webpage-Level Inspection

One of the largest improvements was adding webpage inspection.

When a webpage can be retrieved, the system searches for credibility signals
such as:

- Identifiable authors
- Publication dates
- References
- Bibliographies
- Peer-review indicators
- Correction information
- Retraction warnings

These signals provide additional evidence because they evaluate the webpage
itself rather than only its URL.

If the webpage cannot be accessed, the system falls back to the other
available credibility signals.

---

### 4. Preprint Detection

The scorer handles research preprints separately from peer-reviewed
publications.

Sources hosted on recognized preprint repositories are treated cautiously
because the research may not have completed peer review.

A preprint warning does **not** automatically mean that the source is
unreliable. Instead, preprint status becomes one piece of evidence considered
by the scoring system.

---

### 5. Explainable Credibility Scores

The improved scorer provides explanations describing why individual signals
matter.

Examples include:

- Identifiable authors improve accountability.
- References allow readers to examine supporting evidence.
- Publication information provides useful context.
- HTTPS protects the connection but does not prove that information is true.
- Preprint status indicates that research may not have completed peer review.

This makes the final credibility score easier for users to understand.

---

### 6. Optional LLM Layer

The system includes an optional Claude-based credibility assessment using the
Anthropic API.

The LLM considers contextual characteristics such as:

- Publisher reputation
- Self-publication
- Peer-review status
- Editorial standards
- Source characteristics

The LLM judgment is combined with the rule-based assessment to improve the
final credibility estimate.

If the LLM is unavailable, the application can fall back to rules-only
scoring.

---

## Evaluation

The improved credibility scorer was evaluated on **24 URLs**.

Two configurations were compared:

1. Rules-only scoring
2. Rules + LLM scoring

### Results

| Evaluation | MAE | Band Accuracy | Worst Error |
|---|---:|---:|---:|
| Rules Only | 0.143 | 62.5% | 0.410 |
| Rules + LLM | **0.091** | **83.3%** | **0.230** |

Adding the LLM produced improvements across all three evaluation metrics.

### Performance Improvement

The LLM-assisted version:

- Reduced MAE from **0.143 to 0.091**
- Improved band accuracy from **62.5% to 83.3%**
- Reduced the worst individual error from **0.410 to 0.230**
- Reduced MAE by approximately **36.4%**
- Increased band accuracy by **20.8 percentage points**

These results indicate that combining rule-based signals with an LLM produced
scores that more closely matched the expected credibility labels in the
evaluation dataset.

---

## Calibration Analysis

A calibration plot was created to compare predicted credibility scores with
expected credibility scores.

The scorer was reasonably calibrated overall, but some low- and
medium-credibility predictions were higher than their expected values.

For example:

```text
Mean Predicted Score: 0.520
Mean Expected Score:  0.400
```

At higher credibility levels, predicted and expected scores were more closely
aligned.

The calibration analysis suggests that future improvements should focus on
reducing overestimation among low- and medium-credibility sources.

---

## Technologies and Tools

The project uses technologies including:

- Python
- Anthropic API / Claude
- HTTP requests
- HTML parsing
- Rule-based algorithms
- Large Language Models
- Web metadata analysis
- Data visualization
- Calibration analysis

---

## Core Function

The primary interface for the credibility scorer is:

```python
score_url(url)
```

The function returns a credibility score and an explanation of the evidence
used to produce the score.

Conceptually:

```python
{
    "score": 0.85,
    "explanation": "Explanation of the credibility signals..."
}
```

---

## Suggested Repository Structure

```text
ai-web-credibility-scorer/
│
├── credibility.py
├── evaluate.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── tests/
│   └── ...
│
└── figures/
    └── calibration_plot.png
```

---

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <repository-name>
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Environment

#### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Anthropic API Configuration

The LLM layer requires an Anthropic API key.

Create a `.env` file in the project directory:

```text
ANTHROPIC_API_KEY=your_api_key_here
```

Do **not** commit the `.env` file or your API key to GitHub.

Add it to `.gitignore`:

```text
.env
.venv/
__pycache__/
*.pyc
```

If an API key is not configured, the scorer can operate using its rule-based
credibility signals.

---

## Running the Evaluation

Run the evaluation script with:

```powershell
python evaluate.py
```

The evaluation compares predicted credibility scores with expected scores and
reports metrics such as:

```text
Mean Absolute Error
Band Accuracy
Worst Single Error
```

Use the evaluation results to compare the rules-only and LLM-assisted
configurations.

---

## Limitations

The credibility scorer still has several important limitations.

Some websites may:

- Block automated requests
- Require JavaScript
- Use paywalls
- Store content primarily in PDFs
- Prevent webpage metadata from being retrieved

The presence of an author, publication date, or references also does not
guarantee that a source is trustworthy.

The system currently focuses primarily on whether credibility indicators
exist rather than independently verifying the quality of every reference.

Preprint classification also remains imperfect because a preprint may later
become a peer-reviewed publication.

The LLM layer can also make incorrect assumptions and should not be considered
a source of ground truth.

Finally, the evaluation dataset contains only 24 URLs, so the reported results
should not be interpreted as evidence that the same performance will
generalize across the entire web.

---

## Future Improvements

Potential improvements include:

- Larger evaluation datasets
- Crossref metadata integration
- Retraction database integration
- Automated verification of references
- Improved peer-review detection
- Better preprint-to-publication matching
- Learned credibility weights
- Improved score calibration
- More sophisticated webpage content analysis
- Expanded automated testing

---

## Key Takeaways

This project demonstrates that web credibility assessment benefits from
combining multiple signals rather than relying only on domain reputation.

Adding webpage-level evidence improved the system's ability to examine the
actual characteristics of a source.

The optional LLM layer produced stronger results on the project's evaluation
dataset, reducing MAE and substantially improving credibility-band
classification accuracy.

The final system should be treated as a decision-support tool that helps users
evaluate sources rather than as an automated determination of whether
information is true or false.

---

## Skills Demonstrated

- Python development
- AI/LLM integration
- Anthropic API integration
- Web content analysis
- HTML parsing
- Rule-based systems
- Algorithm design
- Model evaluation
- Calibration analysis
- Error analysis
- Data visualization
- Software testing
- Explainable AI
- Responsible AI design

---
## Hugging Face Deployment

The Project 1 Credibility-Scored Research Chatbot is deployed on Hugging Face Spaces.

**Live Application:** https://huggingface.co/spaces/GQuellTS/credibility-scored-chatbot

## Author

**Shanquell Thompson-Sanders**

Data Science | Machine Learning | AI Development | Statistical Analysis
