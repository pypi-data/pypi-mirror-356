# Bible

## Description
Access any of several versions of the Christian Bible via the command line.

I'm using Henok Woldesenbet's very nice [Bible API](https://github.com/wldeh/bible-api) to access the many versions of the Bible he's provided. Thanks, Henok and the Bible API team!

## Usage
Use `bible versions` for information on the many versions available.

Use `bible config ...` to set, e.g., a default bible version.

Use `bible read -v en-fbv genisis 1 1-4` to get Genisis 1:1-4 from the Free Bible Version.

See `bible --all-help` for full usage details.

## Configuration
Use `bible config --help` for usage. You can show and update configuration variables using `bible config ...`. Once you run `bible ...` once, it will create the following directory structure:

```
~/.local/bible/cache/
~/.local/bible/config.toml
```

The cache directory is for caching compressed JSON files that keep the API from having to hit the Bible network API so often. The config.toml file is a text file that you can edit directly if you wish.

## Installation
If you don't have pipx installed either run `pip3 install pipx`, or if that gives you an "externally-managed-environment" complaint, use whatever package manager is right for your operating system.

* [Debian](https://www.debian.org/doc/manuals/debian-faq/pkgtools.en.html): `apt-get install pipx`
* [Red Hat](https://www.redhat.com/en/blog/how-manage-packages): `yum install pipx`
* [HomeBrew](https://brew.sh): `brew install pipx`

Once pipx is installed, run `pipx install jc-bible` to install it to your `~/.local` directory. (Or run `pipx --global install jc-bible` to install it for all users on your system.)

