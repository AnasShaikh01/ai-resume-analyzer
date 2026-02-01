// Use environment variables for the API URL, with a fallback for local development.
// This makes it easy to switch to a production URL without changing the code.
// In your .env file, you would set: REACT_APP_API_URL=http://your-production-api.com
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
/**
 * Analyzes a resume against a list of job descriptions by calling the backend API.
 *
 * @param {File} resumeFile - The user's resume file.
 * @param {string[]} jobDescriptions - An array of job description strings.
 * @returns {Promise<Object>} A promise that resolves to the analysis results from the API.
 * @throws {Error} Throws an error if the API call fails or returns an error status.
 */
export const analyzeResume = async (resumeFile, jobDescriptions) => {
  const formData = new FormData();

  // Append the files and data in the format the backend expects
  formData.append('resume_file', resumeFile);
  jobDescriptions.forEach(jd => {
    // Ensure we don't send empty strings
    if (jd && jd.trim() !== '') {
      formData.append('job_descriptions', jd);
    }
  });

  try {
    const response = await fetch(`${API_BASE_URL}/analyze-resume/`, {
      method: 'POST',
      body: formData,
      // Note: Don't set 'Content-Type' header when using FormData with fetch,
      // the browser will automatically set it with the correct boundary.
    });

    const data = await response.json();

    if (!response.ok) {
      // If the server returns an error (e.g., 400, 500), throw an error with the message
      throw new Error(data.error || `Server responded with ${response.status}`);
    }

    return data;
  } catch (error) {
    console.error("API call failed:", error);
    // Re-throw the error so the UI component can handle it (e.g., show an error message)
    throw error;
  }
};