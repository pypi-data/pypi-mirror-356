# Quick Start Guide

## Installation

1. Install the package:
```bash
pip install taskdaily
```

2. Initialize configuration (first time only):
```bash
daily config init
```

This will create:
- Configuration directory: `~/.config/taskdaily/`
- Config file: `~/.config/taskdaily/config.yaml`
- Template file: `~/.config/taskdaily/daily_template.md`

## Basic Usage

### 1. Create Today's Tasks

```bash
# Create today's file
daily create

# Create for a specific date
daily create --date 2024-03-15
```

### 2. Share Your Tasks

```bash
# Share daily plan
daily share

# Share EOD report
daily share --report

# Share without copying to clipboard
daily share --no-copy
```

### 3. Manage Configuration

```bash
# View config paths
daily config path

# Reset to defaults
daily config init
```

## Task Status Workflow

Tasks follow this workflow:
1. 📝 **Planned**: New tasks start here
2. ⚡ **In Progress**: Currently working on
3. 🚧 **Blocked**: Waiting on something
4. 📅 **Rescheduled**: Moved to another date
5. ➡️ **Carried Forward**: Moved to next day
6. ✅ **Completed**: Done
7. 🚫 **Cancelled**: Won't do

To change a task's status, just add the corresponding emoji.

## Project Organization

Tasks are organized by projects:
- 🏠 Personal
- 💼 Work
- 📚 Learning

### Example Task Format

```markdown
- [ ] Review PR #123 ⚡
- [ ] Update documentation 📝
- [x] Fix bug in login ✅
```

## Customization

### 1. Edit Project List

Edit `~/.config/taskdaily/config.yaml`:
```yaml
projects:
  - name: "Backend"
    emoji: "⚙️"
  - name: "Frontend"
    emoji: "🎨"
  - name: "DevOps"
    emoji: "🚀"
```

### 2. Customize Template

Edit `~/.config/taskdaily/daily_template.md`:
```markdown
# Daily Tasks - {date}

## Morning Goals
{projects}

## Notes
- 

## Blockers
- 
```

### 3. Add New Status

Edit the status section in config.yaml:
```yaml
status:
  review:
    name: "In Review"
    emoji: "👀"
```

## Tips & Tricks

1. **Carry Forward**: Incomplete tasks automatically carry forward to the next day

2. **Quick Copy**: Share command automatically copies to clipboard

3. **Date Navigation**: Use `--date` flag to work with any date:
   ```bash
   daily create --date 2024-03-15
   daily share --date 2024-03-15 --report
   ```

4. **Template Only**: Create file without carrying forward tasks:
   ```bash
   daily create --template-only
   ```

## Common Issues

1. **Config Not Found**
   ```bash
   daily config init
   ```

2. **Clipboard Not Working**
   ```bash
   daily share --no-copy
   ```

3. **Wrong Date Format**
   Use YYYY-MM-DD format:
   ```bash
   daily create --date 2024-03-15  # Correct
   daily create --date 15-03-2024  # Wrong
   ```

## Next Steps

1. Check out the full README.md for advanced features
2. Explore the configuration file for customization
3. Consider contributing new output handlers (email, Notion, etc.) 