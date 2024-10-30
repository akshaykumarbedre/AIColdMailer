# 🚀 Intelligent Cold Email Automation System

## Overview
An advanced cold email automation system that leverages AI to generate personalized, context-aware email content. Built with modern Python practices and powered by LangChain and Groq's LLM models, this system automates the entire cold email workflow from content generation to delivery.

## 🏗️ Project Structure
```text
project_root/
├── .env
├── requirements.txt
├── logging/
│   └── cold_email_automation.log
├── data/
│   └── generated_emails.csv
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── scraper.py
│   │   ├── email_generator.py
│   │   └── email_sender.py
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── factory.py
│   │   └── options.py
│   ├── ui/
│   │   ├── __init__.py
│   │   └── streamlit_app.py
│   └── main.py
```

## 🚀 Features

- **AI-Powered Email Generation**: Utilizes advanced LLMs through LangChain for context-aware email content
- **Smart Web Scraping**: Automatically extracts relevant information from target websites
- **Intelligent Content Personalization**: Generates highly personalized emails based on scraped context
- **Email Automation**: Handles email sending through Gmail SMTP
- **Modern UI**: Clean Streamlit interface for easy operation
- **Comprehensive Logging**: Detailed logging system for monitoring and debugging
- **Modular Architecture**: Well-organized, maintainable code structure

## 🛠️ Technology Stack

- **Python 3.x**: Core programming language
- **LangChain**: For LLM operations and chains
- **Groq**: LLM provider for fast and efficient text generation
- **BeautifulSoup4**: Web scraping
- **Streamlit**: User interface
- **Gmail SMTP**: Email delivery
- **Pydantic**: Data validation
- **Python-dotenv**: Environment management

## 📋 Prerequisites

- Python 3.8+
- Groq API key
- LangChain API key
- Gmail account with App Password enabled

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cold-email-automation.git
cd cold-email-automation
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root with:
```env
GROQ_API_KEY=your_groq_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
SENDER_EMAIL=your_gmail@gmail.com
SENDER_PASSWORD=your_gmail_app_password
```

## 🚀 Usage

1. Start the Streamlit application:
```bash
streamlit run src/ui/streamlit_app.py
```

2. In the UI:
   - Enter target website URLs
   - Choose LLM model (Groq LLaMA or Groq LLaMA 3.2)
   - Customize email generation parameters
   - Review and send generated emails

## 🔧 Key Components

### Email Generator
```python
class LangChainEmailGenerator(EmailGenerator):
    """
    Generates personalized emails using LangChain and Groq LLM models.
    Features include:
    - Context-aware content generation
    - Multi-step refinement process
    - JSON output parsing
    """
```

### Web Scraper
```python
class NavigationScraper(WebScraper):
    """
    Intelligent web scraping with:
    - Navigation link extraction
    - Domain-aware processing
    - Error handling
    """
```

### Email Sender
```python
class GmailSender(EmailSender):
    """
    Handles email delivery through Gmail SMTP with:
    - Secure authentication
    - Error handling
    - Delivery status tracking
    """
```

## 📊 Monitoring and Logging

The system maintains detailed logs in `logging/cold_email_automation.log`, tracking:
- Email generation attempts and results
- Web scraping operations
- Email sending status
- Error occurrences and handling

## 🔒 Security

- Secure credential management through environment variables
- Gmail App Password authentication
- Rate limiting for API calls and email sending
- Error handling and validation

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

Your Name - [akshaykumarbedre.bm@gmail.com](mailto:akshaykumarbedre.bm@gmail.com)


## 🙏 Acknowledgments

- LangChain for the amazing LLM framework
- Groq for providing fast and efficient LLM models
- Streamlit for the intuitive UI framework
