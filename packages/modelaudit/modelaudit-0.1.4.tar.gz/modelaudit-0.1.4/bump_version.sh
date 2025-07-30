#!/bin/bash

# ModelAudit Version Bump Script
# Usage: ./bump_version.sh [patch|minor|major] [optional_custom_version]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    print_error "GitHub CLI (gh) is not installed. Please install it first:"
    print_error "https://cli.github.com/"
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "Not in a git repository"
    exit 1
fi

# Check if pyproject.toml exists
if [ ! -f "pyproject.toml" ]; then
    print_error "pyproject.toml not found"
    exit 1
fi

# Get current version from pyproject.toml
CURRENT_VERSION=$(grep 'version = ' pyproject.toml | head -1 | sed 's/.*version = "\(.*\)".*/\1/')

if [ -z "$CURRENT_VERSION" ]; then
    print_error "Could not find version in pyproject.toml"
    exit 1
fi

print_status "Current version: $CURRENT_VERSION"

# Parse current version
IFS='.' read -ra VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR=${VERSION_PARTS[0]}
MINOR=${VERSION_PARTS[1]}
PATCH=${VERSION_PARTS[2]}

# Determine new version
BUMP_TYPE=${1:-patch}
CUSTOM_VERSION=$2

if [ -n "$CUSTOM_VERSION" ]; then
    NEW_VERSION=$CUSTOM_VERSION
    print_status "Using custom version: $NEW_VERSION"
else
    case $BUMP_TYPE in
        patch)
            NEW_VERSION="$MAJOR.$MINOR.$((PATCH + 1))"
            ;;
        minor)
            NEW_VERSION="$MAJOR.$((MINOR + 1)).0"
            ;;
        major)
            NEW_VERSION="$((MAJOR + 1)).0.0"
            ;;
        *)
            print_error "Invalid bump type. Use: patch, minor, or major"
            exit 1
            ;;
    esac
    print_status "Bumping $BUMP_TYPE version: $CURRENT_VERSION → $NEW_VERSION"
fi

# Create branch name
BRANCH_NAME="version-bump-$NEW_VERSION"

# Check if branch already exists
if git show-ref --verify --quiet refs/heads/$BRANCH_NAME; then
    print_warning "Branch $BRANCH_NAME already exists. Switching to it."
    git checkout $BRANCH_NAME
else
    # Create and switch to new branch
    print_status "Creating branch: $BRANCH_NAME"
    git checkout -b $BRANCH_NAME
fi

# Update version in pyproject.toml
print_status "Updating version in pyproject.toml"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml
else
    # Linux
    sed -i "s/version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml
fi

# Verify the change
UPDATED_VERSION=$(grep 'version = ' pyproject.toml | head -1 | sed 's/.*version = "\(.*\)".*/\1/')
if [ "$UPDATED_VERSION" != "$NEW_VERSION" ]; then
    print_error "Failed to update version in pyproject.toml"
    exit 1
fi

print_success "Version updated to: $NEW_VERSION"

# Add and commit changes
print_status "Committing changes"
git add pyproject.toml
git commit -m "chore: bump version to $NEW_VERSION"

# Push branch to remote
print_status "Pushing branch to remote"
git push origin $BRANCH_NAME

# Create pull request using GitHub CLI
print_status "Creating pull request"
PR_TITLE="chore: bump version to $NEW_VERSION"
PR_BODY="## Version Bump

Bumps version from \`$CURRENT_VERSION\` to \`$NEW_VERSION\`.

### Changes
- Updated version in \`pyproject.toml\`

### Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [x] Chore (maintenance, version bump, etc.)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)

### Checklist
- [x] Version updated in pyproject.toml
- [ ] Tests pass locally
- [ ] Documentation updated (if applicable)"

# Create the PR and capture the URL
PR_URL=$(gh pr create --title "$PR_TITLE" --body "$PR_BODY" --head $BRANCH_NAME --base main)

print_success "Pull request created: $PR_URL"

# Ask if user wants to open the PR in browser
echo ""
read -p "Do you want to open the PR in your browser? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    gh pr view $BRANCH_NAME --web
fi

print_success "Version bump complete! 🎉"
print_status "Summary:"
print_status "  - Version: $CURRENT_VERSION → $NEW_VERSION"
print_status "  - Branch: $BRANCH_NAME"
print_status "  - PR: $PR_URL" 