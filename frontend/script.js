// --- DOM Elements ---
const transcriptInput = document.getElementById('transcript-input');
const durationInput = document.getElementById('duration-input');
const scoreButton = document.getElementById('score-button');
const resultsArea = document.getElementById('results-area');
const overallScoreValue = document.getElementById('overall-score-value');
const wordCountValue = document.getElementById('word-count-value');
const criterionContainer = document.getElementById('criterion-scores-container');
const loadingSpinner = document.getElementById('loading-spinner'); // We'll use CSS for the spinner

// --- API Endpoint ---
const API_URL = 'http://127.0.0.1:8000/score';

// --- Event Listener ---
scoreButton.addEventListener('click', handleScoreRequest);

async function handleScoreRequest() {
    const transcript = transcriptInput.value;
    const duration = parseInt(durationInput.value, 10);

    // Basic validation
    if (!transcript.trim()) {
        alert('Please paste a transcript before scoring.');
        return;
    }

    // Show loading state
    scoreButton.disabled = true;
    scoreButton.textContent = 'Scoring...';
    resultsArea.classList.remove('hidden');
    criterionContainer.innerHTML = '<div class="loading"></div>'; // Simple loading indicator

    // Prepare request body
    const requestBody = {
        transcript: transcript,
    };
    if (!isNaN(duration) && duration > 0) {
        requestBody.duration_sec = duration;
    }

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
            // Handle server errors (like 422 or 500)
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Something went wrong on the server.');
        }

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        console.error('Error:', error);
        criterionContainer.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    } finally {
        // Reset button state
        scoreButton.disabled = false;
        scoreButton.textContent = 'Score My Transcript';
    }
}

function displayResults(data) {
    // Overall Score
    overallScoreValue.textContent = data.overall_score.toFixed(2);
    wordCountValue.textContent = `Word Count: ${data.word_count}`;

    // Clear previous results
    criterionContainer.innerHTML = '';

    // Per-Criterion Scores
    data.per_criterion_scores.forEach(item => {
        const card = document.createElement('div');
        card.className = 'criterion-card';

        const title = document.createElement('h4');
        title.textContent = item.criteria;

        const scoreText = document.createElement('p');
        scoreText.innerHTML = `Score: <span class="score">${item.score.toFixed(2)}</span>`;
        
        const feedbackText = document.createElement('p');
        feedbackText.textContent = `Feedback: ${item.feedback}`;

        card.appendChild(title);
        card.appendChild(scoreText);
        card.appendChild(feedbackText);
        
        criterionContainer.appendChild(card);
    });
}