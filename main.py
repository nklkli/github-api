"""
Make HTTP requests to the Github API to list, create or delete repositories.
"""
from pprint import pprint
import requests
import os

baseurl = "https://api.github.com"


def delete_repo(token, owner, repo):
    """
    Deletes a Github repository.

    https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#delete-a-repository
    """
    response = requests.delete(url=baseurl + f"/repos/{owner}/{repo}",
                               headers={"Authorization": "Bearer " +
                                        token})
    print("Request URL:", response.url)
    print("Delete Repository Response:")
    print("Response Status:", response.status_code)
    pprint(response.text)
    if response.status_code == 204:
        print(f"OK. Github repository '{repo}' deleted.")


def create_repo(token, repo, description=None, private=True):
    """
    Creates a new repository for the authenticated user.

    https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#create-a-repository-for-the-authenticated-user
    """
    response = requests.post(url=baseurl + f"/user/repos",
                             headers={"Authorization": "Bearer " +
                                      token},
                             json={"name": repo,
                                   "description": description,
                                   "private": private})
    print("Create Repository Response:")
    print("Request URL:", response.url)
    print("Response Status:", response.status_code)
    if response.status_code == 201:
        json_response = response.json()
        pprint(json_response)
        clone_url = json_response["clone_url"]
        print(f"OK. Github repository '{repo}' created.")
        print(f"Clone-URL: {clone_url}")


def list_repositories(token):
    response = requests.get(url=baseurl + f"/user/repos",
                            headers={"Authorization": "Bearer " + token})

    pad = 10

    def print_repo_property(repo, property):
        print(f"{property:<{pad}}:", repo[property])

    for repo in response.json():
        print_repo_property(repo, "name")
        print_repo_property(repo, "description")
        print_repo_property(repo, "private")
        print_repo_property(repo, "size")
        print_repo_property(repo, "clone_url")
        print_repo_property(repo, "language")
        print()


if __name__ == "__main__":

    # CONFIGURE PERSONAL GITHUB SETTINGS

    # Adjust your Github Personal Access Token
    token = os.environ["GITHUB_TOKEN"]
    owner = "...put your Github username here..."

    # MAKE API REQUESTS

    repo = "...put a repository name here..."

    list_repositories(token)
    # delete_repo(token, owner, repo)
    # create_repo(token, repo)
