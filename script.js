// ===== MOBILE-FIRST PROFESSIONAL WEBSITE ===== //
// Menu Hamburger & Interactive Features

document.addEventListener('DOMContentLoaded', function() {
    // ===== MOBILE MENU FUNCTIONALITY =====
    const menuToggle = document.getElementById('menuToggle');
    const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
    
    // Check if elements exist
    if (!menuToggle || !mobileMenuOverlay) {
        console.warn('Menu elements not found');
        return;
    }

    // Toggle mobile menu
    function toggleMobileMenu() {
        const isActive = mobileMenuOverlay.classList.contains('active');
        
        if (isActive) {
            closeMobileMenu();
        } else {
            openMobileMenu();
        }
    }

    // Open mobile menu
    function openMobileMenu() {
        mobileMenuOverlay.classList.add('active');
        menuToggle.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        // Focus management for accessibility
        setTimeout(() => {
            mobileNavLinks[0]?.focus();
        }, 100);
        
        console.log('Mobile menu opened');
    }

    // Close mobile menu
    function closeMobileMenu() {
        mobileMenuOverlay.classList.remove('active');
        menuToggle.classList.remove('active');
        document.body.style.overflow = '';
        
        console.log('Mobile menu closed');
    }

    // Event listeners
    menuToggle.addEventListener('click', toggleMobileMenu);

    // Close menu when clicking nav links
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });

    // Close menu when clicking outside
    mobileMenuOverlay.addEventListener('click', function(e) {
        if (e.target === mobileMenuOverlay) {
            closeMobileMenu();
        }
    });

    // Close menu with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileMenuOverlay.classList.contains('active')) {
            closeMobileMenu();
        }
    });

    // ===== SMOOTH SCROLLING =====
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const headerHeight = 72; // Header height
                const targetPosition = targetSection.offsetTop - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                console.log(`Smooth scroll to: ${targetId}`);
            }
        });
    });

    // ===== HEADER SCROLL EFFECT =====
    const header = document.querySelector('.header');
    let lastScrollTop = 0;
    
    function handleHeaderScroll() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 100) {
            header.style.boxShadow = '0 2px 20px rgba(18, 18, 18, 0.1)';
        } else {
            header.style.boxShadow = 'none';
        }
        
        lastScrollTop = scrollTop;
    }
    
    // Throttle scroll events for performance
    let ticking = false;
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(handleHeaderScroll);
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', function() {
        requestTick();
        ticking = false;
    });

    // ===== FORM HANDLING =====
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            // Basic validation
            if (!data.name || !data.email || !data.subject || !data.message) {
                showNotification('Per favore compila tutti i campi obbligatori', 'error');
                return;
            }
            
            if (!isValidEmail(data.email)) {
                showNotification('Per favore inserisci un indirizzo email valido', 'error');
                return;
            }
            
            // Simulate form submission
            console.log('Form submission:', data);
            
            // Show success message
            showNotification('Messaggio inviato con successo! Ti contatteremo presto.', 'success');
            
            // Reset form
            this.reset();
        });
    }

    // ===== ANIMATION ON SCROLL =====
    const animatedElements = document.querySelectorAll('.about-card, .service-card, .portfolio-item');
    
    if (animatedElements.length > 0) {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);
        
        // Set initial state and observe elements
        animatedElements.forEach(element => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(30px)';
            element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(element);
        });
    }

    // ===== BUTTON INTERACTIONS =====
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            if (!this.classList.contains('btn-loading')) {
                this.style.transform = 'translateY(-2px)';
            }
        });
        
        button.addEventListener('mouseleave', function() {
            if (!this.classList.contains('btn-loading')) {
                this.style.transform = 'translateY(0)';
            }
        });
    });

    // ===== LOADING STATES =====
    function addLoadingState(button) {
        button.classList.add('btn-loading');
        button.style.opacity = '0.7';
        button.style.cursor = 'not-allowed';
    }
    
    function removeLoadingState(button) {
        button.classList.remove('btn-loading');
        button.style.opacity = '1';
        button.style.cursor = 'pointer';
    }

    // ===== UTILITY FUNCTIONS =====
    
    // Email validation
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Show notification
    function showNotification(message, type = 'info') {
        // Remove existing notifications
        const existingNotifications = document.querySelectorAll('.notification');
        existingNotifications.forEach(notification => notification.remove());
        
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        notification.style.cssText = `
            position: fixed;
            top: 24px;
            right: 24px;
            left: 24px;
            background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#C0A784'};
            color: white;
            padding: 16px 24px;
            border-radius: 8px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
            z-index: 10000;
            transform: translateY(-100px);
            transition: transform 300ms ease, opacity 300ms ease;
            font-weight: 500;
            font-family: 'Inter', sans-serif;
            max-width: 400px;
            margin: 0 auto;
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateY(0)';
        }, 100);
        
        // Animate out and remove
        setTimeout(() => {
            notification.style.transform = 'translateY(-100px)';
            notification.style.opacity = '0';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }, 4000);
        
        console.log(`Notification: ${message} (${type})`);
    }

    // ===== PERFORMANCE OPTIMIZATION =====
    
    // Debounce function for performance
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Throttle function for scroll events
    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // ===== ACCESSIBILITY ENHANCEMENTS =====
    
    // Add focus trap for mobile menu
    function trapFocus(element) {
        const focusableElements = element.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];
        
        element.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                if (e.shiftKey) {
                    if (document.activeElement === firstElement) {
                        lastElement.focus();
                        e.preventDefault();
                    }
                } else {
                    if (document.activeElement === lastElement) {
                        firstElement.focus();
                        e.preventDefault();
                    }
                }
            }
        });
    }
    
    // Apply focus trap when menu is open
    if (mobileMenuOverlay) {
        trapFocus(mobileMenuOverlay);
    }

    // ===== RESPONSIVE BEHAVIOR =====
    
    // Handle responsive navigation
    function handleResponsiveNavigation() {
        const width = window.innerWidth;
        const desktopNav = document.querySelector('.desktop-nav');
        const menuToggle = document.getElementById('menuToggle');
        
        if (width >= 768) {
            // Desktop view
            if (mobileMenuOverlay?.classList.contains('active')) {
                closeMobileMenu();
            }
        }
    }
    
    window.addEventListener('resize', debounce(handleResponsiveNavigation, 250));

    // ===== INITIALIZATION COMPLETE =====
    console.log('✨ Professional website initialized successfully');
    console.log('📱 Mobile menu functionality ready');
    console.log('🎯 Smooth scrolling enabled');
    console.log('📋 Form handling configured');
    console.log('♿ Accessibility features active');
});

// ===== GLOBAL FUNCTIONS =====

// Utility function to check if element is in viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Function to scroll to top
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Function to get scroll percentage
function getScrollPercentage() {
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight - windowHeight;
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    return (scrollTop / documentHeight) * 100;
}

// ===== SERVICE WORKER REGISTRATION (Optional) =====
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // navigator.registerServiceWorker('/sw.js')
        //     .then(registration => console.log('SW registered'))
        //     .catch(error => console.log('SW registration failed'));
    });
}

// ===== ERROR HANDLING =====
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
});

// ===== EXPORT FOR TESTING =====
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        toggleMobileMenu: toggleMobileMenu,
        showNotification: showNotification,
        isValidEmail: isValidEmail
    };
}