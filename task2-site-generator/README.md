# Task 2: Site Generator

A web application for generating static personal portfolio sites with customizable templates and themes.

## Features

- **Two Templates**: Modern card-based and gradient social layouts
- **Customization**: Colors, fonts, backgrounds, social links
- **Real-time Preview**: See changes instantly
- **Static Export**: Download generated HTML/CSS
- **Responsive Design**: Works on all devices

## Architecture

- **Frontend**: React.js with modern UI components
- **Backend**: Node.js/Express for template processing
- **Templates**: Handlebars for dynamic content generation

## Setup

### Backend
```bash
cd backend
npm install
npm start
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## API Endpoints

- `POST /api/generate` - Generate static site code
- `GET /api/templates` - Get available templates
- `POST /api/preview` - Generate preview HTML

## Template System

Templates use Handlebars with conditional rendering:
- `{{#if showProfilePicture}}` - Profile picture toggle
- `{{#if showSocialLinks}}` - Social links toggle
- `{{primaryColor}}` - Dynamic color injection

## Customization Options

### User Input
- Name, introduction, email
- Twitter and GitHub links
- Profile image URL

### Template Selection
- Template A: Card-based layout
- Template B: Gradient social layout

### Theme Settings
- Primary/secondary colors
- Font family selection
- Background options
- Social link visibility

## Generated Output

Static HTML/CSS files ready for deployment on any hosting platform.