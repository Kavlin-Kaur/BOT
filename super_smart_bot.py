import os
import random
import csv
from datetime import datetime
import re
from difflib import SequenceMatcher

# Super comprehensive synonym map
SYNONYMS = {
    'internship': ['intern', 'training', 'placement', 'work experience', 'job training', 'career opportunity', 'professional development'],
    'wifi': ['internet', 'wireless', 'network', 'connection', 'online', 'web'],
    'food': ['mess', 'canteen', 'dining', 'eat', 'restaurant', 'cafeteria', 'meal', 'lunch', 'dinner'],
    'library': ['books', 'reading', 'study', 'research', 'learning center', 'study hall'],
    'hostel': ['dorm', 'accommodation', 'room', 'housing', 'residence', 'living'],
    'exam': ['test', 'assessment', 'paper', 'evaluation', 'quiz', 'examination'],
    'grade': ['marks', 'result', 'score', 'performance', 'academic standing'],
    'event': ['activity', 'function', 'fest', 'program', 'celebration', 'gathering'],
    'club': ['society', 'group', 'community', 'organization', 'association'],
    'scholarship': ['grant', 'aid', 'fellowship', 'financial support', 'funding', 'bursary'],
    'fee': ['fees', 'payment', 'charges', 'cost', 'tuition', 'expense'],
    'admission': ['enroll', 'apply', 'registration', 'entry', 'enrollment', 'admission'],
    'faculty': ['teacher', 'professor', 'lecturer', 'instructor', 'staff', 'academic'],
    'course': ['subject', 'class', 'curriculum', 'program', 'module', 'study'],
    'placement': ['job', 'career', 'recruitment', 'employment', 'work', 'position'],
    'sports': ['game', 'athletics', 'outdoor', 'physical activity', 'exercise', 'fitness'],
    'transport': ['bus', 'shuttle', 'commute', 'travel', 'transportation', 'vehicle'],
    'alumni': ['graduate', 'ex-student', 'former student', 'alumnus'],
    'research': ['project', 'lab', 'study', 'investigation', 'experiment', 'analysis'],
    'attendance': ['present', 'absent', 'proxy', 'participation', 'presence'],
    'holiday': ['vacation', 'break', 'leave', 'time off', 'recess'],
    'opportunity': ['chance', 'possibility', 'option', 'prospect', 'opening'],
    'help': ['support', 'assistance', 'aid', 'guidance', 'help'],
    'information': ['details', 'info', 'data', 'facts', 'knowledge'],
    'process': ['procedure', 'method', 'steps', 'way', 'approach'],
    'location': ['where', 'place', 'address', 'site', 'venue'],
    'time': ['when', 'schedule', 'timing', 'hours', 'deadline'],
    'contact': ['phone', 'email', 'reach', 'get in touch', 'call'],
    'apply': ['application', 'submit', 'register', 'sign up', 'enroll'],
    'access': ['use', 'enter', 'get to', 'reach', 'utilize'],
    'find': ['locate', 'discover', 'get', 'obtain', 'search'],
    'get': ['receive', 'obtain', 'acquire', 'secure', 'collect'],
    'how': ['what is the process', 'steps to', 'way to', 'method to'],
    'what': ['tell me about', 'explain', 'describe', 'information about'],
    'when': ['timing', 'schedule', 'time', 'deadline', 'date'],
    'where': ['location', 'place', 'address', 'site', 'venue'],
    'why': ['reason', 'purpose', 'cause', 'explanation', 'motivation'],
    'tell': ['explain', 'describe', 'inform', 'share', 'provide'],
    'about': ['regarding', 'concerning', 'related to', 'on the topic of'],
    'more': ['additional', 'extra', 'further', 'extended', 'detailed'],
    'general': ['overview', 'basic', 'general', 'overall', 'summary'],
    'details': ['specifics', 'particulars', 'information', 'facts', 'data'],
    'services': ['facilities', 'amenities', 'resources', 'support', 'help'],
    'available': ['accessible', 'offered', 'provided', 'accessible', 'open'],
    'campus': ['university', 'college', 'institution', 'school', 'academic'],
    'student': ['learner', 'pupil', 'scholar', 'undergraduate', 'graduate'],
    'academic': ['educational', 'scholastic', 'learning', 'study', 'academic'],
    'support': ['help', 'assistance', 'aid', 'guidance', 'backup'],
    'system': ['platform', 'portal', 'website', 'application', 'tool'],
    'online': ['digital', 'web-based', 'internet', 'virtual', 'electronic'],
    'portal': ['website', 'platform', 'system', 'interface', 'gateway'],
    'website': ['portal', 'site', 'page', 'platform', 'webpage'],
    'office': ['department', 'center', 'service', 'facility', 'unit'],
    'center': ['office', 'facility', 'service', 'department', 'unit'],
    'facility': ['center', 'office', 'service', 'department', 'unit'],
    'service': ['facility', 'center', 'office', 'department', 'unit'],
    'department': ['office', 'center', 'facility', 'service', 'unit'],
    'unit': ['office', 'center', 'facility', 'service', 'department']
}

