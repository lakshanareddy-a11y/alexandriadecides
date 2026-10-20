
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

posts = [
    {
        "id": 1006,
        "title": "Anyone else notice the traffic changes near Bourke Road lately?",
        "category": "Community Discussion",
        "author": "GreenSquareLocal",
        "body": "Ever since the data centre expanded its loading bay, I’ve noticed more trucks around the area. Not complaining, just wondering if others have seen the same thing. Does this affect your commute?",
        "upvotes": 34,
        "replies": [
            {"author": "AlexResident", "body": "Yes! Especially around 7–9 AM. It’s not terrible but definitely busier.", "upvotes": 11},
            {"author": "CycleSydney", "body": "As a cyclist, the trucks make the narrow parts of Bourke Road feel tighter.", "upvotes": 9},
            {"author": "UrbanMapper", "body": "It’s probably related to equipment deliveries. Data centres get regular hardware refreshes.", "upvotes": 7},
            {"author": "LocalBarista", "body": "Our café gets more tech workers now, so maybe it’s connected.", "upvotes": 12}
        ]
    },
    {
        "id": 1007,
        "title": "Do you think the data centre is good or bad for Alexandria?",
        "category": "Local Opinions",
        "author": "NeighbourhoodVoice",
        "body": "I’m curious how people feel about having a major data centre in the middle of our suburb. Do you see it as a positive addition or something that disrupts the area?",
        "upvotes": 51,
        "replies": [
            {"author": "TechFriendly", "body": "Honestly, I think it’s cool. It brings jobs and modern infrastructure.", "upvotes": 18},
            {"author": "OldAlexandria", "body": "I miss when the area was quieter. But I get that cities evolve.", "upvotes": 14},
            {"author": "EcoAnalyst", "body": "Neutral. It’s fine as long as they manage energy use responsibly.", "upvotes": 10},
            {"author": "LocalShopOwner", "body": "We’ve seen more customers since the centre opened, so I’m all for it.", "upvotes": 16},
            {"author": "NoiseSensitive", "body": "The hum at night bothers me sometimes. Wish they’d add more soundproofing.", "upvotes": 8}
        ]
    },
    {
        "id": 1008,
        "title": "Has anyone attended the community info sessions about the data centre?",
        "category": "Events & Meetings",
        "author": "CommunityConnector",
        "body": "I heard they’ve been hosting info sessions about sustainability and future expansion. Did anyone go? Curious what was discussed.",
        "upvotes": 29,
        "replies": [
            {"author": "MeetingAttendee", "body": "Yes, they talked about upgrading cooling systems to reduce energy spikes.", "upvotes": 13},
            {"author": "UrbanPlanner", "body": "They also mentioned adding greenery around the perimeter to reduce heat zones.", "upvotes": 11},
            {"author": "AlexResident", "body": "I liked that they answered questions directly instead of dodging them.", "upvotes": 9}
        ]
    },
    {
        "id": 1009,
        "title": "What improvements would you like to see around the data centre?",
        "category": "Community Ideas",
        "author": "FutureAlexandria",
        "body": "If you could suggest upgrades or changes around the Bourke Road site, what would you pick? More greenery? Better footpaths? Noise reduction?",
        "upvotes": 44,
        "replies": [
            {"author": "GreenSquareLocal", "body": "Trees! The area needs more shade, especially in summer.", "upvotes": 17},
            {"author": "CycleSydney", "body": "Better bike lanes around the industrial blocks would be great.", "upvotes": 14},
            {"author": "NoiseSensitive", "body": "Sound barriers would help a lot with the nighttime hum.", "upvotes": 12},
            {"author": "LocalShopOwner", "body": "More pedestrian crossings. People walk to the cafés and breweries nearby.", "upvotes": 10}
        ]
    }
]

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AlexandriaDecides</title>
<style>
* { box-sizing: border-box; }
body {
  margin: 0; background: #dae0e6; color: #222;
  font-family: Arial, sans-serif;
}
header {
  background: white; padding: 18px 5%;
  border-bottom: 1px solid #ddd;
  color: #ff5722; font-size: 24px; font-weight: bold;
}
main { max-width: 850px; margin: 24px auto; padding: 12px; }
.notice {
  background: #fff0e9; padding: 12px;
  border-radius: 7px; font-size: 13px;
}
.toolbar { display: flex; gap: 10px; margin: 16px 0; }
input {
  width: 100%; padding: 12px; margin-top: 16px;
  border: 1px solid #ccc; border-radius: 8px;
}
button {
  cursor: pointer; border: 1px solid #ddd;
  border-radius: 18px; padding: 8px 14px;
  background: white;
}
button:hover { background: #fff0e9; }
.post {
  background: white; border: 1px solid #ddd;
  border-radius: 9px; padding: 18px; margin: 14px 0;
}
.meta { color: #777; font-size: 12px; }
h2 { font-size: 19px; line-height: 1.4; }
.body { line-height: 1.6; }
.vote { color: #e45020; font-weight: bold; }
.reply { border-left: 3px solid #ddd; padding-left: 12px; }
summary { cursor: pointer; margin-top: 12px; }
@media(max-width:600px) {
  header { font-size: 20px; }
  main { margin: 10px auto; }
}
</style>
</head>
<body>
<header>🟠 AlexandriaDecides</header>
<main>
  <div class="notice">
    FICTIONAL COMMUNITY DEMO — This is an independent project.
    Posts and usernames are sample content, not verified resident testimony.
  </div>
  <h1>Local discussions</h1>
  <input id="search" placeholder="Search discussions...">
  <div class="toolbar">
    <button onclick="sortPosts('popular')">🔥 Popular</button>
    <button onclick="sortPosts('latest')">🕒 Latest</button>
  </div>
  <div id="feed">
  {% for p in posts %}
    <article class="post" data-title="{{ p.title|lower }}"
      data-body="{{ p.body|lower }}"
      data-category="{{ p.category|lower }}"
      data-votes="{{ p.upvotes }}" data-id="{{ p.id }}">
      <div class="meta">u/{{ p.author }} · {{ p.category }}</div>
      <h2>{{ p.title }}</h2>
      <p class="body">{{ p.body }}</p>
      <form method="post" action="{{ url_for('vote', post_id=p.id) }}">
        <button class="vote" type="submit">▲ Upvote · {{ p.upvotes }}</button>
      </form>
      <details>
        <summary>{{ p.replies|length }} replies</summary>
        {% for r in p.replies %}
        <p class="reply"><b>u/{{ r.author }}</b><br>{{ r.body }}
        <br><span class="meta">▲ {{ r.upvotes }}</span></p>
        {% endfor %}
      </details>
    </article>
  {% endfor %}
  </div>
</main>
<script>
const search = document.getElementById("search");
search.addEventListener("input", () => {
  const q = search.value.toLowerCase().trim();
  document.querySelectorAll(".post").forEach(post => {
    post.style.display = post.innerText.toLowerCase().includes(q) ? "" : "none";
  });
});

function sortPosts(mode) {
  const feed = document.getElementById("feed");
  const cards = [...feed.querySelectorAll(".post")];
  cards.sort((a, b) => mode === "popular"
    ? Number(b.dataset.votes) - Number(a.dataset.votes)
    : Number(a.dataset.id) - Number(b.dataset.id));
  cards.forEach(card => feed.appendChild(card));
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE, posts=posts)

@app.route("/vote/<int:post_id>", methods=["POST"])
def vote(post_id):
    for post in posts:
        if post["id"] == post_id:
            post["upvotes"] += 1
            break
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()
