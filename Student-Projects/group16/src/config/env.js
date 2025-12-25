/**
 * Environment configuration
 * Handles all environment variables for the application
 */

export const env = {
  /**
   * Get Google API Key from environment variables
   * @returns {string} The Google API key
   * @throws {Error} If the API key is not set
   */
  getGoogleApiKey() {
    const apiKey = import.meta.env.VITE_GOOGLE_API_KEY || import.meta.env.GOOGLE_API_KEY;
    
    if (!apiKey) {
      throw new Error(
        'Google API key is not set. Please add VITE_GOOGLE_API_KEY to your .env file.'
      );
    }
    
    return apiKey;
  },
};
