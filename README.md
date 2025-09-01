# Landscaper - Mobile-First Web Application

A modern, mobile-first web application for landscaping services, built with Flask and optimized for mobile devices.

## Features

- 📱 **Mobile-First Design**: Optimized for smartphones and tablets
- 🌿 **Landscaping Services**: Complete service catalog and booking system
- 📞 **Contact Integration**: Direct calling, email, and location services
- 🎨 **Modern UI**: Clean, responsive design with touch-friendly interface
- ⚡ **PWA Ready**: Progressive Web App capabilities for app-like experience
- 🔄 **Offline Support**: Service worker for offline functionality

## Project Structure

```
landscaper/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── static/               # Static assets
│   ├── css/
│   │   └── mobile.css    # Mobile-first CSS framework
│   ├── js/
│   │   └── app.js        # Mobile JavaScript functionality
│   └── images/           # Images and icons
├── templates/            # Jinja2 templates
│   ├── base.html         # Base template
│   └── index.html        # Home page
├── src/                  # Source code (for future expansion)
└── tests/                # Test files
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd landscaper
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your mobile browser and navigate to `http://localhost:5000`
   - Or use your computer's browser and resize to mobile view

## Mobile Features

### Touch Gestures
- **Swipe Navigation**: Swipe left/right to navigate between sections
- **Touch Targets**: All buttons and links are optimized for finger navigation
- **Responsive Design**: Adapts to different screen sizes and orientations

### Native Integration
- **Phone Calls**: Tap phone numbers to call directly
- **Email**: Tap email addresses to open email client
- **Maps**: Tap addresses to open in maps application
- **Share**: Share the app using native sharing capabilities

### Performance
- **Fast Loading**: Optimized CSS and JavaScript for mobile networks
- **Offline Support**: Basic functionality works without internet connection
- **PWA Features**: Can be installed as a home screen app

## Development

### Running in Development Mode
```bash
export DEBUG=True
python app.py
```

### Environment Variables
- `DEBUG`: Set to `True` for development mode
- `SECRET_KEY`: Flask secret key for sessions
- `PORT`: Port number (default: 5000)

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src
```

## Deployment

### Local Production
```bash
export DEBUG=False
export SECRET_KEY=your-secret-key
python app.py
```

### Docker Deployment
```bash
# Build image
docker build -t landscaper .

# Run container
docker run -p 5000:5000 landscaper
```

## Browser Support

- **Mobile Browsers**: iOS Safari, Chrome Mobile, Firefox Mobile
- **Desktop Browsers**: Chrome, Firefox, Safari, Edge (with mobile view)
- **PWA Support**: Modern browsers with service worker support

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
