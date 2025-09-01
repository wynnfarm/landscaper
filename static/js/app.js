// Mobile-first JavaScript for Landscaper Web App

class LandscaperApp {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupServiceWorker();
        this.setupTouchGestures();
        this.setupViewportMeta();
    }

    setupEventListeners() {
        // Navigation
        document.addEventListener('DOMContentLoaded', () => {
            this.setupNavigation();
            this.setupForms();
            this.setupButtons();
        });

        // Handle back button
        window.addEventListener('popstate', (e) => {
            this.handleRoute(e.state);
        });

        // Handle orientation changes
        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                this.handleOrientationChange();
            }, 100);
        });

        // Handle online/offline status
        window.addEventListener('online', () => {
            this.showNotification('Connection restored', 'success');
        });

        window.addEventListener('offline', () => {
            this.showNotification('You are offline', 'warning');
        });
    }

    setupNavigation() {
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const href = link.getAttribute('href');
                if (href && href !== '#') {
                    this.navigateTo(href);
                }
            });
        });
    }

    setupForms() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                this.handleFormSubmit(e);
            });
        });

        // Add input validation
        const inputs = document.querySelectorAll('.form-input');
        inputs.forEach(input => {
            input.addEventListener('blur', () => {
                this.validateInput(input);
            });
        });
    }

    setupButtons() {
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(button => {
            button.addEventListener('click', (e) => {
                this.handleButtonClick(e);
            });
        });
    }

    setupServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/js/sw.js')
                .then(registration => {
                    console.log('Service Worker registered:', registration);
                })
                .catch(error => {
                    console.log('Service Worker registration failed:', error);
                });
        }
    }

    setupTouchGestures() {
        let startX, startY, endX, endY;

        document.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });

        document.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            endY = e.changedTouches[0].clientY;
            this.handleSwipe(startX, startY, endX, endY);
        });
    }

    setupViewportMeta() {
        // Ensure proper viewport meta tag for mobile
        let viewport = document.querySelector('meta[name="viewport"]');
        if (!viewport) {
            viewport = document.createElement('meta');
            viewport.name = 'viewport';
            document.head.appendChild(viewport);
        }
        viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
    }

    navigateTo(url) {
        // Add loading state
        this.showLoading();

        // Update URL without page reload
        history.pushState({ url }, '', url);

        // Handle route
        this.handleRoute({ url });

        // Hide loading
        setTimeout(() => {
            this.hideLoading();
        }, 300);
    }

    handleRoute(state) {
        if (!state || !state.url) return;

        const url = state.url;
        const content = document.querySelector('.main-content');

        // Simple routing logic
        switch (url) {
            case '/':
                this.showHome();
                break;
            case '/services':
                this.showServices();
                break;
            case '/contact':
                this.showContact();
                break;
            default:
                this.show404();
        }
    }

    handleFormSubmit(e) {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);

        // Show loading state
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.innerHTML = '<span class="spinner"></span> Sending...';
        submitBtn.disabled = true;

        // Simulate form submission
        setTimeout(() => {
            this.showNotification('Form submitted successfully!', 'success');
            form.reset();
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }, 2000);
    }

    handleButtonClick(e) {
        const button = e.target;
        const action = button.dataset.action;

        if (action) {
            e.preventDefault();
            this.executeAction(action, button);
        }
    }

    executeAction(action, element) {
        switch (action) {
            case 'call':
                this.makeCall(element.dataset.phone);
                break;
            case 'email':
                this.sendEmail(element.dataset.email);
                break;
            case 'location':
                this.openLocation(element.dataset.address);
                break;
            case 'share':
                this.shareContent();
                break;
        }
    }

    handleSwipe(startX, startY, endX, endY) {
        const deltaX = endX - startX;
        const deltaY = endY - startY;
        const minSwipeDistance = 50;

        if (Math.abs(deltaX) > Math.abs(deltaY)) {
            // Horizontal swipe
            if (Math.abs(deltaX) > minSwipeDistance) {
                if (deltaX > 0) {
                    this.handleSwipeRight();
                } else {
                    this.handleSwipeLeft();
                }
            }
        } else {
            // Vertical swipe
            if (Math.abs(deltaY) > minSwipeDistance) {
                if (deltaY > 0) {
                    this.handleSwipeDown();
                } else {
                    this.handleSwipeUp();
                }
            }
        }
    }

    handleSwipeLeft() {
        // Navigate to next section
        console.log('Swipe left detected');
    }

    handleSwipeRight() {
        // Navigate to previous section
        console.log('Swipe right detected');
    }

    handleSwipeUp() {
        // Scroll up or show more content
        console.log('Swipe up detected');
    }

    handleSwipeDown() {
        // Scroll down or refresh
        console.log('Swipe down detected');
    }

    handleOrientationChange() {
        // Adjust layout for orientation change
        const isLandscape = window.innerWidth > window.innerHeight;
        document.body.classList.toggle('landscape', isLandscape);
    }

    makeCall(phoneNumber) {
        if (phoneNumber) {
            window.location.href = `tel:${phoneNumber}`;
        }
    }

    sendEmail(email) {
        if (email) {
            window.location.href = `mailto:${email}`;
        }
    }

    openLocation(address) {
        if (address) {
            const encodedAddress = encodeURIComponent(address);
            window.open(`https://maps.google.com/maps?q=${encodedAddress}`, '_blank');
        }
    }

    shareContent() {
        if (navigator.share) {
            navigator.share({
                title: 'Landscaper Services',
                text: 'Check out our landscaping services!',
                url: window.location.href
            });
        } else {
            // Fallback for browsers that don't support Web Share API
            this.copyToClipboard(window.location.href);
            this.showNotification('Link copied to clipboard!', 'info');
        }
    }

    copyToClipboard(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text);
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
        }
    }

    validateInput(input) {
        const value = input.value.trim();
        const type = input.type;
        const required = input.hasAttribute('required');

        if (required && !value) {
            this.showInputError(input, 'This field is required');
            return false;
        }

        if (type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                this.showInputError(input, 'Please enter a valid email address');
                return false;
            }
        }

        if (type === 'tel' && value) {
            const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
            if (!phoneRegex.test(value.replace(/[\s\-\(\)]/g, ''))) {
                this.showInputError(input, 'Please enter a valid phone number');
                return false;
            }
        }

        this.clearInputError(input);
        return true;
    }

    showInputError(input, message) {
        this.clearInputError(input);
        input.classList.add('error');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'input-error';
        errorDiv.textContent = message;
        errorDiv.style.color = '#dc3545';
        errorDiv.style.fontSize = '14px';
        errorDiv.style.marginTop = '4px';
        
        input.parentNode.appendChild(errorDiv);
    }

    clearInputError(input) {
        input.classList.remove('error');
        const errorDiv = input.parentNode.querySelector('.input-error');
        if (errorDiv) {
            errorDiv.remove();
        }
    }

    showLoading() {
        const loading = document.createElement('div');
        loading.id = 'loading-overlay';
        loading.innerHTML = '<div class="spinner"></div>';
        loading.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.9);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        `;
        document.body.appendChild(loading);
    }

    hideLoading() {
        const loading = document.getElementById('loading-overlay');
        if (loading) {
            loading.remove();
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : type === 'warning' ? '#ffc107' : '#17a2b8'};
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            z-index: 10000;
            font-weight: 500;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(-50%) translateY(-20px)';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }

    showHome() {
        // Implementation for home page
        console.log('Showing home page');
    }

    showServices() {
        // Implementation for services page
        console.log('Showing services page');
    }

    showContact() {
        // Implementation for contact page
        console.log('Showing contact page');
    }

    show404() {
        // Implementation for 404 page
        console.log('Showing 404 page');
    }
}

// Initialize the app
const app = new LandscaperApp();
