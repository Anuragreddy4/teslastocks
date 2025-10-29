// Planonit JavaScript - Client-side functionality

function showStatus(elementId, message, type) {
    const statusEl = document.getElementById(elementId);
    statusEl.textContent = message;
    statusEl.className = `status-message ${type}`;
    statusEl.style.display = 'block';
}

function hideStatus(elementId) {
    const statusEl = document.getElementById(elementId);
    statusEl.style.display = 'none';
}

async function uploadSyllabus() {
    const syllabusInput = document.getElementById('syllabus-input');
    const syllabusText = syllabusInput.value.trim();
    
    if (!syllabusText) {
        showStatus('syllabus-status', 'Please enter your syllabus', 'error');
        return;
    }
    
    showStatus('syllabus-status', 'Saving syllabus...', 'info');
    
    try {
        const response = await fetch('/upload_syllabus', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ syllabus: syllabusText })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showStatus('syllabus-status', '✓ Syllabus saved successfully!', 'success');
        } else {
            showStatus('syllabus-status', `Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus('syllabus-status', `Error: ${error.message}`, 'error');
    }
}

async function uploadQuestionPaper() {
    const fileInput = document.getElementById('question-paper-input');
    const file = fileInput.files[0];
    
    if (!file) {
        showStatus('question-paper-status', 'Please select a file', 'error');
        return;
    }
    
    showStatus('question-paper-status', 'Analyzing question paper...', 'info');
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/upload_question_paper', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showStatus('question-paper-status', '✓ Question paper analyzed successfully!', 'success');
            displayAnalysis(data.analysis);
        } else {
            showStatus('question-paper-status', `Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus('question-paper-status', `Error: ${error.message}`, 'error');
    }
}

function displayAnalysis(analysis) {
    const analysisBox = document.getElementById('analysis-results');
    
    let html = '<h3>📊 Question Paper Analysis</h3>';
    
    if (analysis.error) {
        html += `<p style="color: #e53e3e;">${analysis.error}</p>`;
    }
    
    if (analysis.analysis) {
        html += `<div style="margin-bottom: 15px;"><strong>AI Analysis:</strong><br>${analysis.analysis.replace(/\n/g, '<br>')}</div>`;
    }
    
    if (analysis.topics_covered && analysis.topics_covered.length > 0) {
        html += '<div style="margin-bottom: 15px;"><strong>Topics Covered:</strong><ul>';
        analysis.topics_covered.forEach(topic => {
            html += `<li>${topic}</li>`;
        });
        html += '</ul></div>';
    }
    
    if (analysis.difficulty_level) {
        html += `<div style="margin-bottom: 15px;"><strong>Difficulty Level:</strong> ${analysis.difficulty_level}</div>`;
    }
    
    if (analysis.important_areas && analysis.important_areas.length > 0) {
        html += '<div><strong>Important Areas:</strong><ul>';
        analysis.important_areas.forEach(area => {
            html += `<li>${area}</li>`;
        });
        html += '</ul></div>';
    }
    
    analysisBox.innerHTML = html;
    analysisBox.classList.add('show');
}

async function generatePlan() {
    const durationWeeks = document.getElementById('duration-weeks').value;
    
    showStatus('plan-status', 'Generating your personalized study plan with AI...', 'info');
    
    try {
        const response = await fetch('/generate_plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ duration_weeks: durationWeeks })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showStatus('plan-status', '✓ Study plan generated successfully!', 'success');
            displayStudyPlan(data.plan);
        } else {
            showStatus('plan-status', `Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus('plan-status', `Error: ${error.message}`, 'error');
    }
}

function displayStudyPlan(plan) {
    const planBox = document.getElementById('study-plan-results');
    
    let html = '<h3>📅 Your Personalized Study Plan</h3>';
    
    if (plan.note) {
        html += `<div style="background: #fef3c7; padding: 10px; border-radius: 5px; margin-bottom: 15px; color: #92400e;">${plan.note}</div>`;
    }
    
    if (plan.study_plan) {
        // Convert markdown-like formatting to HTML
        const formattedPlan = plan.study_plan
            .replace(/\n/g, '<br>')
            .replace(/^# (.*?)(<br>|$)/gm, '<h4 style="color: #48bb78; margin-top: 15px;">$1</h4>')
            .replace(/^## (.*?)(<br>|$)/gm, '<h5 style="color: #4a5568; margin-top: 10px;">$1</h5>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/- (.*?)(<br>|$)/gm, '<li style="margin-left: 20px;">$1</li>');
        
        html += `<div style="line-height: 1.8;">${formattedPlan}</div>`;
    }
    
    if (plan.generated_at) {
        html += `<div style="margin-top: 20px; font-size: 0.9em; color: #718096;">Generated at: ${new Date(plan.generated_at).toLocaleString()}</div>`;
    }
    
    planBox.innerHTML = html;
    planBox.classList.add('show');
}

// Check backend health on page load
window.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        
        if (!data.openai_configured) {
            console.warn('OpenAI API key not configured. AI features will use demo mode.');
        }
    } catch (error) {
        console.error('Failed to check backend health:', error);
    }
});
