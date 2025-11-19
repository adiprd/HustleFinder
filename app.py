from flask import Flask, render_template, request, jsonify, session
import pandas as pd
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'sidehustle_secret_2024'

# Side Hustle Database
SIDE_HUSTLES = [
    {
        'id': 1,
        'title': 'Freelance Graphic Design',
        'category': 'Creative',
        'skills': ['design', 'creativity', 'software'],
        'earning_potential': {'low': 500, 'high': 3000},
        'time_commitment': '5-15 hours/week',
        'startup_cost': 'Low ($0-100)',
        'description': 'Create logos, social media graphics, and branding materials for clients',
        'trend_score': 85,
        'platforms': ['Upwork', 'Fiverr', '99designs'],
        'learning_resources': ['Canva Tutorials', 'Adobe Creative Suite Courses']
    },
    {
        'id': 2,
        'title': 'Social Media Management',
        'category': 'Digital Marketing',
        'skills': ['social media', 'content creation', 'analytics'],
        'earning_potential': {'low': 300, 'high': 2000},
        'time_commitment': '3-10 hours/week',
        'startup_cost': 'Very Low ($0-50)',
        'description': 'Manage social media accounts for small businesses and influencers',
        'trend_score': 90,
        'platforms': ['Instagram', 'LinkedIn', 'Facebook'],
        'learning_resources': ['Social Media Marketing Courses', 'Content Strategy Guides']
    },
    {
        'id': 3,
        'title': 'Online Tutoring',
        'category': 'Education',
        'skills': ['teaching', 'subject expertise', 'communication'],
        'earning_potential': {'low': 400, 'high': 2500},
        'time_commitment': '5-20 hours/week',
        'startup_cost': 'Low ($0-100)',
        'description': 'Teach subjects you excel at to students online',
        'trend_score': 80,
        'platforms': ['Tutor.com', 'Chegg', 'Wyzant'],
        'learning_resources': ['Teaching Methodologies', 'Online Education Platforms']
    },
    {
        'id': 4,
        'title': 'E-commerce Store',
        'category': 'Business',
        'skills': ['sales', 'marketing', 'logistics'],
        'earning_potential': {'low': 1000, 'high': 10000},
        'time_commitment': '10-30 hours/week',
        'startup_cost': 'Medium ($100-500)',
        'description': 'Sell products through platforms like Shopify or Etsy',
        'trend_score': 75,
        'platforms': ['Shopify', 'Etsy', 'Amazon'],
        'learning_resources': ['E-commerce Courses', 'Digital Marketing Guides']
    },
    {
        'id': 5,
        'title': 'Content Writing',
        'category': 'Writing',
        'skills': ['writing', 'research', 'seo'],
        'earning_potential': {'low': 300, 'high': 2000},
        'time_commitment': '5-15 hours/week',
        'startup_cost': 'Very Low ($0-50)',
        'description': 'Write blog posts, articles, and web content for businesses',
        'trend_score': 82,
        'platforms': ['Upwork', 'Contena', 'ProBlogger'],
        'learning_resources': ['SEO Writing Courses', 'Content Marketing Guides']
    },
    {
        'id': 6,
        'title': 'Virtual Assistant',
        'category': 'Administrative',
        'skills': ['organization', 'communication', 'time management'],
        'earning_potential': {'low': 400, 'high': 1800},
        'time_commitment': '10-25 hours/week',
        'startup_cost': 'Low ($0-100)',
        'description': 'Provide administrative support to busy professionals and entrepreneurs',
        'trend_score': 78,
        'platforms': ['Upwork', 'Zirtual', 'Time Etc'],
        'learning_resources': ['Virtual Assistant Training', 'Productivity Tools']
    }
]

SKILLS_DATABASE = [
    'writing', 'design', 'programming', 'marketing', 'sales', 'teaching',
    'photography', 'video editing', 'social media', 'seo', 'analytics',
    'customer service', 'project management', 'research', 'data analysis',
    'creativity', 'communication', 'organization', 'leadership', 'problem solving'
]

class SideHustleFinder:
    def __init__(self):
        self.user_profile = {}
        
    def assess_skills(self, skills_input):
        """Assess user skills and match with opportunities"""
        user_skills = [skill.lower().strip() for skill in skills_input]
        
        # Calculate skill matches for each side hustle
        matches = []
        for hustle in SIDE_HUSTLES:
            matching_skills = set(user_skills) & set(hustle['skills'])
            match_score = len(matching_skills) / len(hustle['skills']) * 100
            
            matches.append({
                **hustle,
                'match_score': round(match_score),
                'matching_skills': list(matching_skills),
                'missing_skills': list(set(hustle['skills']) - set(user_skills))
            })
        
        # Sort by match score and trend score
        matches.sort(key=lambda x: (x['match_score'], x['trend_score']), reverse=True)
        return matches
    
    def generate_business_plan(self, hustle_id, user_goals):
        """Generate personalized business plan"""
        hustle = next((h for h in SIDE_HUSTLES if h['id'] == hustle_id), None)
        if not hustle:
            return None
            
        # Calculate realistic timeline based on goals
        weekly_hours = user_goals.get('weekly_hours', 10)
        target_income = user_goals.get('target_income', 1000)
        
        avg_earning = (hustle['earning_potential']['low'] + hustle['earning_potential']['high']) / 2
        estimated_months = max(1, round(target_income / (avg_earning / 3)))  # 3 months rolling average
        
        plan = {
            'hustle': hustle,
            'timeline': {
                'months_to_profit': estimated_months,
                'weekly_hours': weekly_hours,
                'phase_1': 'Setup & Learning (1-2 weeks)',
                'phase_2': 'First Clients (1 month)',
                'phase_3': 'Scale Up (2-3 months)'
            },
            'action_steps': [
                f"Learn essential skills: {', '.join(hustle['learning_resources'][:2])}",
                f"Create portfolio or sample work",
                f"Join platforms: {', '.join(hustle['platforms'][:2])}",
                "Reach out to first 10 potential clients",
                "Collect testimonials and build reputation"
            ],
            'financial_projections': {
                'month_1_income': hustle['earning_potential']['low'] * 0.3,
                'month_3_income': hustle['earning_potential']['low'],
                'month_6_income': avg_earning
            }
        }
        
        return plan

finder = SideHustleFinder()

@app.route('/')
def index():
    return render_template('index.html', skills=SKILLS_DATABASE)

@app.route('/assess', methods=['POST'])
def assess():
    data = request.json
    
    # Store user profile
    finder.user_profile = {
        'skills': data.get('skills', []),
        'interests': data.get('interests', []),
        'weekly_hours': data.get('weekly_hours', 10),
        'target_income': data.get('target_income', 1000)
    }
    
    # Get matches
    matches = finder.assess_skills(finder.user_profile['skills'])
    
    return jsonify({
        'matches': matches[:5],  # Top 5 matches
        'user_profile': finder.user_profile
    })

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    data = request.json
    hustle_id = data.get('hustle_id')
    
    plan = finder.generate_business_plan(hustle_id, finder.user_profile)
    
    return jsonify({
        'business_plan': plan
    })

if __name__ == '__main__':
    print("🚀 Side Hustle Finder started at http://localhost:5000")
    app.run(debug=True, port=5000)
