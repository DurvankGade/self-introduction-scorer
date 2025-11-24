// --- DOM Elements ---
const transcriptInput = document.getElementById('transcript-input');
const durationInput = document.getElementById('duration-input');
const scoreButton = document.getElementById('score-button');
const resultsArea = document.getElementById('results-area');
const overallScoreValue = document.getElementById('overall-score-value');
const wordCountValue = document.getElementById('word-count-value');
const criterionContainer = document.getElementById('criterion-scores-container');
const loadingSpinner = document.getElementById('loading-spinner');
const scrollBtn = document.getElementById('scroll-to-score');
const yearSpan = document.getElementById('year');
const fileUploadInput = document.getElementById('file-upload');

//API Endpoint
//const API_URL = 'http://127.0.0.1:8000/score';
const API_URL = 'https://self-introduction-scorer.onrender.com/score';

//Initial Setup
if (yearSpan) yearSpan.textContent = new Date().getFullYear();

//Event Listeners
if (scrollBtn) {
    scrollBtn.addEventListener('click', (e) => {
        e.preventDefault();
        document.getElementById('scoring').scrollIntoView({ behavior: 'smooth', block: 'start' });
        transcriptInput.focus();
    });
}

scoreButton.addEventListener('click', handleScoreRequest);

if (fileUploadInput) {
    fileUploadInput.addEventListener('change', handleFileUpload);
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) {
        return; // No file selected
    }

    if (file.type !== 'text/plain') {
        alert('Please select a valid .txt file.');
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        transcriptInput.value = e.target.result;
    };
    reader.onerror = function() {
        alert('Error reading the file.');
    };
    reader.readAsText(file);
}

async function handleScoreRequest() {
    const transcript = transcriptInput.value;
    const duration = parseInt(durationInput.value, 10);

    if (!transcript.trim()) {
        alert('Please paste a transcript before scoring.');
        return;
    }

    // --- UI Loading State ---
    scoreButton.disabled = true;
    scoreButton.textContent = 'Scoring...';
    loadingSpinner.classList.remove('hidden');
    resultsArea.classList.remove('hidden');
    criterionContainer.innerHTML = '';
    // Scroll to results
    resultsArea.scrollIntoView({ behavior: 'smooth', block: 'center' });

    const requestBody = { transcript };
    if (!isNaN(duration) && duration > 0) {
        requestBody.duration_sec = duration;
    }

    try {
        const resp = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody)
        });

        if (!resp.ok) {
            const errData = await resp.json().catch(() => ({}));
            throw new Error(errData.detail || 'A server error occurred.');
        }

        const data = await resp.json();
        displayResults(data);

    } catch (err) {
        console.error('API Request Error:', err);
        criterionContainer.innerHTML = `<div class="criterion-card"><p style="color:#ff6b6b; font-weight: bold;">Error: ${err.message}</p></div>`;
    } finally {
        // --- Reset UI State ---
        scoreButton.disabled = false;
        scoreButton.textContent = 'Score My Transcript';
        loadingSpinner.classList.add('hidden');
    }
}

function displayResults(data) {
    overallScoreValue.textContent = (data.overall_score ?? 0).toFixed(2);
    wordCountValue.textContent = `Words: ${data.word_count ?? 0}`;
    criterionContainer.innerHTML = '';

    const items = data.per_criterion_scores || [];
    items.forEach(item => {
        const card = document.createElement('div');
        card.className = 'criterion-card';

        const title = document.createElement('h4');
        title.textContent = item.criteria || 'Criterion';

        const scoreText = document.createElement('p');
        scoreText.innerHTML = `Score: <span class="score-value">${(item.score ?? 0).toFixed(2)}</span>`;

        const feedbackText = document.createElement('p');
        feedbackText.textContent = `Feedback: ${item.feedback || 'No feedback'}`;

        card.appendChild(title);
        card.appendChild(scoreText);
        card.appendChild(feedbackText);
        criterionContainer.appendChild(card);
    });
}