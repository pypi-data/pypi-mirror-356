# 🗂️ Daily Technical Logs

## 📅 Years

- [2025](./2025/README.md)

# TaskDaily

A flexible and customizable daily task management system that helps you organize and track your daily tasks across different projects.

## Features

- 📝 Create daily task files with customizable templates
- 🔄 Automatically carry forward incomplete tasks
- 📊 Multiple project support with custom emojis
- 🎨 Customizable task status workflow
- 📤 Multiple output formats (Slack, with easy extension for email, Notion, etc.)
- ⚙️ User-specific configuration management
- 🔒 Safe configuration handling with defaults

## Installation

```bash
pip install taskdaily
```

## Quick Start

1. Initialize configuration (first time only):
```bash
daily config init
```

2. Create today's task file:
```bash
daily create
```

3. Share your daily plan/report:
```bash
daily share --report  # For EOD report
daily share          # For daily plan
```

## Configuration

The package uses a configuration file located at `~/.config/daily-task/config.yaml`. You can:

- Reset to defaults: `daily config init`
- View config paths: `daily config path`

### Customizing Status Workflow

The default status workflow is:
- 📝 Planned
- ⚡ In Progress
- 🚧 Blocked
- 📅 Rescheduled
- ➡️ Carried Forward
- ✅ Completed
- 🚫 Cancelled

You can customize this in your config file.

### Customizing Projects

Default projects:
- 🏠 Personal
- 💼 Work
- 📚 Learning

Add or modify projects in your config file.

## Extending

The package is designed to be easily extensible:

1. Create a new formatter in `handlers/formatters/`
2. Create a new handler in `handlers/`
3. Register the handler in the CLI

Example for adding email support:
```python
from taskdaily.handlers import OutputHandler

class EmailHandler(OutputHandler):
    def format_content(self, tasks, date, is_report=False):
        # Format tasks for email
        pass

    def send(self, content, **kwargs):
        # Send email
        pass
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request to the [GitHub repository](https://github.com/nainesh-rabadiya/taskdaily).

## Author

- **Nainesh Rabadiya** - [GitHub](https://github.com/nainesh-rabadiya)
- Email: nkrabadiya@gmail.com

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
