import React, { useState } from 'react';
import { Upload, Link, Calendar } from 'lucide-react';

const NewsInput = ({ onAnalysisComplete }) => {
  const [inputType, setInputType] = useState('url');
  const [urls, setUrls] = useState(['']);
  const [dateRange, setDateRange] = useState({
    start: '',
    end: ''
  });
  const [isLoading, setIsLoading] = useState(false);

  const addUrlInput = () => {
    setUrls([...urls, '']);
  };

  const updateUrl = (index, value) => {
    const newUrls = [...urls];
    newUrls[index] = value;
    setUrls(newUrls);
  };

  const removeUrl = (index) => {
    const newUrls = urls.filter((_, i) => i !== index);
    setUrls(newUrls);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const requestData = {
        input_type: inputType,
        urls: urls.filter(url => url.trim() !== ''),
        date_range: dateRange
      };

      // Mock API call - replace with actual backend endpoint
      const response = await fetch('/api/analyze-news', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });

      if (response.ok) {
        const data = await response.json();
        onAnalysisComplete(data);
      } else {
        console.error('Analysis failed');
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          News Analysis Input
        </h2>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Input Type Selection */}
          <div>
            <label className="text-base font-medium text-gray-900">
              Select Input Method
            </label>
            <div className="mt-4 space-y-4">
              <div className="flex items-center">
                <input
                  id="url-input"
                  name="input-type"
                  type="radio"
                  value="url"
                  checked={inputType === 'url'}
                  onChange={(e) => setInputType(e.target.value)}
                  className="h-4 w-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                />
                <label htmlFor="url-input" className="ml-3 block text-sm font-medium text-gray-700">
                  <div className="flex items-center">
                    <Link className="h-4 w-4 mr-2" />
                    News URLs
                  </div>
                </label>
              </div>
              <div className="flex items-center">
                <input
                  id="date-range"
                  name="input-type"
                  type="radio"
                  value="date"
                  checked={inputType === 'date'}
                  onChange={(e) => setInputType(e.target.value)}
                  className="h-4 w-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                />
                <label htmlFor="date-range" className="ml-3 block text-sm font-medium text-gray-700">
                  <div className="flex items-center">
                    <Calendar className="h-4 w-4 mr-2" />
                    Date Range Analysis
                  </div>
                </label>
              </div>
            </div>
          </div>

          {/* URL Input Section */}
          {inputType === 'url' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                News URLs
              </label>
              {urls.map((url, index) => (
                <div key={index} className="flex mb-2">
                  <input
                    type="url"
                    value={url}
                    onChange={(e) => updateUrl(index, e.target.value)}
                    placeholder="https://example.com/news-article"
                    className="flex-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                  />
                  {urls.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeUrl(index)}
                      className="ml-2 px-3 py-2 border border-red-300 text-red-700 rounded-md hover:bg-red-50"
                    >
                      Remove
                    </button>
                  )}
                </div>
              ))}
              <button
                type="button"
                onClick={addUrlInput}
                className="mt-2 px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
              >
                Add Another URL
              </button>
            </div>
          )}

          {/* Date Range Section */}
          {inputType === 'date' && (
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Start Date
                </label>
                <input
                  type="date"
                  value={dateRange.start}
                  onChange={(e) => setDateRange({...dateRange, start: e.target.value})}
                  className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  End Date
                </label>
                <input
                  type="date"
                  value={dateRange.end}
                  onChange={(e) => setDateRange({...dateRange, end: e.target.value})}
                  className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                />
              </div>
            </div>
          )}

          {/* Submit Button */}
          <div className="flex justify-end">
            <button
              type="submit"
              disabled={isLoading}
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {isLoading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Analyzing...
                </>
              ) : (
                <>
                  <Upload className="h-5 w-5 mr-2" />
                  Analyze News
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default NewsInput;
