"""
Planonit - AI-Powered Study Planning Platform
A web application that helps students create personalized study plans
by analyzing syllabus and previous year question papers.
"""

from flask import Flask, render_template, request, jsonify, session
import os
import PyPDF2
import openai
from datetime import datetime
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'txt'}

# OpenAI API configuration
openai.api_key = os.environ.get('OPENAI_API_KEY', '')

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_pdf(pdf_path):
    """Extract text content from a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def analyze_question_paper(pdf_text):
    """Analyze previous year question paper using ChatGPT."""
    if not openai.api_key:
        return {
            "topics_covered": ["Topic analysis requires OpenAI API key"],
            "difficulty_level": "Unable to analyze",
            "important_areas": ["Configure OPENAI_API_KEY to enable AI analysis"],
            "patterns": ["Demo mode - set up API key for real analysis"]
        }
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an educational expert analyzing exam papers."},
                {"role": "user", "content": f"Analyze this previous year question paper and identify key topics, difficulty patterns, and important areas:\n\n{pdf_text[:3000]}"}
            ],
            max_tokens=500
        )
        
        analysis = response.choices[0].message.content
        return {
            "analysis": analysis,
            "topics_covered": ["Extracted from AI analysis"],
            "difficulty_level": "Based on question complexity",
            "important_areas": ["High-frequency topics identified"]
        }
    except Exception as e:
        return {
            "error": f"AI analysis error: {str(e)}",
            "topics_covered": ["Analysis unavailable"],
            "difficulty_level": "Unknown",
            "important_areas": ["Unable to analyze"]
        }

def generate_study_plan(syllabus, analysis_data, duration_weeks):
    """Generate a personalized study plan using ChatGPT."""
    if not openai.api_key:
        # Return a sample study plan when API key is not configured
        return {
            "study_plan": create_sample_study_plan(syllabus, duration_weeks),
            "note": "This is a sample plan. Configure OPENAI_API_KEY for AI-generated plans."
        }
    
    try:
        prompt = f"""Create a detailed {duration_weeks}-week study plan based on:
        
Syllabus:
{syllabus}

Previous Year Analysis:
{json.dumps(analysis_data, indent=2)}

Provide a week-by-week breakdown with:
- Topics to cover each week
- Time allocation
- Practice recommendations
- Important areas to focus on based on previous year patterns
"""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert study planner helping students prepare effectively."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500
        )
        
        return {
            "study_plan": response.choices[0].message.content,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "error": f"Study plan generation error: {str(e)}",
            "study_plan": create_sample_study_plan(syllabus, duration_weeks)
        }

def create_sample_study_plan(syllabus, duration_weeks):
    """Create a basic study plan template."""
    plan = f"# {duration_weeks}-Week Study Plan\n\n"
    plan += f"**Syllabus Overview:**\n{syllabus[:200]}...\n\n"
    
    weeks_per_section = max(1, duration_weeks // 4)
    sections = ["Foundation Concepts", "Core Topics", "Advanced Topics", "Revision & Practice"]
    
    current_week = 1
    for section in sections:
        plan += f"\n## Weeks {current_week}-{min(current_week + weeks_per_section - 1, duration_weeks)}: {section}\n"
        plan += f"- Study main concepts\n"
        plan += f"- Complete exercises\n"
        plan += f"- Review previous year questions\n"
        current_week += weeks_per_section
    
    return plan

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/upload_syllabus', methods=['POST'])
def upload_syllabus():
    """Handle syllabus text input."""
    try:
        data = request.get_json()
        syllabus = data.get('syllabus', '')
        
        if not syllabus:
            return jsonify({'error': 'Syllabus text is required'}), 400
        
        session['syllabus'] = syllabus
        return jsonify({
            'success': True,
            'message': 'Syllabus saved successfully',
            'preview': syllabus[:200] + '...' if len(syllabus) > 200 else syllabus
        })
    except Exception as e:
        # Log the error for debugging (in production, use proper logging)
        print(f"Error in upload_syllabus: {e}")
        return jsonify({'error': 'Failed to save syllabus'}), 500

@app.route('/upload_question_paper', methods=['POST'])
def upload_question_paper():
    """Handle question paper PDF upload and analysis."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract text from PDF
            pdf_text = extract_text_from_pdf(filepath)
            
            # Analyze the question paper
            analysis = analyze_question_paper(pdf_text)
            
            # Store analysis in session
            session['question_paper_analysis'] = analysis
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'message': 'Question paper analyzed successfully',
                'analysis': analysis
            })
        
        return jsonify({'error': 'Invalid file type. Only PDF and TXT files are allowed'}), 400
    
    except Exception as e:
        # Log the error for debugging (in production, use proper logging)
        print(f"Error in upload_question_paper: {e}")
        return jsonify({'error': 'Failed to process question paper'}), 500

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    """Generate personalized study plan."""
    try:
        data = request.get_json()
        duration_weeks = int(data.get('duration_weeks', 8))
        
        syllabus = session.get('syllabus', '')
        analysis_data = session.get('question_paper_analysis', {})
        
        if not syllabus:
            return jsonify({'error': 'Please upload syllabus first'}), 400
        
        # Generate study plan
        plan_result = generate_study_plan(syllabus, analysis_data, duration_weeks)
        
        return jsonify({
            'success': True,
            'plan': plan_result
        })
    
    except Exception as e:
        # Log the error for debugging (in production, use proper logging)
        print(f"Error in generate_plan: {e}")
        return jsonify({'error': 'Failed to generate study plan'}), 500

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'openai_configured': bool(openai.api_key)
    })

if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Run the application
    # Debug mode should be False in production
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
