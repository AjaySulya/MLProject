# 📊 Student Math Score Predictor

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.0+-green.svg)
![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

A machine learning web application that predicts student mathematics scores based on various demographic and academic factors. Built with Flask and deployed with an intuitive web interface.

## 🎯 Project Overview

This project leverages machine learning algorithms to predict student performance in mathematics based on factors such as:
- Gender and ethnicity
- Parental level of education
- Lunch type (standard/free or reduced)
- Test preparation course completion
- Reading and writing scores

## 🗂️ Project Structure

```
student-math-score-predictor/
├── 📁 src/                     # Source code modules
│   ├── components/             # ML pipeline components
│   ├── pipeline/              # Training and prediction pipelines
│   └── utils.py               # Utility functions
├── 📁 builder/                # Model building scripts
├── 📁 logger/                 # Custom logging configuration
├── 📁 exception/              # Custom exception handling
├── 📁 notebook/               # Jupyter notebooks for EDA
├── 📁 templates/              # HTML templates for web app
├── 📁 static/                 # CSS, JS, and image files
├── 📁 venv/                   # Virtual environment
├── 📄 .gitignore             # Git ignore file
├── 🚀 app.py                 # Flask application entry point
├── ⚙️ application.py         # Application configuration
├── 📋 requirements.txt       # Python dependencies
├── 🔧 setup.py              # Package setup configuration
└── 📖 README.md             # Project documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd student-math-score-predictor
   ```

2. **Set up virtual environment**
   ```bash
   conda -m venv python==3.8
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package**
   ```bash
   pip install -e .
   ```

### 🏃‍♂️ Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:5000`

3. **Make predictions**
   Fill in the student information form and get instant math score predictions!

## 📊 Features

- **🎯 Accurate Predictions**: Machine learning model trained on student performance data
- **🌐 Web Interface**: User-friendly Flask web application
- **📱 Responsive Design**: Works on desktop and mobile devices
- **📈 Data Visualization**: Interactive charts and graphs in notebooks
- **🔍 Model Interpretability**: Feature importance analysis
- **⚡ Real-time Predictions**: Instant results through web interface

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python, Flask |
| **Machine Learning** | Scikit-learn, Pandas, NumPy |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Data Analysis** | Jupyter Notebooks, Matplotlib, Seaborn |
| **Deployment** | Flask Development Server |

## 📁 Key Components

### 🔧 Source Code (`src/`)
- **Components**: Modular ML pipeline components (data ingestion, transformation, model training)
- **Pipeline**: End-to-end training and prediction workflows
- **Utils**: Helper functions and utilities

### 🏗️ Builder (`builder/`)
Contains scripts for:
- Model building and training
- Feature engineering
- Model evaluation and validation

### 📝 Logger (`logger/`)
- Custom logging configuration
- Error tracking and debugging
- Performance monitoring

### ⚠️ Exception (`exception/`)
- Custom exception classes
- Error handling mechanisms
- Graceful failure management

### 📓 Notebook (`notebook/`)
- Exploratory Data Analysis (EDA)
- Model experimentation
- Data visualization and insights

## 📋 API Documentation

### Prediction Endpoint

**POST** `/predict`

**Request Body:**
```json
{
    "gender": "male/female",
    "race_ethnicity": "group A/B/C/D/E",
    "parental_level_of_education": "education level",
    "lunch": "standard/free or reduced",
    "test_preparation_course": "completed/none",
    "reading_score": 0-100,
    "writing_score": 0-100
}
```

**Response:**
```json
{
    "predicted_math_score": 85.5,
    "status": "success"
}
```

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| **R² Score** | 0.75+ |
| **Mean Absolute Error** | < 10 points |
| **Root Mean Square Error** | < 15 points |

## 🔬 Data Analysis

The project includes comprehensive data analysis in Jupyter notebooks:

- **Data Distribution Analysis**: Understanding score distributions
- **Feature Correlation**: Identifying important predictive features
- **Model Comparison**: Evaluating different ML algorithms
- **Performance Visualization**: Charts and graphs showing model accuracy

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Update configuration in `application.py`
2. Set environment variables
3. Deploy to your preferred cloud platform

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📈 Future Enhancements

- [ ] **Advanced Models**: Implement ensemble methods and neural networks
- [ ] **Mobile App**: React Native mobile application
- [ ] **API Integration**: RESTful API for external integrations
- [ ] **Cloud Deployment**: AWS/GCP deployment with auto-scaling
- [ ] **A/B Testing**: Model comparison and performance tracking

## 🐛 Troubleshooting

### Common Issues

**Issue**: ImportError when running the application
```bash
# Solution: Ensure all dependencies are installed
pip install -r requirements.txt
```

**Issue**: Model not found error
```bash
# Solution: Train the model first
python -m src.pipeline.train_pipeline
```

**Issue**: Port already in use
```bash
# Solution: Use a different port
python app.py --port 8000
```

## 📞 Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Documentation**: Check the `/notebook` folder for detailed analysis
- **Contact**: [Your contact information]

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Dataset**: Student Performance Dataset from [source]
- **Libraries**: Thanks to the open-source community
- **Inspiration**: Educational data analysis and student success prediction

---

<div align="center">

**Made with ❤️ for educational data science**

[⭐ Star this repo](https://github.com/AjaySulya/studentmarkspredictor) | [🐛 Report Bug](https://github.com/AjaySulya/studentmarkspredictor/issues) | [💡 Request Feature](https://github.com/AjaySulya/studentmarkspredictor/pulls)

</div>

---

### 📊 Quick Stats

![GitHub stars](https://github.com/AjaySulya/studentmarkspredictor?style=social)
![GitHub forks](https://github.com/AjaySulya/studentmarkspredictor?style=social)
![GitHub issues](https://github.com/AjaySulya/studentmarkspredictor/issues)
![GitHub pull requests](https://github.com/AjaySulya/studentmarkspredictor/pulls)

*Last updated: [13-Aug-2025]*