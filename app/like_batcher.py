from models import Post, db

class LikeBatcher:
    def __init__(self, batch_size=10):
        self.batch_size = batch_size
        self.likes = {}

    def add_like(self, post_id):
        if post_id in self.likes:
            self.likes[post_id] += 1
        else:
            self.likes[post_id] = 1

        if self.likes[post_id] >= self.batch_size:
            self.update_database(post_id)

    def update_database(self, post_id):
        # Update the database with the batched likes for the post
        post = Post.query.get(post_id)
        if post:
            likes_in_batch = self.likes[post_id] // self.batch_size * self.batch_size
            post.likes_count += likes_in_batch
            self.likes[post_id] %= self.batch_size  # Reset the count of likes in the batch
            db.session.commit()
