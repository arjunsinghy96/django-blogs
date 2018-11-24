# Changelog

This document contains the notable changes to this project.

## 0.2.0

### Added

- Setting `BLOGS_SHOW_FOOTER_LINK` to hide/show link to [djangoblogs](https://github.com/arjunsinghy96/djangoblogs) in footer.
- Setting `BLOGS_PARENT_SITE_NAME` for parent site name.
- Google Analytics through a simple setting `BLOGS_GA_TRACKING_ID`.
- Upvote/Like feature. Anonymous users can upvote a blog post. Each upvote is identified though a unique fingerprint generated using [fingerprintjs2](http://valve.github.io/fingerprintjs2/)

### Changed

- Max width of the blog post to 700px