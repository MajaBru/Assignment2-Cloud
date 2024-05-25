document.addEventListener('DOMContentLoaded', function() {
    // Get all like buttons
    const likeButtons = document.querySelectorAll('.like-button');

    // Add click event listener to each like button
    likeButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            // Prevent the default form submission behavior
            event.preventDefault();

            // Get the post ID from the data attribute
            const postId = button.dataset.postId;

            // Send a POST request to the /likes endpoint with the post ID
            fetch('/likes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ post_id: postId })
            })
            .then(response => response.json())
            .then(data => {
                // Update the likes count on the page
                const likesCountElement = document.getElementById('likes-count-' + postId);
                if (likesCountElement) {
                    likesCountElement.textContent = parseInt(likesCountElement.textContent) + 1;
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
