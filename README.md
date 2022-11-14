# Streamlit-Pages

Streamlit recently [released multi-page apps](https://blog.streamlit.io/introducing-multipage-apps/) 🎉
where page filenames are the source of truth for page settings.

This is an experimental package to try our what page-management might work if
you could name the files whatevery you wanted, and instead called a function
to specify pages.

This enables you to:

- Set page name, icon and order independently of file name/path
- Dynamically make pages hide/show

## Tested with the following versions:

- python=={3.8, 3.9, 3.10}
- streamlit=={1.10, 1.11, 1.12, 1.13, 1.14}
