import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';

function App() {
  const [formData, setFormData] = useState({
    name: 'John Doe',
    introduction: 'Full Stack Developer passionate about creating amazing web experiences',
    email: 'john@example.com',
    twitterLink: 'https://twitter.com/johndoe',
    githubLink: 'https://github.com/johndoe',
    imageUrl: 'https://via.placeholder.com/200',
    template: 'template-a',
    showProfilePicture: true,
    showSocialLinks: true,
    primaryColor: '#3b82f6',
    secondaryColor: '#1e40af',
    fontFamily: 'Inter',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  });

  const [generatedHTML, setGeneratedHTML] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const generateSite = async () => {
    setIsLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/generate`, formData);
      setGeneratedHTML(response.data.html);
    } catch (error) {
      console.error('Error generating site:', error);
      alert('Failed to generate site. Please try again.');
    }
    setIsLoading(false);
  };

  const downloadHTML = () => {
    const blob = new Blob([generatedHTML], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'index.html';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎨 Site Generator</h1>
        <p>Create beautiful personal portfolio sites in minutes</p>
      </header>

      <div className="container">
        <div className="form-section">
          <h2>Customize Your Site</h2>
          
          <div className="form-group">
            <label>Name</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              placeholder="Your full name"
            />
          </div>

          <div className="form-group">
            <label>Introduction</label>
            <textarea
              name="introduction"
              value={formData.introduction}
              onChange={handleInputChange}
              placeholder="Brief introduction about yourself"
              rows="3"
            />
          </div>

          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              placeholder="your.email@example.com"
            />
          </div>

          <div className="form-group">
            <label>Profile Image URL</label>
            <input
              type="url"
              name="imageUrl"
              value={formData.imageUrl}
              onChange={handleInputChange}
              placeholder="https://example.com/your-photo.jpg"
            />
          </div>

          <div className="form-group">
            <label>Twitter Link</label>
            <input
              type="url"
              name="twitterLink"
              value={formData.twitterLink}
              onChange={handleInputChange}
              placeholder="https://twitter.com/yourusername"
            />
          </div>

          <div className="form-group">
            <label>GitHub Link</label>
            <input
              type="url"
              name="githubLink"
              value={formData.githubLink}
              onChange={handleInputChange}
              placeholder="https://github.com/yourusername"
            />
          </div>

          <div className="form-group">
            <label>Template</label>
            <select name="template" value={formData.template} onChange={handleInputChange}>
              <option value="template-a">Template A - Card Layout</option>
              <option value="template-b">Template B - Gradient Social</option>
            </select>
          </div>

          <div className="checkbox-group">
            <label>
              <input
                type="checkbox"
                name="showProfilePicture"
                checked={formData.showProfilePicture}
                onChange={handleInputChange}
              />
              Show Profile Picture
            </label>
            <label>
              <input
                type="checkbox"
                name="showSocialLinks"
                checked={formData.showSocialLinks}
                onChange={handleInputChange}
              />
              Show Social Links
            </label>
          </div>

          <div className="color-group">
            <div className="form-group">
              <label>Primary Color</label>
              <input
                type="color"
                name="primaryColor"
                value={formData.primaryColor}
                onChange={handleInputChange}
              />
            </div>
            <div className="form-group">
              <label>Secondary Color</label>
              <input
                type="color"
                name="secondaryColor"
                value={formData.secondaryColor}
                onChange={handleInputChange}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Font Family</label>
            <select name="fontFamily" value={formData.fontFamily} onChange={handleInputChange}>
              <option value="Inter">Inter</option>
              <option value="Roboto">Roboto</option>
              <option value="Open Sans">Open Sans</option>
              <option value="Poppins">Poppins</option>
              <option value="Montserrat">Montserrat</option>
            </select>
          </div>

          <button 
            className="generate-btn" 
            onClick={generateSite}
            disabled={isLoading}
          >
            {isLoading ? 'Generating...' : '🚀 Generate Site'}
          </button>
        </div>

        <div className="preview-section">
          <h2>Preview</h2>
          {generatedHTML ? (
            <div className="preview-container">
              <iframe
                srcDoc={generatedHTML}
                title="Site Preview"
                className="preview-iframe"
              />
              <button className="download-btn" onClick={downloadHTML}>
                📥 Download HTML
              </button>
            </div>
          ) : (
            <div className="preview-placeholder">
              <p>Click "Generate Site" to see your preview</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;