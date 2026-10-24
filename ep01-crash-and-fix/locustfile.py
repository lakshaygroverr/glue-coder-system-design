# Fake users: each one opens the feed, waits 1-2 seconds, and does it again.
from locust import HttpUser, task, between


class FeedUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def open_feed(self):
        self.client.get("/feed", timeout=5)  # nobody waits more than 5 seconds for a feed
