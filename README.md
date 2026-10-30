# Yuzhe Gu's personal website

A single-page Jekyll research homepage, adapted from [Leonid Keselman's website](https://leonidk.com/) and [Jon Barron's website](https://jonbarron.info/).

## Local development

On macOS, install a separate Ruby on the Mac where you want to preview:

```sh
brew install ruby@3.3
```

Install [Homebrew](https://brew.sh) first if `brew` is unavailable. The launcher automatically uses Homebrew Ruby 3.3 when the default Ruby is the older macOS system version. Missing system Ruby headers (`ruby/config.h`) require a separate Ruby installation; updating RubyGems alone does not supply those headers.

From the repository root, run:

```sh
sh scripts/site serve
```

The script installs the locked Bundler and gems in a machine-local cache on first use (`~/Library/Caches/yzguu830-site` on macOS). Preview output is stored there too. Dependencies are separated by Ruby version and platform. They are not synchronized through Google Drive. The script does not require `sudo` or global gem installation. Subsequent runs reuse the cache; if it is missing, the script installs it again.

The path is `scripts/site` (plural `scripts`). On macOS, if native gem compilation cannot find `iostream`, the launcher detects the active macOS SDK and adds its C++ headers for dependency installation. WEBrick is included explicitly so the preview server also works with Ruby 3.

Run this command on the same computer where you want to open the browser. Google Drive syncs source files, not running servers. A server started on the Mac mini is not available at localhost on another Mac.

Open <http://127.0.0.1:4000>. Save your edits and refresh the browser after Jekyll rebuilds. The server polls for changes to support the Google Drive checkout. Restart the server after editing `_config.yml`. Press Ctrl+C to stop.

To install dependencies without starting a server:

```sh
sh scripts/site setup
```

To build and check the production output:

```sh
sh scripts/site build
python3 scripts/check_site.py _site
```

The checker uses only Python's standard library. Commit `Gemfile` and `Gemfile.lock` when updating dependencies. Upgrading Ruby automatically selects a separate dependency cache.

## Content and images

- `index.html` is the only homepage entry point; `_layouts/default.html` contains its markup.
- Add research entries to `_research/` with title, date, authors, venue, image, image_width, image_height, and paper/code links. They appear newest first and do not generate standalone pages.
- `style.scss` keeps the original desktop style and stacks the profile and research entries at widths of 640px or less.
- The homepage uses compressed WebP images. Original images remain in the repository and are excluded from the build.
- Removed Projects content is retained under `_archive/projects/` and excluded from the website.

The site uses the default GitHub Pages domain, `https://yzguu830.github.io`. No custom-domain `CNAME` file is needed. GitHub Pages deployment settings are managed separately in the repository settings.
