document.addEventListener('DOMContentLoaded', function() {
    // Get all like buttons
    const likeButtons = document.querySelectorAll('.like-button');

    // Retrieve likes map from LocalStorage or initialize it
    const likesMap = JSON.parse(localStorage.getItem('likesMap')) || {};

    // Batch size for sending likes to the server
    const batchSize = 10;

    // Function to send batched likes to the server
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
                // Reset the likes count for the post in the local storage
                delete likesMap[postId];
                localStorage.setItem('likesMap', JSON.stringify(likesMap));
            }
        })
        .catch(error => console.error('Error:', error));
    }

    // Add click event listener to each like button
    likeButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            // Prevent the default form submission behavior
            event.preventDefault();

            // Get the post ID from the data attribute
            const postId = button.dataset.postId;

            // Initialize likes for the post if not already present
            if (!(postId in likesMap)) {
                likesMap[postId] = 0;
            }

            // Increment the likes count for the post
            likesMap[postId]++;

            // Check if batch size is reached for the post
            if (likesMap[postId] >= batchSize) {
                // Send batched likes to the server
                sendBatchedLikes(postId, likesMap[postId]);
            } else {
                // Save the updated likes map to LocalStorage
                localStorage.setItem('likesMap', JSON.stringify(likesMap));
            }

            // Update the likes count on the page (optional)
            const likesCountElement = document.getElementById('likes-count-' + postId);
            if (likesCountElement) {
                likesCountElement.textContent = parseInt(likesCountElement.textContent) + 1;
            }
        });
    });

    // Function to handle page unload and send any remaining batched likes
    window.addEventListener('beforeunload', function() {
        for (const postId in likesMap) {
            if (likesMap.hasOwnProperty(postId) && likesMap[postId] > 0) {
                sendBatchedLikes(postId, likesMap[postId]);
            }
        }
    });
});
