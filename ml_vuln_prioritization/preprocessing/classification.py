import pandas as pd
import re

# Load the dataset
df = pd.read_csv('../data/cleaned_exploits_data.csv')

# Define application types and corresponding keywords/CMS identifiers
app_types = {
    'ecom': {
        'keywords': ['shop', 'store', 'cart', 'payment', 'checkout', 'orders', 'transactions'],
        'cms': ['Magento', 'PrestaShop', 'WooCommerce', 'Shopify', 'OpenCart']
    },
    'blog': {
        'keywords': ['blog', 'post', 'article', 'publish', 'comments', 'editor'],
        'cms': ['WordPress', 'Ghost', 'Joomla', 'Drupal']
    },
    'social_media': {
        'keywords': ['social', 'friend', 'follow', 'like', 'comment', 'message', 'chat'],
        'cms': ['BuddyPress', 'Dolphin', 'SocialEngine']
    },
    'cms': {
        'keywords': ['content', 'page', 'builder', 'template', 'drag-and-drop', 'themes'],
        'cms': ['WordPress', 'Joomla', 'Wix', 'Weebly', 'Squarespace']
    },
    'forums': {
        'keywords': ['forum', 'thread', 'post', 'discussion', 'reply', 'community'],
        'cms': ['phpBB', 'MyBB', 'vBulletin', 'SMF']
    },
    'educational': {
        'keywords': ['course', 'quiz', 'learning', 'student', 'teacher', 'lessons'],
        'cms': ['Moodle', 'Canvas', 'Blackboard']
    },
    'news_media': {
        'keywords': ['news', 'media', 'journalism', 'headline', 'broadcast', 'report'],
        'cms': ['WordPress', 'Joomla', 'Drupal', 'Ghost']
    },
    'android': {
        'keywords': ['android', 'apk', 'application', 'app', 'mobile', 'device', 'play store'],
        'cms': ['Flutter', 'React Native', 'Android Studio']
    }
}

# Define priorities based on application type
priority_mapping = {
    'ecom': {
        'critical': ['credit card skimming', 'SQL injection', 'unauthorized transaction', 'RCE'],
        'high': ['user account compromise', 'XSS in product reviews', 'admin panel access'],
        'medium': ['cart functionality', 'insufficient logging', 'weak password policy'],
        'low': ['minor UI glitches', 'incorrect product display', 'cart persistence issues']
    },
    'blog': {
        'critical': ['database credential exposure', 'RCE via file upload', 'privilege escalation'],
        'high': ['unauthorized content publishing', 'exposing private data', 'XSS in profiles'],
        'medium': ['comment spam bypass', 'weak admin password policy', 'info disclosure'],
        'low': ['minor layout issues', 'redundant plugin dependencies', 'non-responsive design']
    },
    'social_media': {
        'critical': ['data scraping', 'data leakage', 'malicious access'],
        'high': ['session fixation', 'CSRF', 'phishing attacks'],
        'medium': ['IDOR', 'weak password reset', 'content moderation bypass'],
        'low': ['UI enhancement requests', 'minor accessibility issues', 'outdated documentation']
    },
    'forums': {
        'critical': ['sensitive data leaks', 'SQL injection', 'privilege escalation'],
        'high': ['account takeover', 'file upload exploitation', 'DoS via excessive posts'],
        'medium': ['link injection', 'inadequate CAPTCHA', 'improper session management'],
        'low': ['feature requests', 'minor formatting issues', 'poor search functionality']
    },
    'educational': {
        'critical': ['exposing grades', 'insecure student data', 'unauthorized access'],
        'high': ['credential stuffing', 'weak quiz systems', 'manipulation of user roles'],
        'medium': ['input validation', 'sensitive data exposure', 'insecure file handling'],
        'low': ['layout issues', 'outdated content', 'slow loading materials']
    },
    'news_media': {
        'critical': ['confidential info publication', 'insecure journalist data', 'unauthorized access'],
        'high': ['XSS in comments', 'user data exposure', 'data scraping'],
        'medium': ['weak authentication', 'improper error handling', 'IDOR'],
        'low': ['redundant ads', 'layout inconsistencies', 'CDN issues']
    },
    'android': {
        'critical': ['insecure storage', 'malicious impersonation', 'data access exploitation'],
        'high': ['inadequate permissions', 'insecure API', 'weak SSL validation'],
        'medium': ['insufficient SSL pinning', 'access to sensitive data', 'installation security'],
        'low': ['performance lags', 'minor UI glitches', 'slow response']
    }
}

# Function to classify vulnerabilities based on keywords, description, and file path
def classify_vulnerability(vulnerability, file):
    app_type = "Unknown"
    priority = "Unknown"

    combined_text = f"{vulnerability} {file}"
    found = False
    
    # Identify application type based on keywords
    for type_key, data in app_types.items():
        for keyword in data['keywords'] + data['cms']:
            if re.search(keyword, combined_text, re.IGNORECASE):
                app_type = type_key
                found = True
                break
        if found:
            break

    # Fallback to General if no specific app_type found
    if app_type == "Unknown":
        app_type = 'General'

    # Check for priority based on the application type
    priority_keywords = priority_mapping.get(app_type, {})
    
    for priority_key, vulnerabilities in priority_keywords.items():
        if any(vuln.lower() in combined_text.lower() for vuln in vulnerabilities):
            priority = priority_key
            break

    # If no priority is found, assign a default priority (low)
    if priority == "Unknown":
        priority = 'low'

    return app_type, priority

# Apply the classification, checking 'description', 'file', and 'platform_code' columns
df['application_type'], df['priority'] = zip(*df.apply(lambda row: classify_vulnerability(row['description'], row['file']), axis=1))


# Save the updated dataframe
df.to_csv("../data/classified_exploits.csv")

print(df.columns)
