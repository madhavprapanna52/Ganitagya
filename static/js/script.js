// Ganitagya App - Main JavaScript
class GanitatgyaApp {
  constructor() {
    this.chatForm = document.getElementById('chat-form');
    this.chatInput = document.getElementById('chat-input');
    this.chatWindow = document.getElementById('chat-window');
    this.videoPlayer = document.getElementById('video-player');
    this.videoLoading = document.getElementById('video-loading');
    this.sendButton = document.getElementById('send-button');
    
    this.init();
  }

  init() {
    // Event listeners
    this.chatForm.addEventListener('submit', (e) => this.handleSubmit(e));
    this.chatInput.addEventListener('keydown', (e) => this.handleKeydown(e));
    
    // Initialize video
    this.initializeVideo();
    
    // Welcome message
    this.addMessage('नमस्ते! मैं आपका AI गणित शिक्षक हूँ। कोई भी गणित का प्रश्न पूछें!', 'llm');
  }


  async handleSubmit(e) {
    e.preventDefault();
    const text = this.chatInput.value.trim();
    if (!text) return;

    // Add user message
    this.addMessage(text, 'user');
    this.chatInput.value = '';
    this.setLoading(true);

    try {
      // API call to Flask backend
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();

      // Add AI response
      this.addMessage(data.response || 'कोई उत्तर उपलब्ध नहीं है।', 'llm');
      
      // Handle video if available
      if (data.video_url) {
        this.updateVideo(data.video_url);
      }

    } catch (error) {
      console.error('API Error:', error);
      this.addMessage('माफ करें, सर्वर से कनेक्शन में समस्या है। कृपया फिर से कोशिश करें।', 'llm');
    } finally {
      this.setLoading(false);
    }
  }

  handleKeydown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      this.handleSubmit(e);
    }
  }

  addMessage(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = text;
    
    // Add typing animation for LLM messages
    if (type === 'llm') {
      messageDiv.style.opacity = '0';
      messageDiv.style.transform = 'translateY(20px)';
    }
    
    this.chatWindow.appendChild(messageDiv);
    
    // Animate LLM messages
    if (type === 'llm') {
      setTimeout(() => {
        messageDiv.style.transition = 'all 0.3s ease';
        messageDiv.style.opacity = '1';
        messageDiv.style.transform = 'translateY(0)';
      }, 100);
    }
    
    // Auto-scroll
    this.scrollToBottom();
  }

  setLoading(isLoading) {
    this.sendButton.disabled = isLoading;
    this.sendButton.textContent = isLoading ? '⏳ भेज रहे हैं...' : 'भेजें';
    this.chatInput.disabled = isLoading;
  }

  initializeVideo() {
    this.videoPlayer.addEventListener('loadstart', () => {
      this.videoLoading.style.display = 'block';
    });

    this.videoPlayer.addEventListener('canplay', () => {
      this.videoLoading.style.display = 'none';
    });

    this.videoPlayer.addEventListener('error', () => {
      this.videoLoading.style.display = 'none';
      console.error('Video loading failed');
    });
  }

  updateVideo(videoUrl) {
    this.videoLoading.style.display = 'block';
    this.videoPlayer.src = videoUrl;
    this.videoPlayer.load();
  }

  scrollToBottom() {
    setTimeout(() => {
      this.chatWindow.scrollTop = this.chatWindow.scrollHeight;
    }, 100);
  }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new GanitatgyaApp();
});

// Additional utility functions
const utils = {
  // Format timestamp
  formatTime: (date) => {
    return date.toLocaleTimeString('hi-IN', {
      hour: '2-digit',
      minute: '2-digit'
    });
  },

  // Show notification
  showNotification: (message, type = 'info') => {
    // Can be extended for toast notifications
    console.log(`[${type.toUpperCase()}] ${message}`);
  },

  // Copy text to clipboard
  copyToClipboard: (text) => {
    navigator.clipboard.writeText(text).then(() => {
      utils.showNotification('Text copied to clipboard');
    });
  }
};

