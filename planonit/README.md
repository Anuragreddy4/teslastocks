# Planonit - AI-Powered Study Planning Platform

![Planonit Logo](https://img.shields.io/badge/Planonit-AI%20Study%20Planner-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)

Planonit is an intelligent web application that helps students create personalized study plans by analyzing their syllabus and previous year question papers using AI-powered analysis.

## 🌟 Features

- **📝 Syllabus Input**: Paste your course syllabus or curriculum
- **📄 PDF Analysis**: Upload previous year question papers (PDF format)
- **🤖 AI-Powered Analysis**: Uses ChatGPT to analyze question patterns and important topics
- **📅 Personalized Study Plans**: Generates customized week-by-week study schedules
- **🎯 Smart Insights**: Identifies high-frequency topics and difficulty patterns
- **⚡ Interactive UI**: Clean, modern, and responsive web interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (optional for demo mode)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Anuragreddy4/teslastocks.git
   cd teslastocks/planonit
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (Optional)
   
   Create a `.env` file in the `planonit` directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   SECRET_KEY=your_secret_key_here
   ```

   > **Note**: The application can run in demo mode without an OpenAI API key. In demo mode, it will generate sample study plans based on templates.

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   
   Navigate to: `http://localhost:5000`

## 📖 How to Use

### Step 1: Enter Your Syllabus
- Paste your course syllabus, curriculum, or list of topics in the text area
- Click "Save Syllabus"

### Step 2: Upload Question Papers (Optional)
- Upload PDF files of previous year examination papers
- The AI will analyze patterns, topics, and difficulty levels
- Multiple files can be uploaded sequentially

### Step 3: Generate Study Plan
- Select your desired study duration (4-16 weeks)
- Click "Generate Study Plan with AI"
- Receive a personalized, week-by-week study schedule

## 🛠️ Technical Architecture

### Backend
- **Framework**: Flask 3.0
- **PDF Processing**: PyPDF2
- **AI Integration**: OpenAI GPT-3.5-turbo
- **Session Management**: Flask sessions

### Frontend
- **HTML5**: Semantic structure
- **CSS3**: Modern, gradient-based design
- **JavaScript**: Async/await API calls
- **Responsive Design**: Mobile-friendly interface

### Project Structure
```
planonit/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
├── static/
│   ├── css/
│   │   └── style.css      # Styling
│   └── js/
│       └── script.js      # Client-side logic
├── templates/
│   └── index.html         # Main HTML template
└── uploads/               # Temporary file storage
```

## 🔑 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application page |
| `/upload_syllabus` | POST | Save syllabus text |
| `/upload_question_paper` | POST | Upload and analyze PDF |
| `/generate_plan` | POST | Generate study plan |
| `/health` | GET | Health check |

## 🎨 Features in Detail

### AI-Powered Analysis
- Extracts text from uploaded PDF question papers
- Identifies recurring topics and themes
- Analyzes question difficulty patterns
- Provides insights on important areas

### Smart Study Plan Generation
- Personalized based on syllabus content
- Incorporates insights from previous year papers
- Flexible duration (4-16 weeks)
- Week-by-week breakdown with actionable tasks

### User-Friendly Interface
- Progressive disclosure (step-by-step)
- Real-time status updates
- Clear visual feedback
- Responsive design for all devices

## 🔒 Security Features

- File upload validation (PDF and TXT only)
- Maximum file size limit (16MB)
- Secure filename handling
- Session-based data storage
- Environment variable configuration

## 🌐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | No (demo mode available) |
| `SECRET_KEY` | Flask session secret key | No (auto-generated in dev) |

## 🐛 Troubleshooting

### Issue: "OpenAI API key not configured"
**Solution**: Either add your OpenAI API key to the `.env` file, or continue using demo mode which generates template-based plans.

### Issue: "PDF upload fails"
**Solution**: Ensure the file is a valid PDF under 16MB in size.

### Issue: "Port 5000 already in use"
**Solution**: Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 🚧 Future Enhancements

- [ ] User authentication and profiles
- [ ] Save and export study plans
- [ ] Progress tracking dashboard
- [ ] Multiple question paper comparison
- [ ] Subject-specific templates
- [ ] Mobile app version
- [ ] Calendar integration
- [ ] Study reminders

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Anuragreddy4**

- GitHub: [@Anuragreddy4](https://github.com/Anuragreddy4)

## 🙏 Acknowledgments

- OpenAI for the GPT API
- Flask framework community
- All contributors and users

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainer.

---

**Made with ❤️ for students everywhere**
