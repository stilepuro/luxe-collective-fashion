// LUXE Collective - Interactive Features
document.addEventListener('DOMContentLoaded', function() {
    // Navigation scroll effect
    const navbar = document.getElementById('navbar');
    const hero = document.querySelector('.hero');
    
    // Handle navbar scroll behavior
    function handleNavbarScroll() {
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
    
    // Throttle scroll events for performance
    let ticking = false;
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateScroll);
            ticking = true;
        }
    }
    
    function updateScroll() {
        handleNavbarScroll();
        ticking = false;
    }
    
    // Add scroll listener
    window.addEventListener('scroll', requestTick, { passive: true });
    
    // Mobile menu toggle
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const navMenu = document.getElementById('nav-menu');
    
    mobileMenuToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        mobileMenuToggle.classList.toggle('active');
        
        // Animate hamburger menu
        const spans = mobileMenuToggle.querySelectorAll('span');
        if (mobileMenuToggle.classList.contains('active')) {
            spans[0].style.transform = 'rotate(45deg) translate(6px, 6px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translate(6px, -6px)';
        } else {
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }
    });
    
    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const navbarHeight = navbar.offsetHeight;
                const targetPosition = targetSection.offsetTop - navbarHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
            
            // Close mobile menu if open
            navMenu.classList.remove('active');
            mobileMenuToggle.classList.remove('active');
        });
    });
    
    // Product card interactions
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        const quickAddBtn = card.querySelector('.quick-add-btn');
        
        card.addEventListener('mouseenter', function() {
            if (quickAddBtn) {
                quickAddBtn.style.transform = 'translateX(-50%) translateY(0)';
                quickAddBtn.style.opacity = '1';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            if (quickAddBtn) {
                quickAddBtn.style.transform = 'translateX(-50%) translateY(100%)';
                quickAddBtn.style.opacity = '0';
            }
        });
        
        // Quick add functionality
        if (quickAddBtn) {
            quickAddBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                addToCart();
            });
        }
        
        // Product click functionality
        card.addEventListener('click', function() {
            const productTitle = card.querySelector('.product-title').textContent;
            showProductModal(productTitle);
        });
    });
    
    // Newsletter form submission
    const newsletterForm = document.querySelector('.newsletter-form');
    newsletterForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const emailInput = this.querySelector('.newsletter-input');
        const email = emailInput.value;
        
        if (validateEmail(email)) {
            subscribeNewsletter(email);
            emailInput.value = '';
        } else {
            showNotification('Please enter a valid email address', 'error');
        }
    });
    
    // Category card interactions
    const categoryCards = document.querySelectorAll('.category-card');
    categoryCards.forEach(card => {
        card.addEventListener('click', function() {
            const categoryName = card.querySelector('h3').textContent;
            handleCategoryClick(categoryName);
        });
    });
    
    // Editorial card interactions
    const editorialCards = document.querySelectorAll('.editorial-card');
    editorialCards.forEach(card => {
        card.addEventListener('click', function() {
            const articleTitle = card.querySelector('.editorial-title').textContent;
            handleArticleClick(articleTitle);
        });
    });
    
    // Button ripple effect
    const buttons = document.querySelectorAll('.btn, .btn-link');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            createRippleEffect(e, this);
        });
    });
    
    // Lazy loading for images
    const images = document.querySelectorAll('img');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => {
        imageObserver.observe(img);
    });
    
    // Animation on scroll
    const animatedElements = document.querySelectorAll('.product-card, .category-card, .editorial-card');
    const elementObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 600ms ease, transform 600ms ease';
        elementObserver.observe(el);
    });
});

// Utility Functions

function addToCart() {
    // Simulate adding to cart
    const cartCount = document.querySelector('.cart-count');
    const currentCount = parseInt(cartCount.textContent);
    cartCount.textContent = currentCount + 1;
    
    // Animate cart count
    cartCount.style.transform = 'scale(1.5)';
    setTimeout(() => {
        cartCount.style.transform = 'scale(1)';
    }, 200);
    
    showNotification('Item added to cart!', 'success');
}

function showProductModal(productTitle) {
    // Create a simple modal or redirect to product page
    console.log(`Opening product: ${productTitle}`);
    showNotification(`${productTitle} added to favorites!`, 'success');
}

function handleCategoryClick(categoryName) {
    console.log(`Exploring category: ${categoryName}`);
    showNotification(`Discovering ${categoryName} collection...`, 'success');
}

function handleArticleClick(articleTitle) {
    console.log(`Reading article: ${articleTitle}`);
    showNotification(`Opening: ${articleTitle}`, 'success');
}

function subscribeNewsletter(email) {
    console.log(`Subscribing email: ${email}`);
    showNotification('Successfully subscribed to newsletter!', 'success');
}

function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style the notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#3C8F63' : type === 'error' ? '#C53939' : '#B99763'};
        color: white;
        padding: 16px 24px;
        border-radius: 4px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        transform: translateX(400px);
        transition: transform 300ms ease;
        font-weight: 600;
        max-width: 300px;
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Animate out and remove
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

function createRippleEffect(event, button) {
    const ripple = document.createElement('span');
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        transform: scale(0);
        animation: ripple 600ms linear;
        pointer-events: none;
    `;
    
    button.style.position = 'relative';
    button.style.overflow = 'hidden';
    button.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Add CSS for ripple animation
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
    
    .notification {
        font-family: 'Inter', sans-serif;
    }
`;
document.head.appendChild(style);

// Performance optimizations
// Debounce scroll events
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

// Enhanced mobile menu styles
const mobileMenuStyles = `
    @media (max-width: 768px) {
        .nav-menu {
            position: fixed;
            top: 96px;
            left: 0;
            width: 100%;
            height: calc(100vh - 96px);
            background-color: var(--surface);
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 32px;
            transform: translateX(-100%);
            transition: transform 400ms cubic-bezier(0.25, 0.8, 0.25, 1);
            z-index: 999;
        }
        
        .nav-menu.active {
            transform: translateX(0);
        }
        
        .nav-link {
            font-size: 24px;
        }
    }
`;

const mobileStyleSheet = document.createElement('style');
mobileStyleSheet.textContent = mobileMenuStyles;
document.head.appendChild(mobileStyleSheet);