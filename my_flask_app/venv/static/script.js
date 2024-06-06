document.getElementById('news-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;
    
    fetch('/add_news', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `title=${title}&content=${content}`
    })
    .then(response => response.json())
    .then(data => {
        const newsArticlesDiv = document.getElementById('news-articles');
        const articleDiv = document.createElement('div');
        articleDiv.classList.add('news-article');
        articleDiv.innerHTML = `<h3>${data.title}</h3><p>${data.summary}</p>`;
        newsArticlesDiv.appendChild(articleDiv);
        document.getElementById('news-form').reset();
    });
});

window.onload = function() {
    fetch('/get_news')
    .then(response => response.json())
    .then(data => {
        const newsArticlesDiv = document.getElementById('news-articles');
        data.forEach(article => {
            const articleDiv = document.createElement('div');
            articleDiv.classList.add('news-article');
            articleDiv.innerHTML = `<h3>${article.title}</h3><p>${article.summarized_content}</p>`;
            newsArticlesDiv.appendChild(articleDiv);
        });
    });
}
