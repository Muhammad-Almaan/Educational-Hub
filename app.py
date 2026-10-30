from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Poetry templates
POEM_TEMPLATES = {
    'sonnet': [
        "In {word1}'s embrace, the {word2} does shine,\nWhere {word3} and {word4} in harmony dance,\nAnd {word5} creates a love divine,\nThat fills our hearts with sweet romance.\n\nThe gentle {word1} whispers soft and low,\nWhile {word2} paints the sky in golden hue,\nAnd {word3} makes our spirits glow,\nWith {word4} that's forever true.\n\nIn {word5}'s realm we find our peace,\nWhere {word1} and {word2} unite,\nAnd all our worldly troubles cease,\nBeneath the {word3}'s guiding light.\n\nSo let these words forever ring,\nOf {word4} and the joy they bring."
    ],
    'free-verse': [
        "{word1}\nfalls like scattered thoughts\nacross the landscape of {word2}\n\n{word3}—\na whisper in the darkness\nspeaking truths that {word4} cannot hold\n\nI trace the outline of {word5}\nwith fingertips of memory\nfinding patterns in chaos\nmeaning in the spaces between"
    ],
    'haiku': [
        "{word1} whispers soft\n{word2} meets {word3} in the dawn—\n{word4} holds {word5}",
        "Gentle {word1} flows\nThrough {word2} where {word3} grows wild—\n{word4} dreams of {word5}"
    ],
    'rhyme': [
        "{word1} dances in the light,\n{word2} makes everything bright,\n{word3} sings a song so sweet,\nMaking life feel so complete.\n\n{word4} whispers in my ear,\nWords that I love to hear,\n{word5} paints the sky above,\nFilling hearts with peace and love."
    ]
}

# Seasonal facts
seasonal_facts = [
    "Earth's 23.5-degree axial tilt is what creates our seasons, not our distance from the sun!",
    "When it's summer in the Northern Hemisphere, it's winter in the Southern Hemisphere.",
    "The first day of spring and autumn are called equinoxes, when day and night are nearly equal.",
    "Trees change color in autumn because chlorophyll breaks down, revealing other pigments.",
    "The Arctic experiences 6 months of daylight and 6 months of darkness.",
    "Earth is actually closest to the sun during Northern Hemisphere winter!"
]


def clean_words(word_string):
    words = [word.strip().lower() for word in word_string.split(',')]
    words = [word for word in words if word and word.replace(' ', '').isalpha()]

    default_words = ['beauty', 'wonder', 'dream', 'light', 'hope']
    while len(words) < 5:
        words.append(random.choice(default_words))

    return words[:5]


def generate_creative_poem(words, poem_type):
    templates = POEM_TEMPLATES.get(poem_type, POEM_TEMPLATES['sonnet'])
    template = random.choice(templates)

    word_mapping = {
        'word1': words[0], 'word2': words[1], 'word3': words[2],
        'word4': words[3], 'word5': words[4]
    }

    return template.format(**word_mapping)


