document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.like-button');
    const likesMap = JSON.parse(localStorage.getItem('likesMap')) || {};
    const batchSize = 10;

    function sendBatchedLikes(postId, likesCount) {
        fetch('/likes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ post_id: postId, likes_count: likesCount })
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                console.error('Failed to send batched likes:', data.message);
            } else {
                delete likesMap[postId];
                localStorage.setItem('likesMap', JSON.stringify(likesMap));
            }
        })
        .catch(error => console.error('Error:', error));
    }

    likeButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const postId = button.dataset.postId;

            if (!(postId in likesMap)) {
                likesMap[postId] = 0;
            }

            likesMap[postId]++;

            if (likesMap[postId] >= batchSize) {
                sendBatchedLikes(postId, likesMap[postId]);
            } else {
                localStorage.setItem('likesMap', JSON.stringify(likesMap));
            }

            const likesCountElement = document.getElementById('likes-count-' + postId);
            if (likesCountElement) {
                likesCountElement.textContent = parseInt(likesCountElement.textContent) + 1;
            }
        });
    });

    window.addEventListener('beforeunload', function() {
        for (const postId in likesMap) {
            if (likesMap.hasOwnProperty(postId) && likesMap[postId] > 0) {
                sendBatchedLikes(postId, likesMap[postId]);
            }
        }
    });
});
