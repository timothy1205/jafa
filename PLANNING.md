# Jafa Plans

## Description

Jafa (Just another forum app) is intended to be a simple forum-based social media not unlike Reddit in which users can create their own subforums (assuming its not already taken) and moderate it as they please. Users should be able to post text, images, and videos.

The following proposed features are split between the backend and frontend. All backend features that be accessed through the frontend can be assumed present. Instead the frontend section will list unique features.

## Proposed Features

### Backend

- [ ] Locally stored user authentication

  - [ ] Hashed passwords
  - [ ] Sensible password requirements
  - [ ] Username-based login (email not necessary but can be used)

- [ ] Ability to create subforums

  - [ ] Users are marked as a _Creator_ in their respective subforum (more info below)
  - [ ] Must have a title
  - [ ] Must have a description
  - [ ] Can be edited later on (except for title - a new subforum should be made in this case)
  - [ ] Can be deleted
  - [ ] Server must generate a unique url for it

- [ ] Ability to post to subforums

  - [ ] Users are marked as the _OP_ of their own post in comments (more info below)
  - [ ] Must include a title
  - [ ] May include tags
  - [ ] Text
  - [ ] Photos
  - [ ] Videos
  - [ ] Can be edited later on
  - [ ] Can be deleted
  - [ ] Can be locked (cannot commented on or edited)
  - [ ] Can be liked / disliked

- [ ] Ability to make comments to posts

  - [ ] Must include text
  - [ ] Can be edited later on
  - [ ] Can be deleted (Should be retained on server)
  - [ ] Can be liked / disliked

- [ ] Grab a list of posts to display to user

  - [ ] Filter based on most recent, most popular, etc
  - [ ] Search for posts containing keywords, tags, specific subforums

- [ ] Role-based hierarchy

  - [ ] Moderation type actions can only flow downwards (roles cannot target those higher than them)

  - [ ] _Admin_ (Apply to entire site)

    - [ ] Inherit _Creator_ privileges (global mod)
    - [ ] Can (un)ban users across the site

  - [ ] _Creator_ (Apply to their respective subforum)

    - [ ] Inherit _Mod_ privileges
    - [ ] Can edit subforum
    - [ ] Can delete subforum
    - [ ] Can assign users as a _Mod_

  - [ ] _Mod_ (Apply to their respective subforum)

    - [ ] Inherit _User_ privileges
    - [ ] Can lock posts
    - [ ] Can delete posts
    - [ ] Can delete comments
    - [ ] Can ban users from a subreddit

  - [ ] _User_

    - [ ] Can create subforums
    - [ ] Can create posts
    - [ ] Can create comments
    - [ ] Can delete their own posts / comments
    - [ ] Can like / dislike posts or comments (except their own) and undo said action
    - [ ] Can view all non-deleted posts

### Frontend

- [ ] Infinite scrolling for post feed

## Nice To Have Features

- [ ] Text editor with a reasonable amount of features

  - [ ] Bold, italic, hyperlinking, etc

- [ ] Private messaging
- [ ] Report system