@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Educational Hub - Poetry & Science</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            min-height: 100vh; color: white; overflow-x: hidden;
        }
        .navbar {
            position: fixed; top: 0; width: 100%; background: rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(15px); z-index: 1000; padding: 1rem 2rem;
        }
        .nav-container {
            display: flex; justify-content: space-between; align-items: center;
            max-width: 1200px; margin: 0 auto;
        }
        .logo {
            font-size: 1.8rem; font-weight: 700; color: #fff;
            text-decoration: none; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .nav-links { display: flex; list-style: none; gap: 2rem; }
        .nav-links a {
            color: #fff; text-decoration: none; padding: 0.7rem 1.5rem;
            border-radius: 30px; font-weight: 500; transition: all 0.3s ease;
        }
        .nav-links a:hover {
            background: rgba(255, 255, 255, 0.2); transform: translateY(-2px);
        }
        .hero {
            height: 100vh; display: flex; align-items: center;
            justify-content: center; text-align: center;
        }
        .hero-title {
            font-size: 4rem; font-weight: 700; margin-bottom: 1.5rem;
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
            background: linear-gradient(45deg, #fff, #f0f8ff, #e6e6fa);
            background-clip: text; -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-subtitle {
            font-size: 1.4rem; margin-bottom: 3rem; opacity: 0.9;
        }
        .projects-section {
            padding: 4rem 2rem; display: flex; justify-content: center;
            align-items: center; min-height: 80vh;
        }
        .projects-container {
            display: grid; grid-template-columns: 1fr 1fr; gap: 4rem;
            max-width: 1200px; width: 100%;
        }
        .project-card {
            background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px);
            border-radius: 25px; padding: 3rem; text-align: center;
            transition: all 0.5s ease; border: 1px solid rgba(255, 255, 255, 0.2);
            cursor: pointer;
        }
        .project-card:hover {
            transform: translateY(-15px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        .project-icon { font-size: 4rem; margin-bottom: 1.5rem; display: block; }
        .project-title {
            font-size: 2rem; font-weight: 600; margin-bottom: 1rem;
            color: #fff; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .project-description {
            font-size: 1.1rem; line-height: 1.6; margin-bottom: 2rem; opacity: 0.9;
        }
        .project-button {
            background: linear-gradient(45deg, #ff6b6b, #ffa500); color: white;
            border: none; padding: 1rem 2.5rem; border-radius: 50px;
            font-size: 1.1rem; font-weight: 600; cursor: pointer;
            transition: all 0.3s ease; text-decoration: none; display: inline-block;
        }
        .project-button:hover { transform: translateY(-3px); }
        .footer {
            text-align: center; padding: 3rem 2rem;
            background: rgba(0, 0, 0, 0.1); backdrop-filter: blur(10px);
        }
        @media (max-width: 768px) {
            .hero-title { font-size: 2.5rem; }
            .projects-container { grid-template-columns: 1fr; gap: 2rem; }
            .nav-links { display: none; }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <a href="/" class="logo">🎓 EduHub</a>
            <ul class="nav-links">
                <li><a href="/">Home</a></li>
                <li><a href="/poetry">Poetry</a></li>
                <li><a href="/seasons">Seasons</a></li>
            </ul>
        </div>
    </nav>

    <section class="hero">
        <div class="hero-content">
            <h1 class="hero-title">Educational Hub</h1>
            <p class="hero-subtitle">Explore the beautiful intersection of Poetry and Science</p>
        </div>
    </section>

    <section class="projects-section">
        <div class="projects-container">
            <div class="project-card" onclick="window.location.href='/poetry'">
                <span class="project-icon">📜</span>
                <h2 class="project-title">Poetry Generator</h2>
                <p class="project-description">
                    Create beautiful poems with different styles. Generate sonnets, haikus, free verse, and rhyming poems from just 5 words.
                </p>
                <a href="/poetry" class="project-button">Start Creating Poetry</a>
            </div>

            <div class="project-card" onclick="window.location.href='/seasons'">
                <span class="project-icon">🌍</span>
                <h2 class="project-title">Seasons Explorer</h2>
                <p class="project-description">
                    Discover how Earth's tilt creates seasons. Interactive animations and educational content await you.
                </p>
                <a href="/seasons" class="project-button">Explore Seasons</a>
            </div>
        </div>
    </section>

    <footer class="footer">
        <h3>Muhammad Almaan Shabbir</h3>
        <p>Programmer & Science Enthusiast</p>
    </footer>
</body>
</html>'''


@app.route('/poetry')
def poetry():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Poetry Generator</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh; display: flex; flex-direction: column;
            transition: all 0.6s ease; overflow-x: hidden;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        /* Theme Classes */
        .sonnet-theme {
            background: linear-gradient(135deg, #8B4513 0%, #D2691E 50%, #F4A460 100%) !important;
            color: #2F1B14 !important;
        }
        .free-verse-theme {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
            color: #e94560 !important;
        }
        .haiku-theme {
            background: linear-gradient(135deg, #2D5A27 0%, #568203 50%, #8FBC8F 100%) !important;
            color: #1B4332 !important;
        }
        .rhyme-theme {
            background: linear-gradient(135deg, #FFB6C1 0%, #FF69B4 50%, #FF1493 100%) !important;
            color: #8B0000 !important;
        }

        .back-btn {
            position: fixed; top: 2rem; left: 2rem;
            background: rgba(255, 255, 255, 0.2); backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3); color: white;
            padding: 0.8rem 1.5rem; border-radius: 25px;
            text-decoration: none; font-weight: 500; z-index: 1000;
        }
        .container {
            flex: 1; display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            padding: 2rem; margin-top: 2rem;
        }
        .poem-nav {
            display: flex; gap: 1rem; margin-bottom: 3rem;
            flex-wrap: wrap; justify-content: center;
        }
        .nav-btn {
            padding: 1rem 2rem; border: none; border-radius: 50px;
            font-size: 1.1rem; font-weight: 600; cursor: pointer;
            background: rgba(255, 255, 255, 0.2); color: white;
            backdrop-filter: blur(10px); border: 2px solid rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
        }
        .nav-btn:hover { transform: translateY(-5px); }
        .nav-btn.active {
            background: rgba(255, 255, 255, 0.4); transform: scale(1.05);
        }
        .content-section { text-align: center; max-width: 600px; width: 100%; }
        .title {
            font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .subtitle {
            font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.9;
        }
        .text-input {
            width: 100%; padding: 1.5rem 2rem; border: none;
            border-radius: 25px; font-size: 1.1rem;
            background: rgba(255, 255, 255, 0.9); outline: none;
            margin: 2rem 0;
        }
        .generate-btn {
            padding: 1rem 3rem; border: none; border-radius: 50px;
            font-size: 1.2rem; font-weight: 600; cursor: pointer;
            background: linear-gradient(45deg, #ff6b6b, #ee5a52);
            color: white; transition: all 0.3s ease;
        }
        .generate-btn:hover { transform: translateY(-3px); }
        .poem-output {
            margin-top: 2rem; padding: 2rem;
            background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px);
            border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.2);
            min-height: 200px; white-space: pre-line;
            font-family: 'Georgia', serif; font-size: 1.1rem;
            line-height: 1.6; display: none;
        }
        .footer {
            text-align: center; padding: 2rem;
            background: rgba(0, 0, 0, 0.1); backdrop-filter: blur(10px);
        }
        .loading {
            display: inline-block; width: 20px; height: 20px;
            border: 3px solid rgba(255, 255, 255, 0.3); border-radius: 50%;
            border-top-color: #fff; animation: spin 1s ease-in-out infinite;
        }
        @keyframes spin { to { transform: rotate(360deg); } }

        @media (max-width: 768px) {
            .title { font-size: 2rem; }
            .nav-btn { padding: 0.8rem 1.5rem; font-size: 1rem; }
        }
    </style>
</head>
<body>
    <a href="/" class="back-btn">← Back to Home</a>

    <div class="container">
        <nav class="poem-nav">
            <button class="nav-btn active" data-theme="sonnet">📜 Sonnet</button>
            <button class="nav-btn" data-theme="free-verse">🎨 Free Verse</button>
            <button class="nav-btn" data-theme="haiku">🌸 Haiku</button>
            <button class="nav-btn" data-theme="rhyme">🎵 Rhyme</button>
        </nav>

        <div class="content-section">
            <h1 class="title" id="pageTitle">Classical Sonnet Generator</h1>
            <p class="subtitle" id="pageSubtitle">Enter 5 words to craft a beautiful sonnet</p>

            <input type="text" class="text-input" id="wordInput" 
                   placeholder="Enter 5 words separated by commas (e.g., love, moon, dream, ocean, time)">

            <button class="generate-btn" id="generateBtn" onclick="generatePoem()">
                <span id="btnText">Generate Sonnet</span>
            </button>

            <div class="poem-output" id="poemOutput"></div>
        </div>
    </div>

    <footer class="footer">
        <h3>Muhammad Almaan Shabbir</h3>
        <p>Programmer & Science Enthusiast</p>
    </footer>

    <script>
        const themes = {
            sonnet: {
                title: "Classical Sonnet Generator",
                subtitle: "Enter 5 words to craft a beautiful sonnet",
                btnText: "Generate Sonnet",
                class: "sonnet-theme"
            },
            "free-verse": {
                title: "Free Verse Poetry Creator",
                subtitle: "Create expressive free verse poetry",
                btnText: "Create Free Verse",
                class: "free-verse-theme"
            },
            haiku: {
                title: "Haiku Garden",
                subtitle: "Compose traditional 5-7-5 syllable haiku",
                btnText: "Compose Haiku",
                class: "haiku-theme"
            },
            rhyme: {
                title: "Rhyming Verse Studio",
                subtitle: "Create playful rhyming poems",
                btnText: "Create Rhyme",
                class: "rhyme-theme"
            }
        };

        let currentTheme = 'sonnet';

        function switchTheme(themeName) {
            if (currentTheme === themeName) return;

            currentTheme = themeName;
            const theme = themes[themeName];

            // Update active button
            document.querySelectorAll('.nav-btn').forEach(btn => {
                btn.classList.remove('active');
                if (btn.dataset.theme === themeName) {
                    btn.classList.add('active');
                }
            });

            // Apply theme
            document.body.className = theme.class;
            document.getElementById('pageTitle').textContent = theme.title;
            document.getElementById('pageSubtitle').textContent = theme.subtitle;
            document.getElementById('btnText').textContent = theme.btnText;
            document.getElementById('poemOutput').style.display = 'none';
        }

        async function generatePoem() {
            const wordInput = document.getElementById('wordInput');
            const generateBtn = document.getElementById('generateBtn');
            const poemOutput = document.getElementById('poemOutput');
            const btnText = document.getElementById('btnText');

            const words = wordInput.value.trim();
            if (!words) {
                alert('Please enter some words!');
                return;
            }

            btnText.innerHTML = '<span class="loading"></span> Generating...';
            generateBtn.disabled = true;

            try {
                const response = await fetch('/generate-poem', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ words: words, type: currentTheme })
                });

                const data = await response.json();
                if (!response.ok) throw new Error(data.error);

                poemOutput.textContent = data.poem;
                poemOutput.style.display = 'block';
            } catch (error) {
                poemOutput.innerHTML = '❌ Error generating poem. Try again!';
                poemOutput.style.display = 'block';
            }

            setTimeout(() => {
                btnText.textContent = themes[currentTheme].btnText;
                generateBtn.disabled = false;
            }, 1500);
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            switchTheme('sonnet');

            document.querySelectorAll('.nav-btn').forEach(btn => {
                btn.addEventListener('click', () => switchTheme(btn.dataset.theme));
            });

            document.getElementById('wordInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') generatePoem();
            });
        });
    </script>
</body>
</html>'''


@app.route('/seasons')
def seasons():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Seasons - How They Form</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Arial', sans-serif; line-height: 1.6;
            scroll-behavior: smooth; overflow-x: hidden;
        }
        .back-btn {
            position: fixed; top: 2rem; left: 2rem;
            background: rgba(255, 255, 255, 0.2); backdrop-filter: blur(10px);
            color: white; padding: 0.8rem 1.5rem; border-radius: 25px;
            text-decoration: none; z-index: 1000;
        }
        .hero {
            height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex; align-items: center; justify-content: center;
            text-align: center; color: white;
        }
        .hero-content h1 { font-size: 4rem; margin-bottom: 1rem; }
        .hero-content p { font-size: 1.5rem; margin-bottom: 2rem; }
        .season-section {
            min-height: 100vh; padding: 5rem 2rem; position: relative;
        }
        .container {
            max-width: 1200px; margin: 0 auto; display: grid;
            grid-template-columns: 1fr 1fr; gap: 4rem; align-items: center;
        }
        .season-content h2 { font-size: 3rem; margin-bottom: 2rem; }
        .season-content p { font-size: 1.2rem; margin-bottom: 1.5rem; }
        .season-visual {
            height: 400px; border-radius: 20px; display: flex;
            align-items: center; justify-content: center; position: relative;
            overflow: hidden; cursor: pointer; transition: all 0.5s ease;
        }
        .season-visual:hover { transform: scale(1.05); }

        /* Season Themes */
        .spring { background: linear-gradient(135deg, #a8e6cf 0%, #88d8a3 100%); color: #2d5a27; }
        .spring .season-visual { background: linear-gradient(135deg, #c3f0ca 0%, #a8e6cf 100%); }
        .summer { background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); color: #8b4513; }
        .summer .season-visual { background: linear-gradient(135deg, #ffb347 0%, #ffa500 100%); }
        .autumn { background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%); color: #8b4513; }
        .autumn .season-visual { background: linear-gradient(135deg, #d2691e 0%, #cd853f 100%); }
        .winter { background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); color: #1565c0; }
        .winter .season-visual { background: linear-gradient(135deg, #87ceeb 0%, #4682b4 100%); }

        /* Animation Elements */
        .flower {
            position: absolute; width: 20px; height: 20px;
            background: #ff69b4; border-radius: 50%;
            animation: bloom 2s ease-in-out infinite;
        }
        .sun-ray {
            position: absolute; width: 4px; height: 40px;
            background: #ffd700; transform-origin: center bottom;
            animation: rotate 3s linear infinite;
        }
.leaf {
    position: absolute;
    width: 20px;
    height: 12px;
    background: linear-gradient(45deg, #f4a261, #e9c46a); /* lighter orange to yellow */
    border-radius: 60% 40% 60% 40%; /* stretched, leaf-like shape */
    animation: fall 3s ease-in infinite;
}

        
        .snowflake {
            position: absolute; color: #fff; font-size: 20px;
            animation: snow 4s linear infinite;
        }

        .quiz-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 5rem 2rem; color: white; text-align: center;
        }
        .quiz-button {
            background: rgba(255, 255, 255, 0.2); color: white;
            border: 2px solid white; padding: 1rem 2rem; margin: 1rem;
            border-radius: 25px; cursor: pointer; font-size: 1.2rem;
        }
        .fact-display {
            background: rgba(0, 0, 0, 0.7); padding: 2rem;
            border-radius: 15px; margin-top: 2rem; min-height: 150px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.5rem;
        }

        @keyframes bloom { 0%, 100% { transform: scale(0.5); opacity: 0.7; } 50% { transform: scale(1.2); opacity: 1; } }
        @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        @keyframes fall { 0% { transform: translateY(-100px) rotate(0deg); opacity: 1; } 100% { transform: translateY(400px) rotate(360deg); opacity: 0; } }
        @keyframes snow { 0% { transform: translateY(-100px); opacity: 1; } 100% { transform: translateY(400px); opacity: 0; } }

        @media (max-width: 768px) {
            .hero-content h1 { font-size: 2.5rem; }
            .container { grid-template-columns: 1fr; gap: 2rem; }
            .season-content h2 { font-size: 2rem; }
        }
    </style>
</head>
<body>
    <a href="/" class="back-btn">← Back to Home</a>

    <section class="hero">
        <div class="hero-content">
            <h1>The Magic of Seasons</h1>
            <p>Discover how Earth's tilt creates the beautiful cycle of seasons</p>
        </div>
    </section>

    <section class="season-section spring">
        <div class="container">
            <div class="season-content">
                <h2>Spring 🌸</h2>
                <p>Spring arrives when Earth's axis tilts toward the sun, bringing longer days and warmer temperatures. This awakening season triggers new plant growth and animal activity.</p>
                <p><strong>Key Features:</strong> Increasing daylight, warming temperatures, plant growth, animal awakening.</p>
            </div>
            <div class="season-visual" onclick="createSpringAnimation()">
                <div id="spring-animation"></div>
            </div>
        </div>
    </section>

    <section class="season-section summer">
        <div class="container">
            <div class="season-content">
                <h2>Summer ☀️</h2>
                <p>Summer occurs when your hemisphere is tilted closest to the sun, receiving the most direct sunlight and experiencing the longest days.</p>
                <p><strong>Key Features:</strong> Longest days, highest sun angle, maximum temperatures, peak plant growth.</p>
            </div>
            <div class="season-visual" onclick="createSummerAnimation()">
                <div id="summer-animation"></div>
            </div>
        </div>
    </section>

    <section class="season-section autumn">
        <div class="container">
            <div class="season-content">
                <h2>Autumn 🍂</h2>
                <p>Autumn begins as Earth's axis tilts away from the sun, reducing daylight hours and solar energy.</p>
                <p><strong>Key Features:</strong> Decreasing daylight, cooling temperatures, changing leaf colors, animal preparation.</p>
            </div>
            <div class="season-visual" onclick="createAutumnAnimation()">
                <div id="autumn-animation"></div>
            </div>
        </div>
    </section>

    <section class="season-section winter">
        <div class="container">
            <div class="season-content">
                <h2>Winter ❄️</h2>
                <p>Winter arrives when your hemisphere tilts farthest from the sun, receiving minimal direct sunlight and experiencing the shortest days.</p>
                <p><strong>Key Features:</strong> Shortest days, lowest sun angle, minimum temperatures, plant dormancy, snow and ice.</p>
            </div>
            <div class="season-visual" onclick="createWinterAnimation()">
                <div id="winter-animation"></div>
            </div>
        </div>
    </section>
    
    <!-- Quiz Section (paste this before your footer) -->
<section id="quiz" class="quiz-section">
    <div class="quiz-container">
        <h2>Test Your Knowledge! 🧠</h2>
        <p>Learn fascinating facts about how seasons form — try the mini quiz, or get a random question.</p>

        <div style="margin-top: 1.2rem; display: flex; gap: 0.6rem; justify-content: center; flex-wrap: wrap;">
            <button class="quiz-button" onclick="getRandomFact()">Get Random Fact</button>
            <button class="quiz-button" onclick="startMiniQuiz()">Take Mini Quiz (10 questions)</button>
            <button class="quiz-button" onclick="showRandomQuestion()">Random Question</button>
        </div>

        <div id="fact-display" class="fact-display" style="margin-top: 1.6rem;">
            Click "Get Random Fact" to discover amazing seasonal science or start the mini quiz.
        </div>
    </div>
</section>

<script>
(function () {
    // Master question bank — add/remove items here to expand the quiz.
  const ALL_QUIZ_QUESTIONS = [
    { 
        question: "What causes the seasons on Earth?", 
        options: ["Earth's tilt", "Earth's distance from the Sun", "The Moon's gravity", "Solar flares"], 
        correct: 0, 
        explanation: "Seasons happen because Earth's axis is tilted, changing which areas get more sunlight during the year." 
    },
    { 
        question: "How tilted is Earth's axis approximately?", 
        options: ["20°", "23.5°", "25°", "27°"], 
        correct: 1, 
        explanation: "Earth's axis is tilted about 23.5° relative to its orbit, causing seasonal changes." 
    },
    { 
        question: "During which season is Earth closest to the Sun (Northern Hemisphere)?", 
        options: ["Spring", "Summer", "Autumn", "Winter"], 
        correct: 3, 
        explanation: "Earth is closest to the Sun around January, which is winter in the Northern Hemisphere." 
    },
    { 
        question: "What happens during an equinox?", 
        options: ["Longest day", "Shortest day", "Day and night are equal", "Moon eclipse"], 
        correct: 2, 
        explanation: "During an equinox, the Sun is above the equator and day and night are roughly equal." 
    },
    { 
        question: "Which hemisphere has summer in June?", 
        options: ["Northern Hemisphere", "Southern Hemisphere", "Eastern Hemisphere", "Western Hemisphere"], 
        correct: 0, 
        explanation: "The Northern Hemisphere tilts toward the Sun in June, giving it summer." 
    },
    { 
        question: "What is 'perihelion'?", 
        options: ["Earth farthest from Sun", "Earth closest to Sun", "Axis tilt zero", "Solar eclipse"], 
        correct: 1, 
        explanation: "Perihelion is the point in Earth's orbit when it is closest to the Sun." 
    },
    { 
        question: "What does 'solstice' mean?", 
        options: ["Day and night equal", "Longest or shortest day of the year", "Moon overhead", "Noon"], 
        correct: 1, 
        explanation: "A solstice marks the longest or shortest day of the year (summer or winter solstice)." 
    },
    { 
        question: "Why do leaves change color in autumn?", 
        options: ["It gets cold", "Chlorophyll breaks down", "They stop growing", "Less water"], 
        correct: 1, 
        explanation: "Chlorophyll fades, revealing other pigments like yellow and red." 
    },
    { 
        question: "Which regions have the biggest change in daylight between seasons?", 
        options: ["Equator", "Tropics", "Poles", "Coasts"], 
        correct: 2, 
        explanation: "Polar regions can have months of continuous daylight or darkness." 
    },
    { 
        question: "If Earth's tilt was 0°, what would happen?", 
        options: ["No weather", "No seasons", "No day and night", "Always winter"], 
        correct: 1, 
        explanation: "Without tilt, there would be no seasonal changes." 
    },
    { 
        question: "When is the summer solstice in the Northern Hemisphere?", 
        options: ["March 21", "June 21", "September 23", "December 21"], 
        correct: 1, 
        explanation: "The summer solstice usually occurs around June 21." 
    },
    { 
        question: "Why do the poles have long days in summer?", 
        options: ["Earth spins faster", "Tilt keeps Sun above horizon", "Ocean currents", "Moon phases"], 
        correct: 1, 
        explanation: "The tilt keeps the pole pointed toward the Sun for months." 
    },
    { 
        question: "What is the 'subsolar point'?", 
        options: ["Point where Sun is directly overhead", "Farthest point from Sun", "Prime meridian", "Moon's shadow"], 
        correct: 0, 
        explanation: "The subsolar point is where the Sun is directly overhead at noon." 
    },
    { 
        question: "What marks the start of autumn in many places?", 
        options: ["Solstice", "Equinox", "Perihelion", "Full moon"], 
        correct: 1, 
        explanation: "The autumnal equinox marks the start of autumn." 
    },
    { 
        question: "Does Earth's orbit shape affect seasonal temperature much?", 
        options: ["Main cause", "Small effect", "No effect", "Changes day/night"], 
        correct: 1, 
        explanation: "Tilt causes seasons; orbit shape only slightly changes timing/intensity." 
    },
    { 
        question: "Which animals often migrate seasonally?", 
        options: ["Bears", "Snakes", "Birds", "Sharks"], 
        correct: 2, 
        explanation: "Many birds migrate long distances to find food or breeding grounds." 
    },
    { 
        question: "What do equatorial regions usually experience instead of four seasons?", 
        options: ["Wet and dry seasons", "Four extreme seasons", "No change", "Constant winter"], 
        correct: 0, 
        explanation: "Near the equator, regions have wet and dry seasons instead of four temperate seasons." 
    },
    { 
        question: "How does snow help plants in winter?", 
        options: ["Kills them", "Keeps them warm", "Warms them", "Makes them grow"], 
        correct: 1, 
        explanation: "Snow insulates the ground and roots from extreme cold." 
    }
];

    // Internal state for mini-quiz
    let miniList = [];
    let miniIndex = 0;
    let miniScore = 0;
    let inMini = false;
    let currentQuestion = null;

    // Fisher-Yates shuffle
    function shuffle(arr) {
        const a = arr.slice();
        for (let i = a.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [a[i], a[j]] = [a[j], a[i]];
        }
        return a;
    }

    // Start mini quiz (default 10 questions)
    function startMiniQuiz(length = 10) {
        const display = document.getElementById('fact-display');
        length = Math.min(length, ALL_QUIZ_QUESTIONS.length);
        miniList = shuffle(ALL_QUIZ_QUESTIONS).slice(0, length);
        miniIndex = 0;
        miniScore = 0;
        inMini = true;
        display.innerHTML = '<div style="opacity:0.8;">Starting quiz — good luck!</div>';
        setTimeout(() => showMiniQuestion(), 700);
    }

    // Show the next question in mini quiz
    function showMiniQuestion() {
        if (!inMini) return;
        if (miniIndex >= miniList.length) {
            showMiniResults();
            return;
        }
        displayQuestion(miniList[miniIndex], true, miniIndex + 1, miniList.length);
    }

    // Show a single random question (one-off)
    function showRandomQuestion() {
        inMini = false;
        const idx = Math.floor(Math.random() * ALL_QUIZ_QUESTIONS.length);
        displayQuestion(ALL_QUIZ_QUESTIONS[idx], false);
    }

    // Build question UI inside #fact-display
    function displayQuestion(q, isMini, progressNum = 0, progressTotal = 0) {
        currentQuestion = q;
        const display = document.getElementById('fact-display');

        let header = `<h3 style="margin-bottom:0.6rem; text-align:center;">❓ ${q.question}</h3>`;
        if (isMini) {
            header += `<div style="text-align:center; margin-bottom:0.6rem; opacity:0.85;">Question ${progressNum} of ${progressTotal}</div>`;
        }

        let optionsHtml = '<div style="display:grid; gap:0.6rem; text-align:left;">';
        q.options.forEach((opt, i) => {
            optionsHtml += `
                <button onclick="checkAnswer(${i})"
                        style="background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2);
                               color: white; padding: 1rem 1.4rem; font-size: 1.4rem; border-radius: 8px; cursor: pointer; text-align:left;"
                        onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.12)'">
                    ${opt}
                </button>
            `;
        });
        optionsHtml += '</div>';

        display.innerHTML = `<div style="text-align:left; max-width: 720px; margin: 0 auto;">${header}${optionsHtml}</div>`;
    }

    // Handle an answer click
    function checkAnswer(selected) {
        const display = document.getElementById('fact-display');
        if (!currentQuestion) return;

        const correctIndex = currentQuestion.correct;
        const correctText = currentQuestion.options[correctIndex];
        const explanation = currentQuestion.explanation ? currentQuestion.explanation : '';

        if (selected === correctIndex) {
            display.innerHTML = `<div style="color:#4ade80; font-size:1.2rem; text-align:center; margin-bottom:0.6rem;">✅ Correct!</div>
                                 <div style="text-align:center; opacity:0.9; margin-bottom:0.8rem;">${explanation}</div>`;
            if (inMini) miniScore++;
        } else {
            display.innerHTML = `<div style="color:#f87171; font-size:1.1rem; text-align:center; margin-bottom:0.6rem;">❌ Not quite.</div>
                                 <div style="text-align:center; margin-bottom:0.6rem;">Correct answer: <strong>${correctText}</strong></div>
                                 <div style="text-align:center; opacity:0.9;">${explanation}</div>`;
        }

        // Advance based on mode
        if (inMini) {
            miniIndex++;
            // small pause then next question or results
            setTimeout(() => {
                if (miniIndex < miniList.length) showMiniQuestion();
                else showMiniResults();
            }, 1400);
        } else {
            // one-off random question — offer quick reset message after delay
            setTimeout(() => {
                display.innerHTML = '🎯 Ready for another question? Click "Random Question" or "Take Mini Quiz".';
            }, 1800);
        }
    }

    // Show mini-quiz results
    function showMiniResults() {
        inMini = false;
        const display = document.getElementById('fact-display');
        const total = miniList.length || 0;
        const percentage = total ? Math.round((miniScore / total) * 100) : 0;
        let message = '';
        if (percentage >= 90) message = "Outstanding! You're a seasons expert! 🌟";
        else if (percentage >= 70) message = "Great job! You know your seasons well! 🎉";
        else if (percentage >= 50) message = "Good effort! Keep learning about seasons! 👍";
        else message = "Keep exploring — seasons are full of surprises! 🌍";

        display.innerHTML = `
            <div style="text-align:center;">
                <div style="font-size:1.4rem; font-weight:700; margin-bottom:0.5rem;">Quiz Complete</div>
                <div style="font-size:1.5rem; margin-bottom:0.4rem;">Score: ${miniScore} / ${total} (${percentage}%)</div>
                <div style="margin-bottom:0.8rem; opacity:0.9;">${message}</div>
                <div style="display:flex; gap:0.6rem; justify-content:center; margin-top:0.6rem;">
                    <button class="quiz-button" onclick="startMiniQuiz(${total})">Retry (${total})</button>
                    <button class="quiz-button" onclick="startMiniQuiz()">Try another set</button>
                    <button class="quiz-button" onclick="showRandomQuestion()">Random Question</button>
                </div>
            </div>
        `;
    }

    // Expose the functions the page buttons call
    window.startMiniQuiz = startMiniQuiz;
    window.showRandomQuestion = showRandomQuestion;
    window.checkAnswer = checkAnswer;
})();
</script>



    <script>
        function createSpringAnimation() {
            const container = document.getElementById('spring-animation');
            container.innerHTML = '';
            for (let i = 0; i < 12; i++) {
                const flower = document.createElement('div');
                flower.className = 'flower';
                flower.style.left = Math.random() * 300 + 'px';
                flower.style.top = Math.random() * 300 + 'px';
                flower.style.animationDelay = Math.random() * 2 + 's';
                container.appendChild(flower);
            }
        }

        function createSummerAnimation() {
            const container = document.getElementById('summer-animation');
            container.innerHTML = '';

            const sun = document.createElement('div');
            sun.style.cssText = `width: 80px; height: 80px; background: radial-gradient(circle, #ffd700 0%, #ffa500 100%);
                border-radius: 50%; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);`;
            container.appendChild(sun);

            for (let i = 0; i < 8; i++) {
                const ray = document.createElement('div');
                ray.className = 'sun-ray';
                ray.style.left = '50%'; ray.style.top = '50%';
                ray.style.transform = `translate(-50%, -50%) rotate(${i * 45}deg)`;
                container.appendChild(ray);
            }
        }

        function createAutumnAnimation() {
            const container = document.getElementById('autumn-animation');
            container.innerHTML = '';
            for (let i = 0; i < 15; i++) {
                const leaf = document.createElement('div');
                leaf.className = 'leaf';
                leaf.style.left = Math.random() * 350 + 'px';
                leaf.style.animationDelay = Math.random() * 3 + 's';
                container.appendChild(leaf);
            }
        }

        function createWinterAnimation() {
            const container = document.getElementById('winter-animation');
            container.innerHTML = '';
            const snowSymbols = ['❄', '❅', '❆'];
            for (let i = 0; i < 20; i++) {
                const snowflake = document.createElement('div');
                snowflake.className = 'snowflake';
                snowflake.textContent = snowSymbols[Math.floor(Math.random() * snowSymbols.length)];
                snowflake.style.left = Math.random() * 350 + 'px';
                snowflake.style.animationDelay = Math.random() * 4 + 's';
                container.appendChild(snowflake);
            }
        }

        function getRandomFact() {
            const display = document.getElementById('fact-display');
            display.innerHTML = '🔄 Loading fact...';

            fetch('/random-fact')
                .then(response => response.json())
                .then(data => {
                    display.innerHTML = '🌟 ' + data.fact;
                })
                .catch(() => {
                    display.innerHTML = '🌟 Earth\\'s 23.5-degree axial tilt creates our seasons!';
                });
        }

        // Initialize spring animation on load
        document.addEventListener('DOMContentLoaded', () => {
            createSpringAnimation();
        });
    </script>
</body>
</html>'''


# API Routes
@app.route('/generate-poem', methods=['POST'])
def generate_poem():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        words_input = data.get('words', '').strip()
        poem_type = data.get('type', 'sonnet').strip()

        if not words_input:
            return jsonify({'error': 'Please provide words for the poem'}), 400

        words = clean_words(words_input)
        poem = generate_creative_poem(words, poem_type)

        return jsonify({
            'poem': poem,
            'words_used': words[:5],
            'type': poem_type,
            'generated_at': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': 'Failed to generate poem. Please try again.'}), 500


@app.route('/random-fact')
def random_fact():
    fact = random.choice(seasonal_facts)
    return jsonify({'fact': fact})


if __name__ == '__main__':
    print("🎓 Starting Educational Hub server...")
    print("🌐 Main page: http://localhost:5000")
    print("📝 Poetry Generator: http://localhost:5000/poetry")
    print("🌍 Seasons Explorer: http://localhost:5000/seasons")

    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='127.0.0.1', port=port)