# Question categories with better understanding
QUESTION_CATEGORIES = {
    'identity': ['who are you', 'what is your name', 'about you', 'tum kaun ho', 'apka naam', 'introduce yourself', 'kya ho tum', 'kaun ho tum'],
    'explanation': ['explain', 'tell me more', 'elaborate', 'details', 'more information', 'what do you mean', 'tell me about', 'describe'],
    'location': ['where', 'location', 'place', 'address', 'site', 'venue'],
    'process': ['how to', 'steps', 'procedure', 'method', 'way to', 'process'],
    'timing': ['when', 'time', 'schedule', 'hours', 'deadline', 'date'],
    'contact': ['contact', 'phone', 'email', 'reach', 'get in touch', 'call'],
    'opportunity': ['opportunity', 'chance', 'possibility', 'available', 'can i', 'internship', 'placement'],
    'problem': ['problem', 'issue', 'trouble', 'difficulty', 'help', 'support'],
    'requirement': ['need', 'require', 'must', 'should', 'necessary', 'requirement'],
    'comparison': ['difference', 'compare', 'versus', 'vs', 'better', 'best'],
    'general': ['what is', 'tell me about', 'information about', 'details of', 'general']
}

# Super Smart Cute Bot
class SuperSmartCuteBot:
    def __init__(self):
        self.greetings = [
            "Hi! 👋 Welcome to Super Smart QonnectBot!", 
            "Hello! ✨ I'm your intelligent campus assistant!", 
            "Hey there! 🌟 Ready to answer with super accuracy!",
            "Hi friend! 🎓 I'm smarter than ever before!",
            "Hello! 🌸 Let me show you how smart I can be!"
        ]
        self.cute_endings = [
            "Let me know if you want to know more! 🌸", 
            "Hope that helps! 😊", 
            "Anything else I can help with? 🐾",
            "Feel free to ask more questions! 💫",
            "I'm here whenever you need help! 🌟"
        ]
        self.thinking_phrases = [
            "🤔 Let me think about that...",
            "💭 Searching for the best answer...",
            "🔍 Looking through my knowledge...",
            "✨ Finding the perfect response...",
            "🎯 Getting you the right information...",
            "🧠 Processing your question intelligently..."
        ]
        self.identity_responses = [
            "I'm Super Smart QonnectBot, your intelligent campus helper! I use advanced matching algorithms to give you the most accurate answers. ✨",
            "Hi! I'm Super Smart QonnectBot! I've been upgraded with better understanding and smarter matching to help with all your university questions. 🌟",
            "I'm Super Smart QonnectBot! I can understand context, match keywords intelligently, and give you the most relevant answers. 😊"
        ]
    
    def greet(self):
        return random.choice(self.greetings)
    
    def think(self):
        return random.choice(self.thinking_phrases)
    
    def get_identity_response(self):
        return random.choice(self.identity_responses)
    
    def format_answer(self, answer, category=None):
        emoji = "💡"
        if category:
            emoji_map = {
                'location': "📍",
                'process': "📋",
                'timing': "⏰",
                'contact': "📞",
                'opportunity': "🎯",
                'problem': "🛠️",
                'requirement': "📝",
                'comparison': "⚖️",
                'general': "💡",
                'explanation': "📚",
                'identity': "🤖"
            }
            emoji = emoji_map.get(category, "💡")
        
        ending = random.choice(self.cute_endings)
        return f"{emoji} {answer}\n{ending}"

