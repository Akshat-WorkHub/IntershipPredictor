import requests

class GitHubScoreService:

    def extract_username(self, github_url: str) -> str:

        if not github_url:
            return ""

        return github_url.rstrip("/").split("/")[-1]

    def get_profile_data(self, username: str):

        url = f"https://api.github.com/users/{username}"

        response = requests.get(url)

        if response.status_code != 200:
            return None

        return response.json()

    def get_repositories(self, username: str):

        url = f"https://api.github.com/users/{username}/repos"
        response = requests.get(url)

        if response.status_code != 200:
            return []

        return response.json()
    
    def get_unique_languages(self, repos):
        languages = set()
        for repo in repos:

            language = repo.get("language")

            if language:
                languages.add(language)

        return languages

    def get_score(self, github_url: str) -> int:
        if not github_url: return 0

        username = self.extract_username(github_url)
        profile_data = self.get_profile_data(username)

        if not profile_data: return 0

        repos = self.get_repositories(username)
        total_repos = len(repos)

        # --------------------------------------------------
        # 1. Repository Score (Max 4)
        # --------------------------------------------------

        public_repos = profile_data.get(
            "public_repos",
            0
        )

        repos_score = min(
            public_repos / 3,
            4.0
        )

        # --------------------------------------------------
        # 2. Language Diversity Score (Max 2)
        # --------------------------------------------------

        languages = self.get_unique_languages(repos)

        unique_languages = len(languages)

        lang_diversity_score = min(
            unique_languages * 0.4,
            2.0
        )

        # --------------------------------------------------
        # 3. README Score (Max 2)
        # --------------------------------------------------

        repos_with_readme = 0

        for repo in repos:

            if repo.get("description"):
                repos_with_readme += 1

        readme_score = (
            repos_with_readme / total_repos
        ) * 2.0

        # --------------------------------------------------
        # 4. Recency Score (Max 1)
        # --------------------------------------------------

        from datetime import datetime, timezone

        repos_updated_recently = 0

        now = datetime.now(timezone.utc)

        for repo in repos:

            updated_at = repo.get("updated_at")

            if not updated_at:
                continue

            updated_date = datetime.strptime(
                updated_at,
                "%Y-%m-%dT%H:%M:%SZ"
            ).replace(tzinfo=timezone.utc)

            days_old = (
                now - updated_date
            ).days

            if days_old <= 180:
                repos_updated_recently += 1

        recency_score = (
            repos_updated_recently / total_repos
        ) * 1.0

        # --------------------------------------------------
        # 5. Profile Completeness Score (Max 1)
        # --------------------------------------------------

        profile_score = 0

        if profile_data.get("bio"):
            profile_score += 0.25

        if profile_data.get("location"):
            profile_score += 0.25

        if profile_data.get("blog"):
            profile_score += 0.25

        if profile_data.get("company"):
            profile_score += 0.25

        # --------------------------------------------------
        # Final Score
        # --------------------------------------------------

        total_score = (
            repos_score
            + lang_diversity_score
            + readme_score
            + recency_score
            + profile_score
        )

        github_score = round(
            min(total_score, 10),
            2
        )

        return round(github_score)