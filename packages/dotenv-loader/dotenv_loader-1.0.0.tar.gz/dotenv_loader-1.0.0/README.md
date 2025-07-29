# dotenv-loader

Smart and flexible `.env` loader for Python applications.


## 📖 Overview

**dotenv-loader** provides a flexible yet straightforward way to load environment variables from `.env` files, tailored specifically for Python applications, including Django, Flask, Celery, FastCGI, WSGI, CLI tools, and more. It supports hierarchical configuration, making it extremely convenient to manage multiple environments (development, testing, production) without manually switching `.env` files or cluttering code with environment-specific logic.


## 🚀 Historical Context

Managing environment-specific settings is crucial in modern software development. Standard solutions like [python-dotenv](https://github.com/theskumar/python-dotenv) simplify loading variables from `.env` files but lack flexible mechanisms for dynamically switching configurations across multiple deployment environments or nested project structures.

dotenv-loader was created specifically to solve these practical challenges:

- Easily switch environments without changing code or manually managing environment variables.
- Support flexible directory structures (such as monorepos or Django sub-applications).
- Enable clear separation of environment-specific configurations, improving clarity and reducing human error.


## ✨ Features

- **Hierarchical and prioritized .env file search**: dotenv-loader follows a clear and intuitive priority order:
  1. Explicit path provided via `DOTENV` environment variable.
  2. Configuration directory (`DOTCONFIG_ROOT`) with customizable subdirectories per project and environment stage (`DOTSTAGE`).
  3. Automatic fallback to `.env` file located directly in the project root.

- **Dynamic project and stage selection**: Quickly switch configurations by setting the `DOTPROJECT` and `DOTSTAGE` environment variables, allowing effortless toggling between multiple environments or projects.

- **Customizable file names**: Use custom `.env` filenames to further separate and manage your configurations.


## 🔒 Security and Best Practices

Storing `.env` files separately in a dedicated configuration directory (`DOTCONFIG_ROOT`) outside your project source tree is a secure and recommended best practice. This approach significantly reduces the risk of accidentally leaking sensitive information (such as API keys, database credentials, etc.) during backups, version control operations, or file transfers. By keeping secrets separate from your codebase, dotenv-loader helps enforce a clear boundary between configuration and code, enhancing security and compliance.


## ⚙️ Installation

```bash
pip install dotenv-loader
```


## 🛠 Usage

### Basic Usage

By default, dotenv-loader automatically identifies the `.env` file from the current project's root directory:

```python
import dotenv_loader

dotenv_loader.load_env()
```


### Advanced Usage

```python
import dotenv_loader

# Load environment with custom default settings 
# Each parameter is optional and first four can be overridden by environment variables:
dotenv_loader.load_env(
    project='mega-project',          # - explicitly set project name
    stage='production',              # - explicitly set stage name
    dotenv='./dir/.env.test'         # - explicitly set .env file 
    config_root='~/custom-configs',  # - custom config directory
    steps_to_project_root=1,         # - how many directories up to look for project root
    default_env_file='env',          # - change the default '.env' name to you name
    override=True                    # - whether to overwrite existing environment variables 
                                     #   already defined in os.environ. Use False to preserve 
                                     #   values already present (e.g. from OS or CI/CD), or 
                                     #   True to always prefer .env contents.
)
```


### Environment Variables

You can configure dotenv-loader behavior directly from environment variables:

- **DOTENV**: Specify exact path to the `.env` file:

```bash
DOTENV=/path/to/custom.env python manage.py
```

- **DOTPROJECT**: Quickly switch project environments:

```bash
DOTPROJECT=test python manage.py  # loads ~/.config/python-projects/test/.env
```

- **DOTSTAGE**: Switch configuration stages within a project (prod, staging, test):

```bash
DOTSTAGE=staging python manage.py  # loads ~/.config/python-projects/myproject/.env.staging
```

- **DOTCONFIG_ROOT**: Change the root directory for configuration files:

```bash
DOTCONFIG_ROOT=~/myconfigs python manage.py
```


### Typical Directory Structure

```
~/.config/python-projects/
└── myproject/
    ├── .env          # Default configuration (typically a symlink from .env.prod)
    ├── .env.prod     # Production configuration. Explicit usage: DOTSTAGE=prod python manage.py
    ├── .env.staging  # Staging configuration. Explicit usage: DOTSTAGE=staging python manage.py
    └── .env.test     # Testing configuration. Explicit usage: DOTSTAGE=test python manage.py

myproject/
└── manage.py  # By default, loads ~/.config/python-projects/myproject/.env
```

## 🧽 `.env` Resolution Rules and Precedence

`dotenv-loader` uses a deterministic and secure resolution strategy when selecting the appropriate `.env` file to load. The logic ensures maximum flexibility while maintaining clarity and safety.

### Resolution Rules

1. **Environment Variables Take Precedence**  
   The following environment variables have higher priority than the corresponding `load_env()` parameters:
   - `DOTENV` overrides `dotenv`
   - `DOTPROJECT` overrides `project`
   - `DOTSTAGE` overrides `stage`
   - `DOTCONFIG_ROOT` overrides `config_root`

2. **Relative Paths Are Context-Aware**  
   - Paths defined in environment variables (e.g., `DOTENV`, `DOTCONFIG_ROOT`) are resolved relative to the OS working directory (`PWD`, as seen with `pwd` in a terminal).
   - Paths provided as function arguments (`dotenv`, `config_root`) are resolved relative to the script that directly invoked `load_env()`, adjusted by `steps_to_project_root`.  
     For example, if `manage.py` is located at `~/projects/proj1/app/manage.py` and called with `load_env(steps_to_project_root=2)`, then the `project_root` is assumed to be `~/projects/proj1`, and relative paths are resolved from that base.

3. **Project and Stage Names Must Be Basenames**  
   Both `DOTPROJECT` / `project` and `DOTSTAGE` / `stage` must not contain slashes (`/`). They are always interpreted as directory/file basenames and resolved with `Path(name).name`.

4. **Highest Priority: Explicit `.env` Path**  
   If either `DOTENV` or `dotenv` is defined, it is used directly. All other resolution rules are skipped.

5. **Project Name Determination**  
   The project name is resolved in the following order:
   - From `DOTPROJECT` or `project` (if defined)
   - Otherwise, it falls back to the name of the final directory in the `project_root` path

6. **`.env` Filename Construction**  
   The target filename is built using the format:  
   `"[default_env_file][[.]STAGE]"`,  
   where `default_env_file` is `.env` by default, and `STAGE` is the value of `DOTSTAGE` or `stage`.

7. **Primary Search Location**  
   If no explicit `.env` is provided, dotenv-loader first checks the following path:  
   `[DOTCONFIG_ROOT | config_root] / [DOTPROJECT | project] / [default_env_file][.stage]`

8. **Fallback Location**  
   If the file is not found in the config directory, it will search inside the computed project root:  
   `[project_root] / [default_env_file][.stage]`

9. **Error Handling**  
   If no `.env` file is found in any of the candidate locations, a `FileNotFoundError` is raised, detailing all paths that were attempted.


## 🎯 Use Cases

dotenv-loader is especially useful when:

- Deploying applications to multiple environments (development, testing, staging, production).
- Managing complex directory structures (monorepos or multi-app Django projects).
- Simplifying CI/CD workflows by dynamically selecting environment configurations.


## 📜 License

[MIT License](LICENSE)


## 🤝 Contributing

We welcome contributions from the community! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to get started.


## 🤖 Acknowledgments

This project was created in collaboration with ChatGPT (OpenAI), utilizing the GPT-4o, GPT-4.5, and GPT-3 models.


## 📅 Changelog

For detailed release notes, see [CHANGELOG.md](CHANGELOG.md).

---

By clearly managing your environment variables and enabling dynamic configuration switching, dotenv-loader helps you streamline your deployment and development workflows, reduce errors, and maintain cleaner, more maintainable code.

