const express = require('express');
const cors = require('cors');
const handlebars = require('handlebars');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// Load templates
const templateA = fs.readFileSync(path.join(__dirname, 'templates', 'template-a.hbs'), 'utf8');
const templateB = fs.readFileSync(path.join(__dirname, 'templates', 'template-b.hbs'), 'utf8');

const compiledTemplateA = handlebars.compile(templateA);
const compiledTemplateB = handlebars.compile(templateB);

// API Routes
app.get('/api/templates', (req, res) => {
  res.json({
    templates: [
      {
        id: 'template-a',
        name: 'Template A - Card Layout',
        description: 'Clean card-based design with centered content'
      },
      {
        id: 'template-b',
        name: 'Template B - Gradient Social',
        description: 'Gradient background with social media focus'
      }
    ]
  });
});

app.post('/api/generate', (req, res) => {
  try {
    const {
      name,
      introduction,
      email,
      twitterLink,
      githubLink,
      imageUrl,
      template,
      showProfilePicture,
      showSocialLinks,
      primaryColor,
      secondaryColor,
      fontFamily,
      background
    } = req.body;

    // Prepare template data
    const templateData = {
      name: name || 'Your Name',
      introduction: introduction || 'Your introduction here',
      email: email || 'your.email@example.com',
      twitterLink: twitterLink || '#',
      githubLink: githubLink || '#',
      imageUrl: imageUrl || 'https://via.placeholder.com/200',
      showProfilePicture: showProfilePicture !== false,
      showSocialLinks: showSocialLinks !== false,
      primaryColor: primaryColor || '#3b82f6',
      secondaryColor: secondaryColor || '#1e40af',
      fontFamily: fontFamily || 'Inter, sans-serif',
      background: background || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    };

    // Generate HTML based on selected template
    let generatedHTML;
    if (template === 'template-b') {
      generatedHTML = compiledTemplateB(templateData);
    } else {
      generatedHTML = compiledTemplateA(templateData);
    }

    res.json({
      success: true,
      html: generatedHTML,
      data: templateData
    });

  } catch (error) {
    console.error('Generation error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to generate site'
    });
  }
});

app.post('/api/preview', (req, res) => {
  // Same as generate but for preview purposes
  app.handle(req, res);
});

app.listen(PORT, () => {
  console.log(`Site Generator Backend running on port ${PORT}`);
});