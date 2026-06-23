# azwerks Neovim Shell v0.1.0 - Post-Release Options

## Option 1 - Stop Here

Keep v0.1.0 as a source-only local release.

This is the lowest-risk option. The clean source archive and release records are
already available under the project directory.

## Option 2 - Git Repository Track

Initialize Git, commit v0.1.0, and tag the release.

Use this if future patches or feature work are likely.

## Option 3 - Packaging Research Track

Research deb, AppImage, Flatpak, or other distribution formats.

This should be a separate research track. Do not mix packaging work into the
v0.1.0 release lock.

## Option 4 - v0.1.1 Patch Track

Address small quality-of-life issues without changing scope.

Possible patch areas:

- cleaner manual launcher verification notes
- optional screenshot-based visual QA record
- documentation organization for historical handoff material

## Option 5 - Visual QA Track

Run manual `gtk-launch` visual confirmation and document screenshots or notes.

This should verify:

- launcher opens the app
- window title is acceptable
- Neovim appears in the VTE terminal
- Radium visual defaults are visible or acceptable
- exiting Neovim closes the app cleanly

## Recommended Path

Keep v0.1.0 as a source-only local release unless the user wants ongoing version
history. Initialize Git only if future changes are expected.

Start packaging only as a separate research track. Do not mix packaging work
into the v0.1.0 release lock.