# Load Q&A pairs from text file
qa_pairs = []
with open('qonnect_knowledge_qa.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    q, a = '', ''
    for line in lines:
        if line.startswith('Q: '):
            q = line.strip()[3:]
        elif line.startswith('A: '):
            a = line.strip()[3:]
            if q and a:
                qa_pairs.append((q, a))
                q, a = '', ''

print(f"📚 Loaded {len(qa_pairs)} Q&A pairs")

# Initialize
cute_bot = SuperSmartCuteBot()

# Super Smart Analytics
class SuperSmartAnalytics:
    def __init__(self):
        self.data = {
            "questions": 0, 
            "satisfaction": [],
            "categories": {},
            "unanswered": [],
            "session_start": datetime.now(),
            "match_types": {}
        }
    
    def track(self, question, answer, rating=None, category=None, match_type=None):
        self.data["questions"] += 1
        
        if category:
            self.data["categories"][category] = self.data["categories"].get(category, 0) + 1
        
        if match_type:
            self.data["match_types"][match_type] = self.data["match_types"].get(match_type, 0) + 1
        
        if rating:
            self.data["satisfaction"].append(rating)
        
        if not answer or "don't know" in answer.lower():
            self.data["unanswered"].append(question)
    
    def get_stats(self):
        avg = sum(self.data["satisfaction"]) / len(self.data["satisfaction"]) if self.data["satisfaction"] else 0
        session_time = datetime.now() - self.data["session_start"]
        return f"Questions: {self.data['questions']} | Avg Rating: {avg:.1f}/5 | Session: {session_time.seconds}s"

analytics = SuperSmartAnalytics()

def normalize(text):
    return re.sub(r'[^a-z0-9 ]', '', text.lower())

def expand_keywords(words):
    expanded = set(words)
    for word in words:
        for key, syns in SYNONYMS.items():
            if word == key or word in syns:
                expanded.add(key)
                expanded.update(syns)
    return expanded

def extract_keywords(text):
    words = normalize(text).split()
    return expand_keywords(words)

def categorize_question(question):
    question_lower = question.lower()
    for category, phrases in QUESTION_CATEGORIES.items():
        if any(phrase in question_lower for phrase in phrases):
            return category
    return 'general'

def find_best_library_answer(user_q, qa_pairs):
    """Special handling for library questions"""
    library_questions = []
    for q, a in qa_pairs:
        if 'library' in q.lower():
            library_questions.append((q, a))
    
    if not library_questions:
        return None
    
    user_lower = user_q.lower()
    
    # Check for specific library questions
    if any(word in user_lower for word in ['hours', 'time', 'when', 'open', 'close']):
        for q, a in library_questions:
            if any(word in q.lower() for word in ['hours', 'time', 'open']):
                return a
    
    # Check for general library information
    if any(word in user_lower for word in ['what', 'tell', 'about', 'information', 'general']):
        for q, a in library_questions:
            if 'what' in q.lower() and 'library' in q.lower():
                return a
    
    # Default to first library answer
    return library_questions[0][1]

def find_best_internship_answer(user_q, qa_pairs):
    """Special handling for internship questions"""
    internship_questions = []
    for q, a in qa_pairs:
        if any(word in q.lower() for word in ['internship', 'intern', 'placement', 'opportunity']):
            internship_questions.append((q, a))
    
    if not internship_questions:
        return None
    
    user_lower = user_q.lower()
    
    # Check for specific internship questions
    if any(word in user_lower for word in ['how', 'apply', 'process', 'steps']):
        for q, a in internship_questions:
            if any(word in q.lower() for word in ['how', 'apply', 'process']):
                return a
    
    # Check for general internship information
    if any(word in user_lower for word in ['what', 'tell', 'about', 'information', 'general']):
        for q, a in internship_questions:
            if 'what' in q.lower() and any(word in q.lower() for word in ['internship', 'intern']):
                return a
    
    # Default to first internship answer
    return internship_questions[0][1]

def super_smart_match(user_q, qa_pairs):
    """Super smart matching with special handling for common questions"""
    user_q_lower = user_q.lower()
    category = categorize_question(user_q)
    
    # Special handling for identity questions
    identity_phrases = [
        'who are you', 'what is your name', 'about you', 'tum kaun ho', 
        'apka naam', 'introduce yourself', 'kya ho tum', 'kaun ho tum'
    ]
    if any(phrase in user_q_lower for phrase in identity_phrases):
        return cute_bot.get_identity_response(), 'identity', category
    
    # Special handling for library questions
    if 'library' in user_q_lower:
        answer = find_best_library_answer(user_q, qa_pairs)
        if answer:
            return answer, 'library_special', category
    
    # Special handling for internship questions
    if any(word in user_q_lower for word in ['internship', 'intern', 'placement', 'opportunity']):
        answer = find_best_internship_answer(user_q, qa_pairs)
        if answer:
            return answer, 'internship_special', category
    
    # Enhanced keyword matching
    user_keywords = extract_keywords(user_q)
    best_score = 0
    best_answer = None
    best_type = 'keyword'
    
    for q, a in qa_pairs:
        q_keywords = extract_keywords(q)
        overlap = user_keywords.intersection(q_keywords)
        
        if len(user_keywords) > 0:
            overlap_score = len(overlap) / len(user_keywords)
            
            # Boost score for exact word matches
            for word in user_q_lower.split():
                if word in q.lower():
                    overlap_score += 0.1
            
            # Boost score for category matches
            if category in q.lower():
                overlap_score += 0.2
            
            if overlap_score > best_score:
                best_score = overlap_score
                best_answer = a
                best_type = 'keyword'
    
    # If keyword matching fails, try direct matching
    if not best_answer or best_score < 0.3:
        user_q_norm = normalize(user_q)
        for q, a in qa_pairs:
            q_norm = normalize(q)
            score = SequenceMatcher(None, user_q_norm, q_norm).ratio()
            if score > best_score:
                best_score = score
                best_answer = a
                best_type = 'direct'
    
    if best_answer and best_score >= 0.2:  # Lower threshold for better matching
        return best_answer, best_type, category
    
    return "Sorry, I don't know about that yet! Can you ask something else? 🌸", 'fallback', category

# Feedback CSV file
FEEDBACK_FILE = 'super_smart_bot_feedback.csv'
if not os.path.exists(FEEDBACK_FILE):
    with open(FEEDBACK_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'question', 'answer', 'feedback', 'match_type', 'category'])

# Main chat loop
print("🎓 Super Smart QonnectBot Ready! (Intelligent & Accurate)")
print(cute_bot.greet())

while True:
    query = input("\nYou: ").strip()
    
    if not query:
        continue
    
    if query.lower() in ['quit', 'exit', 'bye']:
        print("👋 Thanks for chatting! Have a great day! ✨")
        break
    elif query.lower() == 'stats':
        print(f"📊 {analytics.get_stats()}")
        continue
    elif query.lower() in ['hello', 'hi', 'hey']:
        print(cute_bot.greet())
        continue
    elif query.lower() in ['summary', 'aj kya kiya', 'aaj kya kiya', 'aaj humne kya kiya', 'aj humne kya kya kiya ha', 'today summary']:
        print("✨ Super Smart QonnectBot is now incredibly intelligent!\n- Special handling for library and internship questions\n- Enhanced keyword matching with context understanding\n- Better question categorization and answer selection\n- Improved accuracy and relevance\n- Super cute personality! 🌸")
        continue
    
    try:
        print(cute_bot.think())
        
        # Generate super smart answer
        answer, match_type, category = super_smart_match(query, qa_pairs)
        
        # Format and display
        formatted_answer = cute_bot.format_answer(answer, category)
        print(f"Bot: {formatted_answer}")
        
        # Track analytics
        analytics.track(query, answer, category=category, match_type=match_type)
        
        # Improved feedback system
        print("\n💭 How was this answer?")
        feedback = input("Rate (1-5) or type 'skip': ").strip()
        
        if feedback.lower() == 'skip':
            print("No problem! 😊")
        else:
            # Save feedback to CSV
            with open(FEEDBACK_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().isoformat(timespec='seconds'),
                    query,
                    answer,
                    feedback,
                    match_type,
                    category
                ])
            
            if feedback.isdigit() and 1 <= int(feedback) <= 5:
                analytics.track(query, answer, int(feedback), category, match_type)
                if int(feedback) >= 4:
                    print("Awesome! Thanks! 💕")
                elif int(feedback) >= 3:
                    print("Thanks! 😊")
                else:
                    print("I'll try to improve! 🌟")
            else:
                print("Thanks for the feedback! 😊")
            
    except Exception as e:
        print(f"Oops! Something went wrong: {e} ��")
        continue